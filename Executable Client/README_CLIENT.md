# ��️ GhostSpy Client - Version Silencieuse (v2.0)

## 📋 Version Mise à Jour - Arrière-Plan
Cette version contient toutes les corrections et fonctionne maintenant **en arrière-plan sans terminal** :

### ✅ **Fonctionnalités Corrigées :**
- **Intégration VirusTotal** : Analyse automatique des fichiers suspects
- **Journal d'activité** : Surveillance des fichiers et dossiers
- **Gel/Dégel écran** : Contrôle à distance de l'écran
- **Historique commandes** : Traçabilité complète des actions
- **Transfert de fichiers** : Upload/Download sécurisé
- **Corrections de synchronisation** : Communication serveur optimisée

### 🔇 **NOUVEAU : Fonctionnement Silencieux**
- **Pas de terminal** affiché lors du lancement
- **Fonctionne en arrière-plan** invisible à l'utilisateur
- **Icône système** visible dans la barre des tâches
- **Discrétion maximale** pour la surveillance

## 🚀 **Comment utiliser :**

1. **Lancement simple :**
   ```
   Double-clic sur client_ghostspy.exe
   ```
   ➜ **Aucune fenêtre ne s'ouvre**, le client fonctionne en arrière-plan

2. **Configuration automatique :**
   - Se connecte automatiquement au serveur (localhost:5000 par défaut)
   - Génère un identifiant unique basé sur le nom de la machine
   - Envoie des captures d'écran automatiques
   - Exécute les commandes reçues du serveur

3. **Vérification du fonctionnement :**
   - Aller sur l'interface web du serveur (http://localhost:5000)
   - Vérifier que le client apparaît dans la liste des clients connectés
   - Le client peut apparaître avec un nom comme "DESKTOP-XXXXXX"

## 🔍 **Comment savoir si le client fonctionne :**

### ✅ **Indicateurs de fonctionnement :**
- **Gestionnaire des tâches** : Processus `client_ghostspy.exe` visible
- **Interface serveur** : Client listé comme "Connecté" 
- **Captures d'écran** : Mises à jour automatiquement
- **Réponse aux commandes** : Exécution immédiate

### ❌ **Si le client ne fonctionne pas :**
- Vérifier que le serveur est démarré sur le port 5000
- Contrôler les permissions Windows (antivirus)
- Redémarrer en tant qu'administrateur si nécessaire

## 🛑 **Comment arrêter le client :**

1. **Via le gestionnaire des tâches :**
   - Ouvrir le Gestionnaire des tâches (Ctrl+Shift+Échap)
   - Chercher `client_ghostspy.exe`
   - Clic droit → "Terminer la tâche"

2. **Via l'interface serveur :**
   - Aller sur http://localhost:5000
   - Sélectionner le client
   - Utiliser les commandes d'arrêt

## ⚙️ **Paramètres par défaut :**
- **Serveur cible :** `localhost:5000`
- **Interval capture :** 5 secondes
- **VirusTotal :** Activé si configuré sur le serveur
- **Logs activité :** Selon configuration serveur

---
**Version :** Client v2.0 (Silencieux)  
**Caractéristiques :** Arrière-plan, Pas de console, Discret  
**État :** ✅ Entièrement fonctionnel

## 🔒 **Sécurité :**
- Communication chiffrée avec le serveur
- Authentification par token
- Analyses VirusTotal pour détecter les malwares
- Logs détaillés de toutes les activités

## 📝 **Logs :**
L'application génère automatiquement :
- `port_activity.log` : Activité réseau
- `internet_usage.log` : Utilisation internet
- `client_vt.log` : Résultats VirusTotal

---
**Version :** v2.0 Corrigée  
**Date :** Janvier 2025  
**Taille :** ~31MB 