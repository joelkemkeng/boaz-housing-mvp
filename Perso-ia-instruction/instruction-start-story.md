oui oui mais il faut savoir qu'il ya deja des choses deja fais parport a cela , il faut dabord analyser ce qui    │
│   est                                                                                                               │
│     fais avant de faire autre chose , ou ameliorer quoi que ce soit , et surtout ne complique pas les chose         │
│   n'ajoute                                                                                                          │
│     pas des pratiques qui vont compliquer la tache, n'ajoute pas des contraintes innutiles  , donc toujour rester   │
│   dans                                                                                                              │
│     le principe de mvp , le rendu doit respecter la charte graphique (bleu soft , orange soft ) tres bien les       │
│     harmoniser , et faire que l'affichage soit vraiment User friendly , vraiment soft , pro , et surtout ne met     │
│   pas trop les degrader , c'est pas tres pro  les degrader   





--------------- Reprise de contexte - ----------------

non il faut surtout s'en tenir au planing @"Cahier de charge et contexte/planification/planing.md"   au cahier de 
  charge @"Cahier de charge et contexte/cahier de specification mackdown.md"   aux test attendu @"Cahier de charge et
   contexte/test-livraison/test-livraison.md"  aussi @"Cahier de charge et 
  contexte/information-dynamique-document.txt"







  ------ demande fonctionnaliter proformat -----------

  1- commence par cree un data json sevice au backend , qui vas constituer les service proposer , donc pour notre   │
│   cas oon a la service attestation de logement et de prise en charge dans dans son json il doit y avoir des donnee  │
│   relative au serice , (nom , titre , description, slug, active ou pas active , tarif du service ) et faire des     │
│   end point pou recuperer ces services                                                                              │
│   2- puis faire que sur la plateforme admin , la liste de service porposer provinne de Api                          │
│                                                                                                                     │
│   3- produit un model de proformat tres conforme et tres professionnel ,  qui doit avoir les donnee qui sont par    │
│   exemple dans cette proforma @"Cahier de charge et contexte/Exemple Proformat/PROFORMA Sample.jpg"   , je veux     │
│   vraiment que ce que l'application genere soit vraiment Soft et conforme , l'etape de production de proformat      │
│   doit etre a la derniere etape du Wizard , une requette est envoyer au backend avec tout les donnee des            │
│   souscription puis le backend recois ces donnee de la soucription puis utilise ces donnee pour generer la          │
│   proforma, aussi en fonction de la liste des services soucrit , sachant que il yas les information relative au     │
│   services sous json au backend,et aussi en fonction des information de organisation qui sont du backend ,et aussi  │
│   en foncton des donnee dans le @"Cahier de charge et contexte/Exemple Proformat/PROFORMA Sample.jpg"  tu peux      │
│   mettre les donnee essentiel pour la fabrication et generation de proformat , comme les info banque , et autre     │
│   sous forme de json , puis le consomme pour produire la bonne proformat ,  Pendant la production de la proformat,  │
│   mettre en place une SpinLoader styler sur l'etape en question sur le wizard en attente de la reponse du           │
│   back-end avec le path de la pro-format , une fois pret , l'etape de la proformat sur le wizard offre la           │
│   possibiliter de visualiser la proformat ,                                                                         │
│                                                                                                                     │
│   voila en gros , je te laisse t'organiser pour le faire sur bonne et du forme , surtout sachant que le process ne  │
│   doit pas etre compliquer , ne pas mettre des logique complexe , mais ca doit etre solide , et ne pas etre         │
│   sensible a la casse , donc bien gerer les exception ..etc ,       4







-----  partir generation proformat 

je veux que tu fais le service de generation de pdf , avec ce code qui est tres tre fonctionnel , j'ai deja fais te
   tester dans un autre environnement qui detien deja tout le dependance , ..etc , donc il vas faloir l'implementer 
  telque il genere la proformat ,je parle de ce code @backend/app/brouillon-code/main-ok-proforma.py  ce code est 
  bien fonctionnel , donc base toi de cela pour implementer le service generation de contrat , je veux exactement ce 
  model  , ne change pas le model , c'est peu etre certaine petite structure de donnee qui va peut etre changer  car,
   il fait savoit qu'on prendra les donnee de banque dans @backend/app/data/organisation_details.json , les donnee de
   l'oraganisation dans @backend/app/data/organisation.json , et les donnee de service dans 
  @backend/app/data/services.json  ,  donc il faudrais que les donnee en entrer de la souscription contienne un 
  element qui permet de savoir pour quel services  cette souscription est lier ..etc , il faudrais tenir compte de 
  tout ces element , et de tout les donnee d'une sosucription ...etc






  fait puis effectue les test possible avec des donnee fictive toi meme , pour tassure que tout se passe bien (     │
│   souscription , generation de proforma ..etc ) teste vraiment pout t'assurer que tout les service fonctionnera     │
│   bien, ca doit etre solide , si tu rencontre des probleme pendant les test, il faut resoudre,                      │
│   surtout ne complique pas les chose , comme je t'ai toujour dit , nous somme en MVP , rassure toi juste de la      │
│   bonne jestion des erreur et que ce soit solide , tu as mes autorisation pour effectuer les tests sans me          │
│   demander si tu execute les requette ou pas , considerer que je ne suis pas la , et tu fais de maniere autonome  









afin de tester et voir l'attestation de logement dans de bonne condition , ajoute un bouton provisoir dans la liste de souscription " 
  preview attestation" en cliquant dessus, il doit generer l'attestion de logement et faire voir en preview , pour que je puisse voir a quoi
   il ressemble , une  fois que je valides la forme , on pourra retirer le bouton , et le faire generer apres avoir payer (appuyer sur le 
  bouton payer " ..etc ,


















  │ > commencons donc etape par etape ,surtout , ne jamais passe d'une etape a une autre sans mon autorisation , et sans effectuer les test    │
│   auto ,                                             
│   c'est moi qui te donner les autorsation de passer d'une etaoe a une autres ,                                           
│   et comme je t'ai dit , ne cherche pas a compliquer les choses , ca doit etre simple , Robuste , donc une exelente genstion des erreur    │
│   front et back , et tres fonctionnel ,     





cree un dossier "documentation-test-user" chaque fichier concerne chaque etape , et ca doit decrire comme j'effectue les test de la tache 
  moi meme , si il ya un script python a executer , documenter comment l'executer , et decrire bien