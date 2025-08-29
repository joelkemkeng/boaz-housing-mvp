# CHECKLIST TODO - BOAZ-HOUSING MVP

**Version :** 1.0  
**Date création :** 29/08/2025  
**Durée totale estimée :** 10h réparties sur 5 Epics  
**Points d'effort total :** 56 points  
**Nombre de stories :** 14 stories

---

## LÉGENDE STATUTS

- ⬜ **PENDING** : Non commencé
- 🔄 **IN_PROGRESS** : En cours
- ✅ **COMPLETED** : Terminé
- ❌ **BLOCKED** : Bloqué
- ⚠️ **NEEDS_REVIEW** : Nécessite révision

---

## EPIC 1 : INFRASTRUCTURE & SETUP (2h)

**Statut Epic :** ⬜ PENDING

### Story 1.1 : Configuration environnement de développement (45min)
**Points :** 3 | **Statut :** ⬜ PENDING

#### Backend FastAPI Setup
- [ ] ⬜ Créer structure projet backend avec dossiers app/, models/, schemas/, routers/, services/
- [ ] ⬜ Installer dépendances : fastapi, uvicorn, sqlalchemy, psycopg2-binary, alembic, pydantic, jinja2, reportlab
- [ ] ⬜ Configurer CORS pour requêtes React
- [ ] ⬜ Créer fichier database.py avec SQLAlchemy et connexion PostgreSQL
- [ ] ⬜ Configurer variables d'environnement (.env) : DATABASE_URL, SMTP settings

#### Frontend React Setup  
- [ ] ⬜ Créer application React avec create-react-app
- [ ] ⬜ Créer structure dossiers : components/(admin/bailleur/common), pages/, services/, utils/
- [ ] ⬜ Installer dépendances : axios, react-router-dom, react-hook-form, tailwindcss
- [ ] ⬜ Configurer Tailwind CSS
- [ ] ⬜ Créer service API de base avec axios

#### Database PostgreSQL Setup
- [ ] ⬜ Créer base de données "boaz_housing_mvp"
- [ ] ⬜ Configurer Alembic pour migrations
- [ ] ⬜ Préparer modèles de base (sans créer tables)

#### Tests Setup
- [ ] ⬜ Configurer pytest pour backend
- [ ] ⬜ Configurer Jest/React Testing Library pour frontend
- [ ] ⬜ Créer fichiers configuration de test

#### Procédure de test
- [ ] ⬜ Vérifier FastAPI démarre sur http://localhost:8000
- [ ] ⬜ Vérifier React démarre sur http://localhost:3000
- [ ] ⬜ Vérifier connexion PostgreSQL
- [ ] ⬜ Exécuter tests de base (0 tests)
- [ ] ⬜ Vérifier CORS fonctionne entre React et FastAPI

---

### Story 1.2 : Création des modèles de base de données (1h15)
**Points :** 5 | **Statut :** ⬜ PENDING

#### Modèle Logement
- [ ] ⬜ Créer classe Logement dans models/logement.py
- [ ] ⬜ Champs : id, adresse_complete, pays, ville, type_logement, type_occupation
- [ ] ⬜ Champs : superficie_m2, prix_hors_charges, prix_charges, prix_total (calculé)
- [ ] ⬜ Champs : statut (libre/occupe), created_at, updated_at
- [ ] ⬜ Relation avec souscriptions

#### Modèle Souscription  
- [ ] ⬜ Créer classe Souscription dans models/souscription.py
- [ ] ⬜ Champs : id, reference (ATT-XXXXXXXXX)
- [ ] ⬜ Informations client : nom, prénom, email, date_naissance, ville/pays_naissance
- [ ] ⬜ Informations client : nationalité, pays_destination, date_arrivee_prevue
- [ ] ⬜ Informations académiques : ecole_universite, filiere, pays/ville/code_postal/adresse_ecole
- [ ] ⬜ Informations logement : logement_id, date_entree_prevue, duree_location_mois
- [ ] ⬜ Statut et tracking : statut (attente_paiement/paye/livre/cloture/supprime)
- [ ] ⬜ Timestamps : created_at, updated_at
- [ ] ⬜ Relation avec logement

#### Schémas Pydantic
- [ ] ⬜ Créer schémas validation pour chaque modèle
- [ ] ⬜ Schémas création : LogementCreate, SouscriptionCreate
- [ ] ⬜ Schémas réponse : LogementResponse, SouscriptionResponse
- [ ] ⬜ Schémas mise à jour : LogementUpdate, SouscriptionUpdate

#### Migration Alembic
- [ ] ⬜ Générer migration initiale : `alembic revision --autogenerate -m "Initial migration"`
- [ ] ⬜ Appliquer migration : `alembic upgrade head`

#### Procédure de test
- [ ] ⬜ Exécuter migration et vérifier création tables
- [ ] ⬜ Tester insertion logement via SQLAlchemy
- [ ] ⬜ Tester insertion souscription liée à logement
- [ ] ⬜ Vérifier contraintes clés étrangères
- [ ] ⬜ Tester enums et contraintes
- [ ] ⬜ Vérifier génération automatique timestamps

---

### Story 1.3 : Configuration des données organisation statiques (30min)
**Points :** 2 | **Statut :** ⬜ PENDING

