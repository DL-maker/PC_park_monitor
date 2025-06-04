from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
import platform
import requests
import socket
import subprocess
from collections import Counter
import psutil
import os
import re
import sys
from datetime import datetime


# Fonction pour obtenir le répertoire de base correct selon le contexte d'exécution
def get_base_directory():
    """Obtenir le répertoire de base pour les fichiers de logs et de données."""
    if getattr(sys, 'frozen', False):
        # Dans un exécutable PyInstaller
        executable_dir = os.path.dirname(sys.executable)
        base_dir = os.path.abspath(os.path.join(executable_dir, ".."))
    else:
        # Dans un script Python normal, utiliser le répertoire du script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = script_dir
    
    return base_dir

# Obtenir le répertoire de base
BASE_DIR = get_base_directory()

# Définir les chemins des fichiers de logs avec le répertoire de base
PORT_ACTIVITY_LOG = os.path.join(BASE_DIR, "port_activity.log")
INTERNET_USAGE_LOG = os.path.join(BASE_DIR, "internet_usage.log")

print(f"📂 PDF Data - Répertoire de base: {BASE_DIR}")
print(f"📂 PDF Data - Port activity log: {PORT_ACTIVITY_LOG}")
print(f"📂 PDF Data - Internet usage log: {INTERNET_USAGE_LOG}")


# GESTION MODULES EXTERNES
try:
    import Networkdata
    config = Networkdata.get_network_configuration()
    if not isinstance(config, dict):
        raise ValueError("Configuration réseau invalide")
except Exception:
    config = {}


try:
    import wifi_info
    system = platform.system()
    conn_info = wifi_info.get_connection_info()
    if system == "Windows":
        conn_info = wifi_info.parse_text_to_dict(conn_info)
except Exception:
    conn_info = {"WiFi SSID": "Inconnu", "Signal": "Inconnu"}


# Données config réseau par défaut
list_of_network_data = []
if config:
    for value in config.values():
        list_of_network_data.append(value)



dhcp = list_of_network_data[0] if len(list_of_network_data) > 0 else "Non disponible"
dns = list_of_network_data[1] if len(list_of_network_data) > 1 else "Non disponible"
gateway = list_of_network_data[2] if len(list_of_network_data) > 2 else "Non disponible"
mask = list_of_network_data[3] if len(list_of_network_data) > 3 else "Non disponible"


def parse_traffic_types_with_count(log_path):
    traffic_counter = Counter()
    if not os.path.exists(log_path):
        print(f"⚠️ Fichier de log introuvable: {log_path}")
        return traffic_counter
    try:
        with open(log_path, "r", encoding="utf-8") as file:
            for line in file:
                if "Service:" in line:
                    try:
                        service_part = line.split("Service:")[1].split("|")[0].strip()
                        traffic_counter[service_part] += 1
                    except IndexError:
                        continue
        print(f"✅ Analyse du trafic réussie: {len(traffic_counter)} types trouvés")
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse du trafic: {e}")
    return traffic_counter


counts = parse_traffic_types_with_count(PORT_ACTIVITY_LOG)
protocols = list(counts.keys())
proprotocols = list(counts.values())


def get_recent_connections():
    ip_addresses = set()
    for conn in psutil.net_connections(kind='inet'):
        if conn.raddr and conn.status in ('ESTABLISHED', 'CLOSE_WAIT', 'TIME_WAIT'):
            ip_addresses.add(conn.raddr.ip)
    return list(ip_addresses)[:5]


def get_open_ports():
    return sorted(set(conn.laddr.port for conn in psutil.net_connections(kind='inet') if conn.status == 'LISTEN'))


def get_exposed_ports():
    ports = set()
    for conn in psutil.net_connections(kind='inet'):
        if conn.status == psutil.CONN_LISTEN:
            ip = conn.laddr.ip
            if ip not in ('127.0.0.1', '::1'):
                ports.add(conn.laddr.port)
    return sorted(ports)


def is_local_partition(partition):
    if platform.system() == 'Windows':
        return partition.fstype != 'Network'
    return partition.fstype not in ['cifs', 'nfs', 'fuse', 'smbfs']


def get_total_local_disk_space():
    total = sum(psutil.disk_usage(p.mountpoint).total for p in psutil.disk_partitions() if is_local_partition(p))
    return total / (1024**3)


