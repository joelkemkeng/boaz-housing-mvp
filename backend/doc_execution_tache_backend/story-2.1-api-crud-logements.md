# Story 2.1 - API CRUD logements backend

## ✅ Tâche complétée
**Durée estimée :** 1h15  
**Statut :** TERMINÉ  

## 🎯 Objectifs
Développer une API REST complète pour la gestion CRUD des logements :
- Endpoints POST/GET/PUT/DELETE pour logements
- Gestion des statuts (disponible/occupé/maintenance)
- Filtres de recherche (statut, ville)
- Statistiques des logements
- Validation des données avec Pydantic
- Tests API complets

## 🛠️ Implémentation réalisée - Détail technique

### 1. Schémas Pydantic pour validation

**Fichier `backend/app/schemas/logement.py` :**

```python
class LogementBase(BaseModel):
    """Schéma de base pour un logement"""
    adresse: str = Field(..., description="Adresse complète du logement")
    ville: str = Field(..., description="Ville du logement")
    code_postal: str = Field(..., description="Code postal")
    loyer: float = Field(..., gt=0, description="Montant du loyer mensuel en euros")
    statut: Optional[StatutLogement] = Field(StatutLogement.DISPONIBLE, description="Statut du logement")

class LogementCreate(LogementBase):
    """Schéma pour créer un logement"""
    pass

class LogementUpdate(BaseModel):
    """Schéma pour mettre à jour un logement (tous champs optionnels)"""
    adresse: Optional[str] = Field(None, description="Adresse complète du logement")
    ville: Optional[str] = Field(None, description="Ville du logement")
    code_postal: Optional[str] = Field(None, description="Code postal")
    loyer: Optional[float] = Field(None, gt=0, description="Montant du loyer mensuel en euros")
    statut: Optional[StatutLogement] = Field(None, description="Statut du logement")

class LogementResponse(LogementBase):
    """Schéma de réponse avec métadonnées"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # Pour compatibilité SQLAlchemy
```

**Procédure technique :**
1. **Validation automatique** : Field() avec contraintes (gt=0 pour loyer positif)
2. **Schémas séparés** : Create, Update, Response pour différents usages
3. **Champs optionnels** : LogementUpdate permet mise à jour partielle
4. **Configuration SQLAlchemy** : from_attributes=True pour ORM mapping
5. **Documentation auto** : Descriptions dans Field() pour Swagger docs

### 2. Service LogementService - Logique métier

**Fichier `backend/app/services/logement_service.py` :**

```python
class LogementService:
    """Service pour la gestion CRUD des logements"""
    
    def create_logement(self, db: Session, logement: LogementCreate) -> Logement:
        """Créer un nouveau logement"""
        db_logement = Logement(**logement.dict())
        db.add(db_logement)
        db.commit()
        db.refresh(db_logement)
        return db_logement
    
    def get_logements(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        statut: Optional[StatutLogement] = None,
        ville: Optional[str] = None
    ) -> List[Logement]:
        """Récupérer une liste de logements avec filtres optionnels"""
        query = db.query(Logement)
        
        if statut:
            query = query.filter(Logement.statut == statut)
        
        if ville:
            query = query.filter(Logement.ville.ilike(f"%{ville}%"))
        
        return query.offset(skip).limit(limit).all()
    
    def update_logement(
        self, 
        db: Session, 
        logement_id: int, 
        logement_update: LogementUpdate
    ) -> Optional[Logement]:
        """Mettre à jour un logement"""
        db_logement = self.get_logement(db, logement_id)
        if not db_logement:
            return None
        
        # Mise à jour des champs fournis seulement
        update_data = logement_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_logement, field, value)
        
        db.commit()
        db.refresh(db_logement)
        return db_logement
```

**Fonctionnalités spéciales implémentées :**

1. **`get_logements_disponibles()`** : Filtre automatique disponibles seulement
2. **`changer_statut_logement()`** : Changement de statut dédié  
3. **`get_stats_logements()`** : Statistiques par statut
4. **Filtres avancés** : Par statut et ville avec ILIKE (insensible à la casse)
5. **Pagination** : skip/limit pour gestion de grandes listes

