# 🎯 Guide des Exécutables GhostSpy

## 📦 **Exécutables Disponibles**

### 🖥️ **SERVEUR - UTILISEZ CETTE VERSION :**
- **`server_ghostspy_v2.exe`** ✅ **← NOUVELLE VERSION CORRIGÉE**
  - **Taille :** 27MB
  - **Fonctionnalités :** Interface web complète incluse
  - **Corrections :** Erreur "Not Found" résolue
  - **Contenu :** Fichiers frontend intégrés dans l'exécutable

### 🖥️ **Serveur - Ancienne version :**
- **`server_ghostspy.exe`** ❌ **← ÉVITER (erreur "Not Found")**
  - **Problème :** Ne trouve pas les fichiers frontend
  - **État :** Obsolète, remplacé par v2

### 🕵️ **CLIENT :**
- **`client_ghostspy.exe`** ✅ **← VERSION CORRIGÉE**
  - **Taille :** 31MB  
  - **Fonctionnalités :** Toutes les corrections appliquées
  - **VirusTotal :** Fonctionnel
  - **Surveillance :** Complète

## 🚀 **Instructions d'Utilisation**

### 📋 **Étape 1 : Lancer le Serveur**
```bash
# Dans le dossier "Executable Server"
Double-clic sur : server_ghostspy_v2.exe
```

### 📋 **Étape 2 : Accéder à l'Interface Web**
- Ouvrir un navigateur
- Aller à : `http://localhost:5000`
- Login : `admin` / `123456`

### 📋 **Étape 3 : Lancer le Client**
```bash
# Dans le dossier "Executable Client"
Double-clic sur : client_ghostspy.exe
```

## ⚠️ **Problèmes Résolus**

### ❌ Erreur "Not Found" 
**Problème :** L'ancien serveur ne trouvait pas les fichiers web
**Solution :** Utiliser `server_ghostspy_v2.exe` qui inclut les fichiers frontend

### ❌ Erreur "Détection de fichiers suspects"
**Problème :** VirusTotal ne s'affichait pas correctement
**Solution :** JavaScript corrigé dans la nouvelle version

### ❌ Routes API manquantes
**Problème :** Certaines fonctionnalités ne fonctionnaient pas
**Solution :** Toutes les routes ajoutées dans v2

## 📁 **Structure Finale Recommandée**

```
GhostSpy/
├── Executable Server/
│   ├── server_ghostspy_v2.exe    ← UTILISER CETTE VERSION
│   ├── clients.db
│   ├── config.json
│   └── frontend/                 ← Dossier de sauvegarde
│
└── Executable Client/
    ├── client_ghostspy.exe       ← VERSION CORRIGÉE
    └── README_CLIENT.md
```

## 🔧 **Dépannage**

### Si vous avez encore l'erreur "Not Found" :
1. Assurez-vous d'utiliser `server_ghostspy_v2.exe`
2. Redémarrez complètement l'exécutable
3. Vérifiez que le port 5000 n'est pas déjà utilisé

### Si VirusTotal ne fonctionne pas :
1. Vérifiez que les paramètres sont activés dans l'interface web
2. Le client doit être relancé après modification des paramètres

---
**Versions :** Server v2.0 + Client v2.0  
**Date :** Janvier 2025  
**État :** ✅ Toutes les fonctionnalités opérationnelles 