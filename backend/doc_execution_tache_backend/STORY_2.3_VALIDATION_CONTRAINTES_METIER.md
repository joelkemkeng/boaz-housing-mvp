# Story 2.3 - Validation Statuts et Contraintes Métier - DOCUMENTATION TECHNIQUE

## Vue d'ensemble
Cette story implémente un système complet de validations et de contraintes métier pour assurer l'intégrité et la cohérence des données de logements dans l'application Boaz Housing.

## Architecture de validation

### Niveaux de validation implémentés
1. **Base de données** - Contraintes SQL et validateurs SQLAlchemy
2. **API/Schémas** - Validations Pydantic v2 avec règles personnalisées
3. **Logique métier** - Règles business dans les services
4. **Interface utilisateur** - Messages d'erreur structurés

## 1. Modèle SQLAlchemy renforcé

### Fichier : `app/models/logement.py`

#### Contraintes de base de données
```sql
-- Contraintes ajoutées avec CheckConstraint
CHECK (loyer > 0)                                    -- Loyer positif obligatoire
CHECK (montant_charges >= 0)                         -- Charges positives ou nulles
CHECK (montant_total > 0)                           -- Montant total positif
CHECK (montant_total = loyer + montant_charges)     -- Cohérence calcul total
CHECK (trim(titre) != '')                           -- Titre non vide
CHECK (trim(adresse) != '')                         -- Adresse non vide
CHECK (trim(ville) != '')                           -- Ville non vide  
CHECK (trim(code_postal) != '')                     -- Code postal non vide
```

#### Validateurs SQLAlchemy (@validates)
```python
@validates('titre')
def validate_titre(self, key, titre):
    """Validation titre : min 3 caractères, nettoyage espaces"""
    
@validates('ville')  
def validate_ville(self, key, ville):
    """Validation ville : format lettres/espaces/tirets/apostrophes"""
    
@validates('code_postal')
def validate_code_postal(self, key, code_postal):
    """Validation code postal : formats internationaux supportés"""
    
@validates('pays')
def validate_pays(self, key, pays):
    """Validation pays : liste des pays supportés"""
    
@validates('loyer', 'montant_charges')
def validate_montants(self, key, montant):
    """Validation montants : fourchettes acceptables"""
```

#### Formats de codes postaux supportés
- **France** : 5 chiffres (ex: 75001)
- **Belgique/Suisse** : 4 chiffres (ex: 1000)
- **Canada** : Format A1A 1A1
- **USA** : 5 chiffres ou 5-4 chiffres

#### Pays supportés
```python
pays_valides = {
    'france', 'belgique', 'suisse', 'luxembourg', 'canada', 
    'usa', 'etats-unis', 'allemagne', 'italie', 'espagne'
}
```

## 2. Schémas Pydantic v2

### Fichier : `app/schemas/logement.py`

#### Migration vers Pydantic v2
- **@validator** → **@field_validator** avec **@classmethod**
- **@root_validator** → **@model_validator(mode='after')**
- Gestion des types optionnels améliorée

#### Validations par champ
```python
@field_validator('titre')
@classmethod
def validate_titre(cls, v: str) -> str:
    """Validation titre avec nettoyage et vérification longueur"""
    
@field_validator('ville')
@classmethod  
def validate_ville(cls, v: str) -> str:
    """Validation ville avec regex et formatage automatique"""
    
@field_validator('loyer', 'montant_charges')
@classmethod
def validate_montants(cls, v: float) -> float:
    """Validation montants avec arrondi à 2 décimales"""
```

#### Validation croisée des données
```python
@model_validator(mode='after')
def validate_coherence_prix(self) -> 'LogementBase':
    """Validation cohérence prix : total < 60 000€"""
    loyer = self.loyer if hasattr(self, 'loyer') else 0
    charges = self.montant_charges if hasattr(self, 'montant_charges') else 0
    
    if loyer and charges:
        montant_total = loyer + charges
        if montant_total > 60000:
            raise ValueError('Le montant total semble anormalement élevé')
    return self
```

## 3. Exceptions métier personnalisées

### Fichier : `app/exceptions/logement_exceptions.py`

#### Hiérarchie d'exceptions
```python
LogementException (base)
├── LogementValidationError      # Erreurs de format/validation
├── LogementBusinessRuleError    # Règles métier violées  
├── LogementNotFoundError        # Ressource introuvable
└── LogementStatutError          # Erreurs changement statut
```

