
## **MÉTHODE DE PLANIFICATION PROPOSÉE**

Je propose de diviser la planification en **3 phases** :

1. **Phase 1** : Structure générale et organisation des Epics/Stories 
2. **Phase 2** : Détail complet des tâches techniques pour chaque Epic
3. **Phase 3** : Procédures de test et critères d'acceptation

Commençons par la **Phase 1** :

---

## **PHASE 1 : STRUCTURE GÉNÉRALE ET ORGANISATION**

### **Répartition temporelle sur 10h :**
- **Epic 1 - Infrastructure & Setup** : 2h
- **Epic 2 - Gestion des logements (Bailleur)** : 2h  
- **Epic 3 - Application de souscription (Admin)** : 4h
- **Epic 4 - Génération de documents PDF** : 1.5h
- **Epic 5 - Envoi d'emails** : 0.5h

---

## **EPIC 1 : INFRASTRUCTURE & SETUP (2h)**

### **Story 1.1 : Configuration environnement de développement**
**Points d'estimation** : 3  
**Durée** : 45 min

**Description fonctionnelle :**
Mettre en place l'environnement complet de développement avec tous les outils nécessaires pour développer l'application Boaz-Housing MVP selon les spécifications du cahier des charges.

**Description technique ultra-détaillée :**

**Backend FastAPI Setup :**
- Créer un projet FastAPI avec la structure suivante :
  ```
  backend/
  ├── app/
  │   ├── __init__.py
  │   ├── main.py
  │   ├── database.py
  │   ├── models/
  │   │   ├── __init__.py
  │   │   ├── logement.py
  │   │   └── souscription.py
  │   ├── schemas/
  │   │   ├── __init__.py
  │   │   ├── logement.py
  │   │   └── souscription.py
  │   ├── routers/
  │   │   ├── __init__.py
  │   │   ├── logements.py
  │   │   └── souscriptions.py
  │   └── services/
  │       ├── __init__.py
  │       ├── pdf_generator.py
  │       └── email_service.py
  ├── requirements.txt
  └── tests/
      ├── __init__.py
      └── test_main.py
  ```
- Installer les dépendances : fastapi, uvicorn, sqlalchemy, psycopg2-binary, alembic, pydantic, jinja2, reportlab, smtplib
- Configurer CORS pour permettre les requêtes depuis React
- Créer le fichier database.py avec SQLAlchemy et la connexion PostgreSQL
- Configurer les variables d'environnement (.env) : DATABASE_URL, SMTP settings

**Frontend React Setup :**
- Créer l'application React avec create-react-app
- Structure des dossiers :
  ```
  frontend/
  ├── public/
  ├── src/
  │   ├── components/
  │   │   ├── admin/
  │   │   ├── bailleur/
  │   │   └── common/
  │   ├── pages/
  │   │   ├── AdminDashboard.jsx
  │   │   └── BailleurDashboard.jsx
  │   ├── services/
  │   │   └── api.js
  │   ├── utils/
  │   └── App.js
  └── package.json
  ```
- Installer les dépendances : axios, react-router-dom, react-hook-form, tailwindcss
- Configurer Tailwind CSS
- Créer le service API de base avec axios

**Database PostgreSQL Setup :**
- Créer la base de données "boaz_housing_mvp"
- Configurer Alembic pour les migrations
- Préparer les modèles de base (sans créer les tables)

**Tests Setup :**
- Configurer pytest pour le backend
- Configurer Jest/React Testing Library pour le frontend
- Créer les fichiers de configuration de test

**Procédure de test :**
1. Vérifier que FastAPI démarre sur http://localhost:8000
2. Vérifier que React démarre sur http://localhost:3000
3. Vérifier la connexion à PostgreSQL
4. Exécuter les tests de base (should pass avec 0 tests)
5. Vérifier que CORS fonctionne entre React et FastAPI

---

### **Story 1.2 : Création des modèles de base de données**
**Points d'estimation** : 5  
**Durée** : 1h15

**Description fonctionnelle :**
Créer tous les modèles de données selon les spécifications du cahier des charges pour stocker les informations des logements, souscriptions, clients et organisation.

**Description technique ultra-détaillée :**

**Modèle Logement (models/logement.py) :**
```python
class Logement(Base):
    __tablename__ = "logements"
    
    id = Column(Integer, primary_key=True, index=True)
    adresse_complete = Column(String, nullable=False)
    pays = Column(String, nullable=False)
    ville = Column(String, nullable=False)
    type_logement = Column(Enum('chambre', 'appartement', 'studio'), nullable=False)
    type_occupation = Column(Enum('individuel', 'colocation', 'autre'), nullable=False)
    superficie_m2 = Column(Float, nullable=False)
    prix_hors_charges = Column(Float, nullable=False)
    prix_charges = Column(Float, nullable=False)
    prix_total = Column(Float, nullable=False)  # calculé automatiquement
    statut = Column(Enum('libre', 'occupe'), default='libre')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relation avec souscriptions
    souscriptions = relationship("Souscription", back_populates="logement")
```

