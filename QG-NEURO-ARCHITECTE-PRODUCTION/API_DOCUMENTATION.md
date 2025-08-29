# 🧠 QG Neuro-Architecte™ - Documentation API

## 🎯 Vue d'ensemble

L'API QG Neuro-Architecte™ permet l'intégration complète entre l'application SUPRA-CODE et la plateforme de pilotage neurochimique. Elle gère l'authentification des coachs, la réception des données de scan, et la gestion des opérateurs.

## 🔐 Authentification

### POST `/api/auth/login`
Connexion d'un coach

**Body:**
```json
{
  "email": "contact@izsupra.com",
  "password": "password123"
}
```

**Réponse:**
```json
{
  "success": true,
  "coach": {
    "id": 1,
    "email": "contact@izsupra.com",
    "nom_complet": "Irwin Zelphin - Coach Principal",
    "api_key": "test-api-key-qg-neuro-architecte-2025"
  }
}
```

### POST `/api/auth/logout`
Déconnexion du coach

### GET `/api/auth/me`
Récupère les informations du coach connecté

### GET `/api/auth/check`
Vérifie si l'utilisateur est connecté

## 👥 Gestion des Opérateurs

### GET `/api/operators`
Récupère la liste des opérateurs du coach connecté

**Paramètres optionnels:**
- `search`: Recherche par nom ou email
- `status`: Filtre par statut (Critique, À Surveiller, Stable)

**Réponse:**
```json
{
  "success": true,
  "operators": [
    {
      "id": 1,
      "nom_complet": "Irwin Zelphin",
      "email": "contact@izsupra.com",
      "neurotype": "GABA-Calme Profond",
      "statut_urgence": "Critique",
      "date_dernier_scan": "2025-08-29T14:37:00",
      "scores": {"blocA": 12, "blocB": 3, ...},
      "pourcentages": {"blocA": 44.44, "blocB": 25.00, ...}
    }
  ]
}
```

### GET `/api/operators/{id}`
Récupère un opérateur spécifique

### PUT `/api/operators/{id}/notes`
Met à jour les notes du coach pour un opérateur

**Body:**
```json
{
  "notes": "# Notes du Coach\n\n## Observations\n..."
}
```

## 🔗 Webhook SUPRA-CODE (POINT CRITIQUE)

### POST `/api/v1/ingest`
**Endpoint principal pour recevoir les données de l'application SUPRA-CODE**

**Headers:**
```
Content-Type: application/json
```

**Body complet:**
```json
{
  "apiKey": "test-api-key-qg-neuro-architecte-2025",
  "operateurData": {
    "nomComplet": "Sophie Laurent",
    "email": "sophie.laurent@example.com",
    "telephone": "+33123456789"
  },
  "scanSupraData": {
    "neurotype": "Serotonine-Equilibré",
    "scores": {
      "blocA": 15,
      "blocB": 18,
      "blocC": 12,
      "blocD": 16,
      "blocE": 14
    },
    "pourcentages": {
      "blocA": 55.56,
      "blocB": 60.00,
      "blocC": 80.00,
      "blocD": 53.33,
      "blocE": 93.33
    },
    "sousScores": {
      "dopamine": 45.00,
      "serotonine": 85.00,
      "acetylcholine": 65.00,
      "noradrenaline": 55.00,
      "gaba": 70.00,
      "glutamate": 40.00
    },
    "urlRapport": "https://supra-code.io/rapport/test-sophie-laurent-2025"
  },
  "bilansAdditionnels": {
    "nutrition": "Alimentation équilibrée, consommation modérée de caféine.",
    "sommeil": "Sommeil régulier, 7-8h par nuit, qualité perçue : 8/10."
  }
}
```

**Réponse:**
```json
{
  "success": true,
  "message": "Données reçues et traitées avec succès",
  "operator_id": 4,
  "statut_urgence": "Stable"
}
```

## 🚨 Logique de Calcul des Statuts

L'API calcule automatiquement le statut d'urgence basé sur les pourcentages:

- **Critique**: Bloc B < 30% OU Bloc D < 30%
- **À Surveiller**: Bloc B < 60% OU Bloc D < 60%
- **Stable**: Tous les blocs dans la norme

## 🔑 Clés API

Chaque coach possède une clé API unique pour l'intégration SUPRA-CODE:

**Coach de test:**
- Email: `contact@izsupra.com`
- Mot de passe: `password123`
- Clé API: `test-api-key-qg-neuro-architecte-2025`

## 🧪 Test du Webhook

Utilisez le script `test_webhook.py` pour tester l'intégration:

```bash
cd /home/ubuntu/qg-backend
source venv/bin/activate
python test_webhook.py
```

## 📊 Exemples d'Intégration

### Cas Normal
```bash
curl -X POST http://localhost:5000/api/v1/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "apiKey": "test-api-key-qg-neuro-architecte-2025",
    "operateurData": {...},
    "scanSupraData": {...}
  }'
```

### Cas Critique
Lorsque les blocs B ou D sont < 30%, l'opérateur est automatiquement marqué comme "Critique" et apparaît en rouge dans l'interface.

## 🔒 Sécurité

- Authentification par session avec cookies sécurisés
- Validation des clés API pour le webhook
- Protection CORS configurée
- Validation des données d'entrée

## 🚀 Déploiement

L'application est prête pour déploiement avec:
- Backend Flask intégré
- Frontend React optimisé
- Base de données SQLite
- Configuration CORS
- Gestion des sessions

## 📱 Interface Web

Une fois connecté, les coachs accèdent à:
- Tableau de bord avec liste des opérateurs
- Recherche et filtrage en temps réel
- Fiches détaillées avec 3 onglets
- Système d'alertes automatiques
- Notes éditables par opérateur

---

**🎯 L'API est maintenant 100% fonctionnelle et prête pour l'intégration avec SUPRA-CODE !**

