# Story 1.2 - Création des Modèles de Base de Données (Backend)

## Vue d'ensemble
Création de l'architecture de données pour l'application Boaz Housing avec SQLAlchemy et FastAPI.

## Technologies utilisées
- **SQLAlchemy 2.x** - ORM Python
- **PostgreSQL** - Base de données principale
- **Alembic** - Migrations de schéma
- **FastAPI** - Framework API avec support auto-docs

## Architecture de données

### Base de données : `app/database.py`
```python
from sqlalchemy import create_database_url
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://boaz_user:boaz_pass@boaz-postgres:5432/boaz_housing"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

### Modèle Organisation : `app/models/organisation.py`
**Données statiques de l'entreprise Boaz-Housing**

#### Structure
```python
class Organisation(Base):
    __tablename__ = "organisations"
    
    # Identité de l'entreprise
    nom: str = "Boaz-Housing"
    description: str = "Spécialiste du logement étudiant"
    
    # Informations CEO
    ceo_nom: str = "Joseph Boaz TIEMENI"
    ceo_poste: str = "CEO & Fondateur"
    ceo_bio: str = "Expertise immobilière étudiante"
    
    # Contact professionnel
    telephone_principal: str = "+33 7 68 78 77 68"
    telephone_whatsapp: str = "+33 7 68 78 77 68"  
    email: str = "contact@boaz-housing.com"
    site_web: str = "https://boaz-housing.com"
    
    # Adresse physique
    adresse: str = "123 Avenue des Étudiants"
    ville: str = "Paris"
    code_postal: str = "75001"
    pays: str = "France"
```

#### Services
- `get_organisation_info()` - Informations générales
- `get_ceo_info()` - Données dirigeant
- `get_contact_info()` - Coordonnées
- `generate_reference()` - Codes référence uniques

### Modèle Logement : `app/models/logement.py`
**Gestion du parc immobilier**

#### Structure évoluée
```python
class StatutLogement(str, enum.Enum):
    DISPONIBLE = "disponible"
    OCCUPE = "occupe" 
    MAINTENANCE = "maintenance"

class Logement(Base):
    __tablename__ = "logements"
    
    # Identifiant
    id: int (PK, auto-increment)
    
    # Informations descriptives
    titre: str(200) NOT NULL                    # "Appartement T2 lumineux"
    description: Text NULLABLE                  # Description détaillée
    adresse: str(500) NOT NULL                  # Adresse complète
    ville: str(100) NOT NULL                    # Ville (format validé)
    code_postal: str(20) NOT NULL               # Code postal (multi-format)
    pays: str(100) NOT NULL DEFAULT 'France'   # Pays supporté
    
    # Tarification
    loyer: float NOT NULL                       # Prix base mensuel
    montant_charges: float NOT NULL DEFAULT 0.0 # Charges mensuelles
    montant_total: float NOT NULL              # Calculé automatiquement
    
    # État et suivi
    statut: StatutLogement DEFAULT 'disponible'
    created_at: datetime(timezone=True) 
    updated_at: datetime(timezone=True)
```

#### Contraintes de données
```sql
-- Contraintes financières
CHECK (loyer > 0)
CHECK (montant_charges >= 0) 
CHECK (montant_total > 0)
CHECK (montant_total = loyer + montant_charges)

-- Contraintes de format
CHECK (trim(titre) != '')
CHECK (trim(adresse) != '')
CHECK (trim(ville) != '')
CHECK (trim(code_postal) != '')

-- Index pour performance
CREATE INDEX idx_logement_statut ON logements(statut);
CREATE INDEX idx_logement_ville ON logements(ville);
CREATE UNIQUE INDEX idx_logement_adresse_ville ON logements(adresse, ville);
```

#### Validateurs SQLAlchemy
```python
@validates('titre', 'adresse', 'ville')
def validate_required_fields(self, key, value):
    """Validation champs obligatoires non vides"""
    
@validates('ville') 
def validate_ville_format(self, key, ville):
    """Validation format ville : lettres/espaces/tirets/apostrophes"""
    
@validates('code_postal')
def validate_code_postal_format(self, key, code_postal):
    """Validation codes postaux internationaux"""
    
@validates('pays')
def validate_pays_supported(self, key, pays):
    """Validation pays dans liste supportée"""
    
@validates('loyer', 'montant_charges')
def validate_financial_amounts(self, key, montant):
    """Validation montants dans fourchettes acceptables"""
```

## Configuration Docker

### Base de données PostgreSQL
```yaml
# docker-compose.yml
boaz-postgres:
  image: postgres:15
  environment:
    POSTGRES_DB: boaz_housing
    POSTGRES_USER: boaz_user
    POSTGRES_PASSWORD: boaz_pass
  volumes:
    - postgres_data:/var/lib/postgresql/data
  ports:
    - "5432:5432"
```

### PgAdmin (Administration)
```yaml
boaz-pgadmin:
  image: dpage/pgadmin4
  environment:
    PGADMIN_DEFAULT_EMAIL: admin@boaz-housing.com
    PGADMIN_DEFAULT_PASSWORD: boaz_admin
  ports:
    - "8080:80"
```

## Migrations Alembic

### Configuration
```python
# alembic/env.py
from app.models import Base
target_metadata = Base.metadata

