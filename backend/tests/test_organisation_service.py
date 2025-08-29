import pytest
from app.services.organisation_service import OrganisationService

def test_organisation_service_load_config():
    """Test du chargement de la configuration"""
    service = OrganisationService()
    config = service.get_all_config()
    
    assert "organisation" in config
    assert "ceo" in config
    assert "documents" in config

def test_get_organisation_info():
    """Test récupération infos organisation"""
    service = OrganisationService()
    org = service.get_organisation_info()
    
    assert org["nom"] == "Boaz-Housing"
    assert org["email_contact"] == "info@boaz-study.fr"
    assert org["telephone"] == "+33 01 84 18 02 67"
    assert "Corbeil-Essonnes" in org["adresse_siege"]

def test_get_ceo_info():
    """Test récupération infos CEO"""
    service = OrganisationService()
    ceo = service.get_ceo_info()
    
    assert ceo["nom_complet"] == "Benjamin YOHO BATOMO"
    assert ceo["ville_naissance"] == "Douala"
    assert ceo["pays_naissance"] == "Cameroun"

def test_generate_reference_code():
    """Test génération code de référence"""
    service = OrganisationService()
    
    # Générer plusieurs références pour tester l'unicité
    ref1 = service.generate_reference_code()
    ref2 = service.generate_reference_code()
    
    # Vérifier le format
    assert ref1.startswith("ATT-")
    assert ref2.startswith("ATT-")
    assert len(ref1) == 16  # ATT- (4) + 12 caractères
    assert len(ref2) == 16
    
    # Vérifier l'unicité
    assert ref1 != ref2

def test_generate_qr_code_url():
    """Test génération URL QR code"""
    service = OrganisationService()
    reference = "ATT-TEST123456"
    
    url = service.generate_qr_code_url(reference)
    
    assert url == "http://localhost:3000/verify/ATT-TEST123456"

def test_get_contact_info():
    """Test récupération infos contact formatées"""
    service = OrganisationService()
    contact = service.get_contact_info()
    
    expected_keys = ["email", "telephone", "site_web"]
    for key in expected_keys:
        assert key in contact
    
    assert contact["email"] == "info@boaz-study.fr"
    assert contact["telephone"] == "+33 01 84 18 02 67"
    assert contact["site_web"] == "www.boaz-study.com"

def test_format_address_for_document():
    """Test formatage adresse pour documents"""
    service = OrganisationService()
    address = service.format_address_for_document()
    
    assert "14 Rue Jean Piestre" in address
    assert "Corbeil-Essonnes" in address
    assert "91100" in address