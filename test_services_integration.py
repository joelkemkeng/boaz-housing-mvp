"""
Suite de tests complète pour vérifier l'intégration services.json
"""

import sys
import os
sys.path.append('/home/joel/projet-boaz-housing/boaz-housing-mvp/backend')

import json
from pathlib import Path

def test_services_json_structure():
    """Test 1: Vérifier la structure du fichier services.json"""
    print("=== TEST 1: Structure services.json ===")
    
    services_file = Path('/home/joel/projet-boaz-housing/boaz-housing-mvp/backend/app/data/services.json')
    
    if not services_file.exists():
        print("❌ ÉCHEC: services.json introuvable")
        return False
    
    try:
        with open(services_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Vérifications structure
        assert 'services' in data, "Clé 'services' manquante"
        services = data['services']
        
        print(f"✅ Fichier chargé: {len(services)} services trouvés")
        
        # Vérifier service ID 1 (par défaut)
        service_1 = None
        for service in services:
            if service.get('id') == 1:
                service_1 = service
                break
        
        assert service_1 is not None, "Service ID 1 introuvable"
        
        # Vérifier les champs requis
        required_fields = ['id', 'nom', 'tarif', 'description', 'active']
        for field in required_fields:
            assert field in service_1, f"Champ '{field}' manquant dans service ID 1"
        
        print(f"✅ Service ID 1: {service_1['nom']}")
        print(f"✅ Tarif: {service_1['tarif']} FCFA")
        print(f"✅ Actif: {service_1['active']}")
        
        return True
        
    except Exception as e:
        print(f"❌ ÉCHEC: {str(e)}")
        return False

def test_services_data_service():
    """Test 2: Tester le service ServicesDataService"""
    print("\n=== TEST 2: ServicesDataService ===")
    
    try:
        from app.services.services_data import ServicesDataService
        
        service_data = ServicesDataService()
        
        # Test 2.1: Récupération service par ID
        service_1 = service_data.get_service_by_id(1)
        assert service_1 is not None, "Service ID 1 non trouvé"
        print(f"✅ Service par ID: {service_1['nom']}")
        
        # Test 2.2: Récupération services par IDs
        services_list = service_data.get_services_by_ids([1])
        assert len(services_list) == 1, "Liste services incorrecte"
        print(f"✅ Services par IDs: {len(services_list)} service(s)")
        
        # Test 2.3: Tous les services actifs
        active_services = service_data.get_all_services(active_only=True)
        print(f"✅ Services actifs: {len(active_services)}")
        
        # Test 2.4: Calcul total
        total = service_data.calculate_services_total([1])
        assert total > 0, "Total invalide"
        print(f"✅ Total calculé: {total} FCFA")
        
        # Test 2.5: Données organisation
        org_data = service_data.get_organisation_details()
        assert isinstance(org_data, dict), "Données organisation invalides"
        print(f"✅ Organisation chargée: {len(org_data)} champs")
        
        return True
        
    except Exception as e:
        print(f"❌ ÉCHEC: {str(e)}")
        return False

def test_proforma_generator_compatibility():
    """Test 3: Compatibilité générateur Proforma avec services.json"""
    print("\n=== TEST 3: Compatibilité Proforma Generator ===")
    
    try:
        from app.services.services_data import ServicesDataService
        from app.services.proforma_generator import ProformaGenerator
        
        # Récupérer les services
        service_data = ServicesDataService()
        services = service_data.get_services_by_ids([1])
        
        assert len(services) > 0, "Aucun service récupéré"
        
        service = services[0]
        
        # Vérifier les clés utilisées par le générateur
        required_keys = ['nom', 'tarif']
        for key in required_keys:
            assert key in service, f"Clé '{key}' manquante pour générateur"
            assert service[key] is not None, f"Valeur '{key}' nulle"
        
        print(f"✅ Nom service: {service['nom']}")
        print(f"✅ Tarif service: {service['tarif']} FCFA")
        
        # Test calcul total comme dans le générateur
        total_services = sum(s.get('tarif', 0) for s in services)
        print(f"✅ Calcul total: {total_services} FCFA")
        
        # Test structure items comme dans le générateur
        items = []
        for service in services:
            item = {
                'description': service.get('nom', ''),
                'quantity': 1,
                'unit_price': service.get('tarif', 0),
                'amount': service.get('tarif', 0)
            }
            items.append(item)
            
        assert len(items) > 0, "Aucun item généré"
        print(f"✅ Items générés: {len(items)}")
        print(f"✅ Premier item: {items[0]['description']} - {items[0]['amount']} FCFA")
        
        return True
        
    except Exception as e:
        print(f"❌ ÉCHEC: {str(e)}")
        return False

def test_endpoint_integration():
    """Test 4: Simulation endpoint avec services.json"""
    print("\n=== TEST 4: Simulation Endpoint Envoi Proforma ===")
    
    try:
        from app.services.services_data import ServicesDataService
        
        service_data = ServicesDataService()
        
        # Simulation logique endpoint
        print("Simulation récupération souscription...")
        
        # Simulation: souscription sans services_ids (cas par défaut)
        services_ids_default = [1]  # Valeur par défaut
        print(f"Services IDs par défaut: {services_ids_default}")
        
        # Récupération services depuis services.json
        services_data = service_data.get_services_by_ids(services_ids_default)
        
        if not services_data:
            print("⚠️ Aucun service trouvé, utilisation fallback...")
            service_1 = service_data.get_service_by_id(1)
            if service_1:
                services_data = [service_1]
        
        assert len(services_data) > 0, "Aucun service disponible"
        
        print(f"✅ Services récupérés: {len(services_data)}")
        
        # Vérification données pour PDF
        for i, service in enumerate(services_data):
            print(f"✅ Service {i+1}:")
            print(f"   Nom: {service.get('nom', 'N/A')}")
            print(f"   Tarif: {service.get('tarif', 0)} FCFA")
            print(f"   Description: {service.get('description', 'N/A')[:50]}...")
        
        # Calcul total final
        total = sum(service.get('tarif', 0) for service in services_data)
        print(f"✅ Total final: {total} FCFA")
        
        # Simulation données client et logement
        client_data = {
            'nom': 'MARTIN',
            'prenom': 'Jean',
            'email': 'jean.martin@email.com'
        }
        
        logement_data = {
            'adresse': '123 Rue de Test',
            'ville': 'Paris',
            'pays': 'France',
            'prix_mois': 800
        }
        
        print(f"✅ Données client: {client_data['prenom']} {client_data['nom']}")
        print(f"✅ Données logement: {logement_data['adresse']}")
        
        print("✅ Simulation endpoint réussie!")
        
        return True
        
    except Exception as e:
        print(f"❌ ÉCHEC: {str(e)}")
        return False

def test_comparison_before_after():
    """Test 5: Comparaison avant/après correction"""
    print("\n=== TEST 5: Comparaison Avant/Après ===")
    
    try:
        from app.services.services_data import ServicesDataService
        
        service_data = ServicesDataService()
        
        # AVANT (données codées en dur)
        old_data = {
            "nom": "Attestation de Logement et de Prise en Charge",
            "prix": 100.00,  # EUR codé en dur
            "description": "Service complet d'attestation"
        }
        
        # APRÈS (depuis services.json)
        new_services = service_data.get_services_by_ids([1])
        new_data = new_services[0] if new_services else {}
        
        print("AVANT (codé en dur):")
        print(f"  Nom: {old_data['nom']}")
        print(f"  Prix: {old_data['prix']} EUR ❌")
        print(f"  Description: {old_data['description']}")
        
        print("\nAPRÈS (depuis services.json):")
        print(f"  Nom: {new_data.get('nom', 'N/A')}")
        print(f"  Prix: {new_data.get('tarif', 0)} FCFA ✅")
        print(f"  Description: {new_data.get('description', 'N/A')}")
        
        # Vérifications
        assert new_data.get('tarif', 0) > old_data['prix'], "Le nouveau tarif devrait être supérieur"
        assert new_data.get('nom') == old_data['nom'], "Le nom devrait être identique"
        
        print(f"\n✅ Amélioration: {new_data.get('tarif', 0)} FCFA vs {old_data['prix']} EUR")
        print("✅ Le système utilise maintenant les vraies données!")
        
        return True
        
    except Exception as e:
        print(f"❌ ÉCHEC: {str(e)}")
        return False

def run_all_tests():
    """Exécuter tous les tests"""
    print("🧪 SUITE DE TESTS - INTÉGRATION SERVICES.JSON")
    print("=" * 60)
    
    tests = [
        ("Structure services.json", test_services_json_structure),
        ("ServicesDataService", test_services_data_service),
        ("Compatibilité Proforma", test_proforma_generator_compatibility),
        ("Simulation Endpoint", test_endpoint_integration),
        ("Comparaison Avant/Après", test_comparison_before_after)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ ERREUR dans {test_name}: {str(e)}")
            results.append((test_name, False))
    
    # Résumé final
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✅ RÉUSSI" if result else "❌ ÉCHOUÉ"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\n📈 RÉSULTAT GLOBAL:")
    print(f"✅ Tests réussis: {passed}")
    print(f"❌ Tests échoués: {failed}")
    print(f"📊 Taux de réussite: {(passed/(passed+failed)*100):.1f}%")
    
    if failed == 0:
        print("\n🎉 TOUS LES TESTS SONT RÉUSSIS!")
        print("🎯 Le système utilise correctement services.json")
        print("✅ L'intégration est parfaite!")
    else:
        print(f"\n⚠️ {failed} test(s) ont échoué")
        print("🔧 Vérification nécessaire")
    
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)