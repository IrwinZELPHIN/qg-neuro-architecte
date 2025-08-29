from flask import Blueprint, request, jsonify, session
from src.models.operator import db, Operator, Coach
from datetime import datetime
import json

operators_bp = Blueprint('operators', __name__)

def require_auth():
    """Vérifie que l'utilisateur est connecté"""
    coach_id = session.get('coach_id')
    if not coach_id:
        return None
    return Coach.query.get(coach_id)

@operators_bp.route('/operators', methods=['GET'])
def get_operators():
    """Récupère la liste des opérateurs du coach connecté"""
    coach = require_auth()
    if not coach:
        return jsonify({'error': 'Non connecté'}), 401
    
    try:
        # Filtres optionnels
        search = request.args.get('search', '')
        status_filter = request.args.get('status', 'Tous')
        
        # Requête de base
        query = Operator.query.filter_by(coach_id=coach.id)
        
        # Filtre de recherche
        if search:
            query = query.filter(
                db.or_(
                    Operator.nom_complet.ilike(f'%{search}%'),
                    Operator.email.ilike(f'%{search}%')
                )
            )
        
        # Filtre de statut
        if status_filter and status_filter != 'Tous':
            query = query.filter_by(statut_urgence=status_filter)
        
        operators = query.order_by(Operator.date_dernier_scan.desc()).all()
        
        return jsonify({
            'success': True,
            'operators': [op.to_dict() for op in operators]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@operators_bp.route('/operators/<int:operator_id>', methods=['GET'])
def get_operator(operator_id):
    """Récupère un opérateur spécifique"""
    coach = require_auth()
    if not coach:
        return jsonify({'error': 'Non connecté'}), 401
    
    try:
        operator = Operator.query.filter_by(id=operator_id, coach_id=coach.id).first()
        
        if not operator:
            return jsonify({'error': 'Opérateur non trouvé'}), 404
        
        return jsonify({
            'success': True,
            'operator': operator.to_dict()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@operators_bp.route('/operators/<int:operator_id>/notes', methods=['PUT'])
def update_operator_notes(operator_id):
    """Met à jour les notes du coach pour un opérateur"""
    coach = require_auth()
    if not coach:
        return jsonify({'error': 'Non connecté'}), 401
    
    try:
        data = request.get_json()
        notes = data.get('notes', '')
        
        operator = Operator.query.filter_by(id=operator_id, coach_id=coach.id).first()
        
        if not operator:
            return jsonify({'error': 'Opérateur non trouvé'}), 404
        
        operator.notes_coach = notes
        operator.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Notes mises à jour'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@operators_bp.route('/v1/ingest', methods=['POST'])
def webhook_ingest():
    """Webhook pour recevoir les données de l'application SUPRA-CODE"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Données JSON requises'}), 400
        
        # Vérification de la clé API
        api_key = data.get('apiKey')
        if not api_key:
            return jsonify({'error': 'Clé API manquante'}), 400
        
        # Rechercher le coach par clé API
        coach = Coach.query.filter_by(api_key=api_key).first()
        if not coach:
            return jsonify({'error': 'Clé API invalide'}), 401
        
        # Extraire les données
        operator_data = data.get('operateurData', {})
        scan_data = data.get('scanSupraData', {})
        bilans_data = data.get('bilansAdditionnels', {})
        
        if not operator_data or not scan_data:
            return jsonify({'error': 'Données opérateur et scan requises'}), 400
        
        email = operator_data.get('email')
        if not email:
            return jsonify({'error': 'Email opérateur requis'}), 400
        
        # Rechercher ou créer l'opérateur
        operator = Operator.query.filter_by(email=email, coach_id=coach.id).first()
        
        if not operator:
            # Créer un nouvel opérateur
            operator = Operator(
                coach_id=coach.id,
                nom_complet=operator_data.get('nomComplet', ''),
                email=email,
                telephone=operator_data.get('telephone', ''),
                notes_coach=f"# Notes du Coach\n\n## Observations\n- Nouveau profil créé automatiquement\n- Neurotype: {scan_data.get('neurotype', 'Non défini')}\n\n## Plan d'action\n1. Analyser les résultats\n2. Définir la stratégie d'accompagnement"
            )
            db.session.add(operator)
        else:
            # Mettre à jour les informations de base
            operator.nom_complet = operator_data.get('nomComplet', operator.nom_complet)
            operator.telephone = operator_data.get('telephone', operator.telephone)
        
        # Mettre à jour avec les données du scan
        operator.update_from_scan_data(scan_data)
        
        # Mettre à jour les bilans additionnels
        if bilans_data:
            operator.bilans_additionnels = json.dumps(bilans_data)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Données reçues et traitées avec succès',
            'operator_id': operator.id,
            'statut_urgence': operator.statut_urgence
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erreur lors du traitement: {str(e)}'}), 500

@operators_bp.route('/operators/stats', methods=['GET'])
def get_operators_stats():
    """Récupère les statistiques des opérateurs"""
    coach = require_auth()
    if not coach:
        return jsonify({'error': 'Non connecté'}), 401
    
    try:
        total = Operator.query.filter_by(coach_id=coach.id).count()
        critique = Operator.query.filter_by(coach_id=coach.id, statut_urgence='Critique').count()
        surveiller = Operator.query.filter_by(coach_id=coach.id, statut_urgence='À Surveiller').count()
        stable = Operator.query.filter_by(coach_id=coach.id, statut_urgence='Stable').count()
        
        return jsonify({
            'success': True,
            'stats': {
                'total': total,
                'critique': critique,
                'surveiller': surveiller,
                'stable': stable
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

