from flask import Flask, request, jsonify, session, send_from_directory
from flask_cors import CORS
import os
import json
from datetime import datetime

app = Flask(__name__, static_folder='static')
app.secret_key = os.environ.get('SECRET_KEY', 'qg-neuro-secret-key-2025')

# Configuration CORS
CORS(app, supports_credentials=True, origins=['*'])

# Configuration admin CORRIGÉE
ADMIN_EMAIL = "contact@izsupra.com"
ADMIN_PASSWORD = "password123"

# Données d'exemple avec BLOC E et questionnaires complets
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
            "blocD": 28.1,
            "blocE": 42.3
        },
        "sous_scores": {
            "dopamine": 32.5,
            "serotonine": 28.7,
            "gaba": 22.1,
            "noradrenaline": 45.8,
            "acetylcholine": 38.2
        },
        "ondes_cerebrales": {
            "delta": 35.2,
            "theta": 28.7,
            "alpha": 45.1,
            "beta": 52.8,
            "gamma": 38.9
        },
        "questionnaire_supra": {
            "q1": "A", "q2": "B", "q3": "A", "q4": "A", "q5": "B",
            "q6": "A", "q7": "A", "q8": "A", "q9": "B", "q10": "A",
            "q11": "A", "q12": "B", "q13": "A", "q14": "B", "q15": "B",
            "q16": "A", "q17": "B", "q18": "A", "q19": "A", "q20": "B",
            "q21": "A", "q22": "B", "q23": "A", "q24": "A", "q25": "B",
            "q26": "A", "q27": "B", "q28": "A"
        },
        "questionnaire_nutrition": {
            "objectif_principal": "Amélioration de l'énergie et réduction du stress",
            "situation_ideale": "Me sentir énergique toute la journée sans coup de fatigue",
            "petit_dejeuner": "Café noir + viennoiserie (souvent pressé)",
            "dejeuner": "Sandwich ou salade rapide au bureau",
            "diner": "Repas complet mais tardif (20h-21h)",
            "grignotage": "Chocolat, biscuits en fin d'après-midi",
            "hydratation": "2-3 verres d'eau + 4-5 cafés par jour",
            "allergies": "Aucune allergie connue",
            "supplements": "Vitamine D en hiver",
            "problemes_digestifs": "Ballonnements après repas copieux"
        },
        "questionnaire_sommeil": {
            "heure_coucher": "23h30-00h30 (variable selon le travail)",
            "heure_lever": "7h00 en semaine, 9h00 le weekend",
            "duree_endormissement": "15-30 minutes (parfois plus si stress)",
            "reveils_nocturnes": "2-3 fois par nuit",
            "qualite_sommeil": "Fragmenté, peu réparateur",
            "fatigue_matinale": "Très fatigué au réveil, besoin de café",
            "siestes": "Parfois 20min après déjeuner",
            "ecrans_soir": "Télé/téléphone jusqu'au coucher",
            "environnement": "Chambre pas totalement obscure, bruit circulation"
        },
        "bilans_additionnels": {
            "nutrition": "Déficit en magnésium et vitamine D. Déséquilibre glycémique. Recommandation: supplémentation ciblée + rééquilibrage des repas.",
            "sommeil": "Fragmentation du sommeil REM. Durée moyenne: 5h30. Recommandation: protocole d'hygiène du sommeil + réduction écrans."
        },
        "notes_coach": "Intervention urgente requise. Stress chronique élevé avec impact sur les neurotransmetteurs inhibiteurs. BLOC B et D critiques. Ondes Alpha et Delta déficitaires.",
        "protocole_recommande": "1) Magnésium 400mg le soir 2) Réduction caféine après 14h 3) Méditation 10min/jour 4) Coucher fixe 22h30 5) Petit-déjeuner protéiné"
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
            "blocD": 52.4,
            "blocE": 68.2
        },
        "sous_scores": {
            "dopamine": 68.2,
            "serotonine": 55.4,
            "gaba": 48.7,
            "noradrenaline": 72.1,
            "acetylcholine": 65.8
        },
        "ondes_cerebrales": {
            "delta": 65.8,
            "theta": 78.2,
            "alpha": 72.4,
            "beta": 68.9,
            "gamma": 58.7
        },
        "questionnaire_supra": {
            "q1": "C", "q2": "C", "q3": "B", "q4": "B", "q5": "C",
            "q6": "B", "q7": "B", "q8": "B", "q9": "C", "q10": "C",
            "q11": "B", "q12": "C", "q13": "B", "q14": "C", "q15": "C",
            "q16": "C", "q17": "C", "q18": "B", "q19": "B", "q20": "C",
            "q21": "B", "q22": "C", "q23": "B", "q24": "C", "q25": "C",
            "q26": "C", "q27": "C", "q28": "C"
        },
        "questionnaire_nutrition": {
            "objectif_principal": "Maintenir l'énergie créative et optimiser la concentration",
            "situation_ideale": "Avoir une énergie stable pour mes projets créatifs",
            "petit_dejeuner": "Porridge aux fruits ou yaourt grec avec granola",
            "dejeuner": "Salade complète ou bowl végétarien",
            "diner": "Poisson/légumes ou plat végétarien équilibré",
            "grignotage": "Fruits secs, thé vert",
            "hydratation": "1.5L eau + tisanes + thé vert",
            "allergies": "Légère intolérance au lactose",
            "supplements": "Oméga-3, vitamine B12",
            "problemes_digestifs": "Occasionnels, liés au stress"
        },
        "questionnaire_sommeil": {
            "heure_coucher": "22h30-23h30",
            "heure_lever": "7h30 naturellement",
            "duree_endormissement": "10-15 minutes",
            "reveils_nocturnes": "1 fois par nuit maximum",
            "qualite_sommeil": "Généralement bonne, rêves créatifs",
            "fatigue_matinale": "Forme correcte au réveil",
            "siestes": "Rarement, sauf période intense",
            "ecrans_soir": "Lecture 30min avant coucher",
            "environnement": "Chambre calme, masque de nuit"
        },
        "bilans_additionnels": {
            "nutrition": "Profil équilibré. Légère carence en oméga-3. Optimisation possible des antioxydants pour soutenir la créativité.",
            "sommeil": "Qualité correcte. Durée moyenne: 7h15. Sommeil créatif avec phase REM riche."
        },
        "notes_coach": "Évolution positive. Maintenir le protocole actuel et surveiller l'évolution du bloc B. Profil créatif avec bonnes ondes Theta.",
        "protocole_recommande": "1) Continuer oméga-3 2) Méditation créative 15min 3) Journaling matinal 4) Exercice doux yoga 5) Maintenir rythme sommeil"
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
            "blocD": 82.1,
            "blocE": 84.7
        },
        "sous_scores": {
            "dopamine": 85.7,
            "serotonine": 78.9,
            "gaba": 82.3,
            "noradrenaline": 79.4,
            "acetylcholine": 88.1
        },
        "ondes_cerebrales": {
            "delta": 88.5,
            "theta": 72.8,
            "alpha": 85.2,
            "beta": 89.1,
            "gamma": 78.4
        },
        "questionnaire_supra": {
            "q1": "D", "q2": "D", "q3": "D", "q4": "D", "q5": "D",
            "q6": "D", "q7": "C", "q8": "D", "q9": "C", "q10": "D",
            "q11": "D", "q12": "D", "q13": "D", "q14": "D", "q15": "D",
            "q16": "D", "q17": "D", "q18": "D", "q19": "D", "q20": "D",
            "q21": "D", "q22": "D", "q23": "D", "q24": "D", "q25": "C",
            "q26": "D", "q27": "D", "q28": "D"
        },
        "questionnaire_nutrition": {
            "objectif_principal": "Maintenir la performance optimale et la santé globale",
            "situation_ideale": "Continuer à me sentir en pleine forme et énergique",
            "petit_dejeuner": "Œufs, avocat, pain complet + fruits",
            "dejeuner": "Protéines + légumes + féculents complets",
            "diner": "Repas équilibré, léger, 3h avant coucher",
            "grignotage": "Fruits, noix, très occasionnel",
            "hydratation": "2.5L eau répartie dans la journée",
            "allergies": "Aucune",
            "supplements": "Multivitamines, vitamine D, magnésium",
            "problemes_digestifs": "Aucun"
        },
        "questionnaire_sommeil": {
            "heure_coucher": "22h00 précise",
            "heure_lever": "6h30 naturellement",
            "duree_endormissement": "5-10 minutes",
            "reveils_nocturnes": "Très rare",
            "qualite_sommeil": "Profond et réparateur",
            "fatigue_matinale": "Réveil naturel, pleine forme",
            "siestes": "Jamais besoin",
            "ecrans_soir": "Arrêt 21h, lecture papier",
            "environnement": "Optimal: noir, silencieux, frais"
        },
        "bilans_additionnels": {
            "nutrition": "Profil optimal. Tous les marqueurs dans les normes. Équilibre parfait macro/micronutriments.",
            "sommeil": "Excellent. Durée moyenne: 8h00. Sommeil réparateur avec cycles complets."
        },
        "notes_coach": "Performance excellente. Modèle de référence pour l'équipe. Tous les blocs optimaux. Ondes cérébrales harmonieuses.",
        "protocole_recommande": "1) Maintenir routine actuelle 2) Optimisation performance: créatine 3) Méditation avancée 4) Défis cognitifs 5) Mentoring équipe"
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
            "blocD": 22.7,
            "blocE": 28.4
        },
        "sous_scores": {
            "dopamine": 25.4,
            "serotonine": 19.8,
            "gaba": 15.2,
            "noradrenaline": 35.7,
            "acetylcholine": 28.9
        },
        "ondes_cerebrales": {
            "delta": 22.1,
            "theta": 18.5,
            "alpha": 25.8,
            "beta": 45.2,
            "gamma": 32.7
        },
        "questionnaire_supra": {
            "q1": "A", "q2": "A", "q3": "A", "q4": "A", "q5": "A",
            "q6": "A", "q7": "A", "q8": "A", "q9": "A", "q10": "A",
            "q11": "A", "q12": "A", "q13": "A", "q14": "A", "q15": "A",
            "q16": "A", "q17": "A", "q18": "A", "q19": "A", "q20": "A",
            "q21": "A", "q22": "A", "q23": "A", "q24": "A", "q25": "A",
            "q26": "A", "q27": "A", "q28": "A"
        },
        "questionnaire_nutrition": {
            "objectif_principal": "Retrouver de l'énergie et réduire le stress",
            "situation_ideale": "Ne plus être épuisée en permanence",
            "petit_dejeuner": "Café + biscuits (souvent sautés)",
            "dejeuner": "Sandwich rapide ou plat préparé",
            "diner": "Repas tardif, souvent gras par fatigue",
            "grignotage": "Sucré constant: chocolat, bonbons",
            "hydratation": "1L eau + 6-8 cafés par jour",
            "allergies": "Aucune connue",
            "supplements": "Aucun actuellement",
            "problemes_digestifs": "Brûlures d'estomac, ballonnements fréquents"
        },
        "questionnaire_sommeil": {
            "heure_coucher": "01h00-02h00 (insomnie)",
            "heure_lever": "6h30 (réveil difficile)",
            "duree_endormissement": "1-2 heures",
            "reveils_nocturnes": "5-6 fois par nuit",
            "qualite_sommeil": "Très mauvaise, non réparatrice",
            "fatigue_matinale": "Épuisement total au réveil",
            "siestes": "Impossible de faire sieste",
            "ecrans_soir": "Travail sur ordinateur jusqu'à minuit",
            "environnement": "Bruyant, lumineux, stress"
        },
        "bilans_additionnels": {
            "nutrition": "Carences multiples: B6, B12, magnésium, zinc. Inflammation systémique. Déséquilibre glycémique sévère.",
            "sommeil": "Insomnie sévère. Durée moyenne: 4h20. Micro-réveils fréquents. Architecture du sommeil perturbée."
        },
        "notes_coach": "Situation critique. Plan d'intervention immédiate mis en place. Suivi quotidien requis. Tous les blocs déficitaires. Ondes Delta et Alpha critiques.",
        "protocole_recommande": "URGENCE: 1) Arrêt caféine après 12h 2) Magnésium 600mg + mélatonine 3) Consultation médicale 4) Congé maladie si possible 5) Suivi psychologique"
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
            "blocD": 75.3,
            "blocE": 79.8
        },
        "sous_scores": {
            "dopamine": 76.8,
            "serotonine": 74.2,
            "gaba": 71.5,
            "noradrenaline": 78.9,
            "acetylcholine": 79.3
        },
        "ondes_cerebrales": {
            "delta": 78.2,
            "theta": 82.5,
            "alpha": 85.1,
            "beta": 75.8,
            "gamma": 72.4
        },
        "questionnaire_supra": {
            "q1": "C", "q2": "C", "q3": "C", "q4": "C", "q5": "C",
            "q6": "C", "q7": "C", "q8": "C", "q9": "C", "q10": "C",
            "q11": "C", "q12": "C", "q13": "C", "q14": "C", "q15": "C",
            "q16": "C", "q17": "C", "q18": "C", "q19": "C", "q20": "C",
            "q21": "C", "q22": "C", "q23": "C", "q24": "C", "q25": "D",
            "q26": "C", "q27": "C", "q28": "C"
        },
        "questionnaire_nutrition": {
            "objectif_principal": "Optimiser la performance cognitive et créative",
            "situation_ideale": "Maintenir ma créativité tout en gagnant en focus",
            "petit_dejeuner": "Smoothie fruits/légumes + avoine",
            "dejeuner": "Bowl végétarien ou poisson + légumes",
            "diner": "Cuisine maison équilibrée",
            "grignotage": "Fruits, noix, chocolat noir",
            "hydratation": "2L eau + thé vert",
            "allergies": "Aucune",
            "supplements": "Oméga-3, vitamine D",
            "problemes_digestifs": "Aucun"
        },
        "questionnaire_sommeil": {
            "heure_coucher": "23h00",
            "heure_lever": "7h00",
            "duree_endormissement": "15 minutes",
            "reveils_nocturnes": "1 fois occasionnellement",
            "qualite_sommeil": "Bonne avec rêves créatifs",
            "fatigue_matinale": "Forme correcte",
            "siestes": "20min après déjeuner si besoin",
            "ecrans_soir": "Arrêt 22h, musique douce",
            "environnement": "Calme, température fraîche"
        },
        "bilans_additionnels": {
            "nutrition": "Bon équilibre général. Optimisation possible des antioxydants pour soutenir la créativité visuelle.",
            "sommeil": "Qualité satisfaisante. Durée moyenne: 7h45. Sommeil créatif avec bonnes phases REM."
        },
        "notes_coach": "Progression constante. Continuer le protocole d'optimisation cognitive. Excellent profil visuel-spatial avec ondes Alpha dominantes.",
        "protocole_recommande": "1) Continuer oméga-3 2) Exercices visualisation 3) Méditation mindfulness 4) Art-thérapie 5) Optimisation workspace visuel"
    }
]

