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
    
    # Nettoyer les anciens builds
    print("\n🧹 Nettoyage des anciens builds...")
    cleanup_paths = ["__pycache__", "build", "dist", "Serveur/__pycache__", "Serveur/build", "Serveur/dist"]
    for path in cleanup_paths:
        if os.path.exists(path):
            shutil.rmtree(path)
            print(f"🗑️ Supprimé: {path}")
    
    # Vérifier PyInstaller
    print("\n🔄 Vérification de PyInstaller...")
    if not run_command("pyinstaller --version", "Vérification de PyInstaller"):
        return False
    
    print("\n" + "=" * 50)
    print("🔨 CONSTRUCTION DU CLIENT")
    print("=" * 50)
    
    # Construction du client (SANS CONSOLE - silencieux)
    client_cmd = [
        "pyinstaller",
        "--onefile",
        "--noconsole",  # Client silencieux
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
    
    print("\n🔄 Construction du client...")
    if not run_command(" ".join(client_cmd), "Construction du client"):
        return False
    
    print("\n" + "=" * 50)
    print("🔨 CONSTRUCTION DU SERVEUR")
    print("=" * 50)
    
    # Se déplacer dans le dossier Serveur
    os.chdir("Serveur")
    
    # Construction du serveur (AVEC CONSOLE - pour voir les logs)
    server_cmd = [
        "pyinstaller",
        "--onefile",
        # PAS de --noconsole pour le serveur - on veut voir les logs
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
    
    print("\n🔄 Construction du serveur...")
    if not run_command(" ".join(server_cmd), "Construction du serveur"):
        os.chdir("..")
        return False
    
    # Retour au dossier principal
    os.chdir("..")
    
    print("\n" + "=" * 50)
    print("📦 ORGANISATION DES FICHIERS")
    print("=" * 50)
    
    # S'assurer que les dossiers de destination existent
    ensure_directory_exists("Executable Client")
    ensure_directory_exists("Executable Server")
    
    # Copier l'exécutable client
    client_exe_src = "dist/client_ghostspy_v3.exe"
    client_exe_dst = "Executable Client/client_ghostspy_v3.exe"
    
    if copy_file_if_exists(client_exe_src, client_exe_dst):
        print("✅ Exécutable client copié")
    else:
        print("❌ Erreur: Exécutable client non trouvé")
        return False
    
    # Copier l'exécutable serveur
    server_exe_src = "Serveur/dist/server_ghostspy_v3.exe"
    server_exe_dst = "Executable Server/server_ghostspy_v3.exe"
    
    if copy_file_if_exists(server_exe_src, server_exe_dst):
        print("✅ Exécutable serveur copié")
    else:
        print("❌ Erreur: Exécutable serveur non trouvé")
        return False
    
    # Copier les fichiers nécessaires pour le serveur
    server_files = [
        ("Serveur/frontend", "Executable Server/frontend"),
        ("Serveur/schema.sql", "Executable Server/schema.sql"),
        ("SpyGhost_icon.ico", "Executable Server/SpyGhost_icon.ico"),
        ("requirements.txt", "Executable Server/requirements.txt"),
    ]
    
    for src, dst in server_files:
        if os.path.isdir(src):
            # Copier un dossier
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            print(f"📁 Répertoire copié: {src} -> {dst}")
        else:
            # Copier un fichier
            copy_file_if_exists(src, dst)
    
    # Copier les fichiers nécessaires pour le client
    client_files = [
        ("SpyGhost_icon.ico", "Executable Client/SpyGhost_icon.ico"),
        ("requirements.txt", "Executable Client/requirements.txt"),
    ]
    
    for src, dst in client_files:
        copy_file_if_exists(src, dst)
    
    # Nettoyage final
    print("\n🧹 Nettoyage final...")
    cleanup_paths = ["build", "dist", "Serveur/build", "Serveur/dist"]
    for path in cleanup_paths:
        if os.path.exists(path):
            shutil.rmtree(path)
            print(f"🗑️ Supprimé: {path}")
    
    print("\n" + "=" * 50)
    print("🎉 CONSTRUCTION TERMINÉE AVEC SUCCÈS!")
    print("=" * 50)
    print(f"📦 Client: Executable Client\\client_ghostspy_v3.exe (SILENCIEUX)")
    print(f"📦 Serveur: Executable Server\\server_ghostspy_v3.exe (AVEC TERMINAL)")
    
    print("\n💡 Conseils d'utilisation:")
    print("1. Le serveur affichera ses logs dans un terminal visible")
    print("2. Le client fonctionnera en arrière-plan sans fenêtre")
    print("3. Placez les logs dans le même répertoire que les exécutables")
    print("4. Exécutez d'abord le serveur, puis le client")
    print("5. Les rapports PDF seront générés dans le répertoire parent")
    
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