**Modèle Souscription (models/souscription.py) :**
```python
class Souscription(Base):
    __tablename__ = "souscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    reference = Column(String, unique=True, nullable=False)  # ATT-XXXXXXXXX
    
    # Informations client
    nom_client = Column(String, nullable=False)
    prenom_client = Column(String, nullable=False)
    email_client = Column(String, nullable=False)
    date_naissance_client = Column(Date, nullable=False)
    ville_naissance_client = Column(String, nullable=False)
    pays_naissance_client = Column(String, nullable=False)
    nationalite_client = Column(String, nullable=False)
    pays_destination = Column(String, nullable=False)
    date_arrivee_prevue = Column(Date, nullable=False)
    
    # Informations académiques
    ecole_universite = Column(String, nullable=False)
    filiere = Column(String, nullable=False)
    pays_ecole = Column(String, nullable=False)
    ville_ecole = Column(String, nullable=False)
    code_postal_ecole = Column(String, nullable=False)
    adresse_ecole = Column(String, nullable=False)
    
    # Informations logement
    logement_id = Column(Integer, ForeignKey("logements.id"), nullable=False)
    date_entree_prevue = Column(Date, nullable=False)
    duree_location_mois = Column(Integer, nullable=False)
    
    # Statut et tracking
    statut = Column(Enum('attente_paiement', 'paye', 'livre', 'cloture', 'supprime'), 
                   default='attente_paiement')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    logement = relationship("Logement", back_populates="souscriptions")
```

**Schémas Pydantic correspondants :**
- Créer les schémas de validation pour chaque modèle
- Schémas pour création (LogementCreate, SouscriptionCreate)  
- Schémas pour réponse (LogementResponse, SouscriptionResponse)
- Schémas pour mise à jour (LogementUpdate, SouscriptionUpdate)

**Migration Alembic :**
- Générer la migration initiale : `alembic revision --autogenerate -m "Initial migration"`
- Appliquer la migration : `alembic upgrade head`

**Procédure de test :**
1. Exécuter la migration et vérifier que les tables sont créées
2. Tester l'insertion d'un logement via SQLAlchemy
3. Tester l'insertion d'une souscription liée à un logement
4. Vérifier les contraintes de clés étrangères
5. Tester les enums et contraintes
6. Vérifier la génération automatique des timestamps

---












---

## **EPIC 1 : INFRASTRUCTURE & SETUP (suite)**

### **Story 1.3 : Configuration des données organisation statiques**
**Points d'estimation** : 2  
**Durée** : 30 min

**Description fonctionnelle :**
Créer un système de stockage et de récupération des informations de l'organisation Boaz-Housing en format JSON statique, permettant au frontend de récupérer ces données via une API dédiée pour les utiliser dans la génération de documents.

**Description technique ultra-détaillée :**

**Création du fichier JSON organisation :**
- Créer un fichier `app/data/organisation.json` contenant toutes les informations de Boaz-Housing
- Structure JSON avec tous les champs requis : nom, logo_path, site_web, ceo_nom_complet, ceo_date_naissance, ceo_ville_naissance, ceo_pays_naissance, adresse_siege, ville_rcs, numero_rcs, code_naf, email_contact, telephone, cachet_signature_path
- Valeurs selon les spécifications : nom="Boaz-Housing", site_web="www.boaz-study.com", ceo="Benjamin YOHO BATOMO", adresse="14 Rue Jean Piestre, Corbeil-Essonnes, 91100, France", etc.

**Service de lecture JSON :**
- Créer un service `app/services/organisation_service.py` pour lire le fichier JSON
- Fonction get_organisation_info() qui retourne les données parsées
- Gestion des erreurs de lecture fichier
- Cache en mémoire pour éviter les lectures répétées

**Endpoint API organisation :**
- Créer router `app/routers/organisation.py`
- Endpoint GET `/api/organisation` qui utilise le service
- Retourne les informations organisation en format JSON standardisé
- Headers CORS appropriés

**Schéma Pydantic Organisation :**
- Créer `app/schemas/organisation.py` avec tous les champs typés
- Validation des données lors de la lecture
- Documentation OpenAPI automatique

**Procédure de test :**
1. Vérifier que le fichier JSON est bien formé et parsable
2. Tester le service de lecture avec fichier existant et inexistant
3. Tester l'endpoint `/api/organisation` et vérifier la réponse
4. Vérifier que les données retournées correspondent aux spécifications
5. Tester la performance avec cache en mémoire

---

## **EPIC 2 : GESTION DES LOGEMENTS - APPLICATION BAILLEUR (2h)**

### **Story 2.1 : API CRUD logements backend**
**Points d'estimation** : 5  
**Durée** : 1h15

**Description fonctionnelle :**
Développer l'API complète de gestion des logements pour permettre aux bailleurs d'ajouter, modifier, consulter et supprimer des logements avec toutes les informations requises selon les spécifications (adresse, pays, ville, type, superficie, prix, etc.).

**Description technique ultra-détaillée :**

