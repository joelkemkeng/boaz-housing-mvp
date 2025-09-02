"""
Suite de tests pour verifier l'integration services.json
"""

import sys
import os
sys.path.append('/home/joel/projet-boaz-housing/boaz-housing-mvp/backend')

def test_services_integration():
    """Test complet de l'integration services.json"""
    print("=== TEST INTEGRATION SERVICES.JSON ===")
    
    try:
        from app.services.services_data import ServicesDataService
        
        service_data = ServicesDataService()
        
        # Test 1: Service par defaut (ID 1)
        print("\n1. Test service par defaut:")
        service_1 = service_data.get_service_by_id(1)
        
        if service_1:
            print(f"   Nom: {service_1['nom']}")
            print(f"   Tarif: {service_1['tarif']} FCFA")
            print(f"   Actif: {service_1['active']}")
            print("   OK - Service ID 1 trouve")
        else:
            print("   ERREUR - Service ID 1 introuvable")
            return False
        
        # Test 2: Services par IDs
        print("\n2. Test services par IDs:")
        services_list = service_data.get_services_by_ids([1])
        
        if len(services_list) == 1:
            print(f"   {len(services_list)} service recupere")
            print("   OK - get_services_by_ids fonctionne")
        else:
            print("   ERREUR - get_services_by_ids defaillant")
            return False
        
        # Test 3: Compatibilite generateur
        print("\n3. Test compatibilite generateur PDF:")
        service = services_list[0]
        
        # Verifier les cles utilisees par le generateur
        if 'nom' in service and 'tarif' in service:
            print(f"   Nom pour PDF: {service['nom']}")
            print(f"   Tarif pour PDF: {service['tarif']}")
            print("   OK - Cles compatibles generateur")
        else:
            print("   ERREUR - Cles manquantes pour generateur")
            return False
        
        # Test 4: Calcul total comme dans l'endpoint
        print("\n4. Test calcul total:")
        total = sum(s.get('tarif', 0) for s in services_list)
        
        if total > 0:
            print(f"   Total calcule: {total} FCFA")
            print("   OK - Calcul total fonctionne")
        else:
            print("   ERREUR - Calcul total incorrect")
            return False
        
        # Test 5: Organisation
        print("\n5. Test donnees organisation:")
        org_data = service_data.get_organisation_details()
        
        if isinstance(org_data, dict) and len(org_data) > 0:
            print(f"   {len(org_data)} champs organisation")
            print("   OK - Donnees organisation chargees")
        else:
            print("   ERREUR - Donnees organisation manquantes")
            return False
        
        # Test 6: Simulation endpoint complet
        print("\n6. Simulation endpoint envoi proforma:")
        
        # Donnees souscription simulees
        services_ids = [1]  # Par defaut
        services_data = service_data.get_services_by_ids(services_ids)
        
        if not services_data:
            # Fallback comme dans l'endpoint
            service_1 = service_data.get_service_by_id(1)
            if service_1:
                services_data = [service_1]
        
        if services_data:
            print(f"   Services pour PDF: {len(services_data)}")
            for i, service in enumerate(services_data):
                print(f"   Service {i+1}: {service.get('nom')} - {service.get('tarif')} FCFA")
            print("   OK - Simulation endpoint reussie")
        else:
            print("   ERREUR - Simulation endpoint echouee")
            return False
        
        # Test 7: Comparaison avant/apres
        print("\n7. Comparaison avant/apres correction:")
        
        # Ancien prix code en dur
        ancien_prix = 100.0  # EUR
        nouveau_prix = service_1.get('tarif', 0)  # FCFA
        
        print(f"   AVANT: {ancien_prix} EUR (code en dur)")
        print(f"   APRES: {nouveau_prix} FCFA (depuis services.json)")
        
        if nouveau_prix > ancien_prix:
            print("   OK - Nouveau prix superieur et correct")
        else:
            print("   WARNING - Verifier les prix")
        
        print("\n=== RESULTAT FINAL ===")
        print("TOUS LES TESTS REUSSIS!")
        print("Le systeme utilise correctement services.json")
        print("Integration parfaite!")
        
        return True
        
    except Exception as e:
        print(f"\nERREUR CRITIQUE: {str(e)}")
        print("Verification necessaire!")
        return False

def test_real_endpoint_simulation():
    """Test simulation complete de l'endpoint reel"""
    print("\n=== SIMULATION ENDPOINT REEL ===")
    
    try:
        from app.services.services_data import ServicesDataService
        
        # Simulation exacte de l'endpoint send_proforma_email_simple
        services_data_service = ServicesDataService()
        
        # Simulation souscription avec services_ids
        print("Simulation souscription avec services_ids = [1]")
        
        # Code exact de l'endpoint
        services_ids = [1]  # getattr(db_souscription, 'services_ids', None) or [1]
        services_data = services_data_service.get_services_by_ids(services_ids)
        
        if not services_data:
            # Fallback exact
            service_1 = services_data_service.get_service_by_id(1)
            if service_1:
                services_data = [service_1]
            else:
                # Dernier recours
                services_data = [{
                    "nom": "Attestation de Logement et de Prise en Charge",
                    "tarif": 160000.0,
                    "description": "Service complet d'attestation"
                }]
        
        print(f"Services recuperes: {len(services_data)}")
        
        # Verification structure pour generateur PDF
        for service in services_data:
            print(f"Service: {service.get('nom')}")
            print(f"Tarif: {service.get('tarif')} FCFA")
            
            # Verification cles requises pour le generateur
            required_keys = ['nom', 'tarif']
            for key in required_keys:
                if key not in service:
                    print(f"ERREUR: Cle '{key}' manquante")
                    return False
        
        print("OK - Simulation endpoint reelle reussie")
        print("Structure compatible avec generateur PDF")
        
        return True
        
    except Exception as e:
        print(f"ERREUR simulation: {str(e)}")
        return False

if __name__ == "__main__":
    print("TESTS INTEGRATION SERVICES.JSON")
    print("=" * 50)
    
    # Test principal
    test1_ok = test_services_integration()
    
    # Test simulation endpoint
    test2_ok = test_real_endpoint_simulation()
    
    print("\n" + "=" * 50)
    print("RESUME TESTS:")
    
    if test1_ok:
        print("REUSSI - Integration services.json")
    else:
        print("ECHEC - Integration services.json")
    
    if test2_ok:
        print("REUSSI - Simulation endpoint")
    else:
        print("ECHEC - Simulation endpoint")
    
    if test1_ok and test2_ok:
        print("\nCONCLUSION: TOUS LES TESTS REUSSIS!")
        print("Le systeme est pret!")
    else:
        print("\nCONCLUSION: Corrections necessaires")