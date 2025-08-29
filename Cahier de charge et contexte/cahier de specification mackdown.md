1.  **Contexte & Objectif**
2.  **Périmètre MVP**
3.  **Acteurs & Rôles**
4.  **Fonctionnalités par application**
    *   Application de souscription (administrateur)
    *   Application de gestion locative (bailleur)
5.  **Flux fonctionnels détaillés** (diagrammes textuels, étapes claires)
6.  **Données dynamiques** (organisation, client, logement, souscription)
7.  **Livrables MVP** (Proforma + Attestation)
8.  **Évolutions prévues (Version 2)**

**📘 Cahier de Spécifications Fonctionnelles – MVP**

**Projet : Boaz-Housing**  
**Version : 1.0 – MVP**

**1\. Contexte & Objectif**

Boaz-Housing est une plateforme destinée à faciliter la souscription et la gestion des services liés au logement étudiant à l’étranger.

Pour le **MVP**, l’objectif est de permettre :

*   La **souscription rapide** à un service d’**attestation de logement et de prise en charge** (administrateurs côté Boaz-Study).
*   La **gestion des logements** proposés par les bailleurs partenaires (application locative).

L’approche MVP se concentre sur :

*   Un **parcours simple et fonctionnel**,
*   La génération de **documents dynamiques** (Proforma + Attestation),
*   Une **traçabilité minimale** (statuts de souscription).

**2\. Périmètre MVP**

*   **Inclus :**
    *   Application administrateur : création et gestion de souscriptions.
    *   Application bailleur : ajout et gestion de logements.
    *   Génération automatique de documents PDF (Proforma et Attestation).
    *   Gestion des statuts de souscription (Attente paiement, Payé, Livré, Clôturé).
    *   Envoi des documents générés par email.
*   **Exclus (Version 2) :**
    *   Recherche avancée de logements (par école, distance, filtres).
    *   Modification des infos organisation par interface.
    *   Intégration paiement en ligne.
    *   Portail étudiant (auto-souscription).

**3\. Acteurs & Rôles**

*   **Administrateur (Boaz-Study)**
    *   Crée, modifie, valide ou supprime une souscription.
    *   Suit l’avancement et les statuts des souscriptions.
    *   Génère et envoie les documents aux clients.
*   **Bailleur / Agent immobilier**
    *   Enregistre et gère les logements disponibles.
    *   Met à jour les caractéristiques et statuts des logements (Libre, Occupé).

**4\. Fonctionnalités par Application**

**4.1 Application de Souscription (Administrateur)**

*   **Souscription**
    *   Créer une nouvelle souscription (wizard en étapes).
    *   Modifier une souscription existante.
    *   Supprimer (soft delete) une souscription.
    *   Consulter les détails (lecture seule).
*   **Suivi & Gestion**
    *   Tableau des souscriptions (historique).
    *   Modification manuelle des statuts.
    *   Statistiques globales (total par statut).
*   **Documents**
    *   Génération et prévisualisation de Proforma.
    *   Génération Attestation finale après paiement.
    *   Envoi automatique par email.

**4.2 Application de Gestion Locative (Bailleur)**

*   **Gestion des logements**
    *   Ajouter un logement (adresse, ville, type, prix, superficie).
    *   Modifier un logement.
    *   Supprimer un logement.
    *   Consulter la liste des logements.
    *   Vérifier si un logement est lié à une attestation.

**5\. Flux Fonctionnels (Flows)**

**5.1 Flux de création de souscription**

1.  Admin → “Créer une souscription”
2.  **Étape 1 – Infos client**
    *   Nom, prénom, email, date naissance, nationalité, pays destination, date prévue d’arrivée.
3.  **Étape 2 – Infos académiques**
    *   École/université, filière, Pays de l’école ou l’université, Ville de l’école, ou université, Code postal de l’école l’université, adresse complète école.
