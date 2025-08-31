#!/usr/bin/env python3
"""
Script de test pour la génération de proforma avec le nouveau design
"""

import sys
import os
sys.path.append('/home/joel/projet-boaz-housing/boaz-housing-mvp/backend')

from app.services.proforma_generator import ProformaGenerator

def test_new_design():
    """Teste la génération avec le nouveau design"""
    print("🧪 Test génération proforma avec nouveau design")
    
    # Données du client
    client_data = {
        'nom_client': 'MARTIN',
        'prenom_client': 'Jean-Claude',
        'email_client': 'jean-claude.martin@email.com'
    }
    
    # Données des services
    services_data = [
        {
            'nom': 'Attestation de Logement et Prise en Charge',
            'tarif': 160000.0
        }
    ]
    
    # Données du logement
    logement_data = {
        'adresse': '24 Rue du Docteur Charcot',
        'ville': 'Nanterre'
    }
    
    # Données organisation (vides pour utiliser les valeurs par défaut)
    organisation_data = {}
    
    # Génération
    generator = ProformaGenerator()
    pdf_path = generator.generate_proforma(
        client_data=client_data,
        services_data=services_data, 
        logement_data=logement_data,
        organisation_data=organisation_data,
        numero_proforma="TEST-NEW-DESIGN-001"
    )
    
    if os.path.exists(pdf_path):
        print(f"✅ PDF généré avec nouveau design: {pdf_path}")
        print(f"📄 Taille: {os.path.getsize(pdf_path)} bytes")
        
        # Copier vers le host pour vérification
        host_path = "/home/joel/projet-boaz-housing/boaz-housing-mvp/proforma_new_design.pdf"
        os.system(f"cp {pdf_path} {host_path}")
        print(f"📋 Copie disponible: {host_path}")
        
    else:
        print("❌ Échec de génération PDF")

if __name__ == "__main__":
    test_new_design()