**Router logements :**
- Créer `app/routers/logements.py` avec tous les endpoints CRUD
- GET `/api/logements` : récupérer tous les logements avec pagination optionnelle
- GET `/api/logements/{id}` : récupérer un logement spécifique
- POST `/api/logements` : créer nouveau logement avec validation complète
- PUT `/api/logements/{id}` : modifier logement existant
- DELETE `/api/logements/{id}` : suppression logique (soft delete)

**Logique métier création logement :**
- Validation que prix_total = prix_hors_charges + prix_charges (calcul automatique)
- Vérification unicité adresse_complete (pas de doublons)
- Statut par défaut "libre" à la création
- Génération automatique timestamps created_at/updated_at

**Logique métier modification logement :**
- Si logement utilisé dans une souscription payée, bloquer modification des champs critiques (prix, adresse)
- Permettre modification statut libre/occupé uniquement via logique métier souscription
- Validation cohérence données avant sauvegarde

**Logique métier suppression logement :**
- Vérifier qu'aucune souscription active n'utilise ce logement
- Soft delete : marquer deleted_at au lieu de supprimer physiquement
- Conserver historique pour traçabilité

**Gestion erreurs et validations :**
- Validation formats (email si applicable, codes postaux, etc.)
- Messages d'erreur explicites en français
- Codes HTTP appropriés (201, 400, 404, 409)
- Logging des opérations importantes

**Service logement :**
- Créer `app/services/logement_service.py` avec logique métier
- Fonctions pour vérifications business rules
- Interface entre router et modèle database

**Procédure de test :**
1. Tester création logement avec données valides et invalides
2. Vérifier calcul automatique prix_total
3. Tester récupération liste avec filtres
4. Tester modification avec et sans contraintes
5. Tester suppression logique et vérification contraintes
6. Vérifier validation unicité adresse
7. Tester gestion erreurs et codes retour HTTP

---

### **Story 2.2 : Interface frontend gestion logements**
**Points d'estimation** : 6  
**Durée** : 1h30

**Description fonctionnelle :**
Créer l'interface complète pour les bailleurs permettant de gérer leurs logements via un tableau listant tous les logements avec actions CRUD, formulaires de création/modification, et confirmations de suppression.

**Description technique ultra-détaillée :**

**Page principale BailleurDashboard :**
- Composant `src/pages/BailleurDashboard.jsx` avec layout principal
- Navigation simple avec section "Mes logements"
- État global pour gestion des logements (useState ou useContext)

**Composant ListeLogements :**
- Tableau responsive avec colonnes : Adresse, Ville, Type, Superficie, Prix total, Statut, Actions
- Pagination si plus de 20 logements
- Filtres simples par statut (libre/occupé) et ville
- Actions par ligne : Voir, Modifier, Supprimer
- Indicateur visuel statut (badge vert pour libre, rouge pour occupé)

**Composant FormulaireLogement :**
- Formulaire avec tous les champs requis selon spécifications
- Champs : adresse_complete (textarea), pays (select), ville (input), type_logement (radio), type_occupation (select), superficie_m2 (number), prix_hors_charges (number), prix_charges (number)
- Calcul automatique prix_total en temps réel (prix_hors_charges + prix_charges)
- Validation côté client avant soumission
- Gestion états : création/modification avec mêmes champs

**Gestion d'état et API calls :**
- Service `src/services/logementsAPI.js` pour tous les appels API
- Gestion loading states pendant requêtes
- Gestion erreurs avec affichage messages utilisateur
- Refresh automatique liste après création/modification/suppression

**Confirmations utilisateur :**
- Modal confirmation avant suppression logement
- Messages succès après opérations réussies
- Gestion navigation retour après création/modification

**Responsive design :**
- Design mobile-first avec breakpoints appropriés
- Tableau responsive avec scroll horizontal si nécessaire
- Formulaires adaptés mobile

**Procédure de test :**
1. Vérifier affichage liste logements vide et avec données
2. Tester création logement avec formulaire complet
3. Vérifier calcul automatique prix total
4. Tester modification logement existant
5. Tester suppression avec confirmation
6. Vérifier filtres et pagination
7. Tester responsive sur mobile et desktop
8. Vérifier gestion erreurs et messages utilisateur

---

### **Story 2.3 : Validation statuts logements et contraintes métier**
**Points d'estimation** : 3  
**Durée** : 45 min

**Description fonctionnelle :**
Implémenter la logique de validation des statuts des logements et les contraintes métier pour empêcher la modification/suppression des logements liés à des souscriptions actives, selon les règles définies dans les spécifications.

**Description technique ultra-détaillée :**

**Logique validation backend :**
- Fonction `check_logement_usage(logement_id)` dans service logement
- Vérification existence souscriptions liées avec statuts "payé", "livré", "clôturé"
- Si logement utilisé, retourner erreur 409 Conflict avec message explicite
- Permettre modification champs non-critiques uniquement (ex: description si ajoutée)

