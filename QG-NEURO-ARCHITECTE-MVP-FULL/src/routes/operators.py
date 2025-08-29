import os
from flask import Blueprint, request, jsonify, session
from src.models.operator import db, Operator, Coach
from sqlalchemy import or_

operators_bp = Blueprint('operators', __name__)

def require_auth():
    coach_id = session.get('coach_id')
    if not coach_id:
        return None
    return Coach.query.get(coach_id)

@operators_bp.route('/operators', methods=['GET'])
def list_operators():
    coach = require_auth()
    if not coach:
        return jsonify({"error": "Unauthorized"}), 401

    q = request.args.get('q')
    statut = request.args.get('statut')  # Critique / À Surveiller / Stable

    query = Operator.query.filter_by(coach_id=coach.id)
    if q:
        like = f"%{q}%"
        query = query.filter(or_(Operator.nom_complet.ilike(like), Operator.email.ilike(like)))
    if statut and statut in ('Critique', 'À Surveiller', 'Stable'):
        query = query.filter(Operator.statut_urgence == statut)

    items = [o.to_row() for o in query.order_by(Operator.date_dernier_scan.desc()).all()]
    stats = {
        "total": len(items),
        "critique": sum(1 for o in items if o['statutUrgence'] == 'Critique'),
        "surveiller": sum(1 for o in items if o['statutUrgence'] == 'À Surveiller'),
        "stable": sum(1 for o in items if o['statutUrgence'] == 'Stable'),
    }
    return jsonify({"items": items, "stats": stats})

@operators_bp.route('/operators/<int:op_id>', methods=['GET'])
def get_operator(op_id):
    coach = require_auth()
    if not coach:
        return jsonify({"error": "Unauthorized"}), 401
    op = Operator.query.get_or_404(op_id)
    if op.coach_id != coach.id:
        return jsonify({"error": "Forbidden"}), 403
    return jsonify(op.to_detail())

@operators_bp.route('/webhook/supra-scan', methods=['POST'])
def webhook_supra_scan():
    # Header basé sur la clé API de l'admin (ou var d'env WEBHOOK_API_KEY)
    api_key = request.headers.get('X-API-KEY')
    if not api_key:
        return jsonify({"error": "Missing API key"}), 401

    # Validateur de la clé
    coach = Coach.query.filter_by(email=os.environ.get('ADMIN_EMAIL', 'izelphin@gmail.com').strip().lower()).first()
    expected = os.environ.get('WEBHOOK_API_KEY') or (coach.api_key if coach else None)
    if not expected or api_key != expected:
        return jsonify({"error": "Unauthorized"}), 401

    payload = request.get_json(silent=True) or {}
    nom = payload.get('nomComplet') or payload.get('nom_complet') or 'Sans Nom'
    email = payload.get('email')
    telephone = payload.get('telephone')
    scan = payload.get('scanSupra') or payload.get('scan') or {}

    if not email:
        return jsonify({"error": "email is required"}), 400

    # upsert par email + coach
    op = Operator.query.filter_by(coach_id=coach.id, email=email).first()
    if not op:
        op = Operator(coach_id=coach.id, email=email, nom_complet=nom, telephone=telephone)
        db.session.add(op)
    else:
        op.nom_complet = nom
        op.telephone = telephone

    # Normalisation partielle des champs de scan reçus
    op.update_from_scan({
        "neurotype": scan.get('neurotype'),
        "scores": {
            "blocA": scan.get('scoreA'), "blocB": scan.get('scoreB'),
            "blocC": scan.get('scoreC'), "blocD": scan.get('scoreD'), "blocE": scan.get('scoreE'),
        },
        "pourcentages": {
            "blocA": scan.get('pctA'), "blocB": scan.get('pctB'),
            "blocC": scan.get('pctC'), "blocD": scan.get('pctD'), "blocE": scan.get('pctE'),
        },
        "sousScores": scan.get('sousScores') or {},
        "urlRapport": scan.get('urlRapport'),
        "reponsesBrutes": scan.get('reponses') or scan.get('reponsesBrutes') or [],
    })

    db.session.commit()
    return jsonify({"success": True, "operatorId": op.id, "statutUrgence": op.statut_urgence})
