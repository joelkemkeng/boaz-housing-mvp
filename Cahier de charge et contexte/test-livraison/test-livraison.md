# Procédures de Test et Critères d'Acceptation
## Boaz-Housing MVP

**Version :** 1.0  
**Date :** Décembre 2024  
**Projet :** Boaz-Housing - Plateforme de souscription et gestion logements étudiants

---

## 1. CRITÈRES D'ACCEPTATION GLOBAUX DU MVP

### 1.1 Critères Fonctionnels Généraux

**Le MVP Boaz-Housing sera considéré comme accepté si :**

1. **Application Administrateur** : 
   - Permet la création complète d'une souscription via wizard 4 étapes
   - Affiche l'historique des souscriptions avec actions CRUD
   - Génère et envoie automatiquement les documents PDF requis

2. **Application Bailleur** :
   - Permet la gestion complète des logements (CRUD)
   - Respect des contraintes métier (logements utilisés non modifiables)
   - Interface intuitive et responsive

3. **Génération Documents** :
   - Proforma conforme au modèle avec données dynamiques
   - Attestation 2 pages conforme modèle Livin France adapté Boaz-Housing
   - QR code fonctionnel et référence unique

4. **Workflow Complet** :
   - Parcours end-to-end : création logement → souscription → paiement → génération attestation → envoi email
   - Gestion statuts cohérente et traçabilité complète

### 1.2 Critères Techniques Généraux

1. **Performance** :
   - Temps réponse API < 2 secondes (95% des requêtes)
   - Génération PDF < 5 secondes
   - Interface réactive sur mobile et desktop

2. **Qualité Code** :
   - Couverture tests ≥ 80%
   - 0 erreur critique sécurité
   - Code documenté et maintenable

3. **Compatibilité** :
   - Navigateurs : Chrome, Firefox, Safari (dernières versions)
   - Responsive : mobile, tablet, desktop
   - API REST conforme OpenAPI 3.0

---

## 2. PROCÉDURES DE TEST PAR EPIC

### 2.1 Epic 1 - Infrastructure & Setup

#### Test d'Intégration Infrastructure

**Objectif :** Vérifier que tous les composants techniques communiquent correctement

**Procédure :**
1. **Setup Environnement**
   - Démarrer PostgreSQL et vérifier connexion
   - Lancer backend FastAPI sur port 8000
   - Lancer frontend React sur port 3000
   - Vérifier CORS entre frontend/backend

2. **Base de Données**
   - Exécuter migrations Alembic
   - Vérifier création tables logements/souscriptions
   - Tester contraintes clés étrangères
   - Insérer données test et vérifier intégrité

3. **API Organisation**
   - GET /api/organisation retourne données JSON complètes
   - Vérifier conformité données avec spécifications Boaz-Housing
   - Tester gestion cache et performance

**Critères Acceptation :**
- ✅ Tous services démarrent sans erreur
- ✅ Base données créée avec schéma correct
- ✅ Frontend accède API sans erreur CORS
- ✅ Données organisation conformes spécifications

#### Test Unitaires Modèles

**Procédure :**
1. Tester création/modification/suppression logements
2. Tester relations souscription ↔ logement
3. Vérifier validations modèles (enums, contraintes)
4. Tester génération automatique timestamps

**Critères Acceptation :**
- ✅ Tous tests unitaires passent (100%)
- ✅ Contraintes base données respectées
- ✅ Relations fonctionnelles

---

### 2.2 Epic 2 - Gestion Logements (Bailleur)

#### Test Fonctionnel CRUD Logements

**Objectif :** Valider gestion complète logements par bailleur

**Procédure Détaillée :**

1. **Test Création Logement**
   ```
   Données test :
   - Adresse : "123 Rue de la République, Paris 75011"
   - Pays : "France"
   - Ville : "Paris"
   - Type : "appartement"
   - Occupation : "individuel"
   - Superficie : 25.5 m²
   - Prix hors charges : 800€
   - Prix charges : 150€
   ```
   - Saisir formulaire complet
   - Vérifier calcul automatique prix total (950€)
   - Valider sauvegarde en base
   - Contrôler statut initial "libre"