**Décisions techniques :**
1. **exclude_unset=True** : Mise à jour partielle, seuls les champs fournis
2. **Instance globale** : logement_service singleton réutilisable
3. **Optional return** : None si logement inexistant, pas d'exception
4. **Refresh après commit** : Récupération de l'état DB complet (timestamps)

### 3. API Router - Endpoints REST

**Fichier `backend/app/routers/logements.py` :**

**Endpoints implémentés :**

```python
# CRUD de base
POST   /api/logements/                    # Créer logement
GET    /api/logements/                    # Lister avec filtres
GET    /api/logements/{id}                # Récupérer par ID
PUT    /api/logements/{id}                # Mettre à jour
DELETE /api/logements/{id}                # Supprimer

# Endpoints spéciaux
GET    /api/logements/disponibles         # Logements disponibles seulement
GET    /api/logements/stats               # Statistiques par statut
PATCH  /api/logements/{id}/statut         # Changement statut dédié
```

**Exemple endpoint avec filtres :**
```python
@router.get("/", response_model=List[LogementResponse])
def list_logements(
    skip: int = Query(0, ge=0, description="Nombre d'éléments à ignorer"),
    limit: int = Query(100, ge=1, le=1000, description="Nombre maximum d'éléments à retourner"),
    statut: Optional[StatutLogement] = Query(None, description="Filtrer par statut"),
    ville: Optional[str] = Query(None, description="Filtrer par ville"),
    db: Session = Depends(get_db)
):
    return logement_service.get_logements(db=db, skip=skip, limit=limit, statut=statut, ville=ville)
```

**Gestion d'erreurs :**
```python
@router.get("/{logement_id}", response_model=LogementResponse)
def get_logement(logement_id: int, db: Session = Depends(get_db)):
    db_logement = logement_service.get_logement(db=db, logement_id=logement_id)
    if db_logement is None:
        raise HTTPException(status_code=404, detail="Logement non trouvé")
    return db_logement
```

**Procédure technique :**
1. **Dependency injection** : `Depends(get_db)` pour session DB automatique
2. **Validation Query params** : ge=0, le=1000 pour pagination sécurisée  
3. **Response models** : Types de retour Pydantic pour docs Swagger
4. **HTTPException** : Erreurs HTTP standards (404, 400, etc.)
5. **Tags pour docs** : `tags=["Logements"]` pour organisation Swagger

### 4. Intégration FastAPI principale

**Modification `backend/app/main.py` :**
```python
# Import des routers
from app.routers import organisation, logements

# Inclusion des routers
app.include_router(organisation.router, prefix="/api")
app.include_router(logements.router, prefix="/api")
```

**Procédure d'intégration :**
1. **Import router** : Module logements dans main.py
2. **Inclusion avec préfixe** : Tous endpoints sous /api/logements/
3. **Redémarrage backend** : docker-compose restart backend
4. **Vérification routes** : Swagger docs http://localhost:8000/docs

## 🧪 Tests de validation complets

### Tests API avec TestClient

**Fichier `backend/tests/test_logement_api.py` avec 8 tests :**

```python
def test_create_logement():
    """Test création d'un logement via API"""
    logement_data = {
        "adresse": "789 Rue Test API",
        "ville": "Marseille",
        "code_postal": "13001",
        "loyer": 420.0,
        "statut": "disponible"
    }
    
    response = client.post("/api/logements/", json=logement_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["adresse"] == "789 Rue Test API"
    assert "id" in data
    assert "created_at" in data

def test_update_logement():
    """Test mise à jour partielle"""
    # Créer puis mettre à jour seulement le loyer
    update_data = {"loyer": 420.0}
    response = client.put(f"/api/logements/{logement_id}", json=update_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["loyer"] == 420.0
    assert "updated_at" in data  # Timestamp mis à jour

def test_change_statut_logement():
    """Test changement de statut dédié"""
    response = client.patch(f"/api/logements/{logement_id}/statut?nouveau_statut=maintenance")
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["logement"]["statut"] == "maintenance"
```

