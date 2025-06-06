#!/usr/bin/env python3
"""
Script de test pour vérifier la génération PDF de GhostSpy.
Ce script teste la génération PDF de manière isolée pour identifier les problèmes.
"""

import os
import sys
import time
from datetime import datetime

def test_pdf_generation():
    """Test la génération PDF."""
    print("🧪 Test de génération PDF GhostSpy")
    print("=" * 50)
    
    # Vérifier que nous sommes dans le bon répertoire
    if not os.path.exists("pdf_data.py"):
        print("❌ Erreur: pdf_data.py non trouvé dans le répertoire courant")
        return False
    
    # Vérifier les fichiers de logs requis
    logs_required = ["port_activity.log", "internet_usage.log"]
    missing_logs = []
    
    for log_file in logs_required:
        if not os.path.exists(log_file):
            missing_logs.append(log_file)
    
    if missing_logs:
        print(f"⚠️ Fichiers de logs manquants: {missing_logs}")
        print("📝 Création de fichiers de logs de test...")
        
        # Créer des logs de test
        with open("port_activity.log", "w", encoding="utf-8") as f:
            f.write("[2025-01-20 10:00:00] Service: HTTPS | 192.168.1.100:8080 -> 8.8.8.8:443 | PID: 1234 (chrome.exe)\n")
            f.write("[2025-01-20 10:01:00] Service: HTTP | 192.168.1.100:8081 -> 1.1.1.1:80 | PID: 5678 (firefox.exe)\n")
        
        with open("internet_usage.log", "w", encoding="utf-8") as f:
            f.write("[2025-01-20 10:00:00] Sent: 0.5 MB, Received: 1.2 MB, Total: 1.7 MB\n")
            f.write("[2025-01-20 10:05:00] Sent: 0.3 MB, Received: 0.8 MB, Total: 1.1 MB\n")
        
        print("✅ Fichiers de logs de test créés")
    
    try:
        print("\n🔄 Import du module pdf_data...")
        import pdf_data
        
        print("✅ Module pdf_data importé avec succès")
        
        # Vérifier les données
        print("\n📊 Vérification des données...")
        print(f"  - Répertoire de base: {pdf_data.BASE_DIR}")
        print(f"  - Port activity log: {pdf_data.PORT_ACTIVITY_LOG}")
        print(f"  - Internet usage log: {pdf_data.INTERNET_USAGE_LOG}")
        print(f"  - Protocoles détectés: {len(pdf_data.protocols)}")
        print(f"  - Données système disponibles: {'Oui' if pdf_data.data else 'Non'}")
        
        # Test de génération
        output_file = "test_report.pdf"
        if os.path.exists(output_file):
            os.remove(output_file)
            print(f"🗑️ Ancien fichier de test supprimé: {output_file}")
        
        print(f"\n⏳ Génération du PDF de test: {output_file}")
        start_time = time.time()
        
        success = pdf_data.create_pdf_with_data(output_file, pdf_data.data)
        
        end_time = time.time()
        duration = end_time - start_time
        
        if success:
            if os.path.exists(output_file):
                file_size = os.path.getsize(output_file)
                print(f"✅ PDF généré avec succès!")
                print(f"   📁 Fichier: {os.path.abspath(output_file)}")
                print(f"   📏 Taille: {file_size} octets")
                print(f"   ⏱️ Temps: {duration:.2f} secondes")
                
                if file_size < 1024:
                    print("⚠️ Attention: Fichier très petit, peut être corrompu")
                    return False
                
                return True
            else:
                print("❌ Génération signalée comme réussie mais fichier non trouvé")
                return False
        else:
            print("❌ Échec de la génération PDF")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        print(f"📋 Traceback: {traceback.format_exc()}")
        return False

def test_executable_generation():
    """Test la génération PDF via l'exécutable."""
    print("\n🔬 Test via l'exécutable client")
    print("=" * 50)
    
    exe_path = os.path.join("Executable Client", "client_ghostspy_v3.exe")
    if not os.path.exists(exe_path):
        print(f"⚠️ Exécutable non trouvé: {exe_path}")
        return False
    
    print(f"📦 Exécutable trouvé: {exe_path}")
    
    # Copier les logs vers le répertoire parent de l'exécutable
    parent_dir = os.path.dirname(os.path.abspath(exe_path))
    parent_parent_dir = os.path.dirname(parent_dir)
    
    logs_to_copy = ["port_activity.log", "internet_usage.log"]
    for log_file in logs_to_copy:
        if os.path.exists(log_file):
            dest_path = os.path.join(parent_parent_dir, log_file)
            if not os.path.exists(dest_path):
                import shutil
                shutil.copy2(log_file, dest_path)
                print(f"📋 Log copié: {log_file} -> {dest_path}")
    
    print("💡 Pour tester l'exécutable:")
    print(f"   1. Lancez: {exe_path}")
    print(f"   2. Configurez l'URL du serveur")
    print(f"   3. Testez la génération PDF depuis l'interface web")
    print(f"   4. Vérifiez que le PDF apparaît dans: {parent_parent_dir}")
    
    return True

def main():
    """Fonction principale du test."""
    print(f"📅 Test effectué le: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 Répertoire de travail: {os.getcwd()}")
    
    # Test 1: Génération directe
    success1 = test_pdf_generation()
    
    # Test 2: Vérification de l'exécutable
    success2 = test_executable_generation()
    
    print("\n" + "=" * 50)
    print("📋 RÉSUMÉ DES TESTS")
    print("=" * 50)
    print(f"✅ Génération PDF directe: {'Réussie' if success1 else 'Échec'}")
    print(f"✅ Préparation exécutable: {'Réussie' if success2 else 'Échec'}")
    
    if success1 and success2:
        print("\n🎉 Tous les tests sont réussis!")
        print("💡 Le système de génération PDF devrait fonctionner correctement.")
        return True
    else:
        print("\n❌ Certains tests ont échoué.")
        print("💡 Vérifiez les erreurs ci-dessus pour diagnostiquer les problèmes.")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n❌ Test interrompu par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 