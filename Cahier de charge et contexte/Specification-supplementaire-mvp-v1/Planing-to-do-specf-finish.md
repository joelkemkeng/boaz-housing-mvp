# PLAN DE DÉVELOPPEMENT - FINALISATION MVP BOAZ HOUSING

## 📋 ANALYSE DU PROJET EXISTANT

### État Actuel du Code Base
- ✅ **Backend FastAPI** : Structure fonctionnelle avec modèles Souscription et Logement
- ✅ **Frontend React** : Interface admin basique opérationnelle
- ✅ **Base de données** : SQLAlchemy avec modèles de base
- ✅ **Services** : Génération PDF (proforma, attestations), envoi email
- ❌ **Gestion des utilisateurs** : Pas de modèles User/Role (simple, sans JWT)
- ❌ **Gestion des statuts avancés** : Manque "Attente Livraison", "Clôturé"
- ❌ **Upload de preuves de paiement** : Non implémenté
- ❌ **CRON automatisations** : Absent
- ❌ **Interfaces spécialisées par rôle** : Inexistantes

---

## 🚀 PLAN DE DÉVELOPPEMENT PAR PHASES

### **PHASE 1 : SYSTÈME UTILISATEUR AVEC LOGIN BASIQUE** 
*Durée estimée : 1-2 jours*

#### 1.1 Modèle Utilisateur avec Password (Backend)
**Objectif** : Créer structure basique pour les utilisateurs avec authentification simple

**Tâches** :
- [ ] Créer `app/models/user.py` avec modèle User
- [ ] Définir enum UserRole (CLIENT, AGENT-BOAZ, ADMIN-GENERALE, BAILLEUR)
- [ ] Champs : id, email, nom, prenom, password_hash, role, active
- [ ] **Hash password simple avec passlib (PAS de JWT, PAS de sessions complexes)**
- [ ] Créer migration Alembic pour table users
- [ ] Créer schémas Pydantic dans `app/schemas/user.py` (UserCreate avec password, UserResponse sans password)

**Critères d'acceptation** :
- ✅ Table users créée avec password_hash
- ✅ Hash password basique fonctionnel
- ✅ Migration DB opérationnelle

#### 1.2 Login/Auth Simple (Backend)
**Objectif** : API de connexion basique email/password

**Tâches** :
- [ ] Créer `app/services/auth_service.py` simple :
  - `hash_password()` et `verify_password()` avec passlib
  - `authenticate_user(email, password)` → retourne User ou None
- [ ] Créer `app/routers/auth.py` avec endpoints :
  - `POST /api/auth/login` (email + password → retourne user info)
  - `POST /api/auth/register` (créer utilisateur avec password)
- [ ] Créer `app/routers/users.py` pour CRUD utilisateurs
- [ ] **PAS de JWT, PAS de tokens - juste validation email/password**

**Critères d'acceptation** :
- ✅ Login email/password fonctionnel
- ✅ Retour des infos utilisateur après connexion
- ✅ Création utilisateur avec password

#### 1.3 Données d'exemple avec Passwords (Backend)
**Objectif** : Créer les utilisateurs de test avec mots de passe

**Tâches** :
- [ ] Script de seed `app/scripts/seed_users.py`
- [ ] Créer users par défaut avec passwords :
  - agent@boaz-study.com / agent1234 (AGENT-BOAZ)
  - bailleur@boaz-study.com / bailleur1234 (BAILLEUR) 
  - ceo@boaz-study.com / ceo1234 (ADMIN-GENERALE)
- [ ] Hash des passwords lors du seed
- [ ] Intégrer seed dans startup de l'application

**Critères d'acceptation** :
- ✅ 3 utilisateurs créés avec passwords hashés
- ✅ Connexion possible avec email/password
- ✅ Roles correctement assignés

**Tests Phase 1** :
```bash
pytest backend/tests/test_auth.py -v
curl -X POST "http://localhost:8000/api/auth/login" -H "Content-Type: application/json" -d '{"email":"agent@boaz-study.com","password":"agent1234"}'
```

