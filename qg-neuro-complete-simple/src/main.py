from flask import Flask, request, jsonify, session, send_from_directory
from flask_cors import CORS
import os
import json
from datetime import datetime

app = Flask(__name__, static_folder='static')
app.secret_key = os.environ.get('SECRET_KEY', 'qg-neuro-secret-key-2025')

# Configuration CORS
CORS(app, supports_credentials=True, origins=['*'])

# Configuration admin
ADMIN_EMAIL = "izelphin@gmail.com"
ADMIN_PASSWORD = "password123"

# Données d'exemple avec toutes les informations neurochimiques
SAMPLE_OPERATORS = [
    {
        "id": 1,
        "nom_complet": "Alexandre Martin",
        "email": "a.martin@example.com",
        "telephone": "+33 6 12 34 56 78",
        "neurotype": "Analytique-Dominant",
        "statut_urgence": "Critique",
        "date_dernier_scan": "2025-08-29T21:15:00Z",
        "niveau_stress": 85,
        "performance_cognitive": 45,
        "pourcentages": {
            "blocA": 75.5,
            "blocB": 25.2,
            "blocC": 68.8,
            "blocD": 28.1
        },
        "sous_scores": {
            "dopamine": 32.5,
            "serotonine": 28.7,
            "gaba": 22.1,
            "noradrenaline": 45.8,
            "acetylcholine": 38.2
        },
        "bilans_additionnels": {
            "nutrition": "Déficit en magnésium et vitamine D. Recommandation: supplémentation ciblée.",
            "sommeil": "Fragmentation du sommeil REM. Durée moyenne: 5h30. Recommandation: protocole d'hygiène du sommeil."
        },
        "notes_coach": "Intervention urgente requise. Stress chronique élevé avec impact sur les neurotransmetteurs inhibiteurs."
    },
    {
        "id": 2,
        "nom_complet": "Sophie Dubois",
        "email": "s.dubois@example.com",
        "telephone": "+33 6 23 45 67 89",
        "neurotype": "Créatif-Intuitif",
        "statut_urgence": "À Surveiller",
        "date_dernier_scan": "2025-08-29T17:15:00Z",
        "niveau_stress": 65,
        "performance_cognitive": 72,
        "pourcentages": {
            "blocA": 82.3,
            "blocB": 45.7,
            "blocC": 78.9,
            "blocD": 52.4
        },
        "sous_scores": {
            "dopamine": 68.2,
            "serotonine": 55.4,
            "gaba": 48.7,
            "noradrenaline": 72.1,
            "acetylcholine": 65.8
        },
        "bilans_additionnels": {
            "nutrition": "Profil équilibré. Légère carence en oméga-3.",
            "sommeil": "Qualité correcte. Durée moyenne: 7h15."
        },
        "notes_coach": "Évolution positive. Maintenir le protocole actuel et surveiller l'évolution du bloc B."
    },
    {
        "id": 3,
        "nom_complet": "Thomas Leroy",
        "email": "t.leroy@example.com",
        "telephone": "+33 6 34 56 78 90",
        "neurotype": "Équilibré-Adaptatif",
        "statut_urgence": "Stable",
        "date_dernier_scan": "2025-08-29T22:15:00Z",
        "niveau_stress": 35,
        "performance_cognitive": 88,
        "pourcentages": {
            "blocA": 89.2,
            "blocB": 76.8,
            "blocC": 85.4,
            "blocD": 82.1
        },
        "sous_scores": {
            "dopamine": 85.7,
            "serotonine": 78.9,
            "gaba": 82.3,
            "noradrenaline": 79.4,
            "acetylcholine": 88.1
        },
        "bilans_additionnels": {
            "nutrition": "Profil optimal. Tous les marqueurs dans les normes.",
            "sommeil": "Excellent. Durée moyenne: 8h00. Sommeil réparateur."
        },
        "notes_coach": "Performance excellente. Modèle de référence pour l'équipe."
    },
    {
        "id": 4,
        "nom_complet": "Marie Rousseau",
        "email": "m.rousseau@example.com",
        "telephone": "+33 6 45 67 89 01",
        "neurotype": "Logique-Séquentiel",
        "statut_urgence": "Critique",
        "date_dernier_scan": "2025-08-29T22:45:00Z",
        "niveau_stress": 92,
        "performance_cognitive": 38,
        "pourcentages": {
            "blocA": 45.8,
            "blocB": 18.2,
            "blocC": 52.1,
            "blocD": 22.7
        },
        "sous_scores": {
            "dopamine": 25.4,
            "serotonine": 19.8,
            "gaba": 15.2,
            "noradrenaline": 35.7,
            "acetylcholine": 28.9
        },
        "bilans_additionnels": {
            "nutrition": "Carences multiples: B6, B12, magnésium, zinc. Inflammation systémique.",
            "sommeil": "Insomnie sévère. Durée moyenne: 4h20. Micro-réveils fréquents."
        },
        "notes_coach": "Situation critique. Plan d'intervention immédiate mis en place. Suivi quotidien requis."
    },
    {
        "id": 5,
        "nom_complet": "Lucas Bernard",
        "email": "l.bernard@example.com",
        "telephone": "+33 6 56 78 90 12",
        "neurotype": "Visuel-Spatial",
        "statut_urgence": "Stable",
        "date_dernier_scan": "2025-08-29T19:15:00Z",
        "niveau_stress": 42,
        "performance_cognitive": 81,
        "pourcentages": {
            "blocA": 78.9,
            "blocB": 72.4,
            "blocC": 81.7,
            "blocD": 75.3
        },
        "sous_scores": {
            "dopamine": 76.8,
            "serotonine": 74.2,
            "gaba": 71.5,
            "noradrenaline": 78.9,
            "acetylcholine": 79.3
        },
        "bilans_additionnels": {
            "nutrition": "Bon équilibre général. Optimisation possible des antioxydants.",
            "sommeil": "Qualité satisfaisante. Durée moyenne: 7h45."
        },
        "notes_coach": "Progression constante. Continuer le protocole d'optimisation cognitive."
    }
]

