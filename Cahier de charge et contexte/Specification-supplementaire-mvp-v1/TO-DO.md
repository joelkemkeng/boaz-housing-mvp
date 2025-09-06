------------------------ A FAIRE ------------


-	Développer un module, connexion utilisateur, (juste la connexion pas l’inscription)
o	Ajouter une table utilisateur, (info utilisateur, avec Role) 
o	Faire le crud utilisateur (Endpoint) 
o	Effectuer les tests des Endpoint de crud Utilisateur 
o	Les Type de Role (CLIENT, AGENT-BOAZ, ADMIN-GENERALE, BAILLEUR)
-	Pour le moment nous n’allons pas utiliser le role « CLIENT » parce que pour le moment ce n’ai pas le client qui cree des souscriptions mais Soit l’AGENT, soit  par ADMIN-GENERAL
-	AGENT-BOAZ aurra juste acces a l’interface de souscription 
o	On va cree un exemple qu’on va utiliser en base de donnée :
	Email : agent@boaz-study.com
	Password : agent1234
-	BAILLEUR aura juste acces a l’interface de gestion de Logement,  
o	On va cree un exemple qu’on va utiliser en base de donnée :
	Email : bailleur@boaz-study.com
	Password : bailleur1234
o	
-	ADMIN-GENERALE, aura Access a tout les interface, tout les menu 
o	On va cree un exemple qu’on va utiliser en base de donnée :
	Email : ceo@boaz-study.com
	Password : ceo1234
o	



Restriction : 

-	AGENT-BOAZ pourra :
•	Effectuer une souscription d’attestation hébergement, 
•	Envoyer une preuve de versement de fond (en cliquant sur payer, le système vas demander d’uploader une preuve de payement [soit une image ou un document, si c’est une image, le système va convertir en document PDF] (le système changera le statut de la souscription de « Attente de paiement » vers « Attente Livraison »
•	Il pourra voir les statistiques de souscriptions en fonction des statuts, 

-	BAILLEUR pourra : 
	Ajouter des Logement dans son Espace 
	Suivre les statistiques 
	Modifier un logement 
	Changer le statut d’un logement 
-	ADMIN-GENERALE pourra
	Faire tout ce que le Bailleur et l’Agent peux faire 
	Previsualiser l’attestation de Logement et de prise en charge 
	Voir les details de la souscription avec tout les infos de la souscription y compris la preuve de paiement uploader lors de l’execution de l’action payer , pour les souscriptions en statut « Attente Livraison »
	Voir et utiliser le bouton livrer , pour les souscriptions en statut « Attente Livraison » qui apres livraison succes , doit changer de statut de « Attente livraison » vers « livrer »



Autres specificatiom 
-	Pour l’enregistrement d’une souscription en base de donnee  mettre : 
	Date de livraison (valeur a mettre a jour pendant la livraison du service) 
	Date d’expiration (pour le service attestation D’hébergements, mettre le nombre de temps de validité du livrable dans le JSON service pour les services) .  Donc la valeur de cette data sera calculer en fonction du nombre de jour de validité après la date de livraison , docn cette valeur doit se mettre ajour pendant la livraison 
-	Les statuts à Rajouter.  (Attente Livraison) qui est le statut avant livrer , et le statut « cloturer » qui est ce qui va etre mise a jour grace a un CRON , qui vas a chaque execution , verifier tout les sosucription livrer voir si la date d’expiration est attein, si oui il vas mettre a jour le statut de livrer vers cloturer , et il va verifier si la souscription s’agit du service attestation hebergement et prise en charge , si c’est le cas, il vas changer le statut du logement qui etais lier a cette souscription de « Occuper » vers « Disponible »
-	Pour une souscription en statut « livrer » et « clôturer », on ne peut plus modifier ‘
-	Si en effectuant l'action « livraison » pour une souscription « Attente livraison » , le système doit vérifier a nouveau si le logement choisit pour cette souscription est bien encore disponible, si le logement qui avais été choisit n'ai plus disponible , il doit retourner une réponse claire au front donc a ADMIN-GENERALE, afin que Admin Generale puisse modifier la souscription pour choisit un logement autres,  avant de lancer de nouveau l ;action de livraions

========================================
REGLES D'AFFICHAGE DES BOUTONS D'ACTIONS PAR STATUT (FUSIONNEES - IMPLEMENTED)
========================================

IMPORTANT: Bien distinguer les STATUTS des BOUTONS D'ACTIONS :
- STATUTS : ATTENTE_PAIEMENT, ATTENTE_LIVRAISON, LIVRE, CLOTURE (PAYE supprimé)
- BOUTONS D'ACTIONS : Voir, Modifier, Payer, Livrer, Envoyer Proforma, Preview Attestation, Supprimer

Pour une souscription au statut ATTENTE_PAIEMENT :
	✅ Boutons d'actions visibles : Voir, Modifier, Payer, Envoyer Proforma, Supprimer
	❌ Boutons d'actions masqués : Livrer (pas encore payé)
	🔑 RESTRICTION : Preview Attestation EXCLUSIVEMENT visible pour ADMIN-GENERALE

Pour une souscription au statut ATTENTE_LIVRAISON :
	✅ Boutons d'actions visibles : Voir, Modifier, Envoyer Proforma, Supprimer
	❌ Boutons d'actions masqués : Payer (déjà payé)
	🔑 RESTRICTIONS : 
		- Livrer EXCLUSIVEMENT visible pour ADMIN-GENERALE
		- Preview Attestation EXCLUSIVEMENT visible pour ADMIN-GENERALE

Pour une souscription au statut LIVRE :
	✅ Boutons d'actions visibles : Voir, Envoyer Proforma, Supprimer
	❌ Boutons d'actions masqués : Modifier, Payer, Livrer (déjà livré)
	🔑 RESTRICTION : Preview Attestation EXCLUSIVEMENT visible pour ADMIN-GENERALE

Pour une souscription au statut CLOTURE :
	✅ Boutons d'actions visibles : Voir, Envoyer Proforma, Supprimer
	❌ Boutons d'actions masqués : Modifier, Payer, Livrer (terminé)
	🔑 RESTRICTION : Preview Attestation EXCLUSIVEMENT visible pour ADMIN-GENERALE

WORKFLOW ACTIONS vs STATUTS (SIMPLIFIÉ) :
1. ATTENTE_PAIEMENT → [Action: Payer] → ATTENTE_LIVRAISON
2. ATTENTE_LIVRAISON → [Action: Livrer - ADMIN-GENERALE seulement] → LIVRE  
3. LIVRE → [CRON automatique] → CLOTURE

RESTRICTIONS ADMIN-GENERALE :
- Le bouton d'action "Livrer" est EXCLUSIVEMENT visible pour ADMIN-GENERALE
- Le bouton d'action "Preview Attestation" est EXCLUSIVEMENT visible pour ADMIN-GENERALE
- Les autres rôles (AGENT-BOAZ, BAILLEUR) ne voient jamais ces boutons
