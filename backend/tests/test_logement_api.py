import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.database import SessionLocal, engine, Base
from app.models.logement import StatutLogement

client = TestClient(app)

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

def test_create_logement():
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

def test_get_logements():
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

def test_get_logement_by_id():
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

def test_update_logement():
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

def test_change_statut_logement():
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

def test_get_stats_logements():
    """Test récupération des statistiques"""
    response = client.get("/api/logements/stats")
    
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "disponibles" in data
    assert "occupes" in data
    assert "maintenance" in data

def test_get_logement_not_found():
    """Test récupération logement inexistant"""
    response = client.get("/api/logements/99999")
    
    assert response.status_code == 404
    assert "non trouvé" in response.json()["detail"]

def test_delete_logement():
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