**Endpoint validation contraintes :**
- GET `/api/logements/{id}/can-modify` retourne booléen et raisons
- GET `/api/logements/{id}/can-delete` retourne booléan et raisons
- Utilisé par frontend avant affichage options modification/suppression

**Gestion statuts automatiques :**
- Lors validation souscription (statut "payé"), passer logement automatiquement en "occupé"
- Lors clôture souscription, possibilité de remettre logement en "libre"
- Historique changements statuts avec timestamps

**Interface frontend contraintes :**
- Appel API validation avant affichage boutons Modifier/Supprimer
- Désactivation boutons avec tooltip explicatif si contraintes
- Affichage indicateur "Utilisé dans attestation" sur logements occupés

**Messages utilisateur :**
- Messages d'erreur explicites : "Ce logement ne peut pas être modifié car il est utilisé dans une attestation active"
- Information preview avant actions : "Ce logement est libre et peut être modifié"

**Procédure de test :**
1. Créer logement et vérifier qu'il peut être modifié/supprimé
2. Créer souscription liée et payer, vérifier blocage modification
3. Tester endpoints de validation contraintes
4. Vérifier changement statut automatique lors paiement souscription
5. Tester affichage frontend avec contraintes actives/inactives
6. Vérifier messages d'erreur explicites côté utilisateur

---













## **EPIC 3 : APPLICATION DE SOUSCRIPTION - ADMIN (4h)**

### **Story 3.1 : API backend souscriptions CRUD**
**Points d'estimation** : 4  
**Durée** : 1h

**Description fonctionnelle :**
Développer l'API complète de gestion des souscriptions côté administrateur avec création, lecture, modification, suppression logique et gestion des statuts selon le workflow défini dans les spécifications.

**Description technique ultra-détaillée :**

**Router souscriptions :**
- Créer `app/routers/souscriptions.py` avec endpoints complets
- GET `/api/souscriptions` : liste toutes souscriptions avec pagination et filtres par statut
- GET `/api/souscriptions/{id}` : détails souscription avec données logement jointes
- POST `/api/souscriptions` : création nouvelle souscription en statut "attente_paiement"
- PUT `/api/souscriptions/{id}` : modification souscription existante
- DELETE `/api/souscriptions/{id}` : suppression logique (statut "supprime")
- PATCH `/api/souscriptions/{id}/status` : changement statut uniquement

**Génération référence unique :**
- Service `generate_reference()` format ATT-XXXXXXXXXXXXXX (ATT + 16 caractères alphanumériques)
- Vérification unicité référence en base avant attribution
- Génération automatique lors création souscription

**Logique métier statuts :**
- Workflow strict : attente_paiement -> paye -> livre -> cloture
- PATCH `/api/souscriptions/{id}/pay` : passage statut "paye" + trigger génération PDF + envoi email
- Validation transitions statuts uniquement dans ordre logique
- Blocage modification données client si statut >= "paye"

**Gestion logements associés :**
- Lors création souscription, vérifier logement statut "libre"
- Lors passage statut "paye", changer logement en "occupe"
- Validation cohérence dates (date_entree_prevue >= date_creation)

**Jointures et relations :**
- Récupération souscription avec données logement complètes
- Optimisation requêtes avec eager loading SQLAlchemy
- Formatage réponses avec toutes infos nécessaires frontend

**Procédure de test :**
1. Tester création souscription avec génération référence unique
2. Vérifier workflow statuts et transitions autorisées/interdites
3. Tester modification avec contraintes selon statut
4. Vérifier changement statut logement lors paiement
5. Tester suppression logique et récupération avec filtres
6. Vérifier jointures et performances requêtes

---

### **Story 3.2 : Page d'accueil admin avec sections services et historique**
**Points d'estimation** : 5  
**Durée** : 1h15

**Description fonctionnelle :**
Créer la page d'accueil administrative selon les spécifications avec section choix de services sous forme de cards et section historique des souscriptions sous forme de tableau avec actions.

**Description technique ultra-détaillée :**

**Composant AdminDashboard principal :**
- Layout avec header Boaz-Housing et navigation simple
- Deux sections principales : ServicesSection et HistoriqueSection
- Gestion état global souscriptions avec useContext ou useState
- Refresh automatique données après actions

**Section Services (ServicesSection) :**
- Card unique pour "Attestation de Logement et de Prise en Charge" selon spécifications MVP
- Card contient : titre service, description courte, prix formaté EUR/FCFA, bouton "Souscrire"
- Design card moderne avec hover effects
- Bouton "Souscrire" déclenche ouverture wizard 4 étapes

**Section Historique (HistoriqueSection) :**
- Tableau responsive avec colonnes : Nom service, Nom prénom client, Date création, Statut, Actions
- Pagination 10 souscriptions par page
- Filtres par statut avec dropdowns
- Badge coloré pour chaque statut (rouge=attente_paiement, bleu=paye, vert=livre, gris=cloture)

**Actions disponibles par ligne :**
- Bouton "Voir" : ouvre modal lecture seule avec tous détails
- Bouton "Modifier" : ouvre wizard modification (si statut permet)
- Bouton "Supprimer" : confirmation puis suppression logique
- Bouton "Payer" : si statut="attente_paiement", lance processus paiement