---

### **PHASE 2 : GESTION AVANCÉE DES STATUTS** 
*Durée estimée : 2 jours*

#### 2.1 Extension du Modèle Souscription
**Objectif** : Ajouter les nouveaux statuts et champs requis

**Tâches** :
- [ ] Modifier `StatutSouscription` enum : + ATTENTE_LIVRAISON, CLOTURE
- [ ] Ajouter champs dans modèle Souscription :
  - `date_livraison` (Date, nullable)
  - `date_expiration` (Date, nullable) 
  - `preuve_paiement_path` (String, nullable)
  - `cree_par_user_id` (ForeignKey vers User, nullable)
- [ ] Créer migration Alembic
- [ ] Mettre à jour les schémas Pydantic

**Critères d'acceptation** :
- ✅ Nouveaux statuts disponibles
- ✅ Champs supplémentaires en base de données
- ✅ Transitions de statuts basiques

#### 2.2 Logique Métier des Statuts
**Objectif** : Implémenter les règles de transition des statuts

**Tâches** :
- [ ] Modifier `app/services/souscription_service.py` :
  - Fonction `payer_souscription()` : ATTENTE_PAIEMENT → ATTENTE_LIVRAISON
  - Fonction `livrer_souscription()` : ATTENTE_LIVRAISON → LIVRE (+ calcul date_expiration avec services.json)
  - Fonction `valider_logement_disponible()` avant livraison
- [ ] Ajouter endpoints pour nouvelles actions dans `app/routers/souscriptions.py`
- [ ] Simple validation des transitions

**Critères d'acceptation** :
- ✅ Actions "Payer" et "Livrer" fonctionnelles
- ✅ Date d'expiration calculée selon durée validité service
- ✅ Vérification logement disponible avant livraison

**Tests Phase 2** :
```bash
pytest backend/tests/test_souscription_statuts.py -v
```

---

### **PHASE 3 : UPLOAD DES PREUVES DE PAIEMENT** 
*Durée estimée : 2 jours*

#### 3.1 Upload de Fichiers (Backend)
**Objectif** : Permettre l'upload de preuves de paiement

**Tâches** :
- [ ] Créer `app/services/file_upload_service.py`
- [ ] Support upload images (JPG, PNG) et documents (PDF)
- [ ] Conversion automatique images → PDF (avec Pillow)
- [ ] Stockage dans `backend/app/uploads/preuves_paiement/`
- [ ] Validation basique taille/type de fichiers
- [ ] Endpoint `POST /api/souscriptions/{id}/upload-preuve-paiement`

**Critères d'acceptation** :
- ✅ Upload multi-formats fonctionnel
- ✅ Conversion automatique image→PDF
- ✅ Stockage avec noms de fichiers uniques
- ✅ Validation basique des fichiers

#### 3.2 Intégration Action "Payer" 
**Objectif** : Combiner upload + changement de statut

**Tâches** :
- [ ] Modifier l'action "Payer" pour accepter un fichier optionnel
- [ ] Mettre à jour `preuve_paiement_path` lors du paiement
- [ ] Endpoint pour visualiser/télécharger la preuve
- [ ] Gestion des erreurs simple

**Critères d'acceptation** :
- ✅ Action "Payer" avec upload optionnel
- ✅ Preuve accessible via API
- ✅ Workflow simple et direct

**Tests Phase 3** :
```bash
curl -X POST -F "file=@preuve.jpg" "http://localhost:8000/api/souscriptions/1/upload-preuve-paiement"
```

---

### **PHASE 4 : INTERFACES UTILISATEUR PAR RÔLE** 
*Durée estimée : 3-4 jours*

#### 4.1 Formulaire de Connexion (Frontend)
**Objectif** : Interface de connexion avec email/password

**Tâches** :
- [ ] Créer `src/components/auth/LoginForm.js` (email + password)
- [ ] Créer `src/contexts/AuthContext.js` (stockage utilisateur actuel)
- [ ] Service `src/services/authService.js` (appel API login)
- [ ] Stockage utilisateur en localStorage (pas de token, juste user info)
- [ ] Redirection selon rôle après connexion réussie
- [ ] Gestion des erreurs de connexion (mauvais email/password)
- [ ] Bouton logout simple

