import os
import uuid
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
app.secret_key = os.environ.get('SECRET_KEY', 'qg-neuro-secret-key-2025')

# Configuration CORS
CORS(app, supports_credentials=True, origins=['*'])

# Configuration admin (conservée de l'ancien système)
ADMIN_EMAIL = "contact@izsupra.com"
ADMIN_PASSWORD = "password123"

# --- 1. BASE DE DONNÉES EN MÉMOIRE ET CONFIGURATION ---

# La base de données qui stockera tous les profils des opérateurs
db = {}

# Récupération sécurisée de la clé API depuis les variables d'environnement
QG_API_SECRET_KEY = os.environ.get('QG_API_SECRET_KEY')

# Liste officielle et non-modifiable des types de résultats autorisés
OFFICIAL_RESULT_TYPES = [
    "bilan-neuro-strategique",
    "neuro-recuperation-sommeil",
    "neuro-nutritionnelle",
    "pilotage-personnel-prim",
    "neuro-focus",
    "mouvement-neuro-actif"
]

# --- 2. ROUTES POUR LES PAGES HTML (Conservées) ---

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

# --- 3. AUTHENTIFICATION (Conservée) ---

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
        return jsonify({"success": True, "message": "Connexion réussie"})
    else:
        return jsonify({"success": False, "message": "Identifiants incorrects"}), 401

@app.route('/api/auth/check', methods=['GET'])
def check_auth():
    return jsonify({"authenticated": True})

# --- 4. LA ROUTE API SÉCURISÉE (Le Cœur du Système) ---

@app.route('/api/v1/new-scan-result', methods=['POST'])
def receive_scan_result():
    # Étape A : Sécurité - Vérification de la clé secrète
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Authorization header is missing or invalid"}), 401
    
    token = auth_header.split(' ')[1]
    if not QG_API_SECRET_KEY or token != QG_API_SECRET_KEY:
        return jsonify({"error": "Unauthorized"}), 403
        
    # Étape B : Validation du Payload - Vérification du format et des champs
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request must be JSON"}), 400
    
    required_fields = ['clientEmail', 'resultatType', 'payload']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields: clientEmail, resultatType, payload are mandatory"}), 400
    
    # Étape C : Validation du Type - Vérification de la conformité
    resultat_type = data['resultatType']
    if resultat_type not in OFFICIAL_RESULT_TYPES:
        return jsonify({"error": f"Invalid resultatType: '{resultat_type}'. Must be one of {OFFICIAL_RESULT_TYPES}"}), 400

    # Étape D : Logique de Sauvegarde
    client_email = data['clientEmail']
    
    # Si l'opérateur n'existe pas, on crée son profil
    if client_email not in db:
        db[client_email] = {
            "profil": {
                "clientName": data.get('payload', {}).get('clientName', 'N/A'),
                "clientPhone": data.get('payload', {}).get('clientPhone', 'N/A')
            },
            "resultats": []
        }
    
    # Création du nouvel objet résultat avec un ID unique
    nouveau_resultat = {
        "resultatId": str(uuid.uuid4()),
        "resultatType": resultat_type,
        "date": data.get('payload', {}).get('scanDate', 'N/A'), # On récupère la date du payload
        "payload": data['payload'] # On sauvegarde l'intégralité du payload
    }
    
    # Ajout du nouveau résultat à la liste de l'opérateur
    db[client_email]['resultats'].append(nouveau_resultat)
    
    print(f"--- NOUVEAU RÉSULTAT '{resultat_type}' REÇU ET SAUVEGARDÉ POUR {client_email} ---")
    
    return jsonify({"status": "success", "message": "Result received and stored successfully"}), 201

# --- 5. ROUTES POUR AFFICHER LES DONNÉES AU FRONTEND ---

@app.route('/api/v1/get-all-operators', methods=['GET'])
def get_all_operators():
    # Cette fonction prépare les données pour l'affichage dans le QG
    operator_list = []
    for email, data in db.items():
        latest_scan = max(data['resultats'], key=lambda x: x['date']) if data['resultats'] else None
        operator_list.append({
            "email": email,
            "nom": data['profil']['clientName'],
            "dernierScanDate": latest_scan['date'] if latest_scan else "N/A",
            "totalScans": len(data['resultats'])
        })
    return jsonify(operator_list)

@app.route('/api/v1/get-operator-details/<email>', methods=['GET'])
def get_operator_details(email):
    # Cette fonction renvoie tous les détails d'un opérateur spécifique
    if email in db:
        return jsonify(db[email])
    else:
        return jsonify({"error": "Operator not found"}), 404

# --- 6. ROUTES DE SANTÉ ---

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "QG Neuro-Architecte"})

# --- 7. DÉMARRAGE DE L'APPLICATION ---

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