**Gestion états et interactions :**
- Loading states pendant chargement données
- Messages succès/erreur après actions
- Confirmation modal avant suppressions
- Refresh automatique liste après modifications

**Responsive et UX :**
- Design mobile-first avec collapse colonnes sur mobile
- Actions groupées dans dropdown sur petits écrans
- Skeleton loading pendant requêtes
- Empty states avec messages appropriés

**Procédure de test :**
1. Vérifier affichage correct des deux sections
2. Tester card service et bouton souscrire
3. Vérifier tableau historique avec données réelles et vides
4. Tester filtres par statut et pagination
5. Vérifier toutes actions (voir, modifier, supprimer, payer)
6. Tester responsive design sur différentes tailles écran
7. Vérifier loading states et gestion erreurs

---

### **Story 3.3 : Wizard souscription étape 1 - Informations client**
**Points d'estimation** : 4  
**Durée** : 1h

**Description fonctionnelle :**
Développer la première étape du wizard de souscription permettant la saisie complète des informations personnelles du client selon les champs définis dans les spécifications.

**Description technique ultra-détaillée :**

**Composant WizardSouscription principal :**
- Stepper horizontal avec 4 étapes : Client, Académique, Logement, Proforma
- Navigation entre étapes avec validation
- Stockage données wizard dans état local React (useState)
- Sauvegarde progressive optionnelle ou finale uniquement

**Composant EtapeClient :**
- Formulaire avec tous champs requis spécifications : nom, prénom, email, date_naissance, nationalité, pays_destination, date_arrivee_prevue
- Validation temps réel avec react-hook-form
- Format date_naissance : sélecteur date avec validation âge >= 16 ans
- Liste pays avec autocomplete pour nationalité et pays_destination
- Validation email avec regex appropriée

**Validations spécifiques :**
- Nom/prénom : minimum 2 caractères, pas de caractères spéciaux
- Email : format valide + vérification unicité côté backend optionnelle
- Date naissance : âge minimum 16 ans, maximum 100 ans
- Date arrivée prévue : minimum aujourd'hui + 1 jour, maximum 2 ans
- Nationalité/pays : sélection depuis liste prédéfinie

**Navigation wizard :**
- Boutons "Précédent" (disabled étape 1) et "Suivant"
- Validation complète avant passage étape suivante
- Indicateur progression visuel avec étapes complétées
- Sauvegarde état si utilisateur quitte et revient

**Interface utilisateur :**
- Design cohérent avec identité Boaz-Housing
- Labels explicites et aide contextuelle
- Messages erreur sous champs concernés
- Formatage automatique champs (capitalisation noms, etc.)

**Procédure de test :**
1. Vérifier affichage formulaire avec tous champs
2. Tester validations champs un par un
3. Vérifier validation âge et dates
4. Tester sélection pays avec autocomplete
5. Vérifier navigation disabled/enabled selon validation
6. Tester persistance données lors navigation
7. Vérifier responsive et accessibilité formulaire

---

### **Story 3.4 : Wizard souscription étape 2 - Informations académiques**
**Points d'estimation** : 3  
**Durée** : 45 min

**Description fonctionnelle :**
Développer la deuxième étape du wizard permettant la saisie des informations académiques complètes du client selon les spécifications : école, filière, localisation complète.

**Description technique ultra-détaillée :**

**Composant EtapeAcademique :**
- Formulaire avec champs : école_universite, filière, pays_ecole, ville_ecole, code_postal_ecole, adresse_ecole
- Intégration possible API géolocalisation pour suggestions adresses
- Validation cohérence géographique pays/ville/code_postal

**Champs spécifiques :**
- École/université : input text avec suggestions écoles connues (liste prédéfinie)
- Filière : input text libre avec suggestions communes (informatique, ingénierie, etc.)
- Pays école : select avec liste pays complet
- Ville école : input text avec validation selon pays sélectionné
- Code postal : format selon pays (validation regex dynamique)
- Adresse école : textarea pour adresse complète

**Validations dynamiques :**
- Code postal format selon pays sélectionné
- Vérification cohérence ville/pays si API disponible
- Longueur minimum adresse complète (10 caractères)
- École/université minimum 3 caractères

**Assistance saisie :**
- Autocomplete écoles populaires par pays
- Suggestions filières courantes
- Formatage automatique adresses (capitalisation)
- Validation temps réel avec indicateurs visuels

**Navigation et persistance :**
- Boutons "Précédent" (retour étape 1 avec données) et "Suivant"
- Validation obligatoire tous champs avant progression
- Sauvegarde automatique données dans état wizard
- Possibilité retour modification étape précédente

**Procédure de test :**
1. Vérifier tous champs présents et fonctionnels
2. Tester validations format code postal selon pays
3. Vérifier suggestions écoles et filières
4. Tester navigation retour avec persistance données étape 1
5. Vérifier validation complète avant étape suivante
6. Tester autocomplétion et formatage automatique
7. Vérifier responsive design formulaire