**Critères d'acceptation** :
- ✅ Connexion email/password fonctionnelle
- ✅ Stockage utilisateur après login
- ✅ Redirection automatique selon rôle
- ✅ Gestion des erreurs basique

#### 4.2 Interface AGENT-BOAZ
**Objectif** : Dashboard spécialisé pour les agents

**Tâches** :
- [ ] Créer `src/pages/AgentDashboard.js`
- [ ] Composant `src/components/agent/SouscriptionForm.js` (création souscription)
- [ ] Composant `src/components/agent/PaymentUpload.js` (action payer + upload)
- [ ] Composant `src/components/agent/SouscriptionStats.js` (stats par statut)
- [ ] Navigation simple spécifique aux agents
- [ ] Masquer fonctions non autorisées (via rôle utilisateur)

**Critères d'acceptation** :
- ✅ Interface épurée pour agents uniquement
- ✅ Création de souscription fluide
- ✅ Upload de preuves de paiement intégré
- ✅ Statistiques visuelles simples

#### 4.3 Interface BAILLEUR
**Objectif** : Dashboard pour la gestion des logements

**Tâches** :
- [ ] Créer `src/pages/BailleurDashboard.js`
- [ ] Adapter composants logement existants 
- [ ] Composant `src/components/bailleur/LogementStats.js`
- [ ] Navigation spécifique bailleur
- [ ] Ajouter champ `proprietaire_email` dans modèle Logement (optionnel)
- [ ] Filtrage des logements par bailleur (côté frontend)

**Critères d'acceptation** :
- ✅ CRUD logements pour bailleurs
- ✅ Statistiques logements simples
- ✅ Interface responsive et intuitive

#### 4.4 Interface ADMIN-GENERALE - Extensions
**Objectif** : Étendre l'interface admin existante

**Tâches** :
- [ ] Modifier `src/components/admin/SouscriptionViewModal.js` :
  - Affichage preuve de paiement (si statut ATTENTE_LIVRAISON)
  - Bouton "Livrer" (si statut ATTENTE_LIVRAISON)
  - Prévisualisation attestations
- [ ] Créer `src/components/admin/UserManagement.js` (gestion utilisateurs)
- [ ] Accès à toutes les fonctionnalités existantes
- [ ] Navigation admin complète

**Critères d'acceptation** :
- ✅ Livraison des souscriptions avec vérifications
- ✅ Visualisation des preuves de paiement
- ✅ Gestion basique des utilisateurs
- ✅ Accès complet aux fonctionnalités

**Tests Phase 4** :
- Tests manuels interfaces utilisateur
- Vérification affichage selon rôles
- Tests responsive mobile

---

### **PHASE 5 : AUTOMATISATIONS CRON** 
*Durée estimée : 1-2 jours*

#### 5.1 Service de Clôture Automatique
**Objectif** : Automatiser la clôture des souscriptions expirées

**Tâches** :
- [ ] Créer `app/services/cron_service.py`
- [ ] Fonction `cloturer_souscriptions_expirees()` :
  - Identifier souscriptions LIVRE avec date_expiration < aujourd'hui
  - Changer statut LIVRE → CLOTURE
  - Si service ID 1 (attestation hébergement) : logement OCCUPE → DISPONIBLE
- [ ] Simple logging des actions
- [ ] Script exécutable `app/scripts/run_cron.py`

**Critères d'acceptation** :
- ✅ Clôture automatique fonctionnelle
- ✅ Libération logements appropriée
- ✅ Logs basiques des actions
- ✅ Script manuel exécutable

#### 5.2 Documentation CRON
**Objectif** : Documenter l'usage du CRON

**Tâches** :
- [ ] Documentation setup cron système (crontab)
- [ ] Tests du service cron
- [ ] Configuration recommandée (quotidien)

