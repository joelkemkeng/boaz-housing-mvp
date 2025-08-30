# 📊 Gestion des Données Boaz-Housing

## 📁 Structure des Fichiers

```
backend/
├── data/
│   └── logements_fictifs.json      # 30 logements fictifs prêts à insérer
├── insert_fake_data.py             # Script d'insertion des données JSON
├── clear_data.py                   # Script pour vider toutes les données
└── update_existing_data.py         # Script de mise à jour après migration
```

## 🚀 Utilisation

### 1. Insérer les 30 Logements Fictifs

```bash
# Dans le container backend
docker compose exec backend python insert_fake_data.py
```

**Ce que fait ce script :**
- ✅ Lit le fichier `data/logements_fictifs.json`
- ✅ Insère tous les logements en base
- ✅ Calcule automatiquement `montant_total = loyer + charges`
- ✅ Affiche les statistiques par statut

### 2. Vider Toutes les Données

```bash
# Dans le container backend
docker compose exec backend python clear_data.py
```

**⚠️ ATTENTION :** Ce script supprime TOUS les logements !

### 3. Mise à Jour après Migration

```bash
# Exécuté automatiquement au démarrage du container
python update_existing_data.py
```

## 📋 Contenu des Données Fictives

Le fichier `logements_fictifs.json` contient **30 logements** répartis dans différentes villes françaises :

### 🏙️ **Répartition Géographique**
- Paris (3 logements)
- Lyon, Marseille, Toulouse (2-3 chacun)
- Autres grandes villes (1-2 chacun)

### 🏠 **Types de Logements**
- Studios : 8 logements
- T2 : 10 logements  
- T3 : 7 logements
- T4 : 2 logements
- Autres (Loft, Penthouse, Maison) : 3 logements

### 📊 **Répartition des Statuts**
- 🟢 **Disponible** : ~60% (18 logements)
- 🔴 **Occupé** : ~30% (9 logements)
- 🟡 **Maintenance** : ~10% (3 logements)

### 💰 **Gamme de Prix**
- **Studios** : 320€ - 850€/mois
- **T2** : 420€ - 750€/mois
- **T3+** : 510€ - 2800€/mois

## 🎯 **Workflow Recommandé**

```bash
# 1. Démarrer les services (migrations automatiques)
docker compose up -d

# 2. Insérer les données de démonstration
docker compose exec backend python insert_fake_data.py

# 3. Vérifier via l'API
curl http://localhost:8000/api/logements/stats

# 4. Si besoin de recommencer, vider d'abord
docker compose exec backend python clear_data.py
```

## 📝 **Personnalisation des Données**

Pour modifier les données fictives :

1. **Éditer le fichier JSON** : `data/logements_fictifs.json`
2. **Respecter la structure** :
   ```json
   {
     "titre": "String (obligatoire)",
     "description": "String (optionnel)",
     "adresse": "String (obligatoire)",
     "ville": "String (obligatoire)",
     "code_postal": "String (obligatoire)",
     "pays": "String (défaut: France)",
     "loyer": 0.0,
     "montant_charges": 0.0,
     "statut": "disponible|occupe|maintenance"
   }
   ```
3. **Relancer l'insertion** : `python insert_fake_data.py`

## ✨ **Avantages de cette Approche**

- ✅ **Données réalistes** : Adresses, prix et descriptions cohérentes
- ✅ **Facile à modifier** : Simple édition du fichier JSON
- ✅ **Répétable** : Même jeu de données à chaque insertion
- ✅ **Contrôlable** : Scripts séparés pour insérer/vider
- ✅ **Visible** : Toutes les données dans un fichier lisible