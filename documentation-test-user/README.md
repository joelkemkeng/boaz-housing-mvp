# 📋 DOCUMENTATION TESTS - PHASE 1 : SYSTÈME UTILISATEUR

## 🎯 Vue d'ensemble

Cette documentation vous guide pour tester chaque étape de la **Phase 1.1 : Modèle Utilisateur avec Password**.

## 📁 Structure de la documentation

```
documentation-test-user/
├── README.md                           # Ce fichier - Vue d'ensemble
├── 01-test-modele-user.md             # Test du modèle User (SQLAlchemy)
├── 02-test-migration-database.md      # Test de la migration base de données
├── 03-test-schemas-pydantic.md        # Test des schémas Pydantic
├── 04-test-integration-complete.md    # Test d'intégration complet
└── scripts/                           # Scripts de test
    ├── test_user_model_manual.py
    ├── test_schemas_manual.py
    └── test_database_connection.py
```

## 🚀 Prérequis

Avant de commencer les tests :

1. **Docker doit être démarré** :
   ```bash
   cd /home/joel/projet-boaz-housing/boaz-housing-mvp
   docker-compose up -d
   ```

2. **Vérifier que tous les services sont up** :
   ```bash
   docker-compose ps
   ```
   Vous devez voir :
   - boaz-backend (healthy)
   - boaz-postgres (healthy)
   - boaz-frontend
   - boaz-redis-dev
   - boaz-mailhog
   - boaz-pgadmin

3. **Tester la connexion backend** :
   ```bash
   curl http://localhost:8000/health
   ```
   Réponse attendue : `{"status":"ok"}`

## 📝 Ordre des tests

1. **Étape 1** : [Test du modèle User](./01-test-modele-user.md)
2. **Étape 2** : [Test de la migration database](./02-test-migration-database.md)  
3. **Étape 3** : [Test des schémas Pydantic](./03-test-schemas-pydantic.md)
4. **Étape 4** : [Test d'intégration complet](./04-test-integration-complete.md)

## 🆘 En cas de problème

### Docker ne démarre pas
```bash
# Arrêter tous les containers
docker-compose down

# Redémarrer proprement
docker-compose up -d --build
```

### Base de données corrompue
```bash
# Supprimer le volume de données (ATTENTION : perte de données)
docker-compose down -v
docker-compose up -d
```

### Backend ne répond pas
```bash
# Voir les logs du backend
docker-compose logs backend

# Redémarrer juste le backend
docker-compose restart backend
```

## ✅ Résultats attendus

À la fin de tous les tests, vous devriez avoir :
- ✅ Table `users` créée en base de données
- ✅ Modèle User fonctionnel avec validation
- ✅ Schémas Pydantic opérationnels
- ✅ Enum UserRole avec 4 rôles
- ✅ Aucune erreur dans les tests

---

📍 **Commencer par** : [01-test-modele-user.md](./01-test-modele-user.md)