#### Création fichier JSON organisation
- [ ] ⬜ Créer fichier `app/data/organisation.json`
- [ ] ⬜ Structure JSON avec champs : nom, logo_path, site_web, ceo_nom_complet
- [ ] ⬜ Champs : ceo_date_naissance, ceo_ville_naissance, ceo_pays_naissance
- [ ] ⬜ Champs : adresse_siege, ville_rcs, numero_rcs, code_naf
- [ ] ⬜ Champs : email_contact, telephone, cachet_signature_path
- [ ] ⬜ Valeurs Boaz-Housing : nom="Boaz-Housing", site_web="www.boaz-study.com"
- [ ] ⬜ CEO="Benjamin YOHO BATOMO", adresse="14 Rue Jean Piestre, Corbeil-Essonnes, 91100, France"

#### Service de lecture JSON
- [ ] ⬜ Créer service `app/services/organisation_service.py`
- [ ] ⬜ Fonction get_organisation_info() retournant données parsées
- [ ] ⬜ Gestion erreurs lecture fichier
- [ ] ⬜ Cache en mémoire pour éviter lectures répétées

#### Endpoint API organisation
- [ ] ⬜ Créer router `app/routers/organisation.py`
- [ ] ⬜ Endpoint GET `/api/organisation` utilisant le service
- [ ] ⬜ Retourner informations organisation en JSON standardisé
- [ ] ⬜ Headers CORS appropriés

#### Schéma Pydantic Organisation
- [ ] ⬜ Créer `app/schemas/organisation.py` avec champs typés
- [ ] ⬜ Validation données lors lecture
- [ ] ⬜ Documentation OpenAPI automatique

#### Procédure de test
- [ ] ⬜ Vérifier fichier JSON bien formé et parsable
- [ ] ⬜ Tester service lecture avec fichier existant/inexistant
- [ ] ⬜ Tester endpoint `/api/organisation` et vérifier réponse
- [ ] ⬜ Vérifier données retournées conformes spécifications
- [ ] ⬜ Tester performance avec cache mémoire

---

## EPIC 2 : GESTION DES LOGEMENTS - APPLICATION BAILLEUR (2h)

**Statut Epic :** ⬜ PENDING

### Story 2.1 : API CRUD logements backend (1h15)
**Points :** 5 | **Statut :** ⬜ PENDING

#### Router logements
- [ ] ⬜ Créer `app/routers/logements.py` avec endpoints CRUD
- [ ] ⬜ GET `/api/logements` : récupérer tous logements avec pagination
- [ ] ⬜ GET `/api/logements/{id}` : récupérer logement spécifique
- [ ] ⬜ POST `/api/logements` : créer nouveau logement avec validation
- [ ] ⬜ PUT `/api/logements/{id}` : modifier logement existant
- [ ] ⬜ DELETE `/api/logements/{id}` : suppression logique (soft delete)

#### Logique métier création logement
- [ ] ⬜ Validation prix_total = prix_hors_charges + prix_charges (calcul automatique)
- [ ] ⬜ Vérification unicité adresse_complete (pas doublons)
- [ ] ⬜ Statut par défaut "libre" à création
- [ ] ⬜ Génération automatique timestamps created_at/updated_at

#### Logique métier modification logement
- [ ] ⬜ Si logement utilisé dans souscription payée, bloquer modification champs critiques
- [ ] ⬜ Permettre modification statut libre/occupé uniquement via logique métier souscription
- [ ] ⬜ Validation cohérence données avant sauvegarde

#### Logique métier suppression logement
- [ ] ⬜ Vérifier qu'aucune souscription active utilise ce logement
- [ ] ⬜ Soft delete : marquer deleted_at au lieu suppression physique
- [ ] ⬜ Conserver historique pour traçabilité

#### Gestion erreurs et validations
- [ ] ⬜ Validation formats (email si applicable, codes postaux)
- [ ] ⬜ Messages d'erreur explicites en français
- [ ] ⬜ Codes HTTP appropriés (201, 400, 404, 409)
- [ ] ⬜ Logging opérations importantes

#### Service logement
- [ ] ⬜ Créer `app/services/logement_service.py` avec logique métier
- [ ] ⬜ Fonctions pour vérifications business rules
- [ ] ⬜ Interface entre router et modèle database

#### Procédure de test
- [ ] ⬜ Tester création logement avec données valides/invalides
- [ ] ⬜ Vérifier calcul automatique prix_total
- [ ] ⬜ Tester récupération liste avec filtres
- [ ] ⬜ Tester modification avec/sans contraintes
- [ ] ⬜ Tester suppression logique et vérification contraintes
- [ ] ⬜ Vérifier validation unicité adresse
- [ ] ⬜ Tester gestion erreurs et codes retour HTTP

---

### Story 2.2 : Interface frontend gestion logements (1h30)
**Points :** 6 | **Statut :** ⬜ PENDING

#### Page principale BailleurDashboard
- [ ] ⬜ Composant `src/pages/BailleurDashboard.jsx` avec layout principal
- [ ] ⬜ Navigation simple avec section "Mes logements"
- [ ] ⬜ État global pour gestion logements (useState ou useContext)

#### Composant ListeLogements
- [ ] ⬜ Tableau responsive avec colonnes : Adresse, Ville, Type, Superficie, Prix total, Statut, Actions
- [ ] ⬜ Pagination si plus de 20 logements
- [ ] ⬜ Filtres simples par statut (libre/occupé) et ville
- [ ] ⬜ Actions par ligne : Voir, Modifier, Supprimer
- [ ] ⬜ Indicateur visuel statut (badge vert libre, rouge occupé)

