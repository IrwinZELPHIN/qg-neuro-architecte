# QG Neuro-Architecte™ - Version 2.0

## 🚀 Nouvelle Architecture Intégrée

Cette version 2.0 de QG Neuro-Architecte™ intègre une architecture backend complètement repensée pour servir de système nerveux central pour la gestion de différents types de résultats Supra Scan.

## ✨ Fonctionnalités Principales

### Architecture Backend Évolutive
- **Support officiel de 6 types de scans** :
  - `bilan-neuro-strategique`
  - `neuro-recuperation-sommeil`
  - `neuro-nutritionnelle`
  - `pilotage-personnel-prim`
  - `neuro-focus`
  - `mouvement-neuro-actif`

### API Sécurisée
- **Endpoint principal** : `/api/v1/new-scan-result`
- **Authentification** : Bearer Token via header `Authorization`
- **Validation stricte** : Types de résultats, format JSON, champs obligatoires
- **Stockage structuré** : Base de données en mémoire avec profils opérateurs

### Interface Utilisateur Modernisée
- **Dashboard temps réel** avec statistiques
- **Gestion des opérateurs** avec détails complets
- **Visualisation des scans Supra** avec filtres
- **Interface responsive** et professionnelle

## 🔧 Installation et Déploiement

### Prérequis
- Python 3.11+
- Flask 2.3+
- Flask-CORS 4.0+

### Déploiement Local
```bash
# Installer les dépendances
pip install -r requirements.txt

# Définir la clé API (obligatoire)
export QG_API_SECRET_KEY="votre-cle-secrete-ici"

# Démarrer l'application
cd src
python main.py
```

### Déploiement sur Render
1. **Uploader le contenu** (pas le ZIP) sur GitHub
2. **Configurer Render** :
   - Root Directory: `QG-NEURO-ARCHITECTE-FINAL-V2`
   - Start Command: `python src/main.py`
   - Plan: Free (suffisant pour usage modéré)
3. **Variables d'environnement** :
   - `QG_API_SECRET_KEY`: Votre clé secrète pour l'API

## 📡 Utilisation de l'API

### Envoyer un Résultat de Scan
```bash
curl -X POST https://votre-app.onrender.com/api/v1/new-scan-result \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer VOTRE_CLE_SECRETE" \
  -d '{
    "clientEmail": "client@example.com",
    "resultatType": "bilan-neuro-strategique",
    "payload": {
      "clientName": "Nom Client",
      "clientPhone": "+33123456789",
      "scanDate": "2025-09-01T16:30:00Z",
      "score": 85,
      "details": "Données spécifiques au scan"
    }
  }'
```

### Récupérer Tous les Opérateurs
```bash
curl -X GET https://votre-app.onrender.com/api/v1/get-all-operators
```

### Récupérer les Détails d'un Opérateur
```bash
curl -X GET https://votre-app.onrender.com/api/v1/get-operator-details/client@example.com
```

## 🔐 Sécurité

- **Authentification Bearer Token** obligatoire pour l'API
- **Validation stricte** des types de résultats autorisés
- **CORS configuré** pour l'accès frontend-backend
- **Variables d'environnement** pour les clés sensibles

## 🎯 Types de Scans Supportés

L'architecture supporte officiellement ces 6 types de résultats :

1. **bilan-neuro-strategique** - Bilan neurologique stratégique
2. **neuro-recuperation-sommeil** - Analyse de récupération et sommeil
3. **neuro-nutritionnelle** - Évaluation neuro-nutritionnelle
4. **pilotage-personnel-prim** - Pilotage personnel primaire
5. **neuro-focus** - Analyse de concentration et focus
6. **mouvement-neuro-actif** - Évaluation du mouvement neuro-actif

## 📊 Interface Utilisateur

### Connexion
- Email : `contact@izsupra.com`
- Mot de passe : `password123`

### Fonctionnalités
- **Dashboard** avec statistiques en temps réel
- **Onglet Opérateurs QG** : Vue d'ensemble des opérateurs
- **Onglet Scans Supra** : Historique des scans reçus
- **Recherche et filtres** pour navigation facile
- **Détails opérateurs** avec historique complet

## 🚀 Évolutivité

Cette architecture est conçue pour être **évolutive sans modifications backend** :
- Ajout de nouveaux types de scans via configuration
- Structure de données flexible avec payload JSON
- API RESTful standard pour intégrations futures
- Base de données extensible pour nouveaux champs

## 📝 Notes Techniques

- **Base de données** : En mémoire (redémarrage = perte des données)
- **Performance** : Optimisée pour usage modéré (5-20 coachs)
- **Scalabilité** : Plan payant recommandé pour usage intensif (50+ coachs)
- **Maintenance** : Architecture modulaire pour faciliter les mises à jour

## 🆘 Support

Pour toute question technique ou demande de fonctionnalité, l'application est prête pour la production avec cette nouvelle architecture intégrée.

---

**Version** : 2.0  
**Date** : Septembre 2025  
**Statut** : Production Ready ✅