---

### **Story 3.5 : Wizard souscription étape 3 - Choix logement**
**Points d'estimation** : 5  
**Durée** : 1h15

**Description fonctionnelle :**
Développer l'étape de sélection logement avec affichage des logements disponibles sous forme de cards sélectionnables contenant toutes les informations spécifiées et permettant le choix pour la souscription.

**Description technique ultra-détaillée :**

**Composant EtapeLogement :**
- Récupération logements statut "libre" via API GET `/api/logements?statut=libre`
- Affichage grid responsive de cards logements
- Sélection unique avec indication visuelle choix actuel
- Données chaque card selon spécifications exactes

**Contenu cards logements :**
- Adresse complète logement (titre principal)
- Pays et ville (sous-titre)
- Type occupation (Individuel/Colocation/Autre) avec badge
- Type logement (Chambre/Appartement/Studio) avec icône
- Superficie en m² avec unité
- Prix hors charges formaté
- Prix charges formaté
- Prix total TTC mis en évidence (couleur différente)

**Interaction et sélection :**
- Cards cliquables avec effet hover
- Sélection unique avec border colorée et checkmark
- Bouton radio invisible mais state géré
- Animation transition lors sélection/déselection

**Filtrage et recherche :**
- Filtre par ville (dropdown pays puis villes)
- Filtre par type logement (checkboxes multiples)
- Filtre par fourchette prix avec slider
- Tri par prix croissant/décroissant

**Gestion états :**
- Loading pendant récupération logements
- Message si aucun logement disponible
- Gestion erreurs API avec retry possible
- Validation sélection obligatoire avant étape suivante

**Responsive design :**
- Grid adaptatif : 1 colonne mobile, 2-3 colonnes tablet/desktop
- Cards optimisées taille écran
- Filtres collapse sur mobile

**Procédure de test :**
1. Vérifier récupération et affichage logements libres uniquement
2. Tester contenu complet cards selon spécifications
3. Vérifier sélection unique avec indicateurs visuels
4. Tester filtres ville, type, prix
5. Vérifier tri par prix
6. Tester responsive grid et cards
7. Vérifier validation sélection avant progression
8. Tester gestion cas aucun logement disponible

---

### **Story 3.6 : Wizard souscription étape 4 - Génération et prévisualisation Proforma**
**Points d'estimation** : 4  
**Durée** : 1h

**Description fonctionnelle :**
Développer la dernière étape du wizard permettant la génération, prévisualisation, téléchargement et envoi du Proforma avec toutes les actions spécifiées et finalisation de la souscription.

**Description technique ultra-détaillée :**

**Composant EtapeProforma :**
- Récapitulatif complet données saisies (client + académique + logement)
- Génération automatique référence ATT-XXXX lors affichage étape
- Appel API génération Proforma avec toutes données collectées
- Interface preview avec actions multiples selon spécifications

**Récapitulatif données :**
- Section "Informations client" : affichage formaté données étape 1
- Section "Informations académiques" : affichage formaté données étape 2  
- Section "Logement sélectionné" : card résumé avec prix
- Section "Résumé financier" : prix logement + éventuels frais service

**Génération Proforma :**
- Appel API POST `/api/souscriptions` avec données complètes wizard
- API retourne ID souscription + URL preview PDF Proforma
- Affichage preview PDF dans iframe ou viewer intégré
- Loading states pendant génération document

**Actions disponibles :**
- Bouton "Retour" : modification données (retour étapes précédentes)
- Bouton "Télécharger Proforma" : download direct PDF généré
- Bouton "Envoyer par Email" : envoi email client avec Proforma joint
- Bouton "Terminer" : finalisation et retour accueil avec refresh historique

**Gestion envoi email :**
- Modal confirmation avec email pré-rempli (modifiable)
- Message personnalisable optionnel
- Confirmation envoi avec message succès
- Gestion erreurs envoi avec possibilité retry

**Finalisation souscription :**
- Sauvegarde définitive en base statut "attente_paiement"
- Nettoyage état wizard
- Redirection accueil avec message succès
- Ajout automatique dans historique

**Procédure de test :**
1. Vérifier affichage récapitulatif complet données wizard
2. Tester génération Proforma et preview PDF
3. Vérifier téléchargement PDF fonctionnel
4. Tester envoi email avec confirmation
5. Vérifier bouton retour et modification données
6. Tester finalisation avec sauvegarde base et redirection
7. Vérifier nettoyage état wizard après finalisation
8. Tester gestion erreurs génération/envoi

---

## **EPIC 4 : GÉNÉRATION DOCUMENTS PDF (1.5h)**

### **Story 4.1 : Service génération Proforma PDF**
**Points d'estimation** : 4  
**Durée** : 1h

**Description fonctionnelle :**
Développer le service de génération du document Proforma au format PDF en respectant exactement le design et la structure du modèle fourni, avec toutes les informations dynamiques de l'organisation et du client.

**Description technique ultra-détaillée :**

