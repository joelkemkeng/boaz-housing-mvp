import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.database import SessionLocal, engine, Base
from app.models.logement import StatutLogement

client = TestClient(app)

@pytest.fixture(scope="function")
def setup_database():
    """Setup test database for API tests"""
    # Create tables for testing
    Base.metadata.create_all(bind=engine)
    
    yield
    
    # Clean up tables after tests
    Base.metadata.drop_all(bind=engine)

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

def test_create_logement(setup_database):
    """Test création d'un logement via API"""
    logement_data = {
        "titre": "Appartement test API",
        "description": "Description du logement de test",
        "adresse": "789 Rue Test API",
        "ville": "Marseille",
        "code_postal": "13001",
        "pays": "France",
        "loyer": 420.0,
        "statut": "disponible"
    }
    
    response = client.post("/api/logements/", json=logement_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["titre"] == "Appartement test API"
    assert data["description"] == "Description du logement de test"
    assert data["adresse"] == "789 Rue Test API"
    assert data["ville"] == "Marseille"
    assert data["pays"] == "France"
    assert data["loyer"] == 420.0
    assert data["statut"] == "disponible"
    assert "id" in data
    assert "created_at" in data

def test_get_logements(setup_database):
    """Test récupération liste logements"""
    # Créer d'abord un logement
    logement_data = {
        "titre": "Test List Logement",
        "adresse": "Test List Address",
        "ville": "Nice",
        "code_postal": "06000",
        "pays": "France",
        "loyer": 350.0
    }
    client.post("/api/logements/", json=logement_data)
    
    # Récupérer la liste
    response = client.get("/api/logements/")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_get_logement_by_id(setup_database):
    """Test récupération logement par ID"""
    # Créer un logement
    logement_data = {
        "titre": "Test Get By ID",
        "adresse": "Test Get By ID Address",
        "ville": "Toulouse",
        "code_postal": "31000",
        "pays": "France",
        "loyer": 400.0
    }
    create_response = client.post("/api/logements/", json=logement_data)
    logement_id = create_response.json()["id"]
    
    # Récupérer par ID
    response = client.get(f"/api/logements/{logement_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == logement_id
    assert data["titre"] == "Test Get By ID"

def test_update_logement(setup_database):
    """Test mise à jour d'un logement"""
    # Créer un logement
    logement_data = {
        "titre": "Test Update",
        "adresse": "Test Update Address",
        "ville": "Bordeaux",
        "code_postal": "33000",
        "pays": "France",
        "loyer": 380.0
    }
    create_response = client.post("/api/logements/", json=logement_data)
    logement_id = create_response.json()["id"]
    
    # Mettre à jour
    update_data = {"loyer": 420.0}
    response = client.put(f"/api/logements/{logement_id}", json=update_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["loyer"] == 420.0
    assert "updated_at" in data

def test_change_statut_logement(setup_database):
    """Test changement de statut"""
    # Créer un logement
    logement_data = {
        "titre": "Test Statut Change",
        "adresse": "Test Statut Change Address",
        "ville": "Lille",
        "code_postal": "59000",
        "pays": "France",
        "loyer": 340.0
    }
    create_response = client.post("/api/logements/", json=logement_data)
    logement_id = create_response.json()["id"]
    
    # Changer le statut
    response = client.patch(f"/api/logements/{logement_id}/statut?nouveau_statut=maintenance")
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["logement"]["statut"] == "maintenance"

def test_get_stats_logements(setup_database):
    """Test récupération des statistiques"""
    response = client.get("/api/logements/stats")
    
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "disponibles" in data
    assert "occupes" in data
    assert "maintenance" in data

def test_get_logement_not_found(setup_database):
    """Test récupération logement inexistant"""
    response = client.get("/api/logements/99999")
    
    assert response.status_code == 404
    assert "non trouvé" in response.json()["detail"]

def test_delete_logement(setup_database):
    """Test suppression d'un logement"""
    # Créer un logement
    logement_data = {
        "titre": "Test Delete",
        "adresse": "Test Delete Address",
        "ville": "Nantes",
        "code_postal": "44000",
        "pays": "France",
        "loyer": 360.0
    }
    create_response = client.post("/api/logements/", json=logement_data)
    logement_id = create_response.json()["id"]
    
    # Supprimer
    response = client.delete(f"/api/logements/{logement_id}")
    
    assert response.status_code == 200
    assert "supprimé avec succès" in response.json()["message"]
    
    # Vérifier que le logement n'existe plus
    get_response = client.get(f"/api/logements/{logement_id}")
    assert get_response.status_code == 404

def test_create_logement_with_all_fields(setup_database):
    """Test création logement avec tous les champs"""
    logement_data = {
        "titre": "Appartement Complet",
        "description": "Appartement avec tous les détails remplis",
        "adresse": "100 Boulevard Complet",
        "ville": "Lyon",
        "code_postal": "69000",
        "pays": "France",
        "loyer": 500.0,
        "montant_charges": 75.0,
        "statut": "disponible"
    }
    
    response = client.post("/api/logements/", json=logement_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["titre"] == "Appartement Complet"
    assert data["description"] == "Appartement avec tous les détails remplis"
    assert data["montant_charges"] == 75.0
    assert data["montant_total"] == 575.0  # loyer + charges
    assert data["pays"] == "France"

def test_create_logement_missing_required_fields(setup_database):
    """Test création logement avec champs obligatoires manquants"""
    logement_data = {
        "description": "Logement incomplet",
        "ville": "Test",
        "loyer": 400.0
        # Manque: titre, adresse, code_postal
    }
    
    response = client.post("/api/logements/", json=logement_data)
    
    assert response.status_code == 422  # Validation error

def test_filter_logements_by_ville(setup_database):
    """Test filtrage par ville"""
    # Créer des logements dans différentes villes
    logement1_data = {
        "titre": "Logement Paris",
        "adresse": "Rue Paris",
        "ville": "Paris",
        "code_postal": "75001",
        "pays": "France",
        "loyer": 800.0
    }
    client.post("/api/logements/", json=logement1_data)
    
    logement2_data = {
        "titre": "Logement Lyon", 
        "adresse": "Rue Lyon",
        "ville": "Lyon",
        "code_postal": "69000",
        "pays": "France",
        "loyer": 600.0
    }
    client.post("/api/logements/", json=logement2_data)
    
    # Filtrer par ville
    response = client.get("/api/logements/?ville=Lyon")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    for logement in data:
        assert "Lyon" in logement["ville"]