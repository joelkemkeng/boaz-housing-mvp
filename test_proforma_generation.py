#!/usr/bin/env python3
"""
Test de génération de proforma - Script de test simple et direct
"""

import sys
import os
sys.path.append('/home/joel/projet-boaz-housing/boaz-housing-mvp/backend')

from app.services.proforma_generator import ProformaGenerator
from app.services.services_data import ServicesDataService
import json

def test_proforma_generation():
    """Test complet de génération de proforma"""
    print("🚀 Test de génération de proforma...")
    
    try:
        # 1. Initialiser les services
        proforma_generator = ProformaGenerator()
        services_data_service = ServicesDataService()
        
        # 2. Récupérer les données de l'organisation
        organisation_data = services_data_service.get_organisation_details()
        print("✅ Données organisation récupérées")
        
        # 3. Récupérer les services disponibles
        services = services_data_service.get_all_services(active_only=True)
        print(f"✅ {len(services)} services trouvés")
        
        if not services:
            print("❌ Aucun service actif trouvé!")
            return None
            
        # 4. Données client test
        client_data = {
            "nom": "MARTIN",
            "prenom": "Jean-Claude", 
            "email": "jean-claude.martin@email.com",
            "date_naissance": "15/03/2000",
            "ville_naissance_client": "Douala",
            "pays_naissance_client": "Cameroun",
            "telephone": "+237 690 000 000"
        }
        
        # 5. Données logement test
        logement_data = {
            "adresse": "24 Rue du Docteur Charcot, Nanterre",
            "ville": "Nanterre",
            "pays": "France",
            "loyer": 450000,  # en FCFA
            "charges": 50000
        }
        
        # 6. Sélectionner le premier service actif (Attestation de Logement)
        selected_services = [services[0]]  # Premier service actif
        
        print(f"✅ Service sélectionné: {selected_services[0]['nom']}")
        print(f"   Prix: {selected_services[0]['tarif']} FCFA")
        
        # 7. Générer la proforma
        print("🔄 Génération PDF en cours...")
        pdf_path = proforma_generator.generate_proforma(
            client_data=client_data,
            services_data=selected_services,
            logement_data=logement_data,
            organisation_data={"organisation": organisation_data}
        )
        
        # 8. Vérifier le résultat
        if os.path.exists(pdf_path):
            file_size = os.path.getsize(pdf_path)
            print(f"✅ PDF généré avec succès!")
            print(f"📄 Path: {pdf_path}")
            print(f"📊 Taille: {file_size:,} bytes")
            
            # Créer un lien symbolique pour faciliter l'accès
            link_path = "/home/joel/test_proforma.pdf"
            if os.path.exists(link_path):
                os.remove(link_path)
            os.symlink(pdf_path, link_path)
            print(f"🔗 Lien créé: {link_path}")
            
            return pdf_path
        else:
            print("❌ Fichier PDF non trouvé!")
            return None
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Fonction principale"""
    print("=" * 60)
    print("TEST GÉNÉRATION PROFORMA - BOAZ HOUSING")
    print("=" * 60)
    
    pdf_path = test_proforma_generation()
    
    print("=" * 60)
    if pdf_path:
        print("🎉 TEST RÉUSSI!")
        print(f"📄 PDF disponible: {pdf_path}")
        print("🔗 Lien rapide: /home/joel/test_proforma.pdf")
    else:
        print("💥 TEST ÉCHOUÉ!")
    print("=" * 60)

if __name__ == "__main__":
    main()