#### Composant FormulaireLogement
- [ ] ⬜ Formulaire avec tous champs requis selon spécifications
- [ ] ⬜ Champs : adresse_complete (textarea), pays (select), ville (input)
- [ ] ⬜ Champs : type_logement (radio), type_occupation (select)
- [ ] ⬜ Champs : superficie_m2 (number), prix_hors_charges (number), prix_charges (number)
- [ ] ⬜ Calcul automatique prix_total en temps réel
- [ ] ⬜ Validation côté client avant soumission
- [ ] ⬜ Gestion états : création/modification avec mêmes champs

#### Gestion d'état et API calls
- [ ] ⬜ Service `src/services/logementsAPI.js` pour tous appels API
- [ ] ⬜ Gestion loading states pendant requêtes
- [ ] ⬜ Gestion erreurs avec affichage messages utilisateur
- [ ] ⬜ Refresh automatique liste après création/modification/suppression

#### Confirmations utilisateur
- [ ] ⬜ Modal confirmation avant suppression logement
- [ ] ⬜ Messages succès après opérations réussies
- [ ] ⬜ Gestion navigation retour après création/modification

#### Responsive design
- [ ] ⬜ Design mobile-first avec breakpoints appropriés
- [ ] ⬜ Tableau responsive avec scroll horizontal si nécessaire
- [ ] ⬜ Formulaires adaptés mobile

#### Procédure de test
- [ ] ⬜ Vérifier affichage liste logements vide et avec données
- [ ] ⬜ Tester création logement avec formulaire complet
- [ ] ⬜ Vérifier calcul automatique prix total
- [ ] ⬜ Tester modification logement existant
- [ ] ⬜ Tester suppression avec confirmation
- [ ] ⬜ Vérifier filtres et pagination
- [ ] ⬜ Tester responsive sur mobile et desktop
- [ ] ⬜ Vérifier gestion erreurs et messages utilisateur

---

### Story 2.3 : Validation statuts logements et contraintes métier (45min)
**Points :** 3 | **Statut :** ⬜ PENDING

#### Logique validation backend
- [ ] ⬜ Fonction `check_logement_usage(logement_id)` dans service logement
- [ ] ⬜ Vérification existence souscriptions liées avec statuts "payé", "livré", "clôturé"
- [ ] ⬜ Si logement utilisé, retourner erreur 409 Conflict avec message explicite
- [ ] ⬜ Permettre modification champs non-critiques uniquement

#### Endpoint validation contraintes
- [ ] ⬜ GET `/api/logements/{id}/can-modify` retourne booléen et raisons
- [ ] ⬜ GET `/api/logements/{id}/can-delete` retourne booléen et raisons
- [ ] ⬜ Utilisé par frontend avant affichage options modification/suppression

#### Gestion statuts automatiques
- [ ] ⬜ Lors validation souscription (statut "payé"), passer logement en "occupé"
- [ ] ⬜ Lors clôture souscription, possibilité remettre logement en "libre"
- [ ] ⬜ Historique changements statuts avec timestamps

#### Interface frontend contraintes
- [ ] ⬜ Appel API validation avant affichage boutons Modifier/Supprimer
- [ ] ⬜ Désactivation boutons avec tooltip explicatif si contraintes
- [ ] ⬜ Affichage indicateur "Utilisé dans attestation" sur logements occupés

#### Messages utilisateur
- [ ] ⬜ Messages d'erreur explicites : "Ce logement ne peut pas être modifié car utilisé dans attestation active"
- [ ] ⬜ Information preview avant actions : "Ce logement est libre et peut être modifié"

#### Procédure de test
- [ ] ⬜ Créer logement et vérifier qu'il peut être modifié/supprimé
- [ ] ⬜ Créer souscription liée et payer, vérifier blocage modification
- [ ] ⬜ Tester endpoints validation contraintes
- [ ] ⬜ Vérifier changement statut automatique lors paiement souscription
- [ ] ⬜ Tester affichage frontend avec contraintes actives/inactives
- [ ] ⬜ Vérifier messages d'erreur explicites côté utilisateur

---

## EPIC 3 : APPLICATION DE SOUSCRIPTION - ADMIN (4h)

**Statut Epic :** ⬜ PENDING

### Story 3.1 : API backend souscriptions CRUD (1h)
**Points :** 4 | **Statut :** ⬜ PENDING

#### Router souscriptions
- [ ] ⬜ Créer `app/routers/souscriptions.py` avec endpoints complets
- [ ] ⬜ GET `/api/souscriptions` : liste toutes souscriptions avec pagination et filtres statut
- [ ] ⬜ GET `/api/souscriptions/{id}` : détails souscription avec données logement jointes
- [ ] ⬜ POST `/api/souscriptions` : création nouvelle souscription statut "attente_paiement"
- [ ] ⬜ PUT `/api/souscriptions/{id}` : modification souscription existante
- [ ] ⬜ DELETE `/api/souscriptions/{id}` : suppression logique (statut "supprime")
- [ ] ⬜ PATCH `/api/souscriptions/{id}/status` : changement statut uniquement

#### Génération référence unique
- [ ] ⬜ Service `generate_reference()` format ATT-XXXXXXXXXXXXXX (16 caractères)
- [ ] ⬜ Vérification unicité référence en base avant attribution
- [ ] ⬜ Génération automatique lors création souscription

#### Logique métier statuts
- [ ] ⬜ Workflow strict : attente_paiement -> paye -> livre -> cloture
- [ ] ⬜ PATCH `/api/souscriptions/{id}/pay` : passage statut "paye" + trigger génération PDF + envoi email
- [ ] ⬜ Validation transitions statuts uniquement dans ordre logique
- [ ] ⬜ Blocage modification données client si statut >= "paye"

