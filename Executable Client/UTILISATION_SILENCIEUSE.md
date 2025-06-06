# 🔇 GhostSpy Client Silencieux - Guide d'Utilisation

## ⚡ **Démarrage Rapide**

### 1️⃣ **Lancer le Client (Arrière-plan)**
```
✅ Double-clic sur : client_ghostspy.exe
✅ Résultat : AUCUNE fenêtre ne s'ouvre
✅ Le client fonctionne maintenant en arrière-plan
```

### 2️⃣ **Vérifier que ça marche**
- **Gestionnaire des tâches** : Chercher `client_ghostspy.exe` dans les processus
- **Interface serveur** : Aller sur http://localhost:5000 et voir si le client apparaît

### 3️⃣ **Arrêter le Client**
- **Gestionnaire des tâches** → Terminer `client_ghostspy.exe`
- **OU via l'interface serveur** → Commandes d'arrêt

## 🎯 **Principales Différences avec l'Ancienne Version**

| Avant (v1) | Maintenant (v2) |
|------------|-----------------|
| ❌ Terminal affiché | ✅ Arrière-plan silencieux |
| ❌ Fenêtre visible | ✅ Invisible à l'utilisateur |
| ❌ Peut être fermé accidentellement | ✅ Fonctionne discrètement |

## 🔍 **Surveillance Active**

Une fois lancé, le client :
- 📸 **Capture l'écran** automatiquement
- 🔍 **Surveille les fichiers** (si activé)
- 🦠 **Analyse VirusTotal** (si activé)
- 💻 **Exécute les commandes** du serveur

## ⚠️ **Important à Retenir**

### ✅ **Avantages du Mode Silencieux :**
- Surveillance discrète
- Pas d'interruption de l'utilisateur
- Fonctionnement continu en arrière-plan

### ⚠️ **Attention :**
- Plus difficile à détecter qu'il fonctionne
- Vérifier via le gestionnaire des tâches si nécessaire
- S'assurer que le serveur est bien démarré avant le client

---
**🚀 Prêt à utiliser ! Double-clic et c'est parti en arrière-plan !** 