def get_system_info():
    os_info = f"{platform.system()} {platform.release()}"
    if platform.system() == "Windows":
        try:
            cpu_info = subprocess.check_output("wmic cpu get name", shell=True).decode().strip().split("\n")[1].strip()
        except:
            cpu_info = "Unknown"
    else:
        try:
            cpu_info = subprocess.check_output("lscpu | grep 'Model name' | cut -d: -f2", shell=True).decode().strip()
        except:
            cpu_info = "Unknown"
    ram = f"{psutil.virtual_memory().total / (1024**3):.0f} GB"
    disk = f"{get_total_local_disk_space():.0f} GB"
    hostname = socket.gethostname()
    return os_info, cpu_info, ram, disk, hostname


os_info, cpu_info, ram, disk, hostname = get_system_info()


def get_location_values():
    try:
        data = requests.get("https://ipinfo.io/json").json()
        return [data.get(k, "Non disponible") for k in ["ip", "city", "region", "country", "loc", "org", "timezone"]]
    except Exception as e:
        return [str(e)] * 7


ip, city, region, country, loc, isp, timezone = get_location_values()


data = {
    "network_activity": {
        "connection_history": get_recent_connections(),
        "open_ports": get_open_ports(),
        "traffic_type": protocols,
        "exposed_ports": get_exposed_ports(),
    },
    "connection_information": conn_info,
    "host_characteristics": {
        "os": os_info, "cpu": cpu_info, "ram": ram, "disk": disk, "hostname": hostname
    },
    "localization_and_environment": {
        "Public IP": ip, "City": city, "Region": region, "Country": country,
        "Location (lat,long)": loc, "ISP": isp, "Timezone": timezone
    },
    "network_configuration": {
        "dhcp_server_ip": dhcp, "dns_server_ip": dns,
        "default_gateway(s)": gateway, "subnet_mask": mask
    }
}


from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.shapes import Drawing, _DrawingEditorMixin
from reportlab.lib.colors import PCMYKColor


class PieChart(_DrawingEditorMixin, Drawing):
    def __init__(self, width=400, height=200, *args, **kw):
        Drawing.__init__(self, width, height, *args, **kw)
        self._add(self, Pie(), name='pie')
        self._add(self, Legend(), name='legend')
        self.pie.data = proprotocols
        self.pie.labels = protocols
        self.pie.width = 150
        self.pie.height = 150
        self.pie.x = 25
        self.pie.y = 25
        self.legend.x = 200
        self.legend.y = 100
        self.legend.boxAnchor = 'c'
        self.legend.colorNamePairs = [
            (PCMYKColor(100,0,90,50), f"{protocols[i]} ({proprotocols[i]})")
            for i in range(min(len(protocols), len(proprotocols)))
        ]


