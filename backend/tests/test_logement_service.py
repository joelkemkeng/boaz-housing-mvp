import pytest
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.services.logement_service import logement_service
from app.schemas.logement import LogementCreate, LogementUpdate
from app.models.logement import Logement, StatutLogement
from app.exceptions.logement_exceptions import LogementNotFoundError, LogementBusinessRuleError

@pytest.fixture
def db_session():
    # Create tables for testing
    Base.metadata.create_all(bind=engine)
    
    # Create session
    session = SessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        # Clean up tables after tests
        Base.metadata.drop_all(bind=engine)

def test_create_logement_service(db_session: Session):
    """Test création logement via service"""
    logement_data = LogementCreate(
        titre="Service Test Logement",
        description="Test du service de création",
        adresse="123 Service Street",
        ville="ServiceVille",
        code_postal="12345",
        pays="France",
        loyer=450.0,
        montant_charges=50.0,
        statut=StatutLogement.DISPONIBLE
    )
    
    logement = logement_service.create_logement(db_session, logement_data)
    
    assert logement.id is not None
    assert logement.titre == "Service Test Logement"
    assert logement.montant_total == 500.0  # loyer + charges
    assert logement.created_at is not None

def test_get_logements_service(db_session: Session):
    """Test récupération logements via service"""
    # Créer quelques logements
    logement1_data = LogementCreate(
        titre="Logement 1",
        description="Description logement 1",
        adresse="Address 1",
        ville="Paris",
        code_postal="11111",
        pays="France",
        loyer=400.0,
        montant_charges=0.0,
        statut=StatutLogement.DISPONIBLE
    )
    
    logement2_data = LogementCreate(
        titre="Logement 2",
        description="Description logement 2",
        adresse="Address 2",
        ville="Lyon",
        code_postal="22222",
        pays="France",
        loyer=500.0,
        montant_charges=50.0,
        statut=StatutLogement.OCCUPE
    )
    
    logement_service.create_logement(db_session, logement1_data)
    logement_service.create_logement(db_session, logement2_data)
    
    # Test récupération tous
    logements = logement_service.get_logements(db_session)
    assert len(logements) == 2
    
    # Test avec filtre statut
    logements_disponibles = logement_service.get_logements(
        db_session, 
        statut=StatutLogement.DISPONIBLE
    )
    assert len(logements_disponibles) == 1
    assert logements_disponibles[0].statut == StatutLogement.DISPONIBLE
    
    # Test avec filtre ville
    logements_ville1 = logement_service.get_logements(
        db_session,
        ville="Paris"
    )
    assert len(logements_ville1) == 1
    assert logements_ville1[0].ville == "Paris"

def test_update_logement_service(db_session: Session):
    """Test mise à jour logement via service"""
    # Créer un logement
    logement_data = LogementCreate(
        titre="Logement à modifier",
        adresse="Address Update",
        ville="UpdateVille",
        code_postal="33333",
        pays="France",
        loyer=600.0,
        montant_charges=100.0
    )
    
    logement = logement_service.create_logement(db_session, logement_data)
    
    # Mettre à jour
    update_data = LogementUpdate(
        loyer=650.0,
        description="Description ajoutée"
    )
    
    updated_logement = logement_service.update_logement(
        db_session, 
        logement.id, 
        update_data
    )
    
    assert updated_logement.loyer == 650.0
    assert updated_logement.description == "Description ajoutée"
    assert updated_logement.montant_total == 750.0  # nouveau loyer + charges
    assert updated_logement.updated_at is not None