2. **Test Affichage Liste**
   - Créer 5 logements test différents
   - Vérifier affichage tableau avec toutes colonnes
   - Tester pagination (si >20 logements)
   - Vérifier filtres par statut et ville

3. **Test Modification Logement**
   - Modifier prix d'un logement libre
   - Vérifier sauvegarde modifications
   - Créer souscription payée sur logement
   - Vérifier blocage modification avec message explicite

4. **Test Suppression Logement**
   - Supprimer logement libre (soft delete)
   - Vérifier non-affichage dans liste
   - Tenter supprimer logement utilisé
   - Vérifier blocage avec message erreur

**Critères Acceptation :**
- ✅ CRUD complet fonctionnel
- ✅ Calcul automatique prix total correct
- ✅ Contraintes métier respectées (logement utilisé)
- ✅ Interface responsive et intuitive
- ✅ Messages erreur explicites

#### Test Contraintes Métier

**Procédure :**
1. Créer logement → créer souscription → marquer payée
2. Vérifier changement statut logement "libre" → "occupe"
3. Tenter modifier logement occupé
4. Vérifier API validation contraintes
5. Tester libération logement si souscription clôturée

**Critères Acceptation :**
- ✅ Statuts logements mis à jour automatiquement
- ✅ Modifications bloquées selon règles métier
- ✅ API validation fonctionnelle

---

### 2.3 Epic 3 - Application Souscription (Admin)

#### Test Fonctionnel Wizard Souscription Complet

**Objectif :** Valider parcours création souscription end-to-end

**Procédure Complète :**

**Phase 1 - Page Accueil Admin**
1. Vérifier affichage card service "Attestation de Logement et de Prise en Charge"
2. Tester clic bouton "Souscrire" → ouverture wizard
3. Vérifier section historique vide au démarrage

**Phase 2 - Wizard Étape 1 (Client)**
```
Données test client :
- Nom : "MARTIN"
- Prénom : "Jean"
- Email : "jean.martin@email.com"
- Date naissance : "15/03/2000"
- Nationalité : "Française"
- Pays destination : "France"
- Date arrivée : "01/09/2025"
```
- Saisir toutes informations
- Tester validations (email format, âge minimum, dates)
- Vérifier navigation "Suivant" activée après validation

**Phase 3 - Wizard Étape 2 (Académique)**
```
Données test académiques :
- École : "Université Paris-Saclay"
- Filière : "Master Informatique"
- Pays école : "France"
- Ville école : "Orsay"
- Code postal : "91190"
- Adresse : "Rue André Ampère, Plateau de Moulon"
```
- Saisir informations académiques complètes
- Tester validation code postal français
- Vérifier retour étape précédente avec persistance données

**Phase 4 - Wizard Étape 3 (Logement)**
- Vérifier affichage uniquement logements statut "libre"
- Contrôler contenu cards : adresse, prix, superficie, type
- Sélectionner un logement
- Tester filtres par ville/type/prix
- Valider sélection obligatoire avant progression

**Phase 5 - Wizard Étape 4 (Proforma)**
- Vérifier récapitulatif données complètes
- Contrôler génération automatique référence ATT-XXXX
- Tester prévisualisation Proforma PDF
- Valider bouton téléchargement
- Tester envoi email avec confirmation
- Finaliser avec bouton "Terminer"

**Phase 6 - Finalisation**
- Vérifier retour page accueil
- Contrôler ajout souscription dans historique
- Valider statut "attente_paiement"
- Vérifier changement référence unique

**Critères Acceptation Wizard :**
- ✅ 4 étapes navigation fluide
- ✅ Validation complète chaque étape
- ✅ Persistance données entre étapes
- ✅ Génération référence unique
- ✅ Proforma généré correctement
- ✅ Finalisation et sauvegarde base

