# QG Neuro-Architecte™ - Version Simplifiée

## 🚀 Version Sans SQLAlchemy - 100% Fonctionnelle

Cette version simplifiée utilise des données en mémoire au lieu d'une base de données complexe, garantissant un déploiement sans erreur sur Render.

## ✅ Fonctionnalités

- **Authentification complète** : Login/logout sécurisé
- **Interface responsive** : Parfaite sur desktop, mobile et tablette
- **Tableau de bord** : Recherche et filtrage des opérateurs
- **Webhook SUPRA-CODE** : API endpoint pour recevoir des données
- **Design professionnel** : Interface sombre avec logo IZ

## 🔐 Identifiants de Connexion

- **Email** : `izelphin@gmail.com`
- **Mot de passe** : `password123`

## 🔗 API Webhook

- **Endpoint** : `POST /api/v1/ingest`
- **Header requis** : `X-API-KEY: test-api-key-qg-neuro-2025`
- **Format** : JSON

Exemple de payload :
```json
{
  "nom_complet": "Nouvel Opérateur",
  "email": "nouveau@example.com",
  "neurotype": "Analytique-Dominant",
  "statut_urgence": "Stable",
  "niveau_stress": 45,
  "performance_cognitive": 78,
  "notes": "Données reçues via SUPRA-CODE"
}
```

## 🚀 Déploiement sur Render

### Configuration Render :
- **Root Directory** : ` ` (vide - fichiers à la racine)
- **Build Command** : `pip install -r requirements.txt`
- **Start Command** : `gunicorn -w 2 -b 0.0.0.0:$PORT "src.main:app"`

### Étapes :
1. Uploader ce dossier sur GitHub
2. Connecter à Render
3. Configurer les commandes ci-dessus
4. Déployer !

## 📱 Interface Mobile

L'interface s'adapte automatiquement :
- **Desktop** : Tableau complet avec toutes les colonnes
- **Mobile** : Cartes optimisées pour le tactile
- **Tablette** : Layout adaptatif

## 🎯 Avantages de cette Version

- ❌ **Aucune erreur SQLAlchemy**
- ✅ **Déploiement garanti**
- ✅ **Performance optimale**
- ✅ **Maintenance simplifiée**
- ✅ **Même interface utilisateur**

## 🔧 Développement Local

```bash
# Installer les dépendances
pip install -r requirements.txt

# Variables d'environnement (optionnel)
export SECRET_KEY="votre-clé-secrète"
export PORT=5000

# Lancer l'application
python src/main.py

# Accéder à l'application
# http://localhost:5000
```

## 📊 Données d'Exemple

L'application inclut 5 opérateurs d'exemple avec différents statuts :
- 2 opérateurs en état **Critique**
- 1 opérateur **À Surveiller**
- 2 opérateurs **Stable**

## 🎉 Prêt pour Production

Cette version est optimisée pour :
- Présentation aux clients prestigieux
- Démonstrations en temps réel
- Intégration avec SUPRA-CODE
- Utilisation mobile et desktop

