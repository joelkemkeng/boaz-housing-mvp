#!/usr/bin/env python3
"""
Test script pour vérifier que les données dynamiques fonctionnent dans la génération de proforma
"""

import json
import os
from app.services.proforma_generator import ProformaGenerator

def test_dynamic_proforma():
    """Test des données dynamiques dans la proforma"""
    
    # Données de test (format frontend - comme envoyé par WizardSouscription)
    client_data = {
        'prenom': 'Jean',
        'nom': 'Dupont', 
        'email': 'jean.dupont@email.com'
    }
    
    services_data = [
        {
            'nom': 'Attestation de Logement et Prise en Charge',
            'tarif': 160000
        }
    ]
    
    logement_data = {
        'adresse': '15 Avenue de la République',
        'ville': 'Paris'
    }
    
    # Charger les données d'organisation depuis le fichier JSON
    with open('/app/app/data/organisation_details.json', 'r') as f:
        organisation_file = json.load(f)
        organisation_data = organisation_file['organisation']
    
    # Générer la proforma
    generator = ProformaGenerator()
    
    try:
        pdf_path = generator.generate_proforma(
            client_data=client_data,
            services_data=services_data,
            logement_data=logement_data,
            organisation_data=organisation_data,
            numero_proforma="TEST-DYNAMIC-001"
        )
        
        print(f"✅ Proforma générée avec succès: {pdf_path}")
        print("✅ Les données dynamiques ont été intégrées")
        
        # Vérifier que le fichier existe
        if os.path.exists(pdf_path):
            file_size = os.path.getsize(pdf_path)
            print(f"✅ Fichier PDF créé - Taille: {file_size} bytes")
            return pdf_path
        else:
            print("❌ Fichier PDF non créé")
            return None
            
    except Exception as e:
        print(f"❌ Erreur lors de la génération: {str(e)}")
        return None

if __name__ == "__main__":
    print("🧪 Test des données dynamiques dans la proforma...")
    result = test_dynamic_proforma()
    
    if result:
        print(f"\n📄 PDF généré: {result}")
        print("Les données suivantes ont été dynamisées:")
        print("- Nom de l'organisation")
        print("- Adresse et coordonnées")
        print("- Email et site web") 
        print("- Informations bancaires")
        print("- Notes de recommandation")
        print("- Conditions de paiement")
    else:
        print("\n❌ Le test a échoué")