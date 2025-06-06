# Guide d'utilisation des consoles - GhostSpy v3

## 🎯 Comportement des consoles

### 🔸 **SERVEUR** (`server_ghostspy_v3.exe`)
- ✅ **Console VISIBLE** 
- 📊 Affiche les logs en temps réel
- 🔍 Permet de surveiller l'activité du serveur
- ⚡ Affiche les connexions clients, erreurs, et états

**Avantages :**
- Surveillance en temps réel de l'activité
- Diagnostic facile des problèmes
- Visibilité sur les connexions clients
- Logs d'erreurs directement visibles

### 🔸 **CLIENT** (`client_ghostspy_v3.exe`)
- ❌ **Console CACHÉE** (mode silencieux)
- 🤫 Fonctionne en arrière-plan
- 👤 Invisible pour l'utilisateur surveillé
- 📝 Les logs sont sauvegardés dans des fichiers

**Avantages :**
- Fonctionnement discret
- Pas d'interface visible
- Surveillance silencieuse
- Démarrage automatique possible

## 🚀 Utilisation

### Démarrage du serveur
```cmd
cd "Executable Server"
server_ghostspy_v3.exe
```
**Résultat :** Une fenêtre console s'ouvre et affiche :
```
🚀 Démarrage du serveur GhostSpy v3
📡 Serveur en écoute sur http://localhost:5000
✅ Base de données initialisée
⏱️ En attente de connexions clients...
```

### Démarrage du client
```cmd
cd "Executable Client"  
client_ghostspy_v3.exe
```
**Résultat :** Aucune fenêtre visible, le processus fonctionne en arrière-plan.

## 📊 Surveillance des logs

### Logs du serveur
- **Console :** Logs visibles en temps réel
- **Fichier :** `server.log` (si configuré)

### Logs du client
- **Fichiers uniquement :**
  - `port_activity.log` - Activité réseau
  - `internet_usage.log` - Usage internet
  - `client_vt.log` - Logs détaillés

## 🔧 Vérification du fonctionnement

### Vérifier que le serveur fonctionne
1. Console ouverte avec logs visibles
2. Interface web accessible : http://localhost:5000
3. Messages de connexion clients dans la console

### Vérifier que le client fonctionne
```cmd
# Vérifier le processus en cours
tasklist | findstr client_ghostspy_v3
```

### Vérifier les logs générés
```cmd
dir *.log
```

## 🛠️ Dépannage

### Problème serveur
- **Symptôme :** Pas de console visible
- **Cause :** Version incorrecte
- **Solution :** Utiliser `server_ghostspy_v3.exe` construit avec cette version

### Problème client
- **Symptôme :** Console visible
- **Cause :** Version incorrecte  
- **Solution :** Utiliser `client_ghostspy_v3.exe` construit avec cette version

### Reconstruction si nécessaire
```cmd
cd GhostSpy
python build_executables.py
```

## 📋 Résumé des différences

| Composant | Console | Visibilité | Logs |
|-----------|---------|------------|------|
| **Serveur v3** | ✅ Visible | Ouverte | Console + fichiers |
| **Client v3** | ❌ Cachée | Arrière-plan | Fichiers uniquement |

## 🎉 Avantages de cette configuration

1. **Administration facile** : Logs serveur visibles en temps réel
2. **Surveillance discrète** : Client invisible à l'utilisateur
3. **Diagnostic rapide** : Erreurs serveur immédiatement visibles
4. **Fonctionnement optimal** : Chaque composant adapté à son usage

---

*GhostSpy v3 - Configuration optimisée pour administration et surveillance discrète* 