# Story 2.1 - API CRUD Logements Backend (1h15)

## Vue d'ensemble
Développement de l'API REST complète pour la gestion CRUD des logements avec FastAPI, incluant les endpoints, services, et schémas Pydantic.

## Architecture API

### Structure backend
```
app/
├── routers/
│   └── logements.py          # Endpoints REST
├── services/  
│   └── logement_service.py   # Logique métier
├── schemas/
│   └── logement.py           # Modèles Pydantic
├── models/
│   └── logement.py           # Modèles SQLAlchemy
└── database.py               # Configuration DB
```

## Endpoints REST

### Fichier : `app/routers/logements.py`

#### Configuration du routeur
```python
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

router = APIRouter(prefix="/logements", tags=["Logements"])
```

#### Endpoints CRUD complets

##### 1. Création de logement
```python
@router.post("/", response_model=LogementResponse)
def create_logement(
    logement: LogementCreate,
    db: Session = Depends(get_db)
):
    """Créer un nouveau logement"""
    try:
        return logement_service.create_logement(db=db, logement=logement)
    except LogementException as e:
        raise convert_to_http_exception(e)
```

**Requête :**
```bash
POST /api/logements/
Content-Type: application/json

{
    "titre": "Appartement T2 lumineux",
    "description": "Proche université, balcon",
    "adresse": "15 rue de la Paix", 
    "ville": "Paris",
    "code_postal": "75001",
    "pays": "France",
    "loyer": 1000.0,
    "montant_charges": 150.0,
    "statut": "disponible"
}
```

**Réponse :**
```json
{
    "id": 1,
    "titre": "Appartement T2 lumineux",
    "description": "Proche université, balcon",
    "adresse": "15 rue de la Paix",
    "ville": "Paris", 
    "code_postal": "75001",
    "pays": "France",
    "loyer": 1000.0,
    "montant_charges": 150.0,
    "montant_total": 1150.0,
    "statut": "disponible",
    "created_at": "2025-08-29T10:30:00Z",
    "updated_at": null
}
```

##### 2. Liste des logements avec filtres
```python
@router.get("/", response_model=List[LogementResponse])
def list_logements(
    skip: int = Query(0, ge=0, description="Nombre d'éléments à ignorer"),
    limit: int = Query(100, ge=1, le=1000, description="Nombre maximum d'éléments à retourner"),
    statut: Optional[StatutLogement] = Query(None, description="Filtrer par statut"),
    ville: Optional[str] = Query(None, description="Filtrer par ville"),
    db: Session = Depends(get_db)
):
    """Récupérer la liste des logements avec filtres optionnels"""
    return logement_service.get_logements(
        db=db, skip=skip, limit=limit, statut=statut, ville=ville
    )
```

**Exemples d'utilisation :**
```bash
# Tous les logements (paginé)
GET /api/logements/?skip=0&limit=20

# Logements disponibles à Paris  
GET /api/logements/?statut=disponible&ville=Paris

# Recherche par ville avec pagination
GET /api/logements/?ville=Lyon&skip=20&limit=10
```

##### 3. Récupération d'un logement
```python
@router.get("/{logement_id}", response_model=LogementResponse)
def get_logement(
    logement_id: int,
    db: Session = Depends(get_db)
):
    """Récupérer un logement par son ID"""
    try:
        db_logement = logement_service.get_logement(db=db, logement_id=logement_id)
        if db_logement is None:
            raise HTTPException(status_code=404, detail="Logement non trouvé")
        return db_logement
    except LogementException as e:
        raise convert_to_http_exception(e)
```

##### 4. Modification de logement
```python
@router.put("/{logement_id}", response_model=LogementResponse)
def update_logement(
    logement_id: int,
    logement_update: LogementUpdate,
    db: Session = Depends(get_db)
):
    """Mettre à jour un logement"""
    try:
        return logement_service.update_logement(
            db=db, logement_id=logement_id, logement_update=logement_update
        )
    except LogementException as e:
        raise convert_to_http_exception(e)
```

##### 5. Suppression de logement
```python
@router.delete("/{logement_id}")
def delete_logement(
    logement_id: int,
    db: Session = Depends(get_db)
):
    """Supprimer un logement"""
    success = logement_service.delete_logement(db=db, logement_id=logement_id)
    if not success:
        raise HTTPException(status_code=404, detail="Logement non trouvé")
    return {"message": "Logement supprimé avec succès"}
```