#### Gestion logements associés
- [ ] ⬜ Lors création souscription, vérifier logement statut "libre"
- [ ] ⬜ Lors passage statut "paye", changer logement en "occupe"
- [ ] ⬜ Validation cohérence dates (date_entree_prevue >= date_creation)

#### Jointures et relations
- [ ] ⬜ Récupération souscription avec données logement complètes
- [ ] ⬜ Optimisation requêtes avec eager loading SQLAlchemy
- [ ] ⬜ Formatage réponses avec toutes infos nécessaires frontend

#### Procédure de test
- [ ] ⬜ Tester création souscription avec génération référence unique
- [ ] ⬜ Vérifier workflow statuts et transitions autorisées/interdites
- [ ] ⬜ Tester modification avec contraintes selon statut
- [ ] ⬜ Vérifier changement statut logement lors paiement
- [ ] ⬜ Tester suppression logique et récupération avec filtres
- [ ] ⬜ Vérifier jointures et performances requêtes

---

### Story 3.2 : Page d'accueil admin avec sections services et historique (1h15)
**Points :** 5 | **Statut :** ⬜ PENDING

#### Composant AdminDashboard principal
- [ ] ⬜ Layout avec header Boaz-Housing et navigation simple
- [ ] ⬜ Deux sections principales : ServicesSection et HistoriqueSection
- [ ] ⬜ Gestion état global souscriptions avec useContext ou useState
- [ ] ⬜ Refresh automatique données après actions

#### Section Services (ServicesSection)
- [ ] ⬜ Card unique pour "Attestation de Logement et de Prise en Charge" selon spécifications MVP
- [ ] ⬜ Card contient : titre service, description courte, prix formaté EUR/FCFA, bouton "Souscrire"
- [ ] ⬜ Design card moderne avec hover effects
- [ ] ⬜ Bouton "Souscrire" déclenche ouverture wizard 4 étapes

#### Section Historique (HistoriqueSection)
- [ ] ⬜ Tableau responsive avec colonnes : Nom service, Nom prénom client, Date création, Statut, Actions
- [ ] ⬜ Pagination 10 souscriptions par page
- [ ] ⬜ Filtres par statut avec dropdowns
- [ ] ⬜ Badge coloré pour chaque statut (rouge=attente_paiement, bleu=paye, vert=livre, gris=cloture)

#### Actions disponibles par ligne
- [ ] ⬜ Bouton "Voir" : ouvre modal lecture seule avec tous détails
- [ ] ⬜ Bouton "Modifier" : ouvre wizard modification (si statut permet)
- [ ] ⬜ Bouton "Supprimer" : confirmation puis suppression logique
- [ ] ⬜ Bouton "Payer" : si statut="attente_paiement", lance processus paiement

#### Gestion états et interactions
- [ ] ⬜ Loading states pendant chargement données
- [ ] ⬜ Messages succès/erreur après actions
- [ ] ⬜ Confirmation modal avant suppressions
- [ ] ⬜ Refresh automatique liste après modifications

#### Responsive et UX
- [ ] ⬜ Design mobile-first avec collapse colonnes sur mobile
- [ ] ⬜ Actions groupées dans dropdown sur petits écrans
- [ ] ⬜ Skeleton loading pendant requêtes
- [ ] ⬜ Empty states avec messages appropriés

#### Procédure de test
- [ ] ⬜ Vérifier affichage correct des deux sections
- [ ] ⬜ Tester card service et bouton souscrire
- [ ] ⬜ Vérifier tableau historique avec données réelles et vides
- [ ] ⬜ Tester filtres par statut et pagination
- [ ] ⬜ Vérifier toutes actions (voir, modifier, supprimer, payer)
- [ ] ⬜ Tester responsive design sur différentes tailles écran
- [ ] ⬜ Vérifier loading states et gestion erreurs

---

### Story 3.3 : Wizard souscription étape 1 - Informations client (1h)
**Points :** 4 | **Statut :** ⬜ PENDING

#### Composant WizardSouscription principal
- [ ] ⬜ Stepper horizontal avec 4 étapes : Client, Académique, Logement, Proforma
- [ ] ⬜ Navigation entre étapes avec validation
- [ ] ⬜ Stockage données wizard dans état local React (useState)
- [ ] ⬜ Sauvegarde progressive optionnelle ou finale uniquement

#### Composant EtapeClient
- [ ] ⬜ Formulaire avec champs requis : nom, prénom, email, date_naissance
- [ ] ⬜ Champs : nationalité, pays_destination, date_arrivee_prevue
- [ ] ⬜ Validation temps réel avec react-hook-form
- [ ] ⬜ Format date_naissance : sélecteur date avec validation âge >= 16 ans
- [ ] ⬜ Liste pays avec autocomplete pour nationalité et pays_destination
- [ ] ⬜ Validation email avec regex appropriée

#### Validations spécifiques
- [ ] ⬜ Nom/prénom : minimum 2 caractères, pas caractères spéciaux
- [ ] ⬜ Email : format valide + vérification unicité côté backend optionnelle
- [ ] ⬜ Date naissance : âge minimum 16 ans, maximum 100 ans
- [ ] ⬜ Date arrivée prévue : minimum aujourd'hui + 1 jour, maximum 2 ans
- [ ] ⬜ Nationalité/pays : sélection depuis liste prédéfinie

