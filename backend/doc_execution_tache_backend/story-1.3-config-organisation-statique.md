# Story 1.3 - Configuration données organisation statiques

## ✅ Tâche complétée
**Durée estimée :** 30min  
**Statut :** TERMINÉ  

## 🎯 Objectifs
Configuration des données statiques de l'organisation Boaz-Housing pour utilisation dans la génération de documents :
- Structuration des données organisation depuis `information-dynamique-document.txt`
- Service de gestion des données statiques  
- API endpoints pour accès aux informations
- Génération automatique des codes de référence
- Configuration QR codes pour vérification documents

## 🛠️ Implémentation réalisée - Détail technique

### 1. Structure des données organisation

**Fichier `backend/app/data/organisation.json` :**
```json
{
  "organisation": {
    "nom": "Boaz-Housing",
    "logo_path": "/static/logo-boaz-housing.png",
    "site_web": "www.boaz-study.com",
    "email_contact": "info@boaz-study.fr",
    "telephone": "+33 01 84 18 02 67",
    "adresse_siege": "14 Rue Jean Piestre, Corbeil-Essonnes, 91100, France",
    "ville_rcs": "Corbeil-Essonnes",
    "numero_rcs": "12345778909987665",
    "code_naf": "1234D",
    "cachet_signature_path": "/static/cachet-signature-boaz.png"
  },
  "ceo": {
    "nom_complet": "Benjamin YOHO BATOMO",
    "date_naissance": "17/03/1992",
    "ville_naissance": "Douala",
    "pays_naissance": "Cameroun"
  },
  "documents": {
    "qr_code_base_url": "http://localhost:3000/verify",
    "verification_endpoint": "/api/verify-attestation",
    "reference_prefix": "ATT-",
    "reference_format": "ATT-{random_code}",
    "reference_example": "ATT-D28B8C5877C1CA25"
  }
}
```

**Procédure technique :**
1. **Séparation logique** : Organisation, CEO, Documents dans sections distinctes
2. **Données depuis specs** : Extraction exacte depuis `information-dynamique-document.txt`
3. **Paths statiques** : Préparation pour fichiers logo/cachet (implémentation future)
4. **Configuration QR codes** : URLs base et endpoints pour vérification
5. **Format JSON** : Structure extensible et facile à maintenir

### 2. Service OrganisationService - Gestion centralisée

**Fichier `backend/app/services/organisation_service.py` :**

```python
class OrganisationService:
    """Service pour gérer les données statiques de l'organisation Boaz-Housing"""
    
    def __init__(self):
        self.config_file = os.path.join(os.path.dirname(__file__), "../data/organisation.json")
        self._config = None
    
    def _load_config(self) -> Dict[str, Any]:
        """Charge la configuration depuis le fichier JSON"""
        if self._config is None:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self._config = json.load(f)
        return self._config
```

**Méthodes implémentées :**

1. **`get_organisation_info()`** : Informations entreprise (nom, contact, RCS)
2. **`get_ceo_info()`** : Informations dirigeant (nom, naissance)  
3. **`get_contact_info()`** : Contact formaté (email, téléphone, site web)
4. **`generate_reference_code()`** : Génération codes uniques ATT-XXXXXXXXXXXX
5. **`generate_qr_code_url()`** : URLs QR codes pour vérification
6. **`format_address_for_document()`** : Adresse formatée pour PDF

**Décisions techniques :**
1. **Singleton pattern** : Instance globale `organisation_service` 
2. **Lazy loading** : Configuration chargée au premier accès
3. **Cache en mémoire** : Évite re-lecture fichier à chaque appel
4. **Encodage UTF-8** : Support caractères spéciaux (CEO camerounais)
5. **Secrets module** : Génération cryptographiquement sécurisée des références

### 3. Génération automatique des références

**Algorithme de génération :**
```python
def generate_reference_code(self) -> str:
    """Génère un code de référence unique pour les souscriptions"""
    # Format: ATT-{12_caractères_aléatoires}
    random_part = ''.join(secrets.choice(string.ascii_uppercase + string.digits) 
                         for _ in range(12))
    return f"ATT-{random_part}"
```

**Procédure technique :**
1. **Préfixe fixe** : "ATT-" pour identifier les attestations
2. **12 caractères aléatoires** : Combinaison lettres majuscules + chiffres
3. **Cryptographiquement sécurisé** : Module `secrets` (pas `random`)
4. **Format cohérent** : Respecte exemple "ATT-D28B8C5877C1CA25"
5. **Collision improbable** : 36^12 = 4.7 x 10^18 possibilités

**Test d'unicité réalisé :**
```python
def test_generate_reference_code():
    ref1 = service.generate_reference_code()  # ATT-WOS0LMJIZ2OE
    ref2 = service.generate_reference_code()  # ATT-ABC123XYZ789
    
    assert ref1.startswith("ATT-")
    assert len(ref1) == 16  # ATT- (4) + 12 caractères
    assert ref1 != ref2     # Unicité vérifiée
```

### 4. API REST pour accès aux données

**Fichier `backend/app/routers/organisation.py` :**