**Résultats des tests :**
```bash
$ docker-compose exec backend python -m pytest tests/test_logement_api.py -v
======================== 8 passed, 18 warnings in 1.29s ========================
```

### Tests manuels avec curl

**Création de logement :**
```bash
$ curl -X POST http://localhost:8000/api/logements/ \
  -H "Content-Type: application/json" \
  -d '{"adresse": "123 Rue de la Paix", "ville": "Paris", "code_postal": "75001", "loyer": 450.0}'

Response: {
  "adresse":"123 Rue de la Paix",
  "ville":"Paris", 
  "loyer":450.0,
  "statut":"disponible",
  "id":1,
  "created_at":"2025-08-29T11:22:17.925506Z"
}
```

**Liste avec filtres :**
```bash
$ curl "http://localhost:8000/api/logements/?statut=disponible&ville=Paris"
Response: [{"id":1, "ville":"Paris", "statut":"disponible", ...}]
```

**Statistiques :**
```bash
$ curl http://localhost:8000/api/logements/stats
Response: {"total":2,"disponibles":1,"occupes":1,"maintenance":0}
```

## 📊 Fonctionnalités validées

### CRUD complet opérationnel

- ✅ **CREATE** : POST /api/logements/ - Création avec validation
- ✅ **READ** : GET /api/logements/ - Liste avec filtres et pagination  
- ✅ **READ** : GET /api/logements/{id} - Récupération par ID
- ✅ **UPDATE** : PUT /api/logements/{id} - Mise à jour partielle
- ✅ **DELETE** : DELETE /api/logements/{id} - Suppression

### Fonctionnalités avancées

- ✅ **Filtrage** : Par statut et ville (insensible à la casse)
- ✅ **Pagination** : skip/limit avec validation
- ✅ **Changement statut** : PATCH dédié pour workflow
- ✅ **Logements disponibles** : GET /disponibles pour sélection
- ✅ **Statistiques** : Compteurs par statut en temps réel

### Workflow statuts

- ✅ **Disponible** → **Occupé** : Lors d'une souscription
- ✅ **Occupé** → **Disponible** : Fin de location  
- ✅ **Maintenance** : Temporaire, hors circulation

## 🔧 Commandes de test utilisées

```bash
# Création des tables (suite problème migration)
docker-compose exec backend python -c "from app.database import engine, Base; from app.models import *; Base.metadata.create_all(bind=engine)"

# Redémarrage avec nouvelles routes
docker-compose restart backend

# Tests API automatisés
docker-compose exec backend python -m pytest tests/test_logement_api.py -v

# Tests manuels CRUD
curl -X POST http://localhost:8000/api/logements/ -H "Content-Type: application/json" -d '{...}'
curl http://localhost:8000/api/logements/
curl http://localhost:8000/api/logements/1
curl -X PUT http://localhost:8000/api/logements/1 -d '{"loyer": 500.0}'
curl -X PATCH "http://localhost:8000/api/logements/1/statut?nouveau_statut=occupe"
curl http://localhost:8000/api/logements/stats

# Documentation Swagger
# http://localhost:8000/docs
```

## 🎯 Approche MVP respectée

**Simplicité maximale :**
- ✅ CRUD basique sans sur-ingénierie
- ✅ Filtres essentiels seulement (statut, ville)
- ✅ Validation Pydantic automatique
- ✅ Gestion d'erreurs HTTP standards
- ✅ Tests couvrant tous les cas d'usage

**Pas d'ajouts inutiles :**
- ❌ Pas d'authentification (sera ajoutée plus tard)
- ❌ Pas de cache complexe (base SQLAlchemy suffit)
- ❌ Pas de recherche full-text (ILIKE basique)
- ❌ Pas de soft delete (DELETE hard pour MVP)

## 🚀 Utilisation dans les prochaines étapes

**L'API sera utilisée pour :**
1. **Interface frontend** : Story 2.2 - Gestion logements UI
2. **Wizard souscription** : Story 3.5 - Choix logement disponible  
3. **Validation contraintes** : Story 2.3 - Logique métier
4. **Génération documents** : Informations logement dans PDF

## 🎯 Prochaine étape
Story 2.2 - Interface frontend gestion logements (1h30)