**Service PDFGenerator :**
- Créer `app/services/pdf_generator.py` avec classe ProformaGenerator
- Utilisation bibliothèque ReportLab pour génération PDF programmatique
- Template basé sur modèle Boaz Study fourni dans spécifications
- Méthode `generate_proforma(souscription_data, organisation_data)` retournant bytes PDF

**Structure document Proforma :**
- Header avec logo Boaz-Housing (path depuis organisation.json)
- Titre "FACTURE" avec date génération
- Bloc informations organisation : nom, adresse, contacts, infos légales (RCS, NAF, etc.)
- Section client : nom, adresse email
- Tableau services avec colonnes : Description, Qté, Prix unitaire, Montant
- Total HT et TTC
- Footer avec mentions légales et conditions

**Données dynamiques intégrées :**
- Informations organisation depuis JSON : nom, adresse, téléphone, email, RCS, NAF
- Informations client depuis souscription : nom complet, email
- Services et prix : ligne principale "Frais Attestation de Logement" + autres frais selon business model
- Calculs automatiques totaux avec TVA si applicable
- Date génération automatique format français

**Template et mise en page :**
- Respect exact dimensions et couleurs modèle Boaz Study
- Logo positionné selon modèle (coin supérieur droit)
- Polices et tailles cohérentes avec modèle
- Tableau avec bordures et fond coloré header
- Formatage monétaire EUR/FCFA selon configuration

**Gestion fichiers et stockage :**
- Génération PDF en mémoire (bytes)
- Optionnel : sauvegarde temporaire sur disque avec cleanup
- Nom fichier format : "Proforma_[Reference]_[Date].pdf"
- Headers HTTP appropriés pour download/preview

**Procédure de test :**
1. Tester génération avec données souscription complètes
2. Vérifier intégration correcte informations organisation
3. Contrôler formatage visuel conforme modèle
4. Tester calculs totaux et formatage monétaire
5. Vérifier qualité PDF généré (polices, images, layout)
6. Tester avec différents noms clients (caractères spéciaux)
7. Vérifier performance génération (< 2 secondes)

---

### **Story 4.2 : Service génération Attestation logement + prise en charge PDF**
**Points d'estimation** : 5  
**Durée** : 1h15

**Description fonctionnelle :**
Développer le service de génération du document final "Attestation de logement et prise en charge" combiné (2 pages) selon le modèle Livin France fourni, adapté avec les informations Boaz-Housing.

**Description technique ultra-détaillée :**

**Service AttestationGenerator :**
- Méthode `generate_attestation_complete(souscription_data, organisation_data)` 
- Document PDF 2 pages : page 1 Attestation logement, page 2 Attestation prise en charge
- Structure identique modèle Livin France avec substitutions Boaz-Housing
- Intégration QR code et signature/cachet organisation

**Page 1 - Attestation de logement :**
- Header logo Boaz-Housing centré
- Titre "Attestation de logement" dans encadré noir
- Texte introduction adapté Boaz-Housing (remplace Livin-France.com)
- Bloc signataire : "Je soussigné, Benjamin YOHO BATOMO..." avec infos complètes organisation
- Informations client : nom complet, date/lieu naissance
- Détails logement : adresse, loyer mensuel
- Dates : entrée prévue, durée location
- Footer avec validité 45 jours et section authentification

**Page 2 - Attestation prise en charge :**
- Même header et introduction
- Même bloc signataire
- Liste services prise en charge : validation logement, assurance habitation, assurance voyage, compte bancaire, assurance maladie, visa
- Même footer authentification

**Éléments authentification :**
- QR Code généré avec URL verification : https://boaz-study.com/verify?ref=[Reference]
- Référence unique souscription format ATT-XXXXXXXXX
- Contact organisation : email info@boaz-study.fr, téléphone
- Date/lieu signature : "Fait à Corbeil-Essonnes, France, le [date]"
- Emplacement signature + cachet organisation (image si disponible)

**Mise en page et design :**
- Respect exact layout modèle Livin France
- Mêmes polices, espacements, tailles
- Logo adapté Boaz-Housing même position
- QR Code même taille et position
- Signature même emplacement

**Intégrations techniques :**
- Génération QR Code avec bibliothèque appropriée
- Intégration images logo et cachet depuis paths organisation.json
- Formatage dates français (JJ/MM/AAAA)
- Gestion retour ligne textes longs

**Procédure de test :**
1. Tester génération document 2 pages complet
2. Vérifier adaptation correcte textes Boaz-Housing
3. Contrôler intégration données client et logement
4. Tester génération QR Code avec URL valide
5. Vérifier positionnement logos, signature, cachet
6. Contrôler formatage dates et textes français
7. Comparer rendu final avec modèle Livin France

---

### **Story 4.3 : Endpoints API génération et preview documents**
**Points d'estimation** : 2  
**Durée** : 30 min

**Description fonctionnelle :**
Créer les endpoints API permettant la génération à la demande des documents PDF (Proforma et Attestation) avec possibilité de preview et download direct.

**Description technique ultra-détaillée :**