**Tests Phase 5** :
```bash
python backend/app/scripts/run_cron.py  # Test manuel
```

---

### **PHASE 6 : TESTS ET FINALISATION** 
*Durée estimée : 1-2 jours*

#### 6.1 Tests Essentiels
**Objectif** : Validation des fonctionnalités critiques

**Tâches** :
- [ ] Tests unitaires services principaux
- [ ] Tests endpoints API critiques
- [ ] Tests manuels workflow complet
- [ ] Validation upload fichiers
- [ ] Tests des 3 interfaces utilisateur

#### 6.2 Documentation et Déploiement
**Objectif** : Préparer le MVP pour usage

**Tâches** :
- [ ] Documentation API (Swagger automatique)
- [ ] Guide utilisateur rapide (3 rôles)
- [ ] Instructions déploiement
- [ ] Configuration variables d'environnement

---

## 🎯 PLANNING GLOBAL ESTIMÉ (VERSION SIMPLIFIÉE)

| Phase | Durée | Priorité | Description |
|-------|-------|----------|-------------|
| Phase 1 - Users Simple | 1-2 jours | 🔴 Critique | Utilisateurs sans JWT/auth |
| Phase 2 - Statuts | 2 jours | 🔴 Critique | Nouveaux statuts et logique |
| Phase 3 - Upload | 2 jours | 🟡 Importante | Preuves paiement |
| Phase 4 - Interfaces | 3-4 jours | 🟡 Importante | 3 dashboards rôles |
| Phase 5 - CRON | 1-2 jours | 🟢 Utile | Clôture automatique |
| Phase 6 - Tests | 1-2 jours | 🟡 Importante | Validation finale |

**⏱️ Durée totale estimée : 10-14 jours ouvrés**

---

## 🛠️ COMMANDES DE DÉVELOPPEMENT

### Setup Développement
```bash
# Backend
cd backend
pip install -r requirements.txt
alembic upgrade head
python app/scripts/seed_users.py  # Créer users par défaut

# Frontend  
cd frontend
npm install
npm start

# Test API
curl -X GET "http://localhost:8000/docs"  # Swagger UI
```

### Commandes par Phase
```bash
# Phase 1 - Utilisateurs
alembic revision --autogenerate -m "Add User model simple"
python app/scripts/seed_users.py

# Phase 2 - Statuts
alembic revision --autogenerate -m "Add souscription statuses and dates"

# Phase 3 - Upload
mkdir -p backend/app/uploads/preuves_paiement

# Phase 5 - CRON
python backend/app/scripts/run_cron.py
```

---

## 🎯 CRITÈRES DE SUCCÈS MVP (VERSION SIMPLIFIÉE)

### Fonctionnels
- ✅ 3 types d'utilisateurs accèdent à leurs interfaces spécifiques
- ✅ Workflow complet : Souscription → Paiement+Upload → Livraison → Clôture
- ✅ Upload et visualisation preuves de paiement
- ✅ Actions "Payer" et "Livrer" fonctionnelles
- ✅ Clôture automatique avec libération logements

### Techniques
- ✅ API REST simple et fonctionnelle
- ✅ 3 interfaces utilisateur adaptées aux rôles
- ✅ Upload fichiers avec conversion PDF
- ✅ Base de données cohérente
- ✅ Pas de complexité inutile

### Simplicité MVP
- ✅ **PAS de JWT, PAS de tokens, PAS de sessions complexes**
- ✅ **PAS de middleware auth, PAS de décorateurs permissions**
- ✅ **Connexion simple email/password avec hash basique**
- ✅ **Protection uniquement côté frontend (affichage conditionnel)**
- ✅ **Focus sur les fonctionnalités métier, pas la sécurité avancée**

---

## 🚨 POINTS D'ATTENTION MVP

| Aspect | Approche MVP | Évolution Future |
|--------|--------------|------------------|
| Authentification | Email/password simple, hash basique | JWT, sessions, security |
| Permissions | Frontend uniquement (affichage) | Backend + middleware |
| Validation | Basique côté API | Validation complète |
| Sécurité | Minimale (MVP seulement) | Sécurité production |