#### Navigation wizard
- [ ] ⬜ Boutons "Précédent" (disabled étape 1) et "Suivant"
- [ ] ⬜ Validation complète avant passage étape suivante
- [ ] ⬜ Indicateur progression visuel avec étapes complétées
- [ ] ⬜ Sauvegarde état si utilisateur quitte et revient

#### Interface utilisateur
- [ ] ⬜ Design cohérent avec identité Boaz-Housing
- [ ] ⬜ Labels explicites et aide contextuelle
- [ ] ⬜ Messages erreur sous champs concernés
- [ ] ⬜ Formatage automatique champs (capitalisation noms, etc.)

#### Procédure de test
- [ ] ⬜ Vérifier affichage formulaire avec tous champs
- [ ] ⬜ Tester validations champs un par un
- [ ] ⬜ Vérifier validation âge et dates
- [ ] ⬜ Tester sélection pays avec autocomplete
- [ ] ⬜ Vérifier navigation disabled/enabled selon validation
- [ ] ⬜ Tester persistance données lors navigation
- [ ] ⬜ Vérifier responsive et accessibilité formulaire

---

### Story 3.4 : Wizard souscription étape 2 - Informations académiques (45min)
**Points :** 3 | **Statut :** ⬜ PENDING

#### Composant EtapeAcademique
- [ ] ⬜ Formulaire avec champs : école_universite, filière, pays_ecole
- [ ] ⬜ Champs : ville_ecole, code_postal_ecole, adresse_ecole
- [ ] ⬜ Intégration possible API géolocalisation pour suggestions adresses
- [ ] ⬜ Validation cohérence géographique pays/ville/code_postal

#### Champs spécifiques
- [ ] ⬜ École/université : input text avec suggestions écoles connues (liste prédéfinie)
- [ ] ⬜ Filière : input text libre avec suggestions communes (informatique, ingénierie, etc.)
- [ ] ⬜ Pays école : select avec liste pays complet
- [ ] ⬜ Ville école : input text avec validation selon pays sélectionné
- [ ] ⬜ Code postal : format selon pays (validation regex dynamique)
- [ ] ⬜ Adresse école : textarea pour adresse complète

#### Validations dynamiques
- [ ] ⬜ Code postal format selon pays sélectionné
- [ ] ⬜ Vérification cohérence ville/pays si API disponible
- [ ] ⬜ Longueur minimum adresse complète (10 caractères)
- [ ] ⬜ École/université minimum 3 caractères

#### Assistance saisie
- [ ] ⬜ Autocomplete écoles populaires par pays
- [ ] ⬜ Suggestions filières courantes
- [ ] ⬜ Formatage automatique adresses (capitalisation)
- [ ] ⬜ Validation temps réel avec indicateurs visuels

#### Navigation et persistance
- [ ] ⬜ Boutons "Précédent" (retour étape 1 avec données) et "Suivant"
- [ ] ⬜ Validation obligatoire tous champs avant progression
- [ ] ⬜ Sauvegarde automatique données dans état wizard
- [ ] ⬜ Possibilité retour modification étape précédente

#### Procédure de test
- [ ] ⬜ Vérifier tous champs présents et fonctionnels
- [ ] ⬜ Tester validations format code postal selon pays
- [ ] ⬜ Vérifier suggestions écoles et filières
- [ ] ⬜ Tester navigation retour avec persistance données étape 1
- [ ] ⬜ Vérifier validation complète avant étape suivante
- [ ] ⬜ Tester autocomplétion et formatage automatique
- [ ] ⬜ Vérifier responsive design formulaire

---

### Story 3.5 : Wizard souscription étape 3 - Choix logement (1h15)
**Points :** 5 | **Statut :** ⬜ PENDING

#### Composant EtapeLogement
- [ ] ⬜ Récupération logements statut "libre" via API GET `/api/logements?statut=libre`
- [ ] ⬜ Affichage grid responsive de cards logements
- [ ] ⬜ Sélection unique avec indication visuelle choix actuel
- [ ] ⬜ Données chaque card selon spécifications exactes

#### Contenu cards logements
- [ ] ⬜ Adresse complète logement (titre principal)
- [ ] ⬜ Pays et ville (sous-titre)
- [ ] ⬜ Type occupation (Individuel/Colocation/Autre) avec badge
- [ ] ⬜ Type logement (Chambre/Appartement/Studio) avec icône
- [ ] ⬜ Superficie en m² avec unité
- [ ] ⬜ Prix hors charges formaté
- [ ] ⬜ Prix charges formaté
- [ ] ⬜ Prix total TTC mis en évidence (couleur différente)

#### Interaction et sélection
- [ ] ⬜ Cards cliquables avec effet hover
- [ ] ⬜ Sélection unique avec border colorée et checkmark
- [ ] ⬜ Bouton radio invisible mais state géré
- [ ] ⬜ Animation transition lors sélection/déselection

#### Filtrage et recherche
- [ ] ⬜ Filtre par ville (dropdown pays puis villes)
- [ ] ⬜ Filtre par type logement (checkboxes multiples)
- [ ] ⬜ Filtre par fourchette prix avec slider
- [ ] ⬜ Tri par prix croissant/décroissant

#### Gestion états
- [ ] ⬜ Loading pendant récupération logements
- [ ] ⬜ Message si aucun logement disponible
- [ ] ⬜ Gestion erreurs API avec retry possible
- [ ] ⬜ Validation sélection obligatoire avant étape suivante

