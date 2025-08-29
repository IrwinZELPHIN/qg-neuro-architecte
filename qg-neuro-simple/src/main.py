import os
import json
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, session, send_from_directory
from flask_cors import CORS
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'qg-neuro-secret-2025')

# CORS
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})

# Données en mémoire (remplace la base de données)
ADMIN_EMAIL = "izelphin@gmail.com"
ADMIN_PASSWORD_HASH = generate_password_hash("password123")
ADMIN_NAME = "Irwin Zelphin - Coach Principal"
API_KEY = "test-api-key-qg-neuro-2025"

# Données d'exemple des opérateurs
OPERATORS_DATA = [
    {
        "id": 1,
        "nomComplet": "Alexandre Martin",
        "email": "a.martin@example.com",
        "neurotype": "Analytique-Dominant",
        "statutUrgence": "Critique",
        "dateDernierScan": (datetime.now() - timedelta(hours=2)).isoformat(),
        "niveauStress": 85,
        "performanceCognitive": 45,
        "notes": "Surcharge cognitive détectée. Recommandation: pause immédiate."
    },
    {
        "id": 2,
        "nomComplet": "Sophie Dubois",
        "email": "s.dubois@example.com",
        "neurotype": "Créatif-Intuitif",
        "statutUrgence": "À Surveiller",
        "dateDernierScan": (datetime.now() - timedelta(hours=6)).isoformat(),
        "niveauStress": 65,
        "performanceCognitive": 72,
        "notes": "Légère baisse de créativité. Surveillance recommandée."
    },
    {
        "id": 3,
        "nomComplet": "Thomas Leroy",
        "email": "t.leroy@example.com",
        "neurotype": "Équilibré-Adaptatif",
        "statutUrgence": "Stable",
        "dateDernierScan": (datetime.now() - timedelta(hours=1)).isoformat(),
        "niveauStress": 35,
        "performanceCognitive": 88,
        "notes": "Performance optimale. Maintenir le rythme actuel."
    },
    {
        "id": 4,
        "nomComplet": "Marie Rousseau",
        "email": "m.rousseau@example.com",
        "neurotype": "Logique-Séquentiel",
        "statutUrgence": "Critique",
        "dateDernierScan": (datetime.now() - timedelta(minutes=30)).isoformat(),
        "niveauStress": 92,
        "performanceCognitive": 38,
        "notes": "Épuisement neurologique critique. Intervention immédiate requise."
    },
    {
        "id": 5,
        "nomComplet": "Lucas Bernard",
        "email": "l.bernard@example.com",
        "neurotype": "Visuel-Spatial",
        "statutUrgence": "Stable",
        "dateDernierScan": (datetime.now() - timedelta(hours=4)).isoformat(),
        "niveauStress": 42,
        "performanceCognitive": 81,
        "notes": "Bonne adaptation aux tâches visuelles complexes."
    }
]

# Routes d'authentification
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email', '').lower().strip()
    password = data.get('password', '')
    
    if email == ADMIN_EMAIL and check_password_hash(ADMIN_PASSWORD_HASH, password):
        session['user_id'] = 1
        session['email'] = email
        session['nom_complet'] = ADMIN_NAME
        return jsonify({"success": True, "message": "Connexion réussie"})
    
    return jsonify({"error": "Email ou mot de passe incorrect"}), 401

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"success": True, "message": "Déconnexion réussie"})

@app.route('/api/auth/me', methods=['GET'])
def get_current_user():
    if 'user_id' not in session:
        return jsonify({"error": "Non connecté"}), 401
    
    return jsonify({
        "id": session['user_id'],
        "email": session['email'],
        "nom_complet": session['nom_complet']
    })

# Routes des opérateurs
@app.route('/api/operators', methods=['GET'])
def get_operators():
    if 'user_id' not in session:
        return jsonify({"error": "Non connecté"}), 401
    
    # Filtres
    search_query = request.args.get('q', '').lower()
    statut_filter = request.args.get('statut', '')
    
    # Filtrer les données
    filtered_ops = OPERATORS_DATA.copy()
    
    if search_query:
        filtered_ops = [op for op in filtered_ops 
                       if search_query in op['nomComplet'].lower() 
                       or search_query in op['email'].lower()]
    
    if statut_filter:
        filtered_ops = [op for op in filtered_ops 
                       if op['statutUrgence'] == statut_filter]
    
    # Statistiques
    stats = {
        "total": len(OPERATORS_DATA),
        "critique": len([op for op in OPERATORS_DATA if op['statutUrgence'] == 'Critique']),
        "surveiller": len([op for op in OPERATORS_DATA if op['statutUrgence'] == 'À Surveiller']),
        "stable": len([op for op in OPERATORS_DATA if op['statutUrgence'] == 'Stable'])
    }
    
    return jsonify({
        "items": filtered_ops,
        "stats": stats
    })

@app.route('/api/operators/<int:operator_id>', methods=['GET'])
def get_operator(operator_id):
    if 'user_id' not in session:
        return jsonify({"error": "Non connecté"}), 401
    
    operator = next((op for op in OPERATORS_DATA if op['id'] == operator_id), None)
    if not operator:
        return jsonify({"error": "Opérateur non trouvé"}), 404
    
    return jsonify(operator)

# Webhook pour SUPRA-CODE
@app.route('/api/v1/ingest', methods=['POST'])
def webhook_ingest():
    # Vérifier l'API key
    api_key = request.headers.get('X-API-KEY')
    if api_key != API_KEY:
        return jsonify({"error": "API key invalide"}), 401
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "Données JSON requises"}), 400
    
    # Simuler l'ajout d'un nouvel opérateur
    new_operator = {
        "id": len(OPERATORS_DATA) + 1,
        "nomComplet": data.get('nom_complet', 'Nouvel Opérateur'),
        "email": data.get('email', 'nouveau@example.com'),
        "neurotype": data.get('neurotype', 'Non défini'),
        "statutUrgence": data.get('statut_urgence', 'Stable'),
        "dateDernierScan": datetime.now().isoformat(),
        "niveauStress": data.get('niveau_stress', 50),
        "performanceCognitive": data.get('performance_cognitive', 75),
        "notes": data.get('notes', 'Données reçues via webhook SUPRA-CODE')
    }
    
    OPERATORS_DATA.append(new_operator)
    
    return jsonify({
        "success": True,
        "message": "Données intégrées avec succès",
        "operator_id": new_operator['id']
    })

# Route pour servir les fichiers statiques
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

