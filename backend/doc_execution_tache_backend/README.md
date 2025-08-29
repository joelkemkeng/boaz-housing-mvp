# Documentation des Tâches Backend - Boaz Housing MVP

## Vue d'ensemble
Ce dossier contient la documentation technique détaillée de toutes les tâches backend réalisées dans le cadre du projet Boaz Housing MVP.

## Organisation des documents

### 📚 Epic 1 - Infrastructure & Setup Backend
| Document | Story | Durée | Description |
|----------|-------|-------|-------------|
| `STORY_1.2_MODELES_BASE_DONNEES.md` | Story 1.2 | 1h15 | Création modèles SQLAlchemy, contraintes DB, migrations |

### 📚 Epic 2 - Gestion Logements Backend  
| Document | Story | Durée | Description |
|----------|-------|-------|-------------|
| `STORY_2.1_API_CRUD_LOGEMENTS.md` | Story 2.1 | 1h15 | API REST complète, endpoints CRUD, services métier |
| `STORY_2.3_VALIDATION_CONTRAINTES_METIER.md` | Story 2.3 | 45min | Système validation multi-niveau, règles métier, exceptions |

## Technologies couvertes

### 🔧 Framework et ORM
- **FastAPI** - Framework API moderne avec auto-documentation
- **SQLAlchemy 2.x** - ORM Python avec modèles déclaratifs
- **Pydantic v2** - Validation de données et sérialisation JSON
- **Alembic** - Migrations de schéma de base de données

### 🗄️ Base de données
- **PostgreSQL 15** - Base de données principale
- **PgAdmin 4** - Interface d'administration
- **Docker Compose** - Orchestration des services

### 🛡️ Validation et sécurité
- **Contraintes SQL** - Validation au niveau base de données
- **Validateurs SQLAlchemy** - Règles métier dans les modèles
- **Exceptions personnalisées** - Gestion d'erreurs typées
- **CORS** - Configuration pour frontend React

## Modèles de données

### Organisation
```python
class Organisation(Base):
    # Informations entreprise Boaz-Housing
    nom, description, ceo_nom, telephone_principal, email
    adresse, ville, code_postal, pays
```

### Logement  
```python
class Logement(Base):
    # Informations descriptives
    id, titre, description, adresse, ville, code_postal, pays
    
    # Tarification
    loyer, montant_charges, montant_total (calculé auto)
    
    # État et suivi
    statut: StatutLogement, created_at, updated_at
```

### Énumérations
```python
class StatutLogement(str, enum.Enum):
    DISPONIBLE = "disponible"
    OCCUPE = "occupe" 
    MAINTENANCE = "maintenance"
```

## API Endpoints

### 🏠 Logements (`/api/logements/`)
| Méthode | Endpoint | Description | Validation |
|---------|----------|-------------|------------|
| `POST` | `/` | Création logement | Règles métier + anti-doublon |
| `GET` | `/` | Liste avec filtres | Pagination + tri intelligent |
| `GET` | `/{id}` | Détail logement | Vérification existence |
| `PUT` | `/{id}` | Modification complète | Validation cohérence prix |
| `DELETE` | `/{id}` | Suppression | Confirmation requise |
| `GET` | `/disponibles` | Logements disponibles | Filtre automatique statut |
| `GET` | `/stats` | Statistiques | Comptage par statut |
| `PATCH` | `/{id}/statut` | Changement statut | Règles de transition |

## Règles métier implémentées

### 💰 Règles financières
- **Loyer** : 50€ ≤ loyer ≤ 50 000€
- **Charges** : 0€ ≤ charges ≤ 10 000€
- **Ratio charges/loyer** : ≤ 80%
- **Montant total** : calculé automatiquement, ≤ 60 000€

### 🏘️ Règles de gestion
- **Unicité** : Pas de doublon adresse + ville
- **Délai changement statut** : Minimum 1 heure entre modifications
- **Transitions interdites** : Occupé → Disponible (doit passer par maintenance)

