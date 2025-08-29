import os
import sys
from datetime import datetime

# Assurer que 'src' est dans le PYTHONPATH si lancé différemment
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from werkzeug.security import generate_password_hash

from src.models.operator import db, Coach
from src.routes.auth import auth_bp
from src.routes.operators import operators_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'qg-neuro-architecte-secret-key-2025')

# Cookies/session
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = True if os.environ.get('ENV','production') == 'production' else False

# DB config
db_url = os.environ.get('DATABASE_URL')
if db_url:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# CORS (limiter à ton domaine en prod)
allowed = os.environ.get('CORS_ORIGINS', '*')
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": allowed}})

# Init DB + blueprints
db.init_app(app)
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(operators_bp, url_prefix='/api')

def seed_admin():
    from src.models.operator import gen_api_key
    admin_email = os.environ.get('ADMIN_EMAIL', 'izelphin@gmail.com').lower()
    admin_name = os.environ.get('ADMIN_NAME', 'Irwin Zelphin - Coach Principal')
    admin_password = os.environ.get('ADMIN_PASSWORD', 'password123')
    coach = Coach.query.filter_by(email=admin_email).first()
    if not coach:
        coach = Coach(
            email=admin_email,
            password_hash=generate_password_hash(admin_password),
            nom_complet=admin_name,
            api_key=os.environ.get('WEBHOOK_API_KEY', gen_api_key())
        )
        db.session.add(coach)
        db.session.commit()

with app.app_context():
    os.makedirs(os.path.join(os.path.dirname(__file__), 'database'), exist_ok=True)
    db.create_all()
    seed_admin()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if not static_folder_path:
        return "Static folder not configured", 404
    if path and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    index_path = os.path.join(static_folder_path, 'index.html')
    if os.path.exists(index_path):
        return send_from_directory(static_folder_path, 'index.html')
    return "index.html not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
