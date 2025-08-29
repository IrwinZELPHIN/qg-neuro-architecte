QG du Neuro-Architecte™ — MVP (Render-ready)
===========================================

Démarrage en local:
  python3 -m venv .venv && source .venv/bin/activate
  pip install -r requirements.txt
  export FLASK_APP=src/main.py
  export ADMIN_EMAIL=izelphin@gmail.com
  export ADMIN_PASSWORD=password123
  python src/main.py
  # Ouvrir http://localhost:5000

Démarrage Render:
  Start command: gunicorn -w 2 -b 0.0.0.0:$PORT "src.main:app"
  Variables d'env:
    SECRET_KEY=<longue_chaine>
    ADMIN_EMAIL=izelphin@gmail.com
    ADMIN_PASSWORD=<ton_mdp>
    WEBHOOK_API_KEY=<clé longue>  # si vide, auto-générée à la création
    CORS_ORIGINS=https://app.izelphin.com
    # Option: DATABASE_URL=postgres://.... (sinon SQLite)

Endpoints:
  POST   /api/auth/login
  POST   /api/auth/logout
  GET    /api/operators
  GET    /api/operators/<id>
  POST   /api/webhook/supra-scan (header X-API-KEY requis)

Bon déploiement !
