from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Coach(db.Model):
    __tablename__ = 'coaches'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    nom_complet = db.Column(db.String(100), nullable=False)
    api_key = db.Column(db.String(64), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relation avec les opérateurs
    operators = db.relationship('Operator', backref='coach', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'nom_complet': self.nom_complet,
            'api_key': self.api_key,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Operator(db.Model):
    __tablename__ = 'operators'
    
    id = db.Column(db.Integer, primary_key=True)
    coach_id = db.Column(db.Integer, db.ForeignKey('coaches.id'), nullable=False)
    
    # Données de base
    nom_complet = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telephone = db.Column(db.String(20))
    
    # Données du scan
    date_dernier_scan = db.Column(db.DateTime, default=datetime.utcnow)
    neurotype = db.Column(db.String(50))
    statut_urgence = db.Column(db.String(20))  # Critique, À Surveiller, Stable
    
    # Scores (stockés en JSON)
    scores = db.Column(db.Text)  # JSON: {blocA: 12, blocB: 3, ...}
    pourcentages = db.Column(db.Text)  # JSON: {blocA: 44.44, blocB: 25.00, ...}
    sous_scores = db.Column(db.Text)  # JSON: {dopamine: 83.33, serotonine: 16.67, ...}
    
    # Données additionnelles
    url_rapport = db.Column(db.String(255))
    reponses_brutes = db.Column(db.Text)  # JSON array
    bilans_additionnels = db.Column(db.Text)  # JSON: {nutrition: "...", sommeil: "..."}
    
    # Notes du coach
    notes_coach = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def calculate_statut_urgence(self):
        """Calcule le statut d'urgence basé sur les pourcentages"""
        if self.pourcentages:
            try:
                pourcentages_data = json.loads(self.pourcentages)
                bloc_b = pourcentages_data.get('blocB', 100)
                bloc_d = pourcentages_data.get('blocD', 100)
                
                if bloc_b < 30 or bloc_d < 30:
                    return 'Critique'
                elif bloc_b < 60 or bloc_d < 60:
                    return 'À Surveiller'
                else:
                    return 'Stable'
            except:
                return 'Stable'
        return 'Stable'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nom_complet': self.nom_complet,
            'email': self.email,
            'telephone': self.telephone,
            'date_dernier_scan': self.date_dernier_scan.isoformat() if self.date_dernier_scan else None,
            'neurotype': self.neurotype,
            'statut_urgence': self.statut_urgence,
            'scores': json.loads(self.scores) if self.scores else {},
            'pourcentages': json.loads(self.pourcentages) if self.pourcentages else {},
            'sous_scores': json.loads(self.sous_scores) if self.sous_scores else {},
            'url_rapport': self.url_rapport,
            'reponses_brutes': json.loads(self.reponses_brutes) if self.reponses_brutes else [],
            'bilans_additionnels': json.loads(self.bilans_additionnels) if self.bilans_additionnels else {},
            'notes_coach': self.notes_coach or '',
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def update_from_scan_data(self, scan_data):
        """Met à jour l'opérateur avec les données d'un scan"""
        self.date_dernier_scan = datetime.utcnow()
        self.neurotype = scan_data.get('neurotype')
        self.scores = json.dumps(scan_data.get('scores', {}))
        self.pourcentages = json.dumps(scan_data.get('pourcentages', {}))
        self.sous_scores = json.dumps(scan_data.get('sousScores', {}))
        self.url_rapport = scan_data.get('urlRapport')
        self.reponses_brutes = json.dumps(scan_data.get('reponsesBrutes', []))
        
        # Calcul automatique du statut d'urgence
        self.statut_urgence = self.calculate_statut_urgence()
        
        self.updated_at = datetime.utcnow()