#### Responsive design
- [ ] ⬜ Grid adaptatif : 1 colonne mobile, 2-3 colonnes tablet/desktop
- [ ] ⬜ Cards optimisées taille écran
- [ ] ⬜ Filtres collapse sur mobile

#### Procédure de test
- [ ] ⬜ Vérifier récupération et affichage logements libres uniquement
- [ ] ⬜ Tester contenu complet cards selon spécifications
- [ ] ⬜ Vérifier sélection unique avec indicateurs visuels
- [ ] ⬜ Tester filtres ville, type, prix
- [ ] ⬜ Vérifier tri par prix
- [ ] ⬜ Tester responsive grid et cards
- [ ] ⬜ Vérifier validation sélection avant progression
- [ ] ⬜ Tester gestion cas aucun logement disponible

---

### Story 3.6 : Wizard souscription étape 4 - Génération et prévisualisation Proforma (1h)
**Points :** 4 | **Statut :** ⬜ PENDING

#### Composant EtapeProforma
- [ ] ⬜ Récapitulatif complet données saisies (client + académique + logement)
- [ ] ⬜ Génération automatique référence ATT-XXXX lors affichage étape
- [ ] ⬜ Appel API génération Proforma avec toutes données collectées
- [ ] ⬜ Interface preview avec actions multiples selon spécifications

#### Récapitulatif données
- [ ] ⬜ Section "Informations client" : affichage formaté données étape 1
- [ ] ⬜ Section "Informations académiques" : affichage formaté données étape 2
- [ ] ⬜ Section "Logement sélectionné" : card résumé avec prix
- [ ] ⬜ Section "Résumé financier" : prix logement + éventuels frais service

#### Génération Proforma
- [ ] ⬜ Appel API POST `/api/souscriptions` avec données complètes wizard
- [ ] ⬜ API retourne ID souscription + URL preview PDF Proforma
- [ ] ⬜ Affichage preview PDF dans iframe ou viewer intégré
- [ ] ⬜ Loading states pendant génération document

#### Actions disponibles
- [ ] ⬜ Bouton "Retour" : modification données (retour étapes précédentes)
- [ ] ⬜ Bouton "Télécharger Proforma" : download direct PDF généré
- [ ] ⬜ Bouton "Envoyer par Email" : envoi email client avec Proforma joint
- [ ] ⬜ Bouton "Terminer" : finalisation et retour accueil avec refresh historique

#### Gestion envoi email
- [ ] ⬜ Modal confirmation avec email pré-rempli (modifiable)
- [ ] ⬜ Message personnalisable optionnel
- [ ] ⬜ Confirmation envoi avec message succès
- [ ] ⬜ Gestion erreurs envoi avec possibilité retry

#### Finalisation souscription
- [ ] ⬜ Sauvegarde définitive en base statut "attente_paiement"
- [ ] ⬜ Nettoyage état wizard
- [ ] ⬜ Redirection accueil avec message succès
- [ ] ⬜ Ajout automatique dans historique

#### Procédure de test
- [ ] ⬜ Vérifier affichage récapitulatif complet données wizard
- [ ] ⬜ Tester génération Proforma et preview PDF
- [ ] ⬜ Vérifier téléchargement PDF fonctionnel
- [ ] ⬜ Tester envoi email avec confirmation
- [ ] ⬜ Vérifier bouton retour et modification données
- [ ] ⬜ Tester finalisation avec sauvegarde base et redirection
- [ ] ⬜ Vérifier nettoyage état wizard après finalisation
- [ ] ⬜ Tester gestion erreurs génération/envoi

---

## EPIC 4 : GÉNÉRATION DOCUMENTS PDF (1.5h)

**Statut Epic :** ⬜ PENDING

### Story 4.1 : Service génération Proforma PDF (1h)
**Points :** 4 | **Statut :** ⬜ PENDING

#### Service PDFGenerator
- [ ] ⬜ Créer `app/services/pdf_generator.py` avec classe ProformaGenerator
- [ ] ⬜ Utilisation bibliothèque ReportLab pour génération PDF programmatique
- [ ] ⬜ Template basé sur modèle Boaz Study fourni dans spécifications
- [ ] ⬜ Méthode `generate_proforma(souscription_data, organisation_data)` retournant bytes PDF

#### Structure document Proforma
- [ ] ⬜ Header avec logo Boaz-Housing (path depuis organisation.json)
- [ ] ⬜ Titre "FACTURE" avec date génération
- [ ] ⬜ Bloc informations organisation : nom, adresse, contacts, infos légales (RCS, NAF, etc.)
- [ ] ⬜ Section client : nom, adresse email
- [ ] ⬜ Tableau services avec colonnes : Description, Qté, Prix unitaire, Montant
- [ ] ⬜ Total HT et TTC
- [ ] ⬜ Footer avec mentions légales et conditions

#### Données dynamiques intégrées
- [ ] ⬜ Informations organisation depuis JSON : nom, adresse, téléphone, email, RCS, NAF
- [ ] ⬜ Informations client depuis souscription : nom complet, email
- [ ] ⬜ Services et prix : ligne principale "Frais Attestation de Logement" + autres frais selon business model
- [ ] ⬜ Calculs automatiques totaux avec TVA si applicable
- [ ] ⬜ Date génération automatique format français

#### Template et mise en page
- [ ] ⬜ Respect exact dimensions et couleurs modèle Boaz Study
- [ ] ⬜ Logo positionné selon modèle (coin supérieur droit)
- [ ] ⬜ Polices et tailles cohérentes avec modèle
- [ ] ⬜ Tableau avec bordures et fond coloré header
- [ ] ⬜ Formatage monétaire EUR/FCFA selon configuration

