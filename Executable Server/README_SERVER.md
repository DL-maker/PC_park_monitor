# 🖥️ GhostSpy Server - Nouvel Exécutable

## 📋 Version Mise à Jour
Cette version contient toutes les corrections et améliorations récentes :

### ✅ **Fonctionnalités Corrigées :**
- **Interface Web Moderne** : Dashboard complet et responsive
- **Intégration VirusTotal** : Affichage des résultats de scan
- **Gestion des Clients** : Monitoring en temps réel
- **Routes API Complètes** : Toutes les fonctionnalités accessibles
- **Base de Données** : SQLite optimisée avec toutes les colonnes
- **Corrections de Synchronisation** : Communication client optimisée

## 🚀 **Comment utiliser :**

1. **Lancement simple :**
   ```
   Double-clic sur server_ghostspy.exe
   ```

2. **Accès à l'interface web :**
   - Ouvrir un navigateur
   - Aller à : `http://localhost:5000`
   - Login : `admin` / Password : `123456`

3. **Structure des fichiers :**
   ```
   Executable Server/
   ├── server_ghostspy.exe    # Serveur principal
   ├── frontend/              # Interface web
   │   ├── index.html
   │   ├── script.js
   │   ├── style.css
   │   └── settings.html
   ├── clients.db            # Base de données
   └── screenshots/          # Captures d'écran (créé auto)
   ```

## 🌐 **Fonctionnalités de l'Interface Web :**

### 📊 **Dashboard Principal :**
- Vue d'ensemble des clients connectés
- Statistiques en temps réel
- Alertes de sécurité

### 👥 **Gestion des Clients :**
- Liste des appareils connectés/déconnectés
- Informations détaillées (OS, IP, etc.)
- Actions à distance (commandes, extinction, etc.)

### 🖥️ **Monitoring en Temps Réel :**
- Captures d'écran automatiques
- Surveillance CPU/RAM
- Journaux d'activité fichiers
- Historique des commandes

### 🦠 **Sécurité VirusTotal :**
- Détection automatique de fichiers suspects
- Résultats d'analyse détaillés
- Alertes de malwares en temps réel

### ⚙️ **Paramètres Avancés :**
- Configuration par client
- Activation/désactivation des fonctionnalités
- Seuils d'alerte personnalisables

## 🔧 **Configuration Avancée :**

### Modifier les identifiants de connexion :
Éditez le fichier source `server.py` avant compilation :

```python
# Identifiants admin
USERNAME = "admin"
PASSWORD = "votre_nouveau_mot_de_passe"

# Configuration serveur
PORT = 5000
HOST = "0.0.0.0"  # Écoute sur toutes les interfaces
```

### Clé API VirusTotal :
Pour activer l'analyse VirusTotal, ajoutez votre clé API dans les paramètres client.

## 📡 **Ports et Réseau :**
- **Port principal :** 5000 (HTTP)
- **Interface :** Accessible via navigateur web
- **Base de données :** SQLite locale (clients.db)

## 🗄️ **Base de Données :**
La base de données `clients.db` contient :
- Informations des clients
- Historique des commandes
- Logs d'activité
- Résultats VirusTotal
- Paramètres de configuration

## 📝 **Logs et Rapports :**
- Génération automatique de rapports PDF
- Exportation des données client
- Logs détaillés de toutes les activités

## 🔒 **Sécurité :**
- Authentification web obligatoire
- Tokens sécurisés pour les clients
- Chiffrement des communications
- Isolation des données par client

---
**Version :** v2.0 Corrigée  
**Date :** Janvier 2025  
**Taille :** ~27MB  
**Interface :** Web responsive moderne 