**Endpoints génération documents :**
- POST `/api/souscriptions/{id}/generate-proforma` : génération Proforma pour souscription donnée
- POST `/api/souscriptions/{id}/generate-attestation` : génération Attestation (statut >= "paye" requis)
- GET `/api/documents/proforma/{reference}` : récupération Proforma généré
- GET `/api/documents/attestation/{reference}` : récupération Attestation généré

**Headers et réponses :**
- Content-Type: application/pdf pour download direct
- Content-Disposition: attachment; filename="[nom].pdf" ou inline pour preview
- Headers CORS appropriés pour accès frontend
- Gestion cache avec ETags pour éviter régénérations inutiles

**Validations et sécurité :**
- Vérification existence souscription avant génération
- Validation statut souscription pour attestation finale
- Rate limiting pour éviter spam génération
- Validation référence format avant récupération document

**Intégration services PDF :**
- Appel services ProformaGenerator et AttestationGenerator
- Gestion erreurs génération avec codes HTTP appropriés
- Logging générations pour audit et debug
- Cleanup fichiers temporaires si utilisés

**Performance et optimisation :**
- Cache documents générés pour éviter régénérations
- Génération asynchrone possible pour gros volumes
- Compression PDF pour optimiser taille fichiers
- Timeout appropriés génération (max 10 secondes)

**Procédure de test :**
1. Tester génération Proforma avec souscription valide
2. Vérifier contrainte statut pour génération Attestation
3. Tester download et preview PDF depuis navigateur
4. Vérifier headers HTTP et noms fichiers
5. Tester gestion erreurs souscription inexistante
6. Vérifier performance et timeout
7. Tester cache et évitement régénérations

---

## **EPIC 5 : ENVOI D'EMAILS (0.5h)**

### **Story 5.1 : Service envoi emails avec pièces jointes**
**Points d'estimation** : 3  
**Durée** : 30 min

**Description fonctionnelle :**
Développer le service d'envoi d'emails automatiques pour l'envoi des documents PDF générés aux clients avec templates appropriés et gestion des erreurs d'envoi.

**Description technique ultra-détaillée :**

**Service EmailService :**
- Créer `app/services/email_service.py` avec classe EmailSender
- Configuration SMTP depuis variables environnement
- Méthodes `send_proforma(email_client, pdf_bytes, reference)` et `send_attestation(email_client, pdf_bytes, reference)`
- Support pièces jointes PDF avec noms appropriés

**Templates emails :**
- Template HTML pour email Proforma : objet "Votre Proforma Boaz-Housing - Ref: [reference]"
- Template HTML pour email Attestation : objet "Votre Attestation de logement - Ref: [reference]"
- Corps email avec informations Boaz-Housing et instructions client
- Footer avec coordonnées contact et mentions légales

**Configuration SMTP :**
- Variables environnement : SMTP_HOST, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, SMTP_USE_TLS
- Support Gmail, Outlook, serveurs SMTP personnalisés
- Authentification sécurisée avec gestion erreurs connexion
- From address configurable depuis organisation.json

**Gestion pièces jointes :**
- Attachment PDF depuis bytes en mémoire
- Noms fichiers : "Proforma_[Reference].pdf" et "Attestation_[Reference].pdf"
- Content-Type approprié application/pdf
- Taille limite pièce jointe (max 10MB)

**Gestion erreurs et retry :**
- Try/catch sur erreurs SMTP avec messages explicites
- Retry automatique max 3 fois en cas échec temporaire
- Logging envois réussis/échoués avec détails
- Timeout connexion SMTP (30 secondes)

**Integration API :**
- POST `/api/emails/send-proforma` : envoi Proforma avec génération si nécessaire
- POST `/api/emails/send-attestation` : envoi Attestation avec validation statut
- Réponses JSON avec status succès/erreur et messages
- Endpoint test connexion SMTP pour admin

**Procédure de test :**
1. Configurer SMTP test et vérifier connexion
2. Tester envoi Proforma avec PDF joint réel
3. Tester envoi Attestation avec validation statut
4. Vérifier réception emails avec formatting correct
5. Tester gestion erreurs SMTP et retry
6. Vérifier logs envois et debugging
7. Tester avec différents providers email (Gmail, Outlook)

---

## **RÉCAPITULATIF PLANIFICATION COMPLÈTE**

**Total estimé : 10h réparties comme suit :**
- Epic 1 (Infrastructure) : 2h
- Epic 2 (Gestion logements) : 2h  
- Epic 3 (Application admin) : 4h
- Epic 4 (Génération PDF) : 1.5h
- Epic 5 (Envoi emails) : 0.5h

**Points d'effort total : 56 points**
**Nombre de stories : 14 stories**
**Critères d'acceptation : définis pour chaque story**

Cette planification couvre l'intégralité du MVP Boaz-Housing selon les spécifications, avec descriptions ultra-détaillées permettant l'implémentation par IA sans intervention supplémentaire.

Souhaitez-vous que je détaille les **procédures de test finales** et **critères d'acceptation globaux** du MVP ?