def get_five_min_traffic(log_file=None):
    if log_file is None:
        log_file = INTERNET_USAGE_LOG
    
    five_min_traffic = {}
    try:
        if not os.path.exists(log_file):
            print(f"⚠️ Fichier de log d'usage internet introuvable: {log_file}")
            return []
            
        with open(log_file, "r", encoding="utf-8") as f:
            for line in f:
                match = re.match(r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\].*Total: ([\d.]+) MB", line)
                if match:
                    timestamp = datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S")
                    total_mb = float(match.group(2))
                    minute = (timestamp.minute // 5) * 5
                    time_key = timestamp.replace(minute=minute, second=0).strftime("%Y%m%d%H%M")
                    five_min_traffic[time_key] = five_min_traffic.get(time_key, 0) + total_mb
        print(f"✅ Analyse de l'usage internet réussie: {len(five_min_traffic)} entrées trouvées")
        return [(int(k), round(v, 2)) for k, v in sorted(five_min_traffic.items())]
    except FileNotFoundError:
        print(f"❌ Fichier de log d'usage internet non trouvé: {log_file}")
        return []
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse de l'usage internet: {e}")
        return []


def datetime_formatter(x):
    try:
        return datetime.strptime(str(int(x))[:12], "%Y%m%d%H%M").strftime("%H:%M")
    except ValueError:
        return "N/A"


from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.axes import XValueAxis, YValueAxis
from reportlab.graphics.widgets.markers import makeMarker


class LineChart(_DrawingEditorMixin, Drawing):
    def __init__(self, width=300, height=150, *args, **kw):
        Drawing.__init__(self, width, height, *args, **kw)
        self._add(self, LinePlot(), name='chart')
        self.chart.x = 30
        self.chart.y = 30
        self.chart.height = 90
        self.chart.width = 210
        self.chart.data = [get_five_min_traffic()]
        self.chart.lines[0].strokeColor = PCMYKColor(0, 100, 100, 40)
        self.chart.lines.symbol = makeMarker('FilledCircle')
        self.chart.xValueAxis = XValueAxis()
        self.chart.xValueAxis.labelTextFormat = datetime_formatter
        self.chart.yValueAxis = YValueAxis()
        self.chart.yValueAxis.valueMin = 0
        self.chart.yValueAxis.valueMax = 100
        self.chart.yValueAxis.valueStep = 20


def add_section(content, title, data, style, is_dict=False):
    content.append(Paragraph(f"<b>{title}</b>", style))
    if is_dict:
        for key, value in data.items():
            val = ("\n".join(f"{k}: {v}" for k, v in value.items()) if isinstance(value, dict)
                   else ", ".join(map(str, value)) if isinstance(value, (list, set))
                   else str(value))
            content.append(Paragraph(f"<b>{key}:</b> {val}", style))
    else:
        content.append(Paragraph(f"<b>{title}:</b> {data}", style))
    content.append(Spacer(1, 12))


def create_pdf_with_data(file_name, data):
    try:
        # Si file_name n'est pas un chemin absolu, le placer dans BASE_DIR
        if not os.path.isabs(file_name):
            file_name = os.path.join(BASE_DIR, file_name)
        
        # S'assurer que le répertoire parent existe
        output_dir = os.path.dirname(file_name)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
            print(f"📁 Répertoire de sortie créé: {output_dir}")
        
        print(f"📄 Génération du PDF: {file_name}")
        
        doc = SimpleDocTemplate(file_name, pagesize=A4)
        content = []
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Normal_Left', alignment=TA_LEFT))
        content.append(Paragraph("Network Information Report", styles['Title']))
        content.append(Spacer(1, 12))

        # Ajouter le graphique en secteurs seulement si on a des données
        if protocols and proprotocols:
            try:
                pie = PieChart()
                content.append(pie)
                content.append(Spacer(1, 12))
                print("✅ Graphique en secteurs ajouté")
            except Exception as e:
                print(f"⚠️ Erreur lors de la création du graphique en secteurs: {e}")
        else:
            print("⚠️ Aucune donnée de protocole trouvée pour le graphique")
        
        # Ajouter le graphique en ligne pour l'analyse des téléchargements
        try:
            content.append(Paragraph("Analyze download data mb/5min", styles['Normal_Left']))
            line = LineChart()
            content.append(line)
            content.append(Spacer(1, 12))
            print("✅ Graphique en ligne ajouté")
        except Exception as e:
            print(f"⚠️ Erreur lors de la création du graphique en ligne: {e}")

        # Ajouter chaque section du rapport
        try:
            add_section(content, "Caractéristiques de l'hôte", data["host_characteristics"], styles['Normal_Left'], is_dict=True)
            add_section(content, "Activité réseau", data["network_activity"], styles['Normal_Left'], is_dict=True)
            add_section(content, "Informations de connexion", data["connection_information"], styles['Normal_Left'], is_dict=True)
            add_section(content, "Localisation et environnement", data["localization_and_environment"], styles['Normal_Left'], is_dict=True)
            add_section(content, "Configuration réseau", data["network_configuration"], styles['Normal_Left'], is_dict=True)
            print("✅ Toutes les sections ajoutées")
        except Exception as e:
            print(f"⚠️ Erreur lors de l'ajout des sections: {e}")

        doc.build(content)
        print(f"✅ PDF généré avec succès: {file_name}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération du PDF: {e}")
        return False

# Main function to generate PDF when run directly
if __name__ == "__main__":
    output_file = os.path.join(BASE_DIR, "data.pdf")
    print(f"Generating PDF report: {output_file}")
    if create_pdf_with_data(output_file, data):
        print(f"PDF report successfully generated: {os.path.abspath(output_file)}")
    else:
        print("Failed to generate PDF report") 