#### Test Fonctionnel Gestion Historique

**Procédure :**
1. **Créer 3 souscriptions** avec statuts différents
2. **Tester Action "Voir"** : modal lecture seule avec tous détails
3. **Tester Action "Modifier"** : réouverture wizard avec données
4. **Tester Action "Supprimer"** : confirmation puis soft delete
5. **Tester Action "Payer"** :
   - Passage statut "attente_paiement" → "paye"
   - Génération automatique Attestation PDF
   - Envoi email automatique client
   - Téléchargement immédiat admin
   - Changement statut logement "libre" → "occupe"

**Critères Acceptation Historique :**
- ✅ Toutes actions fonctionnelles
- ✅ Workflow paiement automatisé
- ✅ Documents générés et envoyés
- ✅ Statuts mis à jour correctement

---

### 2.4 Epic 4 - Génération Documents PDF

#### Test Qualité Documents Proforma

**Objectif :** Valider conformité Proforma au modèle Boaz Study

**Procédure Détaillée :**
1. **Génération Document**
   - Créer souscription complète
   - Générer Proforma via API
   - Télécharger PDF résultant

2. **Contrôle Visuel Proforma**
   - Logo Boaz-Housing correctement positionné (coin supérieur droit)
   - Titre "FACTURE" avec date génération
   - Informations organisation complètes et exactes :
     * Nom : Boaz-Housing
     * Adresse : 14 Rue Jean Piestre, Corbeil-Essonnes, 91100, France
     * Email : info@boaz-study.fr
     * Téléphone : +33 01 84 18 02 67
   - Section client avec nom complet et email
   - Tableau services avec prix formatés
   - Totaux HT/TTC calculés correctement

3. **Contrôle Technique**
   - PDF lisible sur tous supports
   - Polices intégrées correctement
   - Images (logo) haute qualité
   - Taille fichier < 2MB

**Critères Acceptation Proforma :**
- ✅ Design conforme modèle fourni
- ✅ Données dynamiques intégrées correctement
- ✅ Calculs totaux exacts
- ✅ Qualité PDF professionnelle

#### Test Qualité Documents Attestation

**Objectif :** Valider conformité Attestation au modèle Livin France adapté

**Procédure Détaillée :**
1. **Génération Document**
   - Marquer souscription comme "payée"
   - Générer Attestation via API
   - Vérifier document 2 pages

2. **Contrôle Page 1 - Attestation Logement**
   - Logo Boaz-Housing centré en haut
   - Titre "Attestation de logement" dans encadré noir
   - Texte introduction adapté Boaz-Housing
   - Bloc signataire "Je soussigné, Benjamin YOHO BATOMO..."
   - Informations complètes organisation
   - Données client : nom, date/lieu naissance
   - Détails logement : adresse exacte, loyer
   - Dates entrée et durée location
   - Section authentification avec QR code

3. **Contrôle Page 2 - Attestation Prise en Charge**
   - Même header que page 1
   - Titre "Attestation de prise en charge"
   - Liste complète services prise en charge :
     * Validation réservation logement
     * Contrat assurance habitation/énergie
     * Assurance voyage étudiants étrangers
     * Compte bancaire français
     * Assurance maladie française + complémentaire
     * Validation visa et renouvellement

4. **Contrôle Authentification**
   - QR Code généré avec URL : https://boaz-study.com/verify?ref=ATT-XXXX
   - Référence unique format ATT- + 16 caractères
   - Contact organisation correct
   - Date/lieu signature : "Fait à Corbeil-Essonnes, France, le [date]"

**Critères Acceptation Attestation :**
- ✅ Document 2 pages conforme modèle
- ✅ Textes adaptés Boaz-Housing corrects
- ✅ QR Code fonctionnel
- ✅ Toutes données dynamiques intégrées
- ✅ Layout identique modèle Livin France

