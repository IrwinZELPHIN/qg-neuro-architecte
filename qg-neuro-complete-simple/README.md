# QG Neuro-Architecte™ - Version Complète

## 🧠 Application Neurochimique Complète

Cette version inclut TOUTES les fonctionnalités neurochimiques avancées :

### ✅ Fonctionnalités Complètes

- **🔐 Authentification sécurisée** : Login admin-only
- **📊 Tableau de bord complet** : Recherche, filtres, statistiques
- **🧠 Fiches opérateurs détaillées** avec 3 onglets :
  - **Synthèse & Plan d'Action** : Profil, alertes, notes coach
  - **Scan Supra-Code** : Scores par blocs + neurotransmetteurs
  - **Données Brutes** : Bilans nutrition/sommeil + données techniques

### 🧪 Données Neurochimiques

- **Scores par Blocs** : A, B, C, D avec barres de progression
- **Neurotransmetteurs** : Dopamine, Sérotonine, GABA, Noradrénaline, Acétylcholine
- **Alertes critiques** : Détection automatique des blocs < 30%
- **Visualisations** : Graphiques colorés selon les seuils

### 📱 Interface Responsive

- **Desktop** : Interface complète avec tous les détails
- **Mobile** : Adaptation automatique pour tactile
- **Tablette** : Layout optimisé

## 🔐 Identifiants

- **Email** : `izelphin@gmail.com`
- **Mot de passe** : `password123`

## 🔗 API Webhook SUPRA-CODE

- **Endpoint** : `POST /api/v1/ingest`
- **Header** : `X-API-KEY: test-api-key-qg-neuro-2025`
- **Format** : JSON avec données neurochimiques complètes

## 🚀 Déploiement Render

### Configuration :
- **Root Directory** : `qg-neuro-complete-simple`
- **Build Command** : `pip install -r requirements.txt`
- **Start Command** : `gunicorn -w 2 -b 0.0.0.0:$PORT "src.main:app"`

### Étapes :
1. Uploader sur GitHub
2. Configurer Render
3. Déployer !

## 📊 Données d'Exemple

5 opérateurs avec profils neurochimiques complets :
- **Alexandre Martin** : Critique (Blocs B et D < 30%)
- **Sophie Dubois** : À Surveiller
- **Thomas Leroy** : Stable (performance optimale)
- **Marie Rousseau** : Critique (stress élevé)
- **Lucas Bernard** : Stable

## 🎯 Fonctionnalités Avancées

- **Notes du coach** éditables et sauvegardables
- **Alertes automatiques** pour les scores critiques
- **Filtrage avancé** par statut et recherche
- **Statistiques temps réel** 
- **Interface professionnelle** sombre
- **Données persistantes** en mémoire

## 🔧 Développement Local

```bash
pip install -r requirements.txt
python src/main.py
# Accès : http://localhost:5000
```

## 🎉 Prêt pour Production

Version complète avec toutes les données neurochimiques demandées !
Parfait pour présentation aux clients prestigieux.