#### Endpoints spécialisés

##### 6. Logements disponibles
```python
@router.get("/disponibles", response_model=List[LogementResponse])
def list_logements_disponibles(db: Session = Depends(get_db)):
    """Récupérer tous les logements disponibles"""
    return logement_service.get_logements_disponibles(db=db)
```

##### 7. Statistiques des logements
```python
@router.get("/stats")
def get_stats_logements(db: Session = Depends(get_db)):
    """Obtenir les statistiques des logements"""
    return logement_service.get_stats_logements(db=db)
```

**Réponse statistiques :**
```json
{
    "total": 25,
    "disponibles": 12,
    "occupes": 10,
    "maintenance": 3
}
```

##### 8. Changement de statut
```python
@router.patch("/{logement_id}/statut")
def changer_statut_logement(
    logement_id: int,
    nouveau_statut: StatutLogement,
    db: Session = Depends(get_db)
):
    """Changer le statut d'un logement"""
    try:
        db_logement = logement_service.changer_statut_logement(
            db=db, logement_id=logement_id, nouveau_statut=nouveau_statut
        )
        return {
            "message": f"Statut changé vers {nouveau_statut.value}", 
            "logement": db_logement
        }
    except LogementException as e:
        raise convert_to_http_exception(e)
```

## Schémas Pydantic

### Fichier : `app/schemas/logement.py`

#### Schéma de base
```python
from pydantic import BaseModel, Field, field_validator, model_validator

class LogementBase(BaseModel):
    """Schéma de base pour un logement"""
    titre: str = Field(..., min_length=3, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    adresse: str = Field(..., min_length=5, max_length=500)
    ville: str = Field(..., min_length=2, max_length=100)
    code_postal: str = Field(..., min_length=4, max_length=20)
    pays: str = Field("France", max_length=100)
    loyer: float = Field(..., gt=0, le=50000)
    montant_charges: float = Field(0.0, ge=0, le=10000)
    statut: Optional[StatutLogement] = Field(StatutLogement.DISPONIBLE)
    
    @field_validator('ville')
    @classmethod
    def validate_ville(cls, v: str) -> str:
        """Validation format ville avec regex"""
        
    @field_validator('code_postal')
    @classmethod
    def validate_code_postal(cls, v: str) -> str:
        """Validation codes postaux internationaux"""
        
    @model_validator(mode='after')
    def validate_coherence_prix(self) -> 'LogementBase':
        """Validation cohérence des prix"""
```

#### Schémas spécialisés
```python
class LogementCreate(LogementBase):
    """Schéma pour créer un logement"""
    pass

class LogementUpdate(BaseModel):
    """Schéma pour mettre à jour un logement (tous champs optionnels)"""
    titre: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    adresse: Optional[str] = None
    ville: Optional[str] = None
    code_postal: Optional[str] = None
    pays: Optional[str] = None
    loyer: Optional[float] = Field(None, gt=0)
    montant_charges: Optional[float] = Field(None, ge=0)
    statut: Optional[StatutLogement] = None

class LogementResponse(LogementBase):
    """Schéma de réponse pour un logement"""
    id: int
    montant_total: float = Field(..., description="Montant total (loyer + charges)")
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
```

## Service métier

### Fichier : `app/services/logement_service.py`

#### Classe de service avec règles métier
```python
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from datetime import datetime, timedelta

class LogementService:
    """Service pour la gestion CRUD des logements"""
    
    # Règles métier configurables
    LOYER_MIN = 50.0
    LOYER_MAX = 50000.0
    CHARGES_MAX = 10000.0
    MONTANT_TOTAL_MAX = 60000.0
    DELAI_MIN_CHANGEMENT_STATUT = 1  # heures
```