# Base de données en mémoire
operators_db = SAMPLE_OPERATORS.copy()

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session['authenticated'] = True
            session['user_email'] = email
            return jsonify({
                'success': True,
                'message': 'Connexion réussie',
                'user': {
                    'email': email,
                    'nom_complet': 'Irwin Zelphin - Coach Principal'
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Email ou mot de passe incorrect'
            }), 401
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Erreur lors de la connexion'
        }), 500

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True, 'message': 'Déconnexion réussie'})

@app.route('/api/auth/check', methods=['GET'])
def check_auth():
    return jsonify({
        'authenticated': session.get('authenticated', False)
    })

@app.route('/api/operators', methods=['GET'])
def get_operators():
    if not session.get('authenticated'):
        return jsonify({'error': 'Non authentifié'}), 401
    
    # Filtres
    search_query = request.args.get('q', '').lower()
    status_filter = request.args.get('statut', '')
    
    # Filtrer les opérateurs
    filtered_operators = []
    for operator in operators_db:
        # Filtre de recherche
        if search_query:
            if not (search_query in operator['nom_complet'].lower() or 
                   search_query in operator['email'].lower()):
                continue
        
        # Filtre de statut
        if status_filter and operator['statut_urgence'] != status_filter:
            continue
            
        filtered_operators.append(operator)
    
    # Statistiques
    stats = {
        'total': len(filtered_operators),
        'critique': len([op for op in filtered_operators if op['statut_urgence'] == 'Critique']),
        'surveiller': len([op for op in filtered_operators if op['statut_urgence'] == 'À Surveiller']),
        'stable': len([op for op in filtered_operators if op['statut_urgence'] == 'Stable'])
    }
    
    return jsonify({
        'success': True,
        'items': filtered_operators,
        'stats': stats
    })

@app.route('/api/operators/<int:operator_id>', methods=['GET'])
def get_operator(operator_id):
    if not session.get('authenticated'):
        return jsonify({'error': 'Non authentifié'}), 401
    
    operator = next((op for op in operators_db if op['id'] == operator_id), None)
    if not operator:
        return jsonify({'error': 'Opérateur non trouvé'}), 404
    
    return jsonify({
        'success': True,
        'operator': operator
    })

@app.route('/api/operators/<int:operator_id>/notes', methods=['PUT'])
def update_operator_notes(operator_id):
    if not session.get('authenticated'):
        return jsonify({'error': 'Non authentifié'}), 401
    
    try:
        data = request.get_json()
        notes = data.get('notes', '')
        
        # Trouver et mettre à jour l'opérateur
        for i, operator in enumerate(operators_db):
            if operator['id'] == operator_id:
                operators_db[i]['notes_coach'] = notes
                return jsonify({
                    'success': True,
                    'message': 'Notes mises à jour'
                })
        
        return jsonify({'error': 'Opérateur non trouvé'}), 404
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Erreur lors de la mise à jour'
        }), 500

@app.route('/api/v1/ingest', methods=['POST'])
def webhook_ingest():
    """Webhook pour recevoir des données SUPRA-CODE"""
    try:
        # Vérifier l'API key
        api_key = request.headers.get('X-API-KEY')
        if api_key != 'test-api-key-qg-neuro-2025':
            return jsonify({'error': 'API key invalide'}), 401
        
        data = request.get_json()
        
        # Créer un nouvel opérateur ou mettre à jour un existant
        new_operator = {
            'id': len(operators_db) + 1,
            'nom_complet': data.get('nom_complet', 'Nouvel Opérateur'),
            'email': data.get('email', 'nouveau@example.com'),
            'telephone': data.get('telephone', '+33 6 00 00 00 00'),
            'neurotype': data.get('neurotype', 'Non défini'),
            'statut_urgence': data.get('statut_urgence', 'Stable'),
            'date_dernier_scan': datetime.now().isoformat() + 'Z',
            'niveau_stress': data.get('niveau_stress', 50),
            'performance_cognitive': data.get('performance_cognitive', 70),
            'pourcentages': data.get('pourcentages', {
                'blocA': 70.0,
                'blocB': 65.0,
                'blocC': 72.0,
                'blocD': 68.0
            }),
            'sous_scores': data.get('sous_scores', {
                'dopamine': 65.0,
                'serotonine': 70.0,
                'gaba': 68.0,
                'noradrenaline': 72.0,
                'acetylcholine': 69.0
            }),
            'bilans_additionnels': data.get('bilans_additionnels', {
                'nutrition': 'Données reçues via SUPRA-CODE',
                'sommeil': 'Analyse en cours'
            }),
            'notes_coach': data.get('notes', 'Données reçues via webhook SUPRA-CODE')
        }
        
        operators_db.append(new_operator)
        
        return jsonify({
            'success': True,
            'message': 'Données reçues et intégrées',
            'operator_id': new_operator['id']
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur lors du traitement: {str(e)}'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'operators_count': len(operators_db)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

