# Story 1.2 - Création des modèles de base de données

## ✅ Tâche complétée
**Durée estimée :** 1h15  
**Statut :** TERMINÉ  

## 🎯 Objectifs
Création des modèles de données essentiels pour un MVP fonctionnel :
- Modèle `Logement` pour les propriétés immobilières
- Modèle `Client` pour les informations des étudiants  
- Modèle `Souscription` pour lier client-logement avec workflow
- Configuration SQLAlchemy + Alembic pour les migrations
- Tests de validation des modèles

## 🛠️ Implémentation réalisée - Détail technique

### 1. Configuration base de données SQLAlchemy

**Création du fichier `backend/app/database.py` :**
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:admin@boaz-postgres:5432/boaz_housing_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Procédure technique :**
1. Configuration de l'engine SQLAlchemy avec PostgreSQL
2. Session factory pour les opérations de base de données
3. Base declarative pour définir les modèles
4. Fonction generator `get_db()` pour injection de dépendance FastAPI
5. Chargement URL depuis variable d'environnement avec fallback

### 2. Modèle Logement - Structure simple

**Fichier `backend/app/models/logement.py` :**
```python
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
from sqlalchemy.sql import func
from app.database import Base
import enum

class StatutLogement(str, enum.Enum):
    DISPONIBLE = "disponible"
    OCCUPE = "occupe" 
    MAINTENANCE = "maintenance"

class Logement(Base):
    __tablename__ = "logements"
    
    id = Column(Integer, primary_key=True, index=True)
    adresse = Column(String, nullable=False)
    ville = Column(String, nullable=False)
    code_postal = Column(String, nullable=False)
    loyer = Column(Float, nullable=False)
    statut = Column(Enum(StatutLogement), default=StatutLogement.DISPONIBLE)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

**Décisions techniques :**
1. **Enum pour statut** : Contraint les valeurs possibles (disponible/occupé/maintenance)
2. **Champs essentiels seulement** : Adresse, ville, code postal, loyer pour MVP
3. **Timestamps automatiques** : `created_at` avec server_default, `updated_at` avec onupdate
4. **Index sur clé primaire** : Pour optimiser les requêtes

### 3. Modèle Client - Informations étudiants

**Fichier `backend/app/models/client.py` :**
```python
class Client(Base):
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Informations personnelles  
    nom_complet = Column(String, nullable=False)
    date_naissance = Column(Date, nullable=False)
    ville_naissance = Column(String, nullable=False)
    pays_naissance = Column(String, nullable=False)
    
    # Informations de contact
    email = Column(String, nullable=False, unique=True, index=True)
    telephone = Column(String, nullable=False)
    
    # Informations académiques
    etablissement = Column(String, nullable=False)
    niveau_etude = Column(String, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

**Décisions techniques :**
1. **Email unique avec index** : Contrainte d'unicité + index pour performance
2. **Champs obligatoires** : Tous les champs nécessaires pour génération documents
3. **Séparation logique** : Groupement par catégorie (personnel, contact, académique)
4. **Types appropriés** : `Date` pour date_naissance, `String` pour le reste

### 4. Modèle Souscription - Lien client-logement

**Fichier `backend/app/models/souscription.py` :**
```python
class StatutSouscription(str, enum.Enum):
    ATTENTE_PAIEMENT = "attente_paiement"
    PAYE = "paye"
    LIVRE = "livre" 
    CLOTURE = "cloture"

class Souscription(Base):
    __tablename__ = "souscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Relations (Foreign Keys)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    logement_id = Column(Integer, ForeignKey("logements.id"), nullable=False)
    
    # Informations souscription
    date_entree = Column(Date, nullable=False)
    duree_location = Column(Integer, nullable=False)  # en mois
    statut = Column(Enum(StatutSouscription), default=StatutSouscription.ATTENTE_PAIEMENT)
    
    # Référence unique pour documents
    reference = Column(String, nullable=False, unique=True, index=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations SQLAlchemy
    client = relationship("Client", backref="souscriptions")
    logement = relationship("Logement", backref="souscriptions")
```

**Décisions techniques :**
1. **Workflow enum** : États métier (attente_paiement → payé → livré → clôturé)
2. **Foreign Keys** : Liaison avec Client et Logement
3. **Référence unique** : Pour identifier documents (ex: ATT-D28B8C5877C1CA25)
4. **Relationships bidirectionnelles** : Navigation client.souscriptions et logement.souscriptions
5. **Durée en mois** : Integer simple pour MVP

### 5. Configuration Alembic pour migrations

**Modification `backend/alembic/env.py` :**
```python
# Import des modèles pour autogenerate
import sys
sys.path.append('/app')

from app.database import Base
from app.models import Logement, Client, Souscription
target_metadata = Base.metadata
```

**Migration manuelle `001_create_initial_tables.py` :**
```python
def upgrade() -> None:
    # Création table clients avec contraintes
    op.create_table('clients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nom_complet', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    # ... autres colonnes
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_clients_email'), 'clients', ['email'], unique=True)
    
    # Création table logements avec enum
    op.create_table('logements',
    sa.Column('statut', sa.Enum('DISPONIBLE', 'OCCUPE', 'MAINTENANCE', name='statutlogement'), nullable=True),
    # ... autres colonnes
    )
    
    # Création table souscriptions avec foreign keys
    op.create_table('souscriptions',
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.Column('logement_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ),
    sa.ForeignKeyConstraint(['logement_id'], ['logements.id'], ),
    # ... autres colonnes
    )
```

**Procédure de migration :**
1. **Création manuelle migration** : Contournement problème permissions Docker
2. **Application migration** : `alembic upgrade head` 
3. **Vérification état** : `alembic current` retourne "001 (head)"

## 🧪 Tests de validation

**Fichier `backend/tests/test_models.py` avec 3 tests :**

```python
def test_create_logement(db_session: Session):
    """Test création d'un logement"""
    logement = Logement(
        adresse="123 Rue Test",
        ville="Paris", 
        code_postal="75001",
        loyer=450.0,
        statut=StatutLogement.DISPONIBLE
    )
    
    db_session.add(logement)
    db_session.commit()
    
    assert logement.id is not None
    assert logement.adresse == "123 Rue Test"
    assert logement.loyer == 450.0

def test_create_client(db_session: Session):
    """Test création d'un client"""
    client = Client(
        nom_complet="Jean Dupont",
        date_naissance=date(1995, 5, 15),
        email="jean.dupont@email.com",
        # ... autres champs
    )
    
    db_session.add(client)
    db_session.commit()
    
    assert client.id is not None
    assert client.email == "jean.dupont@email.com"

def test_create_souscription(db_session: Session):
    """Test création souscription avec relations"""
    # Création logement + client
    # Puis souscription avec foreign keys
    # Vérification relations bidirectionnelles
```

**Résultats des tests :**
```bash
$ docker-compose exec backend python -m pytest tests/test_models.py -v
========================= 3 passed, 3 warnings in 0.48s =========================
```

## 📊 Structure base de données créée

**Tables générées :**
- ✅ `clients` - 11 colonnes (id, nom_complet, email, etc.)
- ✅ `logements` - 8 colonnes (id, adresse, ville, loyer, etc.)  
- ✅ `souscriptions` - 9 colonnes (id, client_id, logement_id, etc.)
- ✅ `alembic_version` - Table de versioning Alembic

**Index créés automatiquement :**
- `ix_clients_id`, `ix_clients_email` (unique)
- `ix_logements_id`
- `ix_souscriptions_id`, `ix_souscriptions_reference` (unique)

**Types Enum PostgreSQL :**
- `statutlogement` : (DISPONIBLE, OCCUPE, MAINTENANCE)
- `statutsouscription` : (ATTENTE_PAIEMENT, PAYE, LIVRE, CLOTURE)

## 🔧 Commandes utilisées

```bash
# Génération migration (fallback manuel à cause permissions)
docker-compose exec backend alembic revision --autogenerate -m "Create initial tables"

# Application migration
docker-compose exec backend alembic upgrade head

# Vérification état migration
docker-compose exec backend alembic current

# Exécution tests
docker-compose exec backend python -m pytest tests/test_models.py -v

# Test import modèles
docker-compose exec backend python -c "from app.models import Logement, Client, Souscription"
```

## 🎯 Approche MVP adoptée

**Simplicité maximale :**
- ✅ Seulement 3 tables essentielles
- ✅ Champs minimum nécessaires pour fonctionnalités
- ✅ Relations simples 1-to-many
- ✅ Enum pour contraintes métier
- ✅ Pas de sur-ingénierie

**Évolutions futures possibles :**
- Ajout table `Paiement` si nécessaire
- Ajout champs `description`, `photos` pour Logement
- Séparation `AdresseClient` / `AdresseLogement` si besoin
- Historisation des changements de statut

## 🎯 Prochaine étape
Story 1.3 - Configuration données organisation statiques