---

## 📝 NOTES IMPORTANTES

1. **Simplicité avec login** : Email/password basique, pas de JWT
2. **Sécurité minimale** : Hash password, pas de protection endpoints
3. **Tests manuels** : Validation par usage, pas de tests automatisés complexes
4. **Évolutif** : Structure permet ajout auth/sécurité plus tard
5. **Pragmatique** : Ce qui marche > Ce qui est parfait

---

## 🎯 MISE À JOUR RÉCENTE - FUSION DES STATUTS ET RESTRICTIONS ADMIN-GÉNÉRALE (IMPLÉMENTÉES)

### **DISTINCTION IMPORTANTE : STATUTS vs BOUTONS D'ACTIONS**

**STATUTS** : ATTENTE_PAIEMENT, ATTENTE_LIVRAISON, LIVRE, CLOTURE *(PAYE supprimé)*
**BOUTONS D'ACTIONS** : Voir, Modifier, Payer, Livrer, Envoyer Proforma, Preview Attestation, Supprimer

### **État des Boutons d'Actions par Statut de Souscription**

| Statut Souscription | Boutons d'Actions Visibles | Boutons d'Actions Masqués | Restrictions ADMIN-GENERALE |
|---------------------|---------------------------|--------------------------|----------------------------|
| **ATTENTE_PAIEMENT** | Voir, Modifier, **Payer**, Envoyer Proforma, Supprimer | Livrer | **Preview Attestation** EXCLUSIF ADMIN |
| **ATTENTE_LIVRAISON** | Voir, Modifier, Envoyer Proforma, Supprimer | **Payer** | **Livrer** + **Preview Attestation** EXCLUSIFS ADMIN |
| **LIVRE** | Voir, Envoyer Proforma, Supprimer | **Modifier**, **Payer**, **Livrer** | **Preview Attestation** EXCLUSIF ADMIN |
| **CLOTURE** | Voir, Envoyer Proforma, Supprimer | **Modifier**, **Payer**, **Livrer** | **Preview Attestation** EXCLUSIF ADMIN |

### **Permissions Spéciales par Rôle**

- **ADMIN-GENERALE** : 
  - Accès à TOUS les boutons selon statut
  - **EXCLUSIF** : Bouton "Livrer" 
  - **EXCLUSIF** : Bouton "Preview Attestation"
- **AGENT-BOAZ** : Accès selon statut, JAMAIS les boutons "Livrer" ni "Preview Attestation"
- **BAILLEUR** : Accès selon statut, JAMAIS les boutons "Livrer" ni "Preview Attestation"
- **CLIENT** : Aucun accès (non implémenté)

### **Workflow Actions → Statuts (SIMPLIFIÉ)**
1. **Action "Payer"** : ATTENTE_PAIEMENT → ATTENTE_LIVRAISON
2. **Action "Livrer"** (ADMIN-GENERALE uniquement) : ATTENTE_LIVRAISON → LIVRE
3. **CRON automatique** : LIVRE → CLOTURE

### **Règles Logiques Boutons Exclusifs ADMIN-GENERALE**
#### **Bouton "Livrer" :**
- ✅ **Visible** : Statut ATTENTE_LIVRAISON + Rôle ADMIN-GENERALE UNIQUEMENT
- ❌ **Masqué** : Tous autres statuts et rôles

#### **Bouton "Preview Attestation" :**
- ✅ **Visible** : Tous statuts + Rôle ADMIN-GENERALE UNIQUEMENT
- ❌ **Masqué** : Tous autres rôles (AGENT-BOAZ, BAILLEUR)

### **Fichiers Modifiés**
- `frontend/src/components/admin/HistoriqueSection.js` - Logique boutons
- `frontend/src/components/admin/SouscriptionViewModal.js` - Affichage statuts
- `frontend/src/services/souscriptionService.js` - Nouvelles fonctions API

---

*Plan adapté pour un MVP rapide et simple, sans complexité technique inutile, focalisé sur les fonctionnalités métier essentielles.*