#!/usr/bin/env python3
"""
Script pour créer des données de test - Logements et Souscriptions
"""

import requests
import json

API_BASE = "http://localhost:8000/api"

def create_test_logements():
    """Créer des logements de test"""
    logements = [
        {
            "titre": "Studio Moderne - Centre Ville",
            "description": "Beau studio meublé avec kitchenette équipée, proche transports",
            "adresse": "24 Rue du Docteur Charcot",
            "ville": "Nanterre",
            "code_postal": "92000", 
            "pays": "France",
            "loyer": 800.0,
            "montant_charges": 150.0,
            "statut": "disponible"
        },
        {
            "titre": "Chambre Étudiante - Résidence",
            "description": "Chambre dans résidence étudiante, accès cuisine commune",
            "adresse": "15 Avenue de la République",
            "ville": "Paris",
            "code_postal": "75011",
            "pays": "France", 
            "loyer": 650.0,
            "montant_charges": 100.0,
            "statut": "disponible"
        },
        {
            "titre": "Appartement T2 - Proche Université",
            "description": "T2 meublé, 2 chambres, cuisine équipée, proche universités",
            "adresse": "8 Rue André Ampère, Plateau de Moulon",
            "ville": "Orsay",
            "code_postal": "91190",
            "pays": "France",
            "loyer": 1200.0,
            "montant_charges": 200.0,
            "statut": "disponible"
        }
    ]
    
    created_logements = []
    for i, logement in enumerate(logements):
        try:
            response = requests.post(f"{API_BASE}/logements/", json=logement)
            if response.status_code in [200, 201]:
                created = response.json()
                print(f"✅ Logement {i+1} créé: {created['titre']}")
                created_logements.append(created)
            else:
                print(f"❌ Erreur logement {i+1}: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Exception logement {i+1}: {str(e)}")
    
    return created_logements

def create_test_souscription(logement_id):
    """Créer une souscription de test"""
    souscription = {
        "nom_client": "MARTIN",
        "prenom_client": "Jean-Claude",
        "email_client": "jean-claude.martin@email.com",
        "date_naissance_client": "2000-03-15",
        "ville_naissance_client": "Douala",
        "pays_naissance_client": "Cameroun",
        "nationalite_client": "Camerounaise",
        "pays_destination": "France",
        "date_arrivee_prevue": "2025-09-01",
        "ecole_universite": "Université Paris-Saclay",
        "filiere": "Master Informatique",
        "pays_ecole": "France",
        "ville_ecole": "Orsay", 
        "code_postal_ecole": "91190",
        "adresse_ecole": "Rue André Ampère, Plateau de Moulon",
        "logement_id": logement_id,
        "date_entree_prevue": "2025-09-01",
        "duree_location_mois": 12
    }
    
    try:
        response = requests.post(f"{API_BASE}/souscriptions/", json=souscription)
        if response.status_code in [200, 201]:
            created = response.json()
            print(f"✅ Souscription créée: {created['reference']}")
            return created
        else:
            print(f"❌ Erreur souscription: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception souscription: {str(e)}")
        return None

def test_endpoints():
    """Tester tous les endpoints"""
    print("\n=== TEST ENDPOINTS ===")
    
    # Test services
    try:
        response = requests.get(f"{API_BASE}/services/")
        print(f"Services: {response.status_code} - {len(response.json())} services")
    except Exception as e:
        print(f"❌ Services error: {e}")
    
    # Test logements
    try:
        response = requests.get(f"{API_BASE}/logements/")
        print(f"Logements: {response.status_code} - {len(response.json())} logements")
    except Exception as e:
        print(f"❌ Logements error: {e}")
    
    # Test souscriptions
    try:
        response = requests.get(f"{API_BASE}/souscriptions/")  
        print(f"Souscriptions: {response.status_code} - {len(response.json())} souscriptions")
    except Exception as e:
        print(f"❌ Souscriptions error: {e}")

def main():
    print("🚀 CRÉATION DE DONNÉES DE TEST")
    print("=" * 50)
    
    # Créer logements
    print("\n📍 Création des logements...")
    logements = create_test_logements()
    
    # Créer une souscription si on a des logements
    if logements:
        print(f"\n📝 Création d'une souscription sur le logement {logements[0]['id']}...")
        create_test_souscription(logements[0]['id'])
    
    # Tester les endpoints
    test_endpoints()
    
    print("\n✅ DONNÉES DE TEST CRÉÉES")
    print("=" * 50)

if __name__ == "__main__":
    main()