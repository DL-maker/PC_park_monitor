#!/usr/bin/env python3
"""
Script de nettoyage pour supprimer les anciennes versions de GhostSpy
et garder seulement les nouvelles versions v3 corrigées.
"""

import os
import sys
from pathlib import Path

def cleanup_old_executables():
    """Supprime les anciennes versions d'exécutables."""
    print("🧹 Nettoyage des anciennes versions GhostSpy")
    print("=" * 50)
    
    # Fichiers à supprimer dans Executable Client
    client_old_files = [
        "client_ghostspyv2.exe",
        "client_ghostspy_v2.exe", 
        "client_ghostspy.exe"
    ]
    
    # Fichiers à supprimer dans Executable Server
    server_old_files = [
        "server_ghostspy_v2.exe",
        "server_ghostspy.exe",
        "server_ghostspyv2.exe"
    ]
    
    client_dir = "Executable Client"
    server_dir = "Executable Server"
    
    removed_count = 0
    
    # Nettoyer les anciens clients
    print(f"\n📁 Nettoyage de {client_dir}...")
    for filename in client_old_files:
        filepath = os.path.join(client_dir, filename)
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                print(f"🗑️ Supprimé: {filepath}")
                removed_count += 1
            except Exception as e:
                print(f"❌ Erreur lors de la suppression de {filepath}: {e}")
        else:
            print(f"⚠️ Déjà absent: {filepath}")
    
    # Nettoyer les anciens serveurs
    print(f"\n📁 Nettoyage de {server_dir}...")
    for filename in server_old_files:
        filepath = os.path.join(server_dir, filename)
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                print(f"🗑️ Supprimé: {filepath}")
                removed_count += 1
            except Exception as e:
                print(f"❌ Erreur lors de la suppression de {filepath}: {e}")
        else:
            print(f"⚠️ Déjà absent: {filepath}")
    
    # Nettoyer les anciens fichiers de build
    build_files_to_remove = [
        "client.spec",
        "server.spec",
        "build",
        "dist",
        "__pycache__",
        "Serveur/__pycache__",
        "Serveur/build",
        "Serveur/dist"
    ]
    
    print(f"\n📁 Nettoyage des fichiers de build...")
    for item in build_files_to_remove:
        if os.path.exists(item):
            try:
                if os.path.isdir(item):
                    import shutil
                    shutil.rmtree(item)
                    print(f"🗑️ Répertoire supprimé: {item}")
                else:
                    os.remove(item)
                    print(f"🗑️ Fichier supprimé: {item}")
                removed_count += 1
            except Exception as e:
                print(f"❌ Erreur lors de la suppression de {item}: {e}")
    
    return removed_count

def verify_new_versions():
    """Vérifie que les nouvelles versions v3 sont présentes."""
    print(f"\n✅ Vérification des nouvelles versions...")
    
    v3_files = [
        ("Executable Client/client_ghostspy_v3.exe", "Client v3"),
        ("Executable Server/server_ghostspy_v3.exe", "Serveur v3")
    ]
    
    all_present = True
    
    for filepath, description in v3_files:
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            size_mb = size / (1024 * 1024)
            print(f"✅ {description}: {filepath} ({size_mb:.1f} MB)")
        else:
            print(f"❌ {description}: MANQUANT - {filepath}")
            all_present = False
    
    return all_present

def update_readme_files():
    """Met à jour les fichiers README pour pointer vers les nouvelles versions."""
    print(f"\n📝 Mise à jour des fichiers README...")
    
    # Contenu README pour le client
    client_readme = """# GhostSpy Client v3

## Utilisation

```bash
./client_ghostspy_v3.exe
```

## Nouveautés v3
- ✅ Correction des problèmes de génération PDF
- ✅ Gestion améliorée des timeouts 
- ✅ Retry automatique pour l'envoi des fichiers
- ✅ Détection intelligente des logs

## Support
Consultez le guide principal: GUIDE_UTILISATION_v3.md
"""
    
    # Contenu README pour le serveur  
    server_readme = """# GhostSpy Server v3

## Utilisation

```bash
./server_ghostspy_v3.exe
```

## Accès web
- URL: http://localhost:5000
- Configurez les identifiants admin au premier lancement

## Nouveautés v3
- ✅ Amélioration de la gestion des chemins PDF
- ✅ Vérification de l'intégrité des fichiers
- ✅ Messages d'erreur plus détaillés
- ✅ Timeout et retry automatiques

## Support
Consultez le guide principal: GUIDE_UTILISATION_v3.md
"""
    
    # Écrire les README
    try:
        with open("Executable Client/README_v3.md", "w", encoding="utf-8") as f:
            f.write(client_readme)
        print("✅ README client v3 créé")
        
        with open("Executable Server/README_v3.md", "w", encoding="utf-8") as f:
            f.write(server_readme)
        print("✅ README serveur v3 créé")
        
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la création des README: {e}")
        return False

def main():
    """Fonction principale du script de nettoyage."""
    print(f"📅 Nettoyage effectué le: {Path().absolute()}")
    
    # Vérifier qu'on est dans le bon répertoire
    if not os.path.exists("client.py") or not os.path.exists("Serveur"):
        print("❌ Erreur: Veuillez exécuter ce script depuis le répertoire GhostSpy")
        return False
    
    # Étape 1: Nettoyer les anciennes versions
    removed_count = cleanup_old_executables()
    
    # Étape 2: Vérifier les nouvelles versions
    versions_ok = verify_new_versions()
    
    # Étape 3: Mettre à jour les README
    readme_ok = update_readme_files()
    
    # Résumé
    print("\n" + "=" * 50)
    print("📋 RÉSUMÉ DU NETTOYAGE")
    print("=" * 50)
    print(f"🗑️ Fichiers supprimés: {removed_count}")
    print(f"✅ Nouvelles versions: {'Présentes' if versions_ok else 'MANQUANTES'}")
    print(f"📝 README mis à jour: {'Oui' if readme_ok else 'Non'}")
    
    if versions_ok and readme_ok:
        print("\n🎉 Nettoyage terminé avec succès!")
        print("💡 Vous pouvez maintenant utiliser les nouvelles versions v3:")
        print("   📦 Client: Executable Client/client_ghostspy_v3.exe")
        print("   📦 Serveur: Executable Server/server_ghostspy_v3.exe")
        print("   📖 Guide: GUIDE_UTILISATION_v3.md")
        return True
    else:
        print("\n❌ Problèmes détectés lors du nettoyage")
        if not versions_ok:
            print("⚠️ Les nouvelles versions v3 ne sont pas toutes présentes")
        if not readme_ok:
            print("⚠️ Erreur lors de la mise à jour des README")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n❌ Nettoyage interrompu par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 