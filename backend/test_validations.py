#!/usr/bin/env python3
"""
Script de test des validations de logement
"""
import pytest
from unittest.mock import MagicMock
from app.models.logement import Logement, StatutLogement
from app.schemas.logement import LogementCreate, LogementUpdate  
from app.services.logement_service import LogementService
from app.exceptions.logement_exceptions import (
    LogementValidationError,
    LogementBusinessRuleError, 
    LogementNotFoundError,
    LogementStatutError
)

def test_create_logement_valid():
    """Test création logement valide"""
    service = LogementService()
    db_mock = MagicMock()
    
    # Mock pour éviter la duplication
    db_mock.query.return_value.filter.return_value.first.return_value = None
    db_mock.add = MagicMock()
    db_mock.commit = MagicMock()
    db_mock.refresh = MagicMock()
    
    logement_data = LogementCreate(
        titre="Appartement T2 lumineux",
        adresse="15 rue de la Paix", 
        ville="Paris",
        code_postal="75001",
        pays="France",
        loyer=1000.0,
        montant_charges=150.0
    )
    
    # Test que la création réussit sans exception
    result = service.create_logement(db_mock, logement_data)
    
    # Vérifications
    db_mock.add.assert_called_once()
    db_mock.commit.assert_called_once()
    print("✅ Test création logement valide: PASSED")

def test_create_logement_loyer_trop_bas():
    """Test création avec loyer trop bas"""
    service = LogementService()
    db_mock = MagicMock()
    
    logement_data = LogementCreate(
        titre="Appartement T2",
        adresse="15 rue de la Paix",
        ville="Paris", 
        code_postal="75001",
        loyer=10.0,  # Trop bas
        montant_charges=0.0
    )
    
    with pytest.raises(LogementBusinessRuleError) as exc_info:
        service.create_logement(db_mock, logement_data)
    
    assert "loyer doit être d'au moins" in str(exc_info.value)
    print("✅ Test loyer trop bas: PASSED")

def test_create_logement_charges_trop_elevees():
    """Test création avec charges supérieures à 80% du loyer"""
    service = LogementService()
    db_mock = MagicMock()
    db_mock.query.return_value.filter.return_value.first.return_value = None
    
    logement_data = LogementCreate(
        titre="Appartement T2",
        adresse="15 rue de la Paix",
        ville="Paris",
        code_postal="75001", 
        loyer=1000.0,
        montant_charges=900.0  # 90% du loyer - trop élevé
    )
    
    with pytest.raises(LogementBusinessRuleError) as exc_info:
        service.create_logement(db_mock, logement_data)
        
    assert "charges ne peuvent pas dépasser 80%" in str(exc_info.value)
    print("✅ Test charges trop élevées: PASSED")

def test_validate_ville_format():
    """Test validation format ville"""
    from app.models.logement import Logement
    
    # Test ville valide
    logement = Logement()
    result = logement.validate_ville("ville", "Saint-Étienne")
    assert result == "Saint-Étienne"
    
    # Test ville avec caractères invalides
    with pytest.raises(ValueError) as exc_info:
        logement.validate_ville("ville", "Paris123")
    
    assert "lettres, espaces, tirets et apostrophes" in str(exc_info.value)
    print("✅ Test validation format ville: PASSED")

def test_validate_code_postal():
    """Test validation code postal"""
    from app.models.logement import Logement
    
    logement = Logement()
    
    # Test code postal français valide
    result = logement.validate_code_postal("code_postal", "75001")
    assert result == "75001"
    
    # Test code postal invalide
    with pytest.raises(ValueError) as exc_info:
        logement.validate_code_postal("code_postal", "123")
        
    assert "Format de code postal invalide" in str(exc_info.value)
    print("✅ Test validation code postal: PASSED")

def test_changement_statut_interdit():
    """Test changement de statut interdit"""
    service = LogementService()
    db_mock = MagicMock()
    
    # Mock logement occupé
    logement_occupe = MagicMock()
    logement_occupe.id = 1
    logement_occupe.statut = StatutLogement.OCCUPE
    logement_occupe.updated_at = None
    
    service.get_logement = MagicMock(return_value=logement_occupe)
    
    # Tenter de passer directement d'occupé à disponible (interdit)
    with pytest.raises(LogementStatutError) as exc_info:
        service.changer_statut_logement(db_mock, 1, StatutLogement.DISPONIBLE)
    
    assert "Transition interdite" in str(exc_info.value)
    print("✅ Test changement statut interdit: PASSED")

if __name__ == "__main__":
    print("🔍 Exécution des tests de validation...")
    
    test_create_logement_valid()
    test_create_logement_loyer_trop_bas()
    test_create_logement_charges_trop_elevees()
    test_validate_ville_format()
    test_validate_code_postal()
    test_changement_statut_interdit()
    
    print("🎉 Tous les tests de validation ont réussi!")