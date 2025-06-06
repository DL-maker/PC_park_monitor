# GhostSpy v3 - Guide d'utilisation

## 🆕 Nouveautés de la version 3

### Corrections majeures de la génération PDF
- ✅ **Résolution des blocages infinis** lors de la génération PDF
- ✅ **Amélioration de la gestion des chemins** dans les exécutables
- ✅ **Timeout automatique** pour éviter les blocages (120 secondes)
- ✅ **Gestion robuste des erreurs** avec messages détaillés
- ✅ **Retry automatique** pour l'envoi des fichiers PDF
- ✅ **Détection intelligente des logs** dans différents emplacements

### Améliorations techniques
- 🔧 Meilleure détection des répertoires de travail
- 🔧 Gestion améliorée des imports dans les exécutables
- 🔧 Logs de débogage plus détaillés
- 🔧 Vérification de l'intégrité des fichiers PDF
- 🔧 Nettoyage automatique des fichiers temporaires

---

## 📦 Structure des fichiers

```
GhostSpy/
├── Executable Client/
│   ├── client_ghostspy_v3.exe     # ✨ Nouveau client corrigé
│   ├── SpyGhost_icon.ico
│   └── README.md
├── Executable Server/
│   ├── server_ghostspy_v3.exe     # ✨ Nouveau serveur corrigé
│   ├── frontend/                  # Interface web
│   ├── schema.sql
│   └── README.md
├── port_activity.log              # Logs d'activité réseau
├── internet_usage.log             # Logs d'utilisation internet
└── data.pdf                       # PDF généré (créé automatiquement)
```

---

## 🚀 Installation et utilisation

### 1. Préparation
```bash
# Les logs doivent être présents dans le répertoire principal GhostSpy
# Ils sont générés automatiquement par le client
```

### 2. Lancement du serveur
```bash
# Naviguer vers le répertoire Executable Server
cd "Executable Server"

# Lancer le serveur
./server_ghostspy_v3.exe
```

### 3. Lancement du client
```bash
# Dans un autre terminal, naviguer vers Executable Client
cd "Executable Client"

# Lancer le client
./client_ghostspy_v3.exe
```

### 4. Configuration
1. **Serveur** : Configurer les identifiants admin lors du premier lancement
2. **Client** : Entrer l'URL du serveur (ex: `http://localhost:5000`)
3. **Interface web** : Accéder à `http://localhost:5000` avec les identifiants admin

---

## 📊 Génération de rapports PDF

### Depuis l'interface web

1. Accéder à l'interface web du serveur
2. Sélectionner un client connecté
3. Cliquer sur **"Générer rapport PDF"**
4. Attendre la génération (message de progression affiché)
5. Télécharger le rapport une fois généré

### Résolution des problèmes

#### ❌ "Échec de la génération du rapport PDF"
**Causes possibles :**
- Logs d'activité manquants ou vides
- Problème de permissions de fichier
- Timeout de génération

**Solutions :**
1. Vérifier la présence des logs dans le répertoire principal
2. Relancer le client pour régénérer les logs
3. Vérifier les permissions du répertoire

#### ⏳ "Génération en cours..." infini
**Nouveau dans v3 :** Cette situation est automatiquement résolue avec le timeout de 120 secondes.

**Si le problème persiste :**
1. Redémarrer le client
2. Vérifier que les fichiers de logs ne sont pas corrompus
3. Consulter les logs de la console pour plus de détails

---

## 🔧 Dépannage avancé

### Logs de débogage
Les nouvelles versions affichent des logs détaillés :

```
📂 PDF Data - Répertoire de base: C:\GhostSpy
📂 PDF Data - Port activity log: C:\GhostSpy\port_activity.log
📂 PDF Data - Internet usage log: C:\GhostSpy\internet_usage.log
✅ Analyse du trafic réussie: 5 types trouvés
✅ PDF généré avec succès: C:\GhostSpy\data.pdf
```

### Vérification manuelle
Pour tester la génération PDF indépendamment :

```bash
# Depuis le répertoire principal GhostSpy
python test_pdf_generation.py
```

### Structure des logs requise

**port_activity.log** :
```
[2025-06-06 15:17:01] Service: HTTPS | 192.168.1.50:51548 -> 18.233.240.219:443 | PID: 14596 (Cursor.exe)
```

**internet_usage.log** :
```
[2025-06-06 15:17:01] Sent: 0.08 MB, Received: 0.14 MB, Total: 0.22 MB
```

---

## 📋 Spécifications techniques

### Nouveaux timeouts
- **Génération PDF** : 120 secondes maximum
- **Envoi au serveur** : 120 secondes maximum
- **Retry automatique** : 3 tentatives avec délai progressif

### Gestion des chemins
- Détection automatique du répertoire de travail
- Support des exécutables PyInstaller
- Recherche intelligente des fichiers de logs
- Copie automatique des logs si nécessaire

### Robustesse
- Vérification de l'intégrité des fichiers PDF
- Nettoyage automatique des fichiers temporaires
- Gestion des erreurs avec messages explicites
- Logs détaillés pour le diagnostic

---

## 🆔 Versions

| Version | Date | Changements principaux |
|---------|------|------------------------|
| v3.0 | 2025-06 | Correction des problèmes PDF, timeouts, retry |
| v2.0 | 2025-05 | Version précédente |

---

## 📞 Support

En cas de problème :

1. **Vérifier les logs** affichés dans la console
2. **Tester manuellement** avec `test_pdf_generation.py`
3. **Consulter les messages d'erreur** détaillés
4. **Redémarrer** les composants dans l'ordre : serveur puis client

### Messages d'erreur courants

| Erreur | Solution |
|--------|----------|
| `pdf_data.py non trouvé` | Vérifier l'emplacement des fichiers |
| `Logs non trouvés` | Lancer le client pour générer les logs |
| `Timeout lors de la génération` | Vérifier la charge système |
| `Fichier PDF trop petit` | Logs probablement corrompus |

---

✨ **Version 3 = Plus de blocages, génération PDF fiable !** ✨ 