### 📝 Règles de format
- **Titre** : 3-200 caractères, non vide
- **Ville** : Lettres, espaces, tirets, apostrophes uniquement
- **Code postal** : Formats FR/BE/CH/CA/US supportés
- **Pays** : Liste prédéfinie de pays supportés

## Architecture des services

### Service Pattern
```python
class LogementService:
    # Règles métier configurables
    LOYER_MIN = 50.0
    CHARGES_MAX = 10000.0
    
    # Méthodes CRUD avec validations
    def create_logement(self, db, logement) -> Logement
    def get_logements(self, db, filters) -> List[Logement] 
    def update_logement(self, db, id, updates) -> Logement
    def delete_logement(self, db, id) -> bool
    
    # Méthodes spécialisées
    def changer_statut_logement(self, db, id, statut) -> Logement
    def get_stats_logements(self, db) -> dict
```

### Gestion d'erreurs
```python
LogementException (base)
├── LogementValidationError     # 422 Unprocessable Entity
├── LogementBusinessRuleError   # 400 Bad Request
├── LogementNotFoundError       # 404 Not Found
└── LogementStatutError         # 409 Conflict
```

## Tests et validation

### 🧪 Tests unitaires
- ✅ Modèles SQLAlchemy avec contraintes
- ✅ Validateurs Pydantic v2
- ✅ Services métier avec règles business
- ✅ Exceptions personnalisées

### 🔗 Tests d'intégration
- ✅ Endpoints API avec curl
- ✅ Validation Pydantic côté requête
- ✅ Règles métier appliquées
- ✅ Gestion d'erreurs HTTP appropriées

## Performance et optimisation

### 📊 Index base de données
```sql
CREATE INDEX idx_logement_statut ON logements(statut);
CREATE INDEX idx_logement_ville ON logements(ville);
CREATE UNIQUE INDEX idx_logement_adresse_ville ON logements(adresse, ville);
```

### ⚡ Optimisations requêtes
- **Pagination** : `LIMIT` + `OFFSET` pour grandes listes
- **Tri intelligent** : Par `updated_at DESC` puis `created_at DESC`
- **Filtrage serveur** : Réduction trafic réseau
- **Pool connexions** : Gestion efficace PostgreSQL

## Évolutions futures

### 🚀 Extensions prévues
- **Story 3.1** : Modèles et API souscriptions
- **Story 4.x** : Génération documents PDF
- **Story 5.x** : Système d'envoi d'emails
- **Authentification** : JWT + rôles utilisateurs
- **Cache Redis** : Performance requêtes fréquentes

### 🔧 Améliorations techniques
- **Monitoring** : Logs structurés + métriques
- **Tests e2e** : Couverture complète scénarios
- **CI/CD** : Pipeline automatisé
- **Documentation** : Swagger enrichie avec exemples

## Comment utiliser cette documentation

### 👥 Pour les développeurs
1. **Nouveaux développeurs** : Lire dans l'ordre chronologique (1.2 → 2.1 → 2.3)
2. **Maintenance** : Consulter le document spécifique à la fonctionnalité
3. **Debugging** : Section gestion d'erreurs + tests de chaque document

### 🏗️ Pour l'architecture
1. **Modèles de données** : Story 1.2 pour la structure DB
2. **API Design** : Story 2.1 pour les patterns REST
3. **Validation** : Story 2.3 pour les règles métier

### 📋 Pour les tests
1. **Scénarios de test** : Exemples curl dans chaque document
2. **Validation règles** : Tests unitaires Story 2.3
3. **Performance** : Métriques et optimisations documentées

---

## Statut actuel
- ✅ **Epic 1** : Infrastructure complète et opérationnelle
- ✅ **Epic 2** : Gestion logements avec validation robuste
- 🔄 **Epic 3** : En cours de développement
- ⏳ **Epic 4-5** : Planifiés

**Dernière mise à jour** : 29 août 2025  
**Version** : v1.0.0