4.  **Étape 3 – Choix logement**
    *   Sélection d’un logement libre Proposer une liste de petits card logement dont le statut du logement est à <<Libre>> dont chaque card (logement) sélectionnable contiennent ces informations : 
        1.  Adresse complète du logement  
        2.  Pays 
        3.  Ville  
        4.  (Individuels, colocation ou autres) 
        5.  Type (chambre, appartement, studio) 
        6.  Nombre de mètres carrés de la chambre  
        7.  Prix logement hors charges  
        8.  Prix des charges 
        9.  Prix logements tous charges comprises
5.  **Étape 4 – Génération Proforma**
    *   Production et prévisualisation de Proforma 
    *   Production de proforma (avec tout information renseigner, ceux du client, ceux de l’organisation ou de l’entreprise) 
    *   Prévisualisation de cette Proformat 
    *   Bouton Retour pour modifier les informations si elle n’ait pas convenable 
    *   Bouton permettant de télécharger cette proforma 
    *   Bouton Permettant d’envoyer cette proforma Email renseigner à la section “informations personnelles du client“, un mail avec pièce Jointe  
    *   Bouton “Terminer” permettant de retourner à l’accueille 
6.  **Retour Accueil** → historique mis à jour (statut = “Attente paiement”).

**📌 Spécification – Page d’Accueil (Application de Souscription)**

La page d’accueil constitue le **point central** de l’application de souscription. Elle permet :

1.  La **sélection et la souscription** d’un service.
2.  Le **suivi et la gestion** des souscriptions existantes.

**1\. Section – Choix de service à souscrire**

*   Présentation sous forme de **cards** (cartes visuelles), similaires à un catalogue produit.
*   Chaque card contient :
    *   **Titre du service** (ex. : _“Attestation de Logement et de Prise en Charge”_).
    *   **Description courte** (objectif du service).
    *   **Prix** (forfait en EUR/FCFA).
    *   **Bouton “Souscrire”** permettant de démarrer immédiatement le processus de souscription (wizard en 4 étapes).

⚠️ Dans le MVP : **un seul service est disponible**, l’Attestation de logement et de prise en charge.

**2\. Section – Historique des souscriptions**

Affichage d’un **tableau listant toutes les souscriptions créées** par l’administrateur.

**Colonnes du tableau :**

*   Nom du service.
*   Nom et prénom du client.
*   Date de création de la souscription.
*   Statut de la souscription (Attente paiement, Payé, Livré, Clôturé).
*   Actions disponibles.

**Actions disponibles (colonne Actions) :**

1.  **Voir** :
    *   Ouvre le formulaire complet de la souscription en **mode lecture seule**.
    *   Aucun champ n’est modifiable.
2.  **Modifier** :
    *   Rouvre le formulaire de la souscription avec tous les champs **éditables**.
    *   L’administrateur peut mettre à jour les données, puis sauvegarder.
3.  **Supprimer** :
    *   Effectue un **soft delete** → la souscription n’est pas réellement supprimée de la base mais son **statut est modifié** (ex. : “Supprimée/Annulée”).
    *   Permet de conserver une traçabilité.
4.  **Payer** :
    *   Change le statut de la souscription en **“Payé”**.
    *   Changer le statut du logement choisit en « **Occupé** » afin que plus tard
    *   Déclenche automatiquement :
        1.  La **génération du PDF final** (Attestation logement + prise en charge).
        2.  Le **téléchargement immédiat** du document pour l’administrateur.
        3.  L’**envoi automatique par email** au client, en pièce jointe, à l’adresse fournie dans les informations personnelles.

**5.2 Flux de validation d’une souscription / livraison**

1.  Admin ouvre l’historique → sélectionne une souscription.
2.  Bouton **“Payer”** → statut passe à **“Payé”**.
3.  Génération automatique de l’**Attestation logement + prise en charge**.
4.  Téléchargement auto + envoi par email au client.
5.  Statut mis à jour → **“Livré”**.

**5.3 Flux bailleur (logements)**

