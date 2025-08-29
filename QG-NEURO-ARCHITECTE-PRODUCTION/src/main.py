import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.operator import db, Coach, Operator
from src.routes.auth import auth_bp
from src.routes.operators import operators_bp
from werkzeug.security import generate_password_hash
import json
from datetime import datetime

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'qg-neuro-architecte-secret-key-2025'

# Configuration CORS pour permettre les requêtes depuis le frontend
CORS(app, supports_credentials=True)

# Enregistrement des blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(operators_bp, url_prefix='/api')

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def create_test_data():
    """Crée des données de test si elles n'existent pas"""
    try:
        # Vérifier si des données existent déjà
        if Coach.query.first():
            return
        
        # Créer un coach de test
        coach = Coach(
            email='contact@izsupra.com',
            password_hash=generate_password_hash('password123'),
            nom_complet='Irwin Zelphin - Coach Principal',
            api_key='test-api-key-qg-neuro-architecte-2025'
        )
        db.session.add(coach)
        db.session.flush()  # Pour obtenir l'ID
        
        # Créer des opérateurs de test
        operators_data = [
            {
                'nom_complet': 'Irwin Zelphin',
                'email': 'contact@izsupra.com',
                'telephone': '+33635390323',
                'neurotype': 'GABA-Calme Profond',
                'scores': {'blocA': 12, 'blocB': 3, 'blocC': 7, 'blocD': 2, 'blocE': 8},
                'pourcentages': {'blocA': 44.44, 'blocB': 25.00, 'blocC': 46.67, 'blocD': 13.33, 'blocE': 53.33},
                'sous_scores': {'dopamine': 83.33, 'serotonine': 16.67, 'acetylcholine': 33.33, 'noradrenaline': 33.33, 'gaba': 100.00, 'glutamate': 0.00},
                'url_rapport': 'https://supra-code.io/rapport/1a2b3c4d-5e6f-7g8h-9i0j-k1l2m3n4o5p6',
                'notes_coach': '# Notes du Coach\n\n## Observations\n- Niveau GABA très élevé (100%)\n- Bloc B et D critiques nécessitant intervention immédiate\n- Profil calme mais déséquilibré\n\n## Plan d\'action\n1. Protocole d\'activation matinal\n2. Exercices de stimulation cognitive\n3. Suivi hebdomadaire',
                'bilans_additionnels': {'nutrition': 'Repas typique : Petit-déjeuner léger, déjeuner équilibré, dîner tardif. Objectifs : Optimiser les horaires. Contraintes : Emploi du temps chargé.', 'sommeil': 'Heure de coucher : 23h30, Qualité perçue : 6/10, Réveils nocturnes fréquents.'}
            },
            {
                'nom_complet': 'Marie Dubois',
                'email': 'marie.dubois@example.com',
                'telephone': '+33123456789',
                'neurotype': 'Dopamine-Dynamique',
                'scores': {'blocA': 18, 'blocB': 12, 'blocC': 15, 'blocD': 8, 'blocE': 14},
                'pourcentages': {'blocA': 66.67, 'blocB': 40.00, 'blocC': 100.00, 'blocD': 26.67, 'blocE': 93.33},
                'sous_scores': {'dopamine': 95.00, 'serotonine': 45.00, 'acetylcholine': 60.00, 'noradrenaline': 70.00, 'gaba': 30.00, 'glutamate': 85.00},
                'url_rapport': 'https://supra-code.io/rapport/2b3c4d5e-6f7g-8h9i-0j1k-l2m3n4o5p6q7',
                'notes_coach': '# Notes du Coach\n\n## Observations\n- Profil dopaminergique dominant\n- Bloc D à surveiller\n- Énergie élevée mais instable\n\n## Plan d\'action\n1. Techniques de régulation\n2. Optimisation des cycles d\'activité',
                'bilans_additionnels': {'nutrition': 'Alimentation riche en protéines, consommation de caféine élevée.', 'sommeil': 'Endormissement difficile, réveil matinal naturel à 6h.'}
            },
            {
                'nom_complet': 'Thomas Martin',
                'email': 'thomas.martin@example.com',
                'telephone': '+33987654321',
                'neurotype': 'Équilibré-Stable',
                'scores': {'blocA': 20, 'blocB': 18, 'blocC': 19, 'blocD': 17, 'blocE': 16},
                'pourcentages': {'blocA': 74.07, 'blocB': 60.00, 'blocC': 126.67, 'blocD': 56.67, 'blocE': 106.67},
                'sous_scores': {'dopamine': 65.00, 'serotonine': 70.00, 'acetylcholine': 75.00, 'noradrenaline': 60.00, 'gaba': 55.00, 'glutamate': 50.00},
                'url_rapport': 'https://supra-code.io/rapport/3c4d5e6f-7g8h-9i0j-1k2l-m3n4o5p6q7r8',
                'notes_coach': '# Notes du Coach\n\n## Observations\n- Profil équilibré et stable\n- Tous les blocs dans la norme\n- Performance optimale\n\n## Plan d\'action\n1. Maintien des bonnes pratiques\n2. Optimisation fine',
                'bilans_additionnels': {'nutrition': 'Alimentation équilibrée et régulière.', 'sommeil': 'Sommeil de qualité, 7-8h par nuit.'}
            }
        ]
        
        for op_data in operators_data:
            operator = Operator(
                coach_id=coach.id,
                nom_complet=op_data['nom_complet'],
                email=op_data['email'],
                telephone=op_data['telephone'],
                neurotype=op_data['neurotype'],
                scores=json.dumps(op_data['scores']),
                pourcentages=json.dumps(op_data['pourcentages']),
                sous_scores=json.dumps(op_data['sous_scores']),
                url_rapport=op_data['url_rapport'],
                notes_coach=op_data['notes_coach'],
                bilans_additionnels=json.dumps(op_data['bilans_additionnels']),
                date_dernier_scan=datetime.utcnow()
            )
            # Calculer le statut d'urgence
            operator.statut_urgence = operator.calculate_statut_urgence()
            db.session.add(operator)
        
        db.session.commit()
        print("✅ Données de test créées avec succès!")
        print(f"📧 Email de connexion: {coach.email}")
        print(f"🔑 Mot de passe: password123")
        print(f"🔗 Clé API: {coach.api_key}")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erreur lors de la création des données de test: {e}")

with app.app_context():
    db.create_all()
    create_test_data()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