#### Méthodes CRUD avec validations
```python
def create_logement(self, db: Session, logement: LogementCreate) -> Logement:
    """Créer un nouveau logement avec validations métier"""
    try:
        logement_data = logement.dict()
        
        # Validation des règles métier
        self._validate_business_rules(logement_data)
        
        # Vérification des doublons
        self._check_duplicate_logement(db, logement_data['adresse'], logement_data['ville'])
        
        # Calcul automatique du montant total
        logement_data['montant_total'] = logement_data['loyer'] + logement_data.get('montant_charges', 0.0)
        
        db_logement = Logement(**logement_data)
        db.add(db_logement)
        db.commit()
        db.refresh(db_logement)
        return db_logement
        
    except IntegrityError as e:
        db.rollback()
        raise LogementValidationError("Données invalides: contrainte de base de données violée")

def get_logements(
    self, 
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    statut: Optional[StatutLogement] = None,
    ville: Optional[str] = None
) -> List[Logement]:
    """Récupérer une liste de logements avec filtres"""
    query = db.query(Logement)
    
    # Filtrage par statut
    if statut:
        query = query.filter(Logement.statut == statut)
    
    # Filtrage par ville (recherche partielle)
    if ville:
        query = query.filter(Logement.ville.ilike(f"%{ville}%"))
    
    # Tri par date de modification (plus récent en premier)
    query = query.order_by(
        Logement.updated_at.desc().nulls_last(),
        Logement.created_at.desc()
    )
    
    return query.offset(skip).limit(limit).all()

def update_logement(
    self, 
    db: Session, 
    logement_id: int, 
    logement_update: LogementUpdate
) -> Logement:
    """Mettre à jour un logement avec validations métier"""
    try:
        db_logement = self.get_logement(db, logement_id)
        if not db_logement:
            raise LogementNotFoundError(logement_id)
        
        update_data = logement_update.dict(exclude_unset=True)
        
        if not update_data:
            raise LogementValidationError("Aucune donnée fournie pour la mise à jour")
        
        # Validation des nouvelles valeurs
        validation_data = {
            'loyer': update_data.get('loyer', db_logement.loyer),
            'montant_charges': update_data.get('montant_charges', db_logement.montant_charges)
        }
        self._validate_business_rules(validation_data)
        
        # Vérification anti-doublon si adresse/ville changée
        if 'adresse' in update_data or 'ville' in update_data:
            new_adresse = update_data.get('adresse', db_logement.adresse)
            new_ville = update_data.get('ville', db_logement.ville)
            self._check_duplicate_logement(db, new_adresse, new_ville, exclude_id=logement_id)
        
        # Application des modifications
        for field, value in update_data.items():
            setattr(db_logement, field, value)
        
        # Recalcul du montant total si nécessaire
        if 'loyer' in update_data or 'montant_charges' in update_data:
            db_logement.montant_total = db_logement.loyer + db_logement.montant_charges
        
        db.commit()
        db.refresh(db_logement)
        return db_logement
        
    except IntegrityError as e:
        db.rollback()
        raise LogementValidationError("Erreur d'intégrité des données")
```

#### Méthodes spécialisées
```python
def get_logements_disponibles(self, db: Session) -> List[Logement]:
    """Récupérer tous les logements disponibles"""
    return self.get_logements(db, statut=StatutLogement.DISPONIBLE)

def changer_statut_logement(
    self, 
    db: Session, 
    logement_id: int, 
    nouveau_statut: StatutLogement
) -> Logement:
    """Changer le statut d'un logement avec validations métier"""
    db_logement = self.get_logement(db, logement_id)
    if not db_logement:
        raise LogementNotFoundError(logement_id)
    
    # Validation des règles de changement
    self._validate_statut_change(db_logement, nouveau_statut)
    
    db_logement.statut = nouveau_statut
    db.commit()
    db.refresh(db_logement)
    return db_logement

def get_stats_logements(self, db: Session) -> dict:
    """Obtenir les statistiques des logements"""
    total = db.query(Logement).count()
    disponibles = db.query(Logement).filter(Logement.statut == StatutLogement.DISPONIBLE).count()
    occupes = db.query(Logement).filter(Logement.statut == StatutLogement.OCCUPE).count()
    maintenance = db.query(Logement).filter(Logement.statut == StatutLogement.MAINTENANCE).count()
    
    return {
        "total": total,
        "disponibles": disponibles,
        "occupes": occupes,
        "maintenance": maintenance
    }

# Instance globale du service
logement_service = LogementService()
```

## Intégration FastAPI

### Configuration du routeur principal
```python
# app/main.py
from fastapi import FastAPI
from app.routers import logements

app = FastAPI(
    title="Boaz Housing API",
    description="API pour la gestion des logements et souscriptions Boaz Housing",
    version="1.0.0"
)

# Inclusion du routeur logements
app.include_router(logements.router, prefix="/api", tags=["Logements"])
```