#### Gestion fichiers et stockage
- [ ] ⬜ Génération PDF en mémoire (bytes)
- [ ] ⬜ Optionnel : sauvegarde temporaire sur disque avec cleanup
- [ ] ⬜ Nom fichier format : "Proforma_[Reference]_[Date].pdf"
- [ ] ⬜ Headers HTTP appropriés pour download/preview

#### Procédure de test
- [ ] ⬜ Tester génération avec données souscription complètes
- [ ] ⬜ Vérifier intégration correcte informations organisation
- [ ] ⬜ Contrôler formatage visuel conforme modèle
- [ ] ⬜ Tester calculs totaux et formatage monétaire
- [ ] ⬜ Vérifier qualité PDF généré (polices, images, layout)
- [ ] ⬜ Tester avec différents noms clients (caractères spéciaux)
- [ ] ⬜ Vérifier performance génération (< 2 secondes)

---

### Story 4.2 : Service génération Attestation logement + prise en charge PDF (1h15)
**Points :** 5 | **Statut :** ⬜ PENDING

#### Service AttestationGenerator
- [ ] ⬜ Méthode `generate_attestation_complete(souscription_data, organisation_data)`
- [ ] ⬜ Document PDF 2 pages : page 1 Attestation logement, page 2 Attestation prise en charge
- [ ] ⬜ Structure identique modèle Livin France avec substitutions Boaz-Housing
- [ ] ⬜ Intégration QR code et signature/cachet organisation

#### Page 1 - Attestation de logement
- [ ] ⬜ Header logo Boaz-Housing centré
- [ ] ⬜ Titre "Attestation de logement" dans encadré noir
- [ ] ⬜ Texte introduction adapté Boaz-Housing (remplace Livin-France.com)
- [ ] ⬜ Bloc signataire : "Je soussigné, Benjamin YOHO BATOMO..." avec infos complètes organisation
- [ ] ⬜ Informations client : nom complet, date/lieu naissance
- [ ] ⬜ Détails logement : adresse, loyer mensuel
- [ ] ⬜ Dates : entrée prévue, durée location
- [ ] ⬜ Footer avec validité 45 jours et section authentification

#### Page 2 - Attestation prise en charge
- [ ] ⬜ Même header et introduction
- [ ] ⬜ Même bloc signataire
- [ ] ⬜ Liste services prise en charge : validation logement, assurance habitation
- [ ] ⬜ Services : assurance voyage, compte bancaire, assurance maladie, visa
- [ ] ⬜ Même footer authentification

#### Éléments authentification
- [ ] ⬜ QR Code généré avec URL verification : https://boaz-study.com/verify?ref=[Reference]
- [ ] ⬜ Référence unique souscription format ATT-XXXXXXXXX
- [ ] ⬜ Contact organisation : email info@boaz-study.fr, téléphone
- [ ] ⬜ Date/lieu signature : "Fait à Corbeil-Essonnes, France, le [date]"
- [ ] ⬜ Emplacement signature + cachet organisation (image si disponible)

#### Mise en page et design
- [ ] ⬜ Respect exact layout modèle Livin France
- [ ] ⬜ Mêmes polices, espacements, tailles
- [ ] ⬜ Logo adapté Boaz-Housing même position
- [ ] ⬜ QR Code même taille et position
- [ ] ⬜ Signature même emplacement

#### Intégrations techniques
- [ ] ⬜ Génération QR Code avec bibliothèque appropriée
- [ ] ⬜ Intégration images logo et cachet depuis paths organisation.json
- [ ] ⬜ Formatage dates français (JJ/MM/AAAA)
- [ ] ⬜ Gestion retour ligne textes longs

#### Procédure de test
- [ ] ⬜ Tester génération document 2 pages complet
- [ ] ⬜ Vérifier adaptation correcte textes Boaz-Housing
- [ ] ⬜ Contrôler intégration données client et logement
- [ ] ⬜ Tester génération QR Code avec URL valide
- [ ] ⬜ Vérifier positionnement logos, signature, cachet
- [ ] ⬜ Contrôler formatage dates et textes français
- [ ] ⬜ Comparer rendu final avec modèle Livin France

---

### Story 4.3 : Endpoints API génération et preview documents (30min)
**Points :** 2 | **Statut :** ⬜ PENDING

#### Endpoints génération documents
- [ ] ⬜ POST `/api/souscriptions/{id}/generate-proforma` : génération Proforma pour souscription donnée
- [ ] ⬜ POST `/api/souscriptions/{id}/generate-attestation` : génération Attestation (statut >= "paye" requis)
- [ ] ⬜ GET `/api/documents/proforma/{reference}` : récupération Proforma généré
- [ ] ⬜ GET `/api/documents/attestation/{reference}` : récupération Attestation généré

#### Headers et réponses
- [ ] ⬜ Content-Type: application/pdf pour download direct
- [ ] ⬜ Content-Disposition: attachment; filename="[nom].pdf" ou inline pour preview
- [ ] ⬜ Headers CORS appropriés pour accès frontend
- [ ] ⬜ Gestion cache avec ETags pour éviter régénérations inutiles

#### Validations et sécurité
- [ ] ⬜ Vérification existence souscription avant génération
- [ ] ⬜ Validation statut souscription pour attestation finale
- [ ] ⬜ Rate limiting pour éviter spam génération
- [ ] ⬜ Validation référence format avant récupération document