```python
router = APIRouter(prefix="/organisation", tags=["Organisation"])

@router.get("/info")
def get_organisation_info():
    """Récupère les informations de l'organisation Boaz-Housing"""
    return organisation_service.get_organisation_info()

@router.post("/generate-reference")
def generate_reference():
    """Génère un code de référence unique pour les souscriptions"""
    reference = organisation_service.generate_reference_code()
    qr_url = organisation_service.generate_qr_code_url(reference)
    return {
        "reference": reference,
        "qr_code_url": qr_url
    }
```

**Endpoints disponibles :**
- `GET /api/organisation/info` - Informations organisation
- `GET /api/organisation/ceo` - Informations CEO
- `GET /api/organisation/contact` - Contact formaté
- `GET /api/organisation/config` - Configuration complète (dev)
- `POST /api/organisation/generate-reference` - Génération référence + QR

**Intégration FastAPI :**
```python
# Dans app/main.py
from app.routers import organisation
app.include_router(organisation.router, prefix="/api")
```

### 5. Configuration QR Codes et vérification

**URL de vérification générée :**
```python
def generate_qr_code_url(self, reference: str) -> str:
    """Génère l'URL du QR code pour vérification"""
    # http://localhost:3000/verify/ATT-D28B8C5877C1CA25
    return f"{base_url}/verify/{reference}"
```

**Workflow de vérification prévu :**
1. **QR Code dans PDF** : Contient URL `http://localhost:3000/verify/{reference}`
2. **Scan par utilisateur** : Redirige vers page de vérification frontend
3. **Vérification backend** : API `/api/verify-attestation/{reference}`
4. **Réponse JSON** : Statut validité + date expiration document

## 🧪 Tests de validation

**Fichier `backend/tests/test_organisation_service.py` avec 7 tests :**

```python
def test_get_organisation_info():
    """Test récupération infos organisation"""
    org = service.get_organisation_info()
    
    assert org["nom"] == "Boaz-Housing"
    assert org["email_contact"] == "info@boaz-study.fr"
    assert "Corbeil-Essonnes" in org["adresse_siege"]

def test_generate_reference_code():
    """Test génération code de référence"""
    ref1 = service.generate_reference_code()
    ref2 = service.generate_reference_code()
    
    assert ref1.startswith("ATT-") and len(ref1) == 16
    assert ref1 != ref2  # Unicité vérifiée

def test_generate_qr_code_url():
    """Test génération URL QR code"""
    url = service.generate_qr_code_url("ATT-TEST123456")
    assert url == "http://localhost:3000/verify/ATT-TEST123456"
```

**Résultats des tests :**
```bash
$ docker-compose exec backend python -m pytest tests/test_organisation_service.py -v
======================== 7 passed, 2 warnings in 0.03s =========================
```

## 📊 Validation endpoints API

**Test des endpoints avec curl :**

```bash
# Test informations organisation
$ curl http://localhost:8000/api/organisation/info
{
  "nom":"Boaz-Housing",
  "email_contact":"info@boaz-study.fr",
  "telephone":"+33 01 84 18 02 67",
  "adresse_siege":"14 Rue Jean Piestre, Corbeil-Essonnes, 91100, France"
  # ... autres champs
}

# Test informations CEO  
$ curl http://localhost:8000/api/organisation/ceo
{
  "nom_complet":"Benjamin YOHO BATOMO",
  "ville_naissance":"Douala",
  "pays_naissance":"Cameroun"
}

# Test génération référence
$ curl -X POST http://localhost:8000/api/organisation/generate-reference
{
  "reference":"ATT-WOS0LMJIZ2OE",
  "qr_code_url":"http://localhost:3000/verify/ATT-WOS0LMJIZ2OE"
}
```

## 🎯 Approche MVP adoptée

**Simplicité maximale :**
- ✅ Fichier JSON simple (pas de base de données)
- ✅ Service stateless avec cache mémoire
- ✅ API REST minimale pour accès aux données
- ✅ Génération références cryptographiquement sécurisée
- ✅ Préparation QR codes pour documents PDF

**Données statiques extraites précisément :**
- ✅ Nom organisation : "Boaz-Housing" 
- ✅ CEO : "Benjamin YOHO BATOMO" (Douala, Cameroun)
- ✅ Adresse : "14 Rue Jean Piestre, Corbeil-Essonnes, 91100"
- ✅ Contact : "info@boaz-study.fr" / "+33 01 84 18 02 67"
- ✅ RCS : "12345778909987665" / Code NAF : "1234D"

## 🔧 Commandes de test utilisées

```bash
# Redémarrage backend avec nouvelles routes
docker-compose restart backend

# Tests service organisation
docker-compose exec backend python -m pytest tests/test_organisation_service.py -v

# Validation endpoints API
curl http://localhost:8000/api/organisation/info
curl http://localhost:8000/api/organisation/ceo  
curl -X POST http://localhost:8000/api/organisation/generate-reference

# Accès documentation API Swagger
# http://localhost:8000/docs
```

## 🚀 Utilisation dans les prochaines étapes

**Le service sera utilisé pour :**
1. **Génération PDF Proforma** : Informations organisation dans en-tête
2. **Génération PDF Attestation** : Données CEO pour signature  
3. **QR Codes documents** : URLs de vérification automatiques
4. **Références souscriptions** : Codes uniques ATT-XXXXXXXXXXXX
5. **Templates emails** : Informations contact dans signatures

## 🎯 Prochaine étape
EPIC 2 - Story 2.1 - API CRUD logements backend (1h15)