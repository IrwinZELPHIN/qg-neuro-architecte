from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash, generate_password_hash
from src.models.operator import db, Coach
import os

auth_bp = Blueprint('auth', __name__)

ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'izelphin@gmail.com').strip().lower()

@auth_bp.route('/login', methods=['POST'])
def login():
    payload = request.get_json(silent=True) or {}
    email = (payload.get('email') or '').strip().lower()
    password = payload.get('password') or ''

    coach = Coach.query.filter_by(email=ADMIN_EMAIL).first()
    if not coach or email != ADMIN_EMAIL:
        return jsonify({"error": "Unauthorized"}), 401
    if not check_password_hash(coach.password_hash, password):
        return jsonify({"error": "Invalid credentials"}), 401

    session['coach_id'] = coach.id
    return jsonify({"success": True, "coach": coach.to_dict()})

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"success": True})