1.  Bailleur se connecte → Menu “Mes logements”.
2.  Actions possibles :
    *   **Ajouter** logement (adresse, type, prix, surface).
    *   **Modifier** logement existant.
    *   **Supprimer** (soft delete).
    *   **Consulter** liste complète.
3.  Chaque logement a un statut : Libre / Utilisé.
    *   Si utilisé dans une attestation → verrouillage modification de certains champs.

*   L'enregistrement d’un logement doit contenir les informations tel que : Adresse complète du logement  
*   Pays 
*   Ville  
*   (Individuels, colocation ou autres) 
*   Type (chambre, appartement, studio) 
*   Nombre de mètres carrés de la chambre  
*   Prix logement hors charges  
*   Prix des charges 
*   Prix logements tous charges comprises 

**6\. Données Dynamiques**

**📌 Informations Organisation**

1.  **Nom de l’organisation** : Boaz-Housing
2.  **Logo** : Logo officiel de Boaz-Housing
3.  **Site web** : [www.boaz-study.com](http://www.boaz-study.com)
4.  **Nom complet du CEO** : Benjamin YOHO BATOMO
5.  **Date de naissance du CEO** : _à compléter_ (ex. : 17 mars 1992)
6.  **Ville de naissance du CEO** : Douala
7.  **Pays de naissance du CEO** : Cameroun
8.  **Adresse du siège social** : 14 Rue Jean Piestre, Corbeil-Essonnes, 91100, France
9.  **Ville d’enregistrement au RCS** : Corbeil-Essonnes
10.  **Numéro de registre de commerce** : _à confirmer_ (ex. : 12345778909987665)
11.  **Code NAF de l’organisation** : _à confirmer_ (ex. : 1234D)
12.  **Cachet et signature de l’organisation** : (image insérée dans les documents générés)
13.  **Email de contact** : [info@boaz-study.fr](mailto:info@boaz-study.fr)
14.  **Numéro de téléphone** : +33 01 84 18 02 67

**📌 Informations Souscription – Attestation Hébergement**

*   **Information de L’organisation ..etc**
*   **Nom complet** : \[Nom + Prénom du client\]
*   **Date de naissance** : \[JJ/MM/AAAA\]
*   **Ville de naissance** : \[Ville\]
*   **Pays de naissance** : \[Pays\]
*   **Identifiant et Adresse du logement sélectionné** : \[Adresse complète du logement choisi\]
*   **Montant du loyer** : \[Montant en € ou FCFA\]
*   **Date d’entrée prévue** : \[JJ/MM/AAAA\]
*   **Durée de location (en mois)** : \[Nombre de mois\]
*   **QR Code** :
    *   Contenu : URL de vérification (ex. : https://boaz-study.com/verify?ref=ATT-XXXX).
    *   Fonction : renvoyer vers une page de vérification affichant :
        *   Statut de validité de l’attestation (Valide / Expirée / Annulée).
        *   Date d’expiration du document.
*   **Référence unique de souscription** :
    *   Exemple : ATT-D28B8C5877C1CA25
    *   Générée automatiquement après chaque souscription.
    *   Utilisée comme identifiant unique pour le suivi et la vérification.
*   **Proforma**
*   **Livrable Attestation Logement et de prise en charge**

**7\. Livrables MVP**

*   **Proforma PDF**
    *   Contient infos organisation + client + logement.
    *   S’assurer qu’il soit comme l’exemple de proforma
*   **Attestation logement + prise en charge PDF**
    *   Infos organisation + client + logement.
    *   Engagement de prise en charge.
    *   Signature + cachet organisation.
    *   QR code (authenticité).
    *   S’assurer qu’il soit exactement comme l’exemple fournit celui de « Livin France »

**8\. Évolutions prévues (Version 2)**

*   Gestion dynamique des infos organisation.
*   Recherche logements par localisation école.
*   Affichage distance école ↔ logement.
*   Filtres (prix, type logement).
*   Paiement en ligne et facturation.