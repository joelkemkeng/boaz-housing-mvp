import pytest
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import Logement, Client, Souscription
from app.models.logement import StatutLogement
from app.models.souscription import StatutSouscription
from datetime import date

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

def test_create_logement(db_session: Session):
    """Test création d'un logement avec les nouveaux champs"""
    logement = Logement(
        titre="Appartement Centre-ville",
        description="Bel appartement moderne en centre-ville",
        adresse="123 Rue Test",
        ville="Paris",
        code_postal="75001",
        pays="France",
        loyer=450.0,
        montant_charges=50.0,
        montant_total=500.0,
        statut=StatutLogement.DISPONIBLE
    )
    
    db_session.add(logement)
    db_session.commit()
    
    # Vérification des nouveaux champs
    assert logement.id is not None
    assert logement.titre == "Appartement Centre-ville"
    assert logement.description == "Bel appartement moderne en centre-ville"
    assert logement.adresse == "123 Rue Test"
    assert logement.ville == "Paris"
    assert logement.code_postal == "75001"
    assert logement.pays == "France"
    assert logement.loyer == 450.0
    assert logement.montant_charges == 50.0
    assert logement.montant_total == 500.0
    assert logement.statut == StatutLogement.DISPONIBLE
    assert logement.created_at is not None

def test_create_client(db_session: Session):
    """Test création d'un client"""
    client = Client(
        nom_complet="Jean Dupont",
        date_naissance=date(1995, 5, 15),
        ville_naissance="Lyon",
        pays_naissance="France",
        email="jean.dupont@email.com",
        telephone="+33123456789",
        etablissement="Université de Paris",
        niveau_etude="Master 2"
    )
    
    db_session.add(client)
    db_session.commit()
    
    # Vérification
    assert client.id is not None
    assert client.nom_complet == "Jean Dupont"
    assert client.email == "jean.dupont@email.com"

def test_create_souscription(db_session: Session):
    """Test création d'une souscription complète"""
    # Créer un logement avec les nouveaux champs obligatoires
    logement = Logement(
        titre="Studio Étudiant",
        description="Studio parfait pour étudiant",
        adresse="456 Rue Exemple",
        ville="Marseille", 
        code_postal="13001",
        pays="France",
        loyer=380.0,
        montant_charges=0.0,
        montant_total=380.0
    )
    db_session.add(logement)
    db_session.flush()
    
    # Créer un client
    client = Client(
        nom_complet="Marie Martin",
        date_naissance=date(1998, 3, 20),
        ville_naissance="Nice",
        pays_naissance="France",
        email="marie.martin@email.com",
        telephone="+33987654321",
        etablissement="ESCP Business School",
        niveau_etude="Master 1"
    )
    db_session.add(client)
    db_session.flush()
    
    # Créer une souscription
    souscription = Souscription(
        client_id=client.id,
        logement_id=logement.id,
        date_entree=date(2024, 9, 1),
        duree_location=12,
        reference="ATT-TEST123456",
        statut=StatutSouscription.ATTENTE_PAIEMENT
    )
    
    db_session.add(souscription)
    db_session.commit()
    
    # Vérifications
    assert souscription.id is not None
    assert souscription.reference == "ATT-TEST123456"
    assert souscription.statut == StatutSouscription.ATTENTE_PAIEMENT
    assert souscription.client.nom_complet == "Marie Martin"
    assert souscription.logement.adresse == "456 Rue Exemple"

def test_logement_validations(db_session: Session):
    """Test des validations du modèle Logement"""
    # Test validation titre
    with pytest.raises(ValueError, match="Le titre ne peut pas être vide"):
        logement = Logement(
            titre="",
            adresse="123 Rue Test",
            ville="Paris",
            code_postal="75001",
            pays="France",
            loyer=450.0,
            montant_charges=50.0,
            montant_total=500.0
        )
        # Les validations se déclenchent lors de l'attribution
        logement.titre = ""
    
    # Test validation ville avec caractères spéciaux
    logement = Logement(
        titre="Test Logement",
        adresse="123 Rue Test",
        ville="Saint-Étienne",  # Ville avec tiret et accent
        code_postal="42000",
        pays="France",
        loyer=400.0,
        montant_charges=50.0,
        montant_total=450.0
    )
    
    db_session.add(logement)
    db_session.commit()
    
    assert logement.ville == "Saint-Étienne"  # Validation des caractères spéciaux
    
def test_logement_default_values(db_session: Session):
    """Test des valeurs par défaut du modèle Logement"""
    logement = Logement(
        titre="Logement Test Défaut",
        adresse="123 Rue Défaut",
        ville="Paris",
        code_postal="75001",
        # pays par défaut = "France"
        loyer=500.0,
        # montant_charges par défaut = 0.0
        montant_total=500.0
        # statut par défaut = DISPONIBLE
    )
    
    db_session.add(logement)
    db_session.commit()
    
    assert logement.pays == "France"
    assert logement.montant_charges == 0.0
    assert logement.statut == StatutLogement.DISPONIBLE