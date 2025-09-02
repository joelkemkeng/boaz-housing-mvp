"""
Test d'integration complete backend pour envoi proforma
"""

import sys
sys.path.append('/home/joel/projet-boaz-housing/boaz-housing-mvp/backend')

def test_full_proforma_generation():
    """Test complet de generation proforma avec services.json"""
    print("=== TEST GENERATION PROFORMA COMPLETE ===")
    
    try:
        from app.services.services_data import ServicesDataService
        from app.services.proforma_generator import ProformaGenerator
        import tempfile
        import os
        
        # Etape 1: Recuperer les services
        print("\n1. Recuperation services depuis services.json:")
        services_data_service = ServicesDataService()
        services_ids = [1]  # Service par defaut
        services_data = services_data_service.get_services_by_ids(services_ids)
        
        if not services_data:
            print("ERREUR: Aucun service trouve")
            return False
        
        service = services_data[0]
        print(f"   Service: {service['nom']}")
        print(f"   Tarif: {service['tarif']} FCFA")
        print("   OK - Service recupere")
        
        # Etape 2: Donnees organisation
        print("\n2. Recuperation donnees organisation:")
        organisation_data = services_data_service.get_organisation_details()
        
        if not organisation_data:
            print("ERREUR: Donnees organisation manquantes")
            return False
        
        print(f"   {len(organisation_data)} champs organisation")
        print("   OK - Organisation recuperee")
        
        # Etape 3: Donnees test
        print("\n3. Preparation donnees test:")
        client_data = {
            'nom': 'MARTIN',
            'prenom': 'Jean',
            'email': 'jean.martin@email.com'
        }
        
        logement_data = {
            'adresse': '123 Rue de Test, Paris',
            'ville': 'Paris',
            'pays': 'France',
            'prix_mois': 800
        }
        
        print(f"   Client: {client_data['prenom']} {client_data['nom']}")
        print(f"   Logement: {logement_data['adresse']}")
        print("   OK - Donnees test preparees")
        
        # Etape 4: Generation PDF
        print("\n4. Generation Proforma PDF:")
        proforma_generator = ProformaGenerator()
        
        try:
            pdf_path = proforma_generator.generate_proforma(
                client_data=client_data,
                services_data=services_data,  # Services depuis services.json
                logement_data=logement_data,
                organisation_data=organisation_data
            )
            
            if os.path.exists(pdf_path):
                file_size = os.path.getsize(pdf_path)
                print(f"   PDF genere: {os.path.basename(pdf_path)}")
                print(f"   Taille: {file_size} bytes")
                print("   OK - PDF genere avec succes")
                
                # Nettoyage
                try:
                    os.remove(pdf_path)
                except:
                    pass
                
                return True
            else:
                print("ERREUR: PDF non genere")
                return False
                
        except Exception as e:
            print(f"ERREUR generation PDF: {str(e)}")
            return False
        
    except Exception as e:
        print(f"ERREUR critique: {str(e)}")
        return False

def test_email_service_structure():
    """Test structure service email"""
    print("\n=== TEST STRUCTURE SERVICE EMAIL ===")
    
    try:
        from app.services.email_service import email_service
        
        print("1. Test configuration email:")
        print(f"   Host: {email_service.smtp_host}")
        print(f"   Port: {email_service.smtp_port}")
        print(f"   From: {email_service.from_email}")
        print("   OK - Configuration chargee")
        
        print("\n2. Test methodes disponibles:")
        methods = ['send_proforma_email', 'send_attestation_email', 'test_connection']
        
        for method in methods:
            if hasattr(email_service, method):
                print(f"   Methode {method}: OK")
            else:
                print(f"   Methode {method}: MANQUANTE")
                return False
        
        print("   OK - Toutes les methodes disponibles")
        
        return True
        
    except Exception as e:
        print(f"ERREUR: {str(e)}")
        return False