#### Conversion automatique HTTP
```python
def convert_to_http_exception(exc: LogementException) -> HTTPException:
    """Convertit les exceptions métier en réponses HTTP appropriées"""
    
    # LogementValidationError → 422 Unprocessable Entity
    # LogementBusinessRuleError → 400 Bad Request  
    # LogementNotFoundError → 404 Not Found
    # LogementStatutError → 409 Conflict
```

#### Format des réponses d'erreur
```json
{
  "detail": {
    "type": "business_rule_error",
    "message": "Le loyer doit être d'au moins 50.0€", 
    "rule": "loyer_minimum"
  }
}
```

## 4. Service métier renforcé

### Fichier : `app/services/logement_service.py`

#### Règles métier configurables
```python
class LogementService:
    # Limites financières
    LOYER_MIN = 50.0              # Loyer minimum acceptable
    LOYER_MAX = 50000.0           # Loyer maximum acceptable  
    CHARGES_MAX = 10000.0         # Charges maximum acceptables
    MONTANT_TOTAL_MAX = 60000.0   # Montant total maximum
    
    # Contraintes temporelles
    DELAI_MIN_CHANGEMENT_STATUT = 1  # Délai minimum entre changements (heures)
```

#### Validations métier
```python
def _validate_business_rules(self, logement_data: dict) -> None:
    """
    Validation complète des règles métier :
    - Fourchette loyer acceptable
    - Charges raisonnables (max 10k€)
    - Ratio charges/loyer ≤ 80%
    - Montant total cohérent
    """
    
def _check_duplicate_logement(self, db: Session, adresse: str, ville: str) -> None:
    """
    Validation unicité logement :
    - Pas de doublon sur adresse + ville
    - Exclusion de l'ID courant en modification
    """
```

#### Règles de changement de statut
```python
def _validate_statut_change(self, db_logement: Logement, nouveau_statut: StatutLogement) -> None:
    """
    Validation changements de statut :
    - Transitions interdites (occupé → disponible direct)
    - Délai minimum entre changements (1h)
    - Pas de changement vers le même statut
    """
    
    # Transitions interdites
    transitions_interdites = {
        StatutLogement.OCCUPE: [StatutLogement.DISPONIBLE]
    }
```

#### Gestion des erreurs d'intégrité
```python
try:
    db_logement = Logement(**logement_data)
    db.add(db_logement)
    db.commit()
    
except IntegrityError as e:
    db.rollback()
    if "check_" in str(e):
        raise LogementValidationError("Contrainte de base de données violée")
    raise LogementValidationError("Erreur d'intégrité des données")
```

## 5. Endpoints API sécurisés

### Fichier : `app/routers/logements.py`

#### Gestion globale des exceptions
```python
@router.post("/", response_model=LogementResponse)
def create_logement(logement: LogementCreate, db: Session = Depends(get_db)):
    try:
        return logement_service.create_logement(db=db, logement=logement)
    except LogementException as e:
        raise convert_to_http_exception(e)
```