#### Intégration services PDF
- [ ] ⬜ Appel services ProformaGenerator et AttestationGenerator
- [ ] ⬜ Gestion erreurs génération avec codes HTTP appropriés
- [ ] ⬜ Logging générations pour audit et debug
- [ ] ⬜ Cleanup fichiers temporaires si utilisés

#### Performance et optimisation
- [ ] ⬜ Cache documents générés pour éviter régénérations
- [ ] ⬜ Génération asynchrone possible pour gros volumes
- [ ] ⬜ Compression PDF pour optimiser taille fichiers
- [ ] ⬜ Timeout appropriés génération (max 10 secondes)

#### Procédure de test
- [ ] ⬜ Tester génération Proforma avec souscription valide
- [ ] ⬜ Vérifier contrainte statut pour génération Attestation
- [ ] ⬜ Tester download et preview PDF depuis navigateur
- [ ] ⬜ Vérifier headers HTTP et noms fichiers
- [ ] ⬜ Tester gestion erreurs souscription inexistante
- [ ] ⬜ Vérifier performance et timeout
- [ ] ⬜ Tester cache et évitement régénérations

---

## EPIC 5 : ENVOI D'EMAILS (0.5h)

**Statut Epic :** ⬜ PENDING

### Story 5.1 : Service envoi emails avec pièces jointes (30min)
**Points :** 3 | **Statut :** ⬜ PENDING

#### Service EmailService
- [ ] ⬜ Créer `app/services/email_service.py` avec classe EmailSender
- [ ] ⬜ Configuration SMTP depuis variables environnement
- [ ] ⬜ Méthodes `send_proforma(email_client, pdf_bytes, reference)` et `send_attestation(email_client, pdf_bytes, reference)`
- [ ] ⬜ Support pièces jointes PDF avec noms appropriés

#### Templates emails
- [ ] ⬜ Template HTML pour email Proforma : objet "Votre Proforma Boaz-Housing - Ref: [reference]"
- [ ] ⬜ Template HTML pour email Attestation : objet "Votre Attestation de logement - Ref: [reference]"
- [ ] ⬜ Corps email avec informations Boaz-Housing et instructions client
- [ ] ⬜ Footer avec coordonnées contact et mentions légales

#### Configuration SMTP
- [ ] ⬜ Variables environnement : SMTP_HOST, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, SMTP_USE_TLS
- [ ] ⬜ Support Gmail, Outlook, serveurs SMTP personnalisés
- [ ] ⬜ Authentification sécurisée avec gestion erreurs connexion
- [ ] ⬜ From address configurable depuis organisation.json

#### Gestion pièces jointes
- [ ] ⬜ Attachment PDF depuis bytes en mémoire
- [ ] ⬜ Noms fichiers : "Proforma_[Reference].pdf" et "Attestation_[Reference].pdf"
- [ ] ⬜ Content-Type approprié application/pdf
- [ ] ⬜ Taille limite pièce jointe (max 10MB)

#### Gestion erreurs et retry
- [ ] ⬜ Try/catch sur erreurs SMTP avec messages explicites
- [ ] ⬜ Retry automatique max 3 fois en cas échec temporaire
- [ ] ⬜ Logging envois réussis/échoués avec détails
- [ ] ⬜ Timeout connexion SMTP (30 secondes)

#### Integration API
- [ ] ⬜ POST `/api/emails/send-proforma` : envoi Proforma avec génération si nécessaire
- [ ] ⬜ POST `/api/emails/send-attestation` : envoi Attestation avec validation statut
- [ ] ⬜ Réponses JSON avec status succès/erreur et messages
- [ ] ⬜ Endpoint test connexion SMTP pour admin

#### Procédure de test
- [ ] ⬜ Configurer SMTP test et vérifier connexion
- [ ] ⬜ Tester envoi Proforma avec PDF joint réel
- [ ] ⬜ Tester envoi Attestation avec validation statut
- [ ] ⬜ Vérifier réception emails avec formatting correct
- [ ] ⬜ Tester gestion erreurs SMTP et retry
- [ ] ⬜ Vérifier logs envois et debugging
- [ ] ⬜ Tester avec différents providers email (Gmail, Outlook)

---

## RÉCAPITULATIF FINAL

### Statistiques
- **Total Epic :** 5 Epics
- **Total Stories :** 14 Stories
- **Total Points :** 56 Points d'effort
- **Durée Estimée :** 10 heures
- **Total Tâches :** 247 tâches individuelles

### Répartition par Epic
- **Epic 1** - Infrastructure : 2h (3 stories, 10 points)
- **Epic 2** - Gestion Logements : 2h (3 stories, 14 points)
- **Epic 3** - Application Admin : 4h (6 stories, 21 points)
- **Epic 4** - Génération PDF : 1.5h (3 stories, 11 points)
- **Epic 5** - Envoi Emails : 0.5h (1 story, 3 points)

### Progression Globale MVP
- ⬜ **EPIC 1** : 0/3 stories complétées
- ⬜ **EPIC 2** : 0/3 stories complétées
- ⬜ **EPIC 3** : 0/6 stories complétées
- ⬜ **EPIC 4** : 0/3 stories complétées
- ⬜ **EPIC 5** : 0/1 story complétée

**PROGRESSION TOTALE : 0/14 stories (0%)**

---

*Dernière mise à jour : 29/08/2025*  
*Fichier généré automatiquement depuis planification détaillée*