---

### 2.5 Epic 5 - Envoi Emails

#### Test Fonctionnel Envoi Documents

**Objectif :** Valider envoi emails automatiques avec pièces jointes

**Procédure :**
1. **Configuration SMTP**
   - Configurer serveur SMTP test
   - Vérifier connexion et authentification

2. **Test Envoi Proforma**
   - Générer Proforma depuis wizard
   - Utiliser fonction "Envoyer par Email"
   - Vérifier réception email client
   - Contrôler pièce jointe PDF correcte

3. **Test Envoi Attestation Automatique**
   - Marquer souscription "payée"
   - Vérifier envoi automatique email
   - Contrôler réception et contenu

4. **Contrôle Contenu Emails**
   - Objet email approprié avec référence
   - Corps email avec informations Boaz-Housing
   - Pièce jointe nom correct et lisible
   - Footer avec coordonnées contact

**Critères Acceptation Emails :**
- ✅ Envoi automatique fonctionnel
- ✅ Pièces jointes correctes
- ✅ Templates emails professionnels
- ✅ Gestion erreurs SMTP

---

## 3. TESTS D'INTÉGRATION GLOBAUX

### 3.1 Parcours Utilisateur Complet - Bailleur

**Scénario :** "Un bailleur ajoute un nouveau logement et le voit utilisé dans une souscription"

**Procédure :**
1. Accéder application bailleur
2. Ajouter logement avec toutes informations
3. Vérifier statut "libre" dans liste
4. [Admin] Créer souscription avec ce logement
5. [Admin] Marquer souscription "payée"
6. Revenir bailleur et vérifier statut logement "occupe"
7. Tenter modifier logement → vérifier blocage

**Critères Succès :**
- ✅ Workflow complet sans erreur
- ✅ Statuts synchronisés entre applications
- ✅ Contraintes métier respectées

### 3.2 Parcours Utilisateur Complet - Admin

**Scénario :** "Un admin traite une souscription de A à Z avec génération documents et paiement"

**Procédure Détaillée :**
1. **Préparation** : S'assurer qu'au moins 1 logement libre existe
2. **Page Accueil** : Clic card service → ouverture wizard
3. **Étape 1** : Saisir informations client complètes
4. **Étape 2** : Saisir informations académiques complètes  
5. **Étape 3** : Sélectionner logement dans liste disponibles
6. **Étape 4** : Générer et télécharger Proforma, envoyer email
7. **Finalisation** : Terminer et retourner accueil
8. **Historique** : Vérifier souscription statut "attente_paiement"
9. **Paiement** : Clic action "Payer" sur souscription
10. **Vérifications** : 
    - Statut → "payé" puis "livré"
    - Attestation générée et téléchargée
    - Email envoyé automatiquement
    - Logement passé "occupe"

**Durée Estimée Parcours :** < 5 minutes

**Critères Succès :**
- ✅ Parcours fluide sans blocage
- ✅ Tous documents générés correctement
- ✅ Emails envoyés automatiquement
- ✅ Statuts mis à jour partout

### 3.3 Test Performance Globale

**Objectifs :**
- Interface réactive
- API performante
- Génération documents rapide

**Métriques Cibles :**
- Chargement page < 2 secondes
- Soumission formulaire < 1 seconde  
- Génération PDF < 5 secondes
- Envoi email < 10 secondes

**Procédure :**
1. Mesurer temps chargement page accueil
2. Chronométrer wizard complet
3. Mesurer génération chaque document
4. Tester avec 10 souscriptions simultanées

**Critères Acceptation :**
- ✅ 95% requêtes respectent métriques cibles
- ✅ Pas de blocage interface utilisateur
- ✅ Dégradation gracieuse si surcharge

---

## 4. TESTS DE RÉGRESSION

### 4.1 Matrice de Régression

**Avant chaque release, vérifier :**

