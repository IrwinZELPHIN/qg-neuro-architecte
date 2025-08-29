from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import secrets
import string

db = SQLAlchemy()

def gen_api_key(n: int = 40) -> str:
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(n))

class Coach(db.Model):
    __tablename__ = 'coaches'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    nom_complet = db.Column(db.String(150), nullable=False)
    api_key = db.Column(db.String(128), unique=True, nullable=False, default=gen_api_key)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    operators = db.relationship('Operator', backref='coach', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "nom_complet": self.nom_complet,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

class Operator(db.Model):
    __tablename__ = 'operators'
    id = db.Column(db.Integer, primary_key=True)
    coach_id = db.Column(db.Integer, db.ForeignKey('coaches.id'), nullable=False)

    # Données de base
    nom_complet = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(255), nullable=False, index=True)
    telephone = db.Column(db.String(30))

    # Données du scan
    date_dernier_scan = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    neurotype = db.Column(db.String(80))
    statut_urgence = db.Column(db.String(20))  # Critique, À Surveiller, Stable

    # Scores JSON
    scores = db.Column(db.Text)         # ex: {"blocA":12,...}
    pourcentages = db.Column(db.Text)   # ex: {"blocA":44.44,...}
    sous_scores = db.Column(db.Text)    # ex: {"dopamine":83.33,...}

    # Données additionnelles
    url_rapport = db.Column(db.String(500))
    reponses_brutes = db.Column(db.Text)       # JSON array
    bilans_additionnels = db.Column(db.Text)   # JSON: {nutrition:"...", sommeil:"..."}

    # Notes
    notes_coach = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def calculate_statut_urgence(self) -> str:
        try:
            pct = json.loads(self.pourcentages) if self.pourcentages else {}
            bloc_b = float(pct.get('blocB', 100))
            bloc_d = float(pct.get('blocD', 100))
            if bloc_b < 30 or bloc_d < 30:
                return 'Critique'
            elif bloc_b < 40 or bloc_d < 40:
                return 'À Surveiller'
            else:
                return 'Stable'
        except Exception:
            return 'Stable'

    def update_from_scan(self, scan: dict):
        self.date_dernier_scan = datetime.utcnow()
        self.neurotype = scan.get('neurotype')
        # Souplesse sur les clés reçues
        self.scores = json.dumps(scan.get('scores') or scan.get('score') or {})
        self.pourcentages = json.dumps(scan.get('pourcentages') or scan.get('pct') or {})
        self.sous_scores = json.dumps(scan.get('sousScores') or scan.get('sous_scores') or {})
        self.url_rapport = scan.get('urlRapport') or scan.get('url_rapport')
        self.reponses_brutes = json.dumps(scan.get('reponsesBrutes') or scan.get('reponses') or [])
        self.statut_urgence = self.calculate_statut_urgence()
        self.updated_at = datetime.utcnow()

    def to_row(self):
        try:
            pct = json.loads(self.pourcentages) if self.pourcentages else {}
        except Exception:
            pct = {}
        return {
            "id": self.id,
            "nomComplet": self.nom_complet,
            "email": self.email,
            "telephone": self.telephone,
            "dateDernierScan": (self.date_dernier_scan.isoformat() if self.date_dernier_scan else None),
            "neurotype": self.neurotype,
            "statutUrgence": self.statut_urgence,
            "pct": pct
        }

    def to_detail(self):
        def loads(s):
            try:
                return json.loads(s) if s else None
            except Exception:
                return None
        return {
            "id": self.id,
            "coachId": self.coach_id,
            "nomComplet": self.nom_complet,
            "email": self.email,
            "telephone": self.telephone,
            "dateDernierScan": self.date_dernier_scan.isoformat() if self.date_dernier_scan else None,
            "neurotype": self.neurotype,
            "statutUrgence": self.statut_urgence,
            "scores": loads(self.scores),
            "pourcentages": loads(self.pourcentages),
            "sousScores": loads(self.sous_scores),
            "urlRapport": self.url_rapport,
            "reponsesBrutes": loads(self.reponses_brutes),
            "bilansAdditionnels": loads(self.bilans_additionnels),
            "notesCoach": self.notes_coach,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None,
        }