# Génération migration
alembic revision --autogenerate -m "Create logements and organisations tables"

# Application migration  
alembic upgrade head
```

### Scripts de migration générés
```sql
-- Création table organisations
CREATE TABLE organisations (
    id SERIAL PRIMARY KEY,
    nom VARCHAR NOT NULL,
    ceo_nom VARCHAR NOT NULL,
    telephone_principal VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    -- ... autres champs
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Création table logements avec contraintes
CREATE TABLE logements (
    id SERIAL PRIMARY KEY,
    titre VARCHAR(200) NOT NULL,
    description TEXT,
    adresse VARCHAR(500) NOT NULL,
    ville VARCHAR(100) NOT NULL, 
    code_postal VARCHAR(20) NOT NULL,
    pays VARCHAR(100) NOT NULL DEFAULT 'France',
    loyer DOUBLE PRECISION NOT NULL,
    montant_charges DOUBLE PRECISION NOT NULL DEFAULT 0.0,
    montant_total DOUBLE PRECISION NOT NULL,
    statut statutlogement NOT NULL DEFAULT 'disponible',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,
    
    -- Contraintes
    CONSTRAINT check_loyer_positive CHECK (loyer > 0),
    CONSTRAINT check_charges_positive_ou_nulle CHECK (montant_charges >= 0),
    CONSTRAINT check_montant_total_positive CHECK (montant_total > 0),
    CONSTRAINT check_coherence_montant_total CHECK (montant_total = loyer + montant_charges),
    CONSTRAINT check_titre_non_vide CHECK (trim(titre) != ''),
    CONSTRAINT check_adresse_non_vide CHECK (trim(adresse) != ''),
    CONSTRAINT check_ville_non_vide CHECK (trim(ville) != ''),
    CONSTRAINT check_code_postal_non_vide CHECK (trim(code_postal) != '')
);

-- Index pour performance
CREATE INDEX idx_logement_statut ON logements(statut);
CREATE INDEX idx_logement_ville ON logements(ville);
CREATE UNIQUE INDEX idx_logement_adresse_ville ON logements(adresse, ville);
```

## Données de test et seed

### Script de données initiales
```python
# scripts/seed_data.py
def seed_organisation_data(db: Session):
    """Insertion données organisation Boaz-Housing"""
    
def seed_logements_test(db: Session):
    """Création logements de test pour développement"""
    
# Logements de test créés
- Appartement T2 Paris (1200€ + 200€ charges)
- Studio Lyon (800€ + 150€ charges)  
- T3 Marseille (1000€ + 180€ charges)
- T1 Toulouse (700€ + 120€ charges)
- T4 Bordeaux (1500€ + 250€ charges)
```

## Intégration FastAPI

### Configuration des modèles
```python
# app/main.py
from app.models import Base
from app.database import engine

# Création des tables au démarrage
Base.metadata.create_all(bind=engine)

# Injection de dépendance session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Health check base de données
```python
@app.get("/health")
def health_check():
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}
```

## Performance et optimisation

### Index de performance
- **Statut logement** : Filtrage rapide par disponibilité
- **Ville** : Recherche géographique optimisée  
- **Adresse + Ville** : Contrainte unicité avec performance

### Pool de connexions
```python
engine = create_engine(
    DATABASE_URL,
    pool_size=20,           # Connexions simultanées
    max_overflow=0,         # Pas de dépassement
    pool_pre_ping=True,     # Vérification connexion
    pool_recycle=3600       # Recyclage toutes les heures
)
```

### Monitoring SQL
- **Logging requêtes** : `echo=True` en développement
- **Métriques performance** : Durée des requêtes
- **Analyse plans** : EXPLAIN pour requêtes complexes

## Sécurité

### Protection des données
- **Pas de données sensibles** : Pas de mots de passe en BDD
- **Validation stricte** : Contraintes SQL + validateurs Python
- **Échappement automatique** : SQLAlchemy ORM

### Sauvegarde et récupération
- **Volumes Docker** : Persistance des données
- **Scripts backup** : Dump automatique PostgreSQL
- **Restauration** : Procédures de récupération documentées

## Tests et validation

### Tests unitaires modèles
```python
def test_logement_creation():
    """Test création logement valide"""
    
def test_logement_validation():
    """Test validations contraintes"""
    
def test_organisation_data():
    """Test données organisation"""
```

### Tests d'intégration
- ✅ **Connexion DB** : Établissement connexion PostgreSQL
- ✅ **Création tables** : Génération schéma complet
- ✅ **Contraintes SQL** : Validation règles métier
- ✅ **Index performance** : Vérification requêtes rapides
- ✅ **Données seed** : Insertion données de test

## Conclusion

La Story 1.2 établit une **foundation robuste** pour l'application Boaz Housing :

### ✅ **Architecture solide**
- Modèles SQLAlchemy bien structurés
- Contraintes de données strictes
- Performance optimisée avec index

### ✅ **Données métier**
- Modèle Organisation pour l'identité entreprise
- Modèle Logement évolutif et extensible
- Validation multi-niveau (SQL + Python)

### ✅ **Infrastructure prête**
- Base PostgreSQL configurée
- Migrations Alembic opérationnelles  
- Intégration FastAPI complète

La base de données est maintenant prête pour supporter toutes les fonctionnalités de l'application de gestion immobilière.