def test_changer_statut_logement_service(db_session: Session):
    """Test changement de statut via service - version MVP sans restrictions"""
    # Créer un logement
    logement_data = LogementCreate(
        titre="Logement Status Test",
        adresse="Status Address",
        ville="StatusVille",
        code_postal="44444",
        pays="France",
        loyer=400.0,
        montant_charges=0.0,
        statut=StatutLogement.DISPONIBLE
    )
    
    logement = logement_service.create_logement(db_session, logement_data)
    
    # Changer vers occupé
    updated_logement = logement_service.changer_statut_logement(
        db_session,
        logement.id,
        StatutLogement.OCCUPE
    )
    
    assert updated_logement.statut == StatutLogement.OCCUPE
    assert updated_logement.updated_at is not None
    
    # MVP: Test que toutes les transitions sont permises
    # Occupé -> Disponible (était interdit avant MVP)
    updated_logement = logement_service.changer_statut_logement(
        db_session,
        logement.id,
        StatutLogement.DISPONIBLE
    )
    
    assert updated_logement.statut == StatutLogement.DISPONIBLE

def test_delete_logement_service(db_session: Session):
    """Test suppression logement via service"""
    # Créer un logement
    logement_data = LogementCreate(
        titre="Logement à supprimer",
        adresse="Delete Address",
        ville="DeleteVille", 
        code_postal="55555",
        pays="France",
        loyer=300.0,
        montant_charges=0.0
    )
    
    logement = logement_service.create_logement(db_session, logement_data)
    logement_id = logement.id
    
    # Supprimer
    success = logement_service.delete_logement(db_session, logement_id)
    assert success is True
    
    # Vérifier suppression
    deleted_logement = logement_service.get_logement(db_session, logement_id)
    assert deleted_logement is None

def test_get_stats_logements_service(db_session: Session):
    """Test statistiques logements via service"""
    # Créer logements avec différents statuts
    logements_data = [
        LogementCreate(
            titre="Disponible 1",
            description="Description disponible 1",
            adresse="Addr1",
            ville="Paris",
            code_postal="11111",
            pays="France",
            loyer=400.0,
            montant_charges=0.0,
            statut=StatutLogement.DISPONIBLE
        ),
        LogementCreate(
            titre="Disponible 2",
            description="Description disponible 2",
            adresse="Addr2", 
            ville="Lyon",
            code_postal="22222",
            pays="France",
            loyer=500.0,
            montant_charges=0.0,
            statut=StatutLogement.DISPONIBLE
        ),
        LogementCreate(
            titre="Occupé 1",
            description="Description occupé 1",
            adresse="Addr3",
            ville="Marseille",
            code_postal="33333",
            pays="France",
            loyer=600.0,
            montant_charges=0.0,
            statut=StatutLogement.OCCUPE
        ),
        LogementCreate(
            titre="Maintenance 1",
            description="Description maintenance 1",
            adresse="Addr4",
            ville="Toulouse",
            code_postal="44444", 
            pays="France",
            loyer=450.0,
            montant_charges=0.0,
            statut=StatutLogement.MAINTENANCE
        )
    ]
    
    for logement_data in logements_data:
        logement_service.create_logement(db_session, logement_data)
    
    stats = logement_service.get_stats_logements(db_session)
    
    assert stats["total"] == 4
    assert stats["disponibles"] == 2
    assert stats["occupes"] == 1
    assert stats["maintenance"] == 1

def test_business_rules_validation(db_session: Session):
    """Test des règles métier du service"""
    # Test création logement valide
    logement_data = LogementCreate(
        titre="Logement valide",
        adresse="Test Valid Address",
        ville="Bordeaux",
        code_postal="12345",
        pays="France",
        loyer=800.0,
        montant_charges=100.0
    )
    
    logement = logement_service.create_logement(db_session, logement_data)
    assert logement.loyer == 800.0
    assert logement.montant_charges == 100.0
    assert logement.montant_total == 900.0

def test_logement_not_found_error(db_session: Session):
    """Test erreur logement non trouvé"""
    with pytest.raises(LogementNotFoundError):
        logement_service.update_logement(
            db_session,
            99999,  # ID inexistant
            LogementUpdate(loyer=500.0)
        )
    
    with pytest.raises(LogementNotFoundError):
        logement_service.changer_statut_logement(
            db_session,
            99999,  # ID inexistant
            StatutLogement.MAINTENANCE
        )