| Fonctionnalité | Test Rapide (5 min) | Status |
|---------------|-------------------|--------|
| Création logement bailleur | Créer 1 logement simple | ⬜ |
| Liste logements + filtres | Vérifier affichage et filtres | ⬜ |
| Wizard souscription 4 étapes | Parcours complet rapide | ⬜ |
| Génération Proforma | 1 génération + preview | ⬜ |
| Génération Attestation | 1 génération après paiement | ⬜ |
| Envoi emails | 1 envoi Proforma + Attestation | ⬜ |
| Actions historique | Voir, modifier, supprimer | ⬜ |
| Workflow paiement | 1 passage "payé" complet | ⬜ |

### 4.2 Tests de Non-Régression Données

**Vérifier intégrité données après modifications :**
1. Références souscriptions restent uniques
2. Relations logements ↔ souscriptions préservées  
3. Statuts cohérents partout
4. Aucune donnée corrompue

---

## 5. CRITÈRES D'ACCEPTATION FINAUX

### 5.1 Critères Fonctionnels MVP

**Le MVP sera accepté si TOUS les critères suivants sont respectés :**

✅ **Application Bailleur** :
- Gestion complète logements (CRUD) ✓
- Contraintes métier respectées ✓
- Interface responsive ✓

✅ **Application Admin** :
- Wizard souscription 4 étapes fonctionnel ✓
- Historique avec toutes actions ✓
- Workflow paiement automatisé ✓

✅ **Documents PDF** :
- Proforma conforme modèle ✓
- Attestation 2 pages conforme ✓
- QR codes et références uniques ✓

✅ **Envoi Emails** :
- Envoi automatique Proforma et Attestation ✓
- Pièces jointes correctes ✓

✅ **Parcours End-to-End** :
- Bailleur → Admin → Client fonctionnel ✓
- Statuts synchronisés ✓
- Traçabilité complète ✓

### 5.2 Critères Techniques MVP

✅ **Performance** :
- Temps réponse API < 2s ✓
- Génération PDF < 5s ✓
- Interface réactive ✓

✅ **Qualité** :
- Tests passent à 100% ✓
- Couverture > 80% ✓
- 0 bug critique ✓

✅ **Compatibilité** :
- Chrome, Firefox, Safari ✓
- Mobile, tablet, desktop ✓

### 5.3 Critères de Livraison

✅ **Documentation** :
- README installation ✓
- API documentée OpenAPI ✓
- Guide utilisateur basique ✓

✅ **Déploiement** :
- Docker compose fonctionnel ✓
- Variables environnement documentées ✓
- Scripts migration base ✓

---

## 6. PROCÉDURE DE VALIDATION FINALE

### 6.1 Checklist Pré-Livraison

**Technique :**
- [ ] Tous tests unitaires passent
- [ ] Tests intégration passent  
- [ ] Performance validée
- [ ] Sécurité basique vérifiée
- [ ] Code review effectué

**Fonctionnel :**
- [ ] Parcours bailleur complet testé
- [ ] Parcours admin complet testé
- [ ] Documents PDF validés
- [ ] Emails fonctionnels
- [ ] Contraintes métier respectées

**Livraison :**
- [ ] Documentation complète
- [ ] Environnement prod-ready
- [ ] Sauvegarde/restauration testée
- [ ] Formation utilisateurs planifiée

### 6.2 Validation Métier Finale

**Validation par Product Owner :**
1. Demo complète MVP (30 min)
2. Test libre fonctionnalités (30 min)
3. Validation documents générés
4. Approbation go-live

**Critères Go-Live :**
- ✅ Toutes fonctionnalités MVP opérationnelles
- ✅ Qualité documents conforme attentes
- ✅ Performance acceptable usage réel
- ✅ Équipe formée utilisation

---

**FIN DU DOCUMENT**

*Ce document constitue la référence complète pour la validation du MVP Boaz-Housing. Toute modification des critères doit être approuvée par le Product Owner et documentée.*