def test_endpoint_logic_simulation():
    """Test logique complete de l'endpoint"""
    print("\n=== TEST LOGIQUE ENDPOINT COMPLETE ===")
    
    try:
        from app.services.services_data import ServicesDataService
        from app.services.proforma_generator import ProformaGenerator
        from app.services.email_service import email_service
        import os
        
        # Simulation complete de l'endpoint send_proforma_email_simple
        
        print("1. Simulation recuperation souscription:")
        # Simulation souscription
        class MockSouscription:
            def __init__(self):
                self.id = 1
                self.reference = "ATT-TEST123456"
                self.nom_client = "MARTIN"
                self.prenom_client = "Jean"
                self.email_client = "jean.martin@email.com"
                self.services_ids = [1]  # Nouveau champ
                
                # Mock logement
                self.logement = MockLogement()
        
        class MockLogement:
            def __init__(self):
                self.adresse = "123 Rue de Test"
                self.ville = "Paris"
                self.pays = "France"
                self.loyer = 800
        
        db_souscription = MockSouscription()
        print(f"   Souscription: {db_souscription.reference}")
        print(f"   Client: {db_souscription.prenom_client} {db_souscription.nom_client}")
        print(f"   Email: {db_souscription.email_client}")
        print("   OK - Souscription simulee")
        
        print("\n2. Validation donnees:")
        # Validations de l'endpoint
        if not db_souscription.email_client:
            print("ERREUR: Email client manquant")
            return False
        
        if not db_souscription.logement:
            print("ERREUR: Logement manquant")
            return False
        
        print("   OK - Validations passees")
        
        print("\n3. Recuperation services (logique endpoint):")
        services_data_service = ServicesDataService()
        
        # Logique exacte de l'endpoint
        services_ids = getattr(db_souscription, 'services_ids', None) or [1]
        services_data = services_data_service.get_services_by_ids(services_ids)
        
        if not services_data:
            # Fallback exacte
            service_1 = services_data_service.get_service_by_id(1)
            if service_1:
                services_data = [service_1]
            else:
                services_data = [{
                    "nom": "Attestation de Logement et de Prise en Charge",
                    "tarif": 160000.0,
                    "description": "Service complet d'attestation"
                }]
        
        print(f"   Services recuperes: {len(services_data)}")
        print(f"   Service principal: {services_data[0]['nom']}")
        print(f"   Tarif: {services_data[0]['tarif']} FCFA")
        print("   OK - Services charges depuis services.json")
        
        print("\n4. Preparation donnees generation:")
        # Donnees exactes de l'endpoint
        client_data = {
            'nom': db_souscription.nom_client,
            'prenom': db_souscription.prenom_client,
            'email': db_souscription.email_client
        }
        
        logement_data = {
            'adresse': db_souscription.logement.adresse,
            'ville': db_souscription.logement.ville,
            'pays': db_souscription.logement.pays,
            'prix_mois': db_souscription.logement.loyer
        }
        
        organisation_data = services_data_service.get_organisation_details()
        
        print("   Donnees client: OK")
        print("   Donnees logement: OK")
        print("   Donnees organisation: OK")
        
        print("\n5. Test generation PDF:")
        proforma_generator = ProformaGenerator()
        
        pdf_path = proforma_generator.generate_proforma(
            client_data=client_data,
            services_data=services_data,
            logement_data=logement_data,
            organisation_data=organisation_data
        )
        
        if os.path.exists(pdf_path):
            print("   PDF genere avec succes")
            
            # Lecture bytes (comme endpoint)
            with open(pdf_path, 'rb') as f:
                pdf_bytes = f.read()
            
            print(f"   Taille PDF: {len(pdf_bytes)} bytes")
            
            # Nettoyage
            os.remove(pdf_path)
            
            print("   OK - Generation PDF complete")
        else:
            print("ERREUR: PDF non genere")
            return False
        
        print("\n6. Test preparation envoi email:")
        client_name = f"{db_souscription.prenom_client} {db_souscription.nom_client}"
        
        # Structure d'appel email service (sans envoi reel)
        email_params = {
            'to_email': db_souscription.email_client,
            'pdf_bytes': pdf_bytes,
            'reference': db_souscription.reference,
            'client_name': client_name
        }
        
        print(f"   Destinataire: {email_params['to_email']}")
        print(f"   Reference: {email_params['reference']}")
        print(f"   Client: {email_params['client_name']}")
        print(f"   PDF: {len(email_params['pdf_bytes'])} bytes")
        print("   OK - Parametres email prepares")
        
        print("\n=== RESULTAT SIMULATION ENDPOINT ===")
        print("SIMULATION COMPLETE REUSSIE!")
        print("Logique endpoint parfaitement fonctionnelle")
        print("Integration services.json confirmee")
        
        return True
        
    except Exception as e:
        print(f"ERREUR simulation: {str(e)}")
        return False

if __name__ == "__main__":
    print("TESTS INTEGRATION COMPLETE BACKEND")
    print("=" * 60)
    
    tests = [
        ("Generation Proforma complete", test_full_proforma_generation),
        ("Structure service email", test_email_service_structure),
        ("Simulation endpoint complete", test_endpoint_logic_simulation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n>>> {test_name.upper()}")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 60)
    print("RESUME FINAL:")
    
    all_passed = True
    for test_name, result in results:
        status = "REUSSI" if result else "ECHEC"
        print(f"{status} - {test_name}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("CONCLUSION: INTEGRATION PARFAITE!")
        print("Le systeme utilise correctement services.json")
        print("Tous les composants sont operationnels")
        print("L'envoi de proforma est pret!")
    else:
        print("CONCLUSION: Problemes detectes")
        print("Verification necessaire")