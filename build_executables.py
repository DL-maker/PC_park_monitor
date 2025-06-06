#!/usr/bin/env python3
"""
Script pour construire les exécutables GhostSpy proprement avec PyInstaller.
Ce script gère automatiquement les dépendances et les fichiers de ressources.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Exécute une commande et affiche le résultat."""
    print(f"\n🔄 {description}...")
    print(f"Commande: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} réussie")
        if result.stdout:
            print(f"Sortie: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de {description}")
        print(f"Code d'erreur: {e.returncode}")
        print(f"Erreur: {e.stderr}")
        if e.stdout:
            print(f"Sortie: {e.stdout}")
        return False

def ensure_directory_exists(path):
    """Crée un répertoire s'il n'existe pas."""
    Path(path).mkdir(parents=True, exist_ok=True)
    print(f"📁 Répertoire vérifié: {path}")

def copy_file_if_exists(src, dst):
    """Copie un fichier s'il existe."""
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"📋 Fichier copié: {src} -> {dst}")
        return True
    else:
        print(f"⚠️ Fichier non trouvé: {src}")
        return False

def main():
    print("🚀 Construction des exécutables GhostSpy")
    print("=" * 50)
    
    # Vérifier que nous sommes dans le bon répertoire
    if not os.path.exists("client.py") or not os.path.exists("Serveur/server.py"):
        print("❌ Erreur: Veuillez exécuter ce script depuis le répertoire GhostSpy")
        sys.exit(1)
    
    # Nettoyer les anciens builds
    print("\n🧹 Nettoyage des anciens builds...")
    for folder in ["build", "dist", "__pycache__"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"🗑️ Supprimé: {folder}")
    
    # Supprimer les anciens fichiers .spec
    for spec_file in ["client.spec", "server.spec"]:
        if os.path.exists(spec_file):
            os.remove(spec_file)
            print(f"🗑️ Supprimé: {spec_file}")
    
    # Vérifier l'installation de PyInstaller
    if not run_command("pyinstaller --version", "Vérification de PyInstaller"):
        print("❌ PyInstaller n'est pas installé. Installation...")
        if not run_command("pip install pyinstaller", "Installation de PyInstaller"):
            sys.exit(1)
    
    # Construire le client
    print("\n" + "="*50)
    print("🔨 CONSTRUCTION DU CLIENT")
    print("="*50)
    
    client_command = [
        "pyinstaller",
        "--onefile",
        "--noconsole",
        "--name=client_ghostspy_v3",
        "--icon=SpyGhost_icon.ico",
        "--add-data=pdf_data.py;.",
        "--add-data=Networkdata.py;.",
        "--add-data=wifi_info.py;.",
        "--add-data=csv_data.py;.",
        "--add-data=Json_data.py;.",
        "--add-data=SpyGhost_icon.ico;.",
        "--add-data=requirements.txt;.",
        "--hidden-import=reportlab",
        "--hidden-import=reportlab.lib",
        "--hidden-import=reportlab.lib.pagesizes",
        "--hidden-import=reportlab.platypus",
        "--hidden-import=reportlab.graphics",
        "--hidden-import=reportlab.graphics.charts",
        "--hidden-import=psutil",
        "--hidden-import=requests",
        "--hidden-import=wmi",
        "--hidden-import=pandas",
        "--hidden-import=PIL",
        "--hidden-import=watchdog",
        "--hidden-import=customtkinter",
        "--hidden-import=getmac",
        "--collect-all=reportlab",
        "client.py"
    ]
    
    if not run_command(" ".join(client_command), "Construction du client"):
        print("❌ Échec de la construction du client")
        return False
    
    # Construire le serveur
    print("\n" + "="*50)
    print("🔨 CONSTRUCTION DU SERVEUR")
    print("="*50)
    
    # Changer vers le répertoire Serveur
    os.chdir("Serveur")
    
    server_command = [
        "pyinstaller",
        "--onefile",
        "--noconsole",
        "--name=server_ghostspy_v3",
        "--icon=SpyGhost_icon.ico",
        "--add-data=frontend;frontend",
        "--add-data=schema.sql;.",
        "--add-data=SpyGhost_icon.ico;.",
        "--add-data=requirements.txt;.",
        "--hidden-import=flask",
        "--hidden-import=customtkinter",
        "--hidden-import=sqlite3",
        "--hidden-import=PIL",
        "--collect-all=flask",
        "--collect-all=customtkinter",
        "server.py"
    ]
    
    if not run_command(" ".join(server_command), "Construction du serveur"):
        print("❌ Échec de la construction du serveur")
        os.chdir("..")
        return False
    
    # Revenir au répertoire principal
    os.chdir("..")
    
    # Organiser les fichiers de sortie
    print("\n" + "="*50)
    print("📦 ORGANISATION DES FICHIERS")
    print("="*50)
    
    # Créer les répertoires de destination
    client_exe_dir = "Executable Client"
    server_exe_dir = "Executable Server"
    
    ensure_directory_exists(client_exe_dir)
    ensure_directory_exists(server_exe_dir)
    
    # Copier l'exécutable client
    client_exe_src = "dist/client_ghostspy_v3.exe"
    client_exe_dst = os.path.join(client_exe_dir, "client_ghostspy_v3.exe")
    
    if copy_file_if_exists(client_exe_src, client_exe_dst):
        print("✅ Exécutable client copié")
    else:
        print("❌ Impossible de copier l'exécutable client")
        return False
    
    # Copier l'exécutable serveur
    server_exe_src = "Serveur/dist/server_ghostspy_v3.exe"
    server_exe_dst = os.path.join(server_exe_dir, "server_ghostspy_v3.exe")
    
    if copy_file_if_exists(server_exe_src, server_exe_dst):
        print("✅ Exécutable serveur copié")
    else:
        print("❌ Impossible de copier l'exécutable serveur")
        return False
    
    # Copier les fichiers de ressources nécessaires pour le serveur
    server_resources = [
        ("Serveur/frontend", os.path.join(server_exe_dir, "frontend")),
        ("Serveur/schema.sql", os.path.join(server_exe_dir, "schema.sql")),
        ("SpyGhost_icon.ico", os.path.join(server_exe_dir, "SpyGhost_icon.ico")),
        ("requirements.txt", os.path.join(server_exe_dir, "requirements.txt"))
    ]
    
    for src, dst in server_resources:
        if os.path.isdir(src):
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            print(f"📁 Répertoire copié: {src} -> {dst}")
        else:
            copy_file_if_exists(src, dst)
    
    # Copier les fichiers de ressources pour le client
    client_resources = [
        ("SpyGhost_icon.ico", os.path.join(client_exe_dir, "SpyGhost_icon.ico")),
        ("requirements.txt", os.path.join(client_exe_dir, "requirements.txt"))
    ]
    
    for src, dst in client_resources:
        copy_file_if_exists(src, dst)
    
    # Créer un README pour les exécutables
    readme_content = """# GhostSpy v3 - Exécutables

## Structure des fichiers

### Client
- `client_ghostspy_v3.exe` : Exécutable principal du client
- Les logs seront créés automatiquement dans le répertoire parent

### Serveur  
- `server_ghostspy_v3.exe` : Exécutable principal du serveur
- `frontend/` : Interface web du serveur
- `schema.sql` : Schéma de la base de données

## Installation

1. Extraire les fichiers dans un répertoire
2. Exécuter d'abord le serveur
3. Puis exécuter le client
4. Les logs et fichiers PDF seront créés automatiquement

## Dépannage

- Si la génération PDF échoue, vérifiez que les logs existent
- Les fichiers sont créés dans le répertoire parent des exécutables
- Consultez les logs de la console pour plus d'informations

Version construite le: """ + str(Path().absolute()) + """
"""
    
    with open(os.path.join(client_exe_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    with open(os.path.join(server_exe_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    # Nettoyer les fichiers temporaires
    print("\n🧹 Nettoyage final...")
    for folder in ["build", "dist", "Serveur/build", "Serveur/dist"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"🗑️ Supprimé: {folder}")
    
    print("\n" + "="*50)
    print("🎉 CONSTRUCTION TERMINÉE AVEC SUCCÈS!")
    print("="*50)
    print(f"📦 Client: {client_exe_dst}")
    print(f"📦 Serveur: {server_exe_dst}")
    print("\n💡 Conseils d'utilisation:")
    print("1. Placez les logs dans le même répertoire que les exécutables")
    print("2. Exécutez d'abord le serveur, puis le client")
    print("3. Les rapports PDF seront générés dans le répertoire parent")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n❌ Construction interrompue par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 