from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash, generate_password_hash
from src.models.operator import db, Coach
import secrets
import string

auth_bp = Blueprint('auth', __name__)

def generate_api_key():
    """Génère une clé API unique"""
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))

@auth_bp.route('/login', methods=['POST'])
def login():
    """Connexion du coach"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email et mot de passe requis'}), 400
        
        # Rechercher le coach
        coach = Coach.query.filter_by(email=email).first()
        
        if not coach or not check_password_hash(coach.password_hash, password):
            return jsonify({'error': 'Email ou mot de passe incorrect'}), 401
        
        # Créer la session
        session['coach_id'] = coach.id
        session['coach_email'] = coach.email
        
        return jsonify({
            'success': True,
            'coach': coach.to_dict()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Déconnexion du coach"""
    session.clear()
    return jsonify({'success': True})

@auth_bp.route('/register', methods=['POST'])
def register():
    """Inscription d'un nouveau coach (pour les tests)"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        nom_complet = data.get('nom_complet')
        
        if not email or not password or not nom_complet:
            return jsonify({'error': 'Tous les champs sont requis'}), 400
        
        # Vérifier si l'email existe déjà
        if Coach.query.filter_by(email=email).first():
            return jsonify({'error': 'Cet email est déjà utilisé'}), 400
        
        # Créer le nouveau coach
        coach = Coach(
            email=email,
            password_hash=generate_password_hash(password),
            nom_complet=nom_complet,
            api_key=generate_api_key()
        )
        
        db.session.add(coach)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Coach créé avec succès',
            'coach': coach.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/me', methods=['GET'])
def get_current_coach():
    """Récupère les informations du coach connecté"""
    coach_id = session.get('coach_id')
    
    if not coach_id:
        return jsonify({'error': 'Non connecté'}), 401
    
    coach = Coach.query.get(coach_id)
    if not coach:
        return jsonify({'error': 'Coach non trouvé'}), 404
    
    return jsonify({
        'success': True,
        'coach': coach.to_dict()
    })

@auth_bp.route('/check', methods=['GET'])
def check_auth():
    """Vérifie si l'utilisateur est connecté"""
    coach_id = session.get('coach_id')
    return jsonify({
        'authenticated': bool(coach_id),
        'coach_id': coach_id
    })