#### Endpoints protégés
- **POST /api/logements/** - Création avec validations complètes
- **PUT /api/logements/{id}** - Modification avec contrôles métier
- **PATCH /api/logements/{id}/statut** - Changement statut avec règles
- **DELETE /api/logements/{id}** - Suppression avec vérifications

## 6. Tests et validation

### Fichier : `test_validations.py`

#### Suite de tests unitaires
```bash
✅ test_create_logement_valid()           # Création logement valide
✅ test_create_logement_loyer_trop_bas()  # Validation loyer minimum
✅ test_create_logement_charges_trop_elevees() # Validation ratio charges
✅ test_validate_ville_format()          # Format ville (regex)
✅ test_validate_code_postal()           # Formats codes postaux
✅ test_changement_statut_interdit()     # Transitions interdites
```

#### Tests d'intégration API
```bash
# Tests réels via curl sur API en production
✅ Validation Pydantic (titre trop court)
✅ Règles métier (loyer trop bas) 
✅ Contraintes business (charges > 80% loyer)
✅ Anti-doublon (adresse + ville)
✅ Transitions statut (occupé → disponible interdit)
✅ Délai changement statut (< 1h interdit)
```

## 7. Règles métier détaillées

### Règles financières
| Règle | Valeur | Justification |
|-------|---------|---------------|
| Loyer minimum | 50€ | Éviter erreurs de saisie |
| Loyer maximum | 50 000€ | Limite raisonnable marché |
| Charges maximum | 10 000€ | Limite haute charges |
| Ratio charges/loyer | 80% | Éviter charges abusives |
| Montant total maximum | 60 000€ | Sécurité globale |

### Règles de statut
| Transition | Autorisée | Règle |
|------------|-----------|-------|
| Disponible → Occupé | ✅ | Location normale |
| Disponible → Maintenance | ✅ | Travaux préventifs |
| Occupé → Maintenance | ✅ | Travaux avec locataire |
| Occupé → Disponible | ❌ | Doit passer par maintenance |
| Maintenance → Disponible | ✅ | Fin des travaux |
| Maintenance → Occupé | ✅ | Location directe post-travaux |

### Règles temporelles
- **Délai minimum entre changements de statut** : 1 heure
- **Justification** : Éviter les changements erratiques ou erreurs

### Règles de format
- **Ville** : Lettres, espaces, tirets, apostrophes uniquement
- **Titre** : Minimum 3 caractères, maximum 200
- **Adresse** : Minimum 5 caractères, maximum 500
- **Description** : Maximum 2000 caractères (optionnel)

## 8. Messages d'erreur utilisateur

### Validation Pydantic (422)
```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "titre"], 
      "msg": "String should have at least 3 characters",
      "input": "AB"
    }
  ]
}
```

### Règles métier (400)
```json
{
  "detail": {
    "type": "business_rule_error",
    "message": "Les charges ne peuvent pas dépasser 80% du loyer",
    "rule": "ratio_charges_loyer"
  }
}
```

### Changement de statut (409)
```json
{
  "detail": {
    "type": "statut_error", 
    "message": "Transition interdite: de occupe vers disponible. Le logement doit d'abord passer par 'maintenance'.",
    "current_statut": "occupe",
    "target_statut": "disponible"
  }
}
```

### Logement introuvable (404)
```json
{
  "detail": {
    "type": "not_found_error",
    "message": "Logement avec l'ID 999 non trouvé",
    "logement_id": 999
  }
}
```

## 9. Performance et optimisation

### Optimisations base de données
- **Contraintes SQL** : Validation rapide au niveau SGBD
- **Index** : Recherche efficace sur adresse + ville pour doublons
- **Transactions** : Rollback automatique en cas d'erreur

### Optimisations application
- **Validation précoce** : Échec rapide sur erreurs évidentes
- **Cache des règles** : Règles métier en constantes de classe
- **Exceptions typées** : Gestion d'erreurs optimisée

### Monitoring
- **Logging** : Traçabilité des erreurs de validation
- **Métriques** : Comptage des erreurs par type
- **Alertes** : Détection des pics d'erreurs

## 10. Sécurité

### Protection contre les injections
- **Validation stricte** : Tous les champs validés avant BD
- **Paramètres liés** : Aucune concaténation SQL directe
- **Échappement** : Gestion automatique SQLAlchemy

### Validation des permissions
- **Contrôle d'accès** : Vérification des droits avant actions
- **Audit trail** : Traçage des modifications de statut
- **Isolation** : Séparation validation/authorization

## 11. Maintenance et évolution

### Configuration externalisée
```python
# Règles métier configurables via variables d'environnement
LOYER_MIN = float(os.getenv('LOYER_MIN', '50.0'))
LOYER_MAX = float(os.getenv('LOYER_MAX', '50000.0'))
```

### Points d'extension
- **Nouvelles règles** : Ajout facile via méthodes privées
- **Pays supplémentaires** : Extension liste pays supportés
- **Règles temporelles** : Configuration des délais métier
- **Notifications** : Alertes sur violations de règles

### Documentation code
- **Docstrings** : Documentation complète des méthodes
- **Type hints** : Typage strict Python 3.11+
- **Comments** : Explication des règles métier complexes

## Conclusion

La Story 2.3 implémente un système de validation multi-niveau garantissant :

### ✅ **Intégrité des données**
- Contraintes SQL strictes
- Validations Pydantic v2 robustes  
- Règles métier configurables

### ✅ **Expérience utilisateur**
- Messages d'erreur clairs et structurés
- Validation précoce côté client
- Feedback immédiat sur les actions

### ✅ **Maintenabilité**
- Architecture modulaire et extensible
- Exceptions typées et gestion centralisée
- Tests automatisés complets

### ✅ **Sécurité**
- Protection contre injections
- Validation stricte des entrées
- Audit trail des modifications

Le système est maintenant prêt pour la production avec un niveau de robustesse professionnel.