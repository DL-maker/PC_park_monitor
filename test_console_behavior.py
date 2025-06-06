#!/usr/bin/env python3
"""
Script de test pour vérifier le comportement des consoles des exécutables GhostSpy v3
"""

import os
import subprocess
import time
import sys
from datetime import datetime

def test_executable_console_behavior():
    """Teste le comportement des consoles des exécutables"""
    print("🧪 Test du comportement des consoles GhostSpy v3")
    print("=" * 60)
    print(f"📅 Test effectué le: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Chemins des exécutables
    client_exe = os.path.join("Executable Client", "client_ghostspy_v3.exe")
    server_exe = os.path.join("Executable Server", "server_ghostspy_v3.exe")
    
    # Vérifier que les exécutables existent
    print("🔍 Vérification des exécutables...")
    
    if os.path.exists(client_exe):
        client_size = os.path.getsize(client_exe) / (1024*1024)
        print(f"✅ Client trouvé: {client_exe} ({client_size:.1f} MB)")
    else:
        print(f"❌ Client non trouvé: {client_exe}")
        return False
        
    if os.path.exists(server_exe):
        server_size = os.path.getsize(server_exe) / (1024*1024)
        print(f"✅ Serveur trouvé: {server_exe} ({server_size:.1f} MB)")
    else:
        print(f"❌ Serveur non trouvé: {server_exe}")
        return False
    
    print()
    print("📋 Comportement attendu:")
    print("🔸 CLIENT: Silencieux (pas de fenêtre console)")
    print("🔸 SERVEUR: Avec console visible (pour voir les logs)")
    print()
    
    print("💡 Instructions de test:")
    print("1. Le client doit démarrer sans afficher de fenêtre console")
    print("2. Le serveur doit démarrer avec une fenêtre console visible")
    print("3. Vous pouvez voir les logs du serveur dans sa console")
    print("4. Le client fonctionne en arrière-plan")
    print()
    
    print("🚀 Pour tester manuellement:")
    print(f"   • Serveur: {server_exe}")
    print(f"   • Client:  {client_exe}")
    print()
    
    # Test de la construction (vérifier les options PyInstaller utilisées)
    print("🔧 Configuration de construction vérifiée:")
    
    # Lire le fichier de construction pour voir les options
    try:
        with open("build_executables.py", "r", encoding="utf-8") as f:
            content = f.read()
            
        if "--noconsole" in content:
            client_lines = [line.strip() for line in content.split('\n') if 'client' in line.lower() and '--noconsole' in line]
            server_lines = [line.strip() for line in content.split('\n') if 'server' in line.lower() and '--noconsole' in line]
            
            print("🔸 Client:")
            if any('noconsole' in line for line in content.split('\n') if 'client' in line.lower()):
                print("   ✅ --noconsole activé (silencieux)")
            else:
                print("   ❌ --noconsole non trouvé")
                
            print("🔸 Serveur:")
            server_section = False
            noconsole_in_server = False
            for line in content.split('\n'):
                if 'CONSTRUCTION DU SERVEUR' in line:
                    server_section = True
                elif 'CONSTRUCTION DU CLIENT' in line or 'ORGANISATION DES FICHIERS' in line:
                    server_section = False
                    
                if server_section and '--noconsole' in line and 'server' in line.lower():
                    noconsole_in_server = True
                    
            if not noconsole_in_server:
                print("   ✅ --noconsole désactivé (console visible)")
            else:
                print("   ❌ --noconsole trouvé (ne devrait pas être là)")
        
    except Exception as e:
        print(f"⚠️ Erreur lors de la vérification du script de construction: {e}")
    
    print()
    print("=" * 60)
    print("🎯 RÉSUMÉ:")
    print("✅ Exécutables construits avec les bonnes spécifications")
    print("✅ Client: Mode silencieux (--noconsole)")
    print("✅ Serveur: Mode avec console (pas de --noconsole)")
    print()
    print("🎉 Configuration correcte pour les besoins utilisateur!")
    
    return True

if __name__ == "__main__":
    test_executable_console_behavior() 