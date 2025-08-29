#!/usr/bin/env python3
"""
Script de test pour le webhook QG Neuro-Architecte™
Simule l'envoi de données depuis l'application SUPRA-CODE
"""

import requests
import json

# Configuration
API_BASE = "http://localhost:5000"
API_KEY = "test-api-key-qg-neuro-architecte-2025"

def test_webhook():
    """Teste l'endpoint webhook avec des données d'exemple"""
    
    # Données d'exemple pour un nouvel opérateur
    payload = {
        "apiKey": API_KEY,
        "operateurData": {
            "nomComplet": "Sophie Laurent",
            "email": "sophie.laurent@example.com",
            "telephone": "+33123456789"
        },
        "scanSupraData": {
            "neurotype": "Serotonine-Equilibré",
            "scores": {
                "blocA": 15,
                "blocB": 18,
                "blocC": 12,
                "blocD": 16,
                "blocE": 14
            },
            "pourcentages": {
                "blocA": 55.56,
                "blocB": 60.00,
                "blocC": 80.00,
                "blocD": 53.33,
                "blocE": 93.33
            },
            "sousScores": {
                "dopamine": 45.00,
                "serotonine": 85.00,
                "acetylcholine": 65.00,
                "noradrenaline": 55.00,
                "gaba": 70.00,
                "glutamate": 40.00
            },
            "urlRapport": "https://supra-code.io/rapport/test-sophie-laurent-2025"
        },
        "bilansAdditionnels": {
            "nutrition": "Alimentation équilibrée, consommation modérée de caféine.",
            "sommeil": "Sommeil régulier, 7-8h par nuit, qualité perçue : 8/10."
        }
    }
    
    try:
        print("🚀 Test du webhook QG Neuro-Architecte™")
        print(f"📡 Envoi vers: {API_BASE}/api/v1/ingest")
        print(f"🔑 Clé API: {API_KEY}")
        print()
        
        response = requests.post(
            f"{API_BASE}/api/v1/ingest",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"📊 Statut HTTP: {response.status_code}")
        print(f"📋 Réponse: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Webhook testé avec succès!")
                print(f"👤 Opérateur ID: {data.get('operator_id')}")
                print(f"⚠️ Statut d'urgence: {data.get('statut_urgence')}")
            else:
                print("❌ Erreur dans la réponse:", data.get('error'))
        else:
            print("❌ Erreur HTTP:", response.status_code)
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")

def test_critical_case():
    """Teste un cas critique avec des scores très bas"""
    
    payload = {
        "apiKey": API_KEY,
        "operateurData": {
            "nomComplet": "Alexandre Critique",
            "email": "alex.critique@example.com",
            "telephone": "+33987654321"
        },
        "scanSupraData": {
            "neurotype": "Dopamine-Hyperactif",
            "scores": {
                "blocA": 8,
                "blocB": 2,
                "blocC": 5,
                "blocD": 1,
                "blocE": 6
            },
            "pourcentages": {
                "blocA": 29.63,
                "blocB": 16.67,
                "blocC": 33.33,
                "blocD": 6.67,
                "blocE": 40.00
            },
            "sousScores": {
                "dopamine": 95.00,
                "serotonine": 15.00,
                "acetylcholine": 25.00,
                "noradrenaline": 85.00,
                "gaba": 10.00,
                "glutamate": 90.00
            },
            "urlRapport": "https://supra-code.io/rapport/test-alexandre-critique-2025"
        },
        "bilansAdditionnels": {
            "nutrition": "Alimentation irrégulière, forte consommation de stimulants.",
            "sommeil": "Insomnie fréquente, 4-5h par nuit, qualité perçue : 3/10."
        }
    }
    
    try:
        print("\n🚨 Test d'un cas critique")
        
        response = requests.post(
            f"{API_BASE}/api/v1/ingest",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Cas critique traité: {data.get('statut_urgence')}")
        else:
            print(f"❌ Erreur: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("🧠 QG NEURO-ARCHITECTE™ - TEST WEBHOOK")
    print("=" * 60)
    
    # Test normal
    test_webhook()
    
    # Test cas critique
    test_critical_case()
    
    print("\n" + "=" * 60)
    print("✅ Tests terminés!")
    print("📱 Vérifiez l'interface web pour voir les nouveaux opérateurs")
    print("=" * 60)