### Documentation automatique
- **Swagger UI** : `http://localhost:8000/docs`
- **ReDoc** : `http://localhost:8000/redoc`
- **OpenAPI Schema** : `http://localhost:8000/openapi.json`

### Middleware et configuration
```python
from fastapi.middleware.cors import CORSMiddleware

# CORS pour le frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Gestion d'erreurs

### Exceptions personnalisées
```python
# app/exceptions/logement_exceptions.py
class LogementException(Exception):
    """Exception de base pour les logements"""

class LogementValidationError(LogementException):
    """Erreur de validation des données"""

class LogementBusinessRuleError(LogementException):
    """Erreur de règle métier"""

class LogementNotFoundError(LogementException):
    """Logement non trouvé"""

class LogementStatutError(LogementException):
    """Erreur liée au changement de statut"""
```

### Conversion vers HTTPException
```python
def convert_to_http_exception(exc: LogementException) -> HTTPException:
    """Convertir une exception métier en HTTPException FastAPI"""
    if isinstance(exc, LogementValidationError):
        return HTTPException(status_code=422, detail={
            "type": "validation_error",
            "message": exc.message
        })
    elif isinstance(exc, LogementBusinessRuleError):
        return HTTPException(status_code=400, detail={
            "type": "business_rule_error", 
            "message": exc.message
        })
    # ... autres types d'erreurs
```

## Tests API

### Tests unitaires des services
```python
def test_create_logement_valid():
    """Test création logement valide"""
    
def test_create_logement_loyer_trop_bas():
    """Test validation loyer minimum"""
    
def test_get_logements_with_filters():
    """Test filtrage par statut et ville"""
    
def test_update_logement_partial():
    """Test mise à jour partielle"""
    
def test_changement_statut_valide():
    """Test changement de statut autorisé"""
    
def test_changement_statut_interdit():
    """Test transition interdite"""
```

### Tests d'intégration API
```bash
# Création logement
curl -X POST "http://localhost:8000/api/logements/" \
  -H "Content-Type: application/json" \
  -d '{"titre":"Test","adresse":"123 rue Test","ville":"Paris","code_postal":"75001","loyer":1000}'

# Liste avec filtres  
curl "http://localhost:8000/api/logements/?statut=disponible&ville=Paris"

# Modification
curl -X PUT "http://localhost:8000/api/logements/1" \
  -H "Content-Type: application/json" \
  -d '{"loyer":1200}'

# Changement statut
curl -X PATCH "http://localhost:8000/api/logements/1/statut?nouveau_statut=occupe"

# Statistiques
curl "http://localhost:8000/api/logements/stats"
```

## Performance et optimisation

### Requêtes optimisées
- **Index sur statut et ville** : Filtrage rapide
- **Pagination** : Limitation des résultats via `skip`/`limit`
- **Tri intelligent** : Par date de modification DESC

### Cache et résilience
- **Pool de connexions** : Gestion optimale des connexions DB
- **Retry logic** : Nouvelle tentative sur erreurs temporaires
- **Timeout** : Limitation du temps de réponse

## Monitoring et observabilité

### Logging structuré
```python
import logging

logger = logging.getLogger(__name__)

@router.post("/")
def create_logement(...):
    logger.info(f"Création logement: {logement.titre} à {logement.ville}")
    try:
        result = logement_service.create_logement(db=db, logement=logement)
        logger.info(f"Logement créé avec ID: {result.id}")
        return result
    except Exception as e:
        logger.error(f"Erreur création logement: {str(e)}")
        raise
```

### Métriques
- **Temps de réponse** par endpoint
- **Nombre de requêtes** par statut HTTP
- **Erreurs** par type d'exception

## Conclusion

La Story 2.1 livre une **API REST complète et robuste** pour la gestion des logements :

### ✅ **Endpoints CRUD complets**
- Création, lecture, mise à jour, suppression
- Filtrage avancé et pagination
- Actions spécialisées (statut, statistiques)

### ✅ **Architecture solide**
- Services métier avec règles business
- Schémas Pydantic avec validations
- Gestion d'erreurs structurée

### ✅ **Qualité professionnelle**
- Documentation automatique OpenAPI
- Tests unitaires et d'intégration
- Performance optimisée

L'API est maintenant prête pour l'intégration frontend et la mise en production.