# Base de données en mémoire
operators_db = SAMPLE_OPERATORS.copy()

# Base de données pour les scans Supra Scan (organisée par email client)
supra_scans_db = {}

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
                'blocD': 68.0,
                'blocE': 69.0
            }),
            'sous_scores': data.get('sous_scores', {
                'dopamine': 65.0,
                'serotonine': 70.0,
                'gaba': 68.0,
                'noradrenaline': 72.0,
                'acetylcholine': 69.0
            }),
            'ondes_cerebrales': data.get('ondes_cerebrales', {
                'delta': 70.0,
                'theta': 68.0,
                'alpha': 72.0,
                'beta': 69.0,
                'gamma': 65.0
            }),
            'bilans_additionnels': data.get('bilans_additionnels', {
                'nutrition': 'Données reçues via SUPRA-CODE',
                'sommeil': 'Analyse en cours'
            }),
            'notes_coach': data.get('notes', 'Données reçues via webhook SUPRA-CODE'),
            'protocole_recommande': data.get('protocole', 'Protocole en cours d\'élaboration')
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

# Nouvelle route API sécurisée pour recevoir les résultats de Supra Scan
QG_API_SECRET_KEY = os.environ.get('QG_API_SECRET_KEY')

@app.route('/api/v1/new-scan-result', methods=['POST'])
def receive_scan_result():
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Authorization header is missing or invalid"}), 401
    
    token = auth_header.split(' ')[1]
    
    if not QG_API_SECRET_KEY or token != QG_API_SECRET_KEY:
        return jsonify({"error": "Unauthorized"}), 403
        
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request must be JSON"}), 400
    
    # Validation des champs obligatoires
    required_fields = [
        'clientEmail', 'clientName', 'clientPhone', 'clientSex', 
        'clientBirthdate', 'discipline', 'scanDate', 'neurotype',
        'rawAnswers', 'scoreData', 'reportContent'
    ]
    
    missing_fields = []
    for field in required_fields:
        if field not in data or data[field] is None:
            missing_fields.append(field)
    
    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "missing_fields": missing_fields
        }), 400
    
    # Sauvegarde dans la base de données
    client_email = data['clientEmail']
    
    # Structure du scan à sauvegarder
    scan_record = {
        'id': len(supra_scans_db.get(client_email, [])) + 1,
        'clientEmail': data['clientEmail'],
        'clientName': data['clientName'],
        'clientPhone': data['clientPhone'],
        'clientSex': data['clientSex'],
        'clientBirthdate': data['clientBirthdate'],
        'discipline': data['discipline'],
        'scanDate': data['scanDate'],
        'neurotype': data['neurotype'],
        'rawAnswers': data['rawAnswers'],
        'scoreData': data['scoreData'],
        'reportContent': data['reportContent'],
        'receivedAt': datetime.now().isoformat()
    }
    
    # Initialiser la liste pour ce client si elle n'existe pas
    if client_email not in supra_scans_db:
        supra_scans_db[client_email] = []
    
    # Ajouter le scan à la liste du client
    supra_scans_db[client_email].append(scan_record)
    
    print("--- NOUVEAU RÉSULTAT DE SCAN REÇU ET SAUVEGARDÉ ---")
    print(f"Client: {data['clientName']} ({data['clientEmail']})")
    print(f"Neurotype: {data['neurotype']}")
    print(f"Discipline: {data['discipline']}")
    print(f"Date scan: {data['scanDate']}")
    print(f"Total scans pour ce client: {len(supra_scans_db[client_email])}")
    
    return jsonify({
        "status": "success", 
        "message": "Scan result received and saved",
        "scan_id": scan_record['id'],
        "total_scans": len(supra_scans_db[client_email])
    }), 200

@app.route('/api/supra-scans', methods=['GET'])
def get_supra_scans():
    """Récupérer tous les scans Supra avec résumé par client"""
    if not session.get('authenticated'):
        return jsonify({'error': 'Non authentifié'}), 401
    
    scans_summary = []
    for client_email, scans in supra_scans_db.items():
        if scans:  # Si le client a au moins un scan
            latest_scan = max(scans, key=lambda x: x['scanDate'])
            scans_summary.append({
                'clientEmail': client_email,
                'clientName': latest_scan['clientName'],
                'clientPhone': latest_scan['clientPhone'],
                'latestScanDate': latest_scan['scanDate'],
                'neurotype': latest_scan['neurotype'],
                'discipline': latest_scan['discipline'],
                'totalScans': len(scans)
            })
    
    # Trier par date de dernier scan (plus récent en premier)
    scans_summary.sort(key=lambda x: x['latestScanDate'], reverse=True)
    
    return jsonify({
        'success': True,
        'items': scans_summary,
        'total': len(scans_summary)
    })

@app.route('/api/supra-scans/<client_email>', methods=['GET'])
def get_client_scans(client_email):
    """Récupérer tous les scans d'un client spécifique"""
    if not session.get('authenticated'):
        return jsonify({'error': 'Non authentifié'}), 401
    
    if client_email not in supra_scans_db:
        return jsonify({'error': 'Client non trouvé'}), 404
    
    scans = supra_scans_db[client_email]
    # Trier par date de scan (plus récent en premier)
    scans_sorted = sorted(scans, key=lambda x: x['scanDate'], reverse=True)
    
    return jsonify({
        'success': True,
        'clientEmail': client_email,
        'scans': scans_sorted,
        'totalScans': len(scans_sorted)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

