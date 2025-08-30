# 🔄 Gestion Automatique des Migrations

## 📋 Fonctionnement Automatique

Depuis cette mise à jour, **les migrations s'appliquent automatiquement** à chaque démarrage/rebuild du container backend grâce au script `entrypoint.sh` :

1. ⏳ Attente que la base de données soit prête
2. 🔄 Application automatique des migrations (`alembic upgrade head`)
3. 🛠️ Exécution du script de mise à jour des données (`update_existing_data.py`)
4. 🚀 Démarrage du serveur FastAPI

## 🛠️ Workflow de Développement

### 1. Modifier un Modèle SQLAlchemy
```python
# Exemple: Ajouter un champ dans app/models/logement.py
class Logement(Base):
    # ... champs existants
    nouveau_champ = Column(String(100), nullable=True)  # Nouveau !
```

### 2. Créer la Migration Automatiquement
```bash
# Dans le container backend
docker compose exec backend ./create_migration.sh "Ajout nouveau_champ au modèle Logement"
```

### 3. Appliquer la Migration
```bash
# Option 1: Restart automatique (recommandé)
docker compose restart backend

# Option 2: Application manuelle
docker compose exec backend alembic upgrade head
```

## 🔧 Commandes Utiles

### Voir l'état des migrations
```bash
docker compose exec backend alembic current -v
```

### Voir l'historique des migrations
```bash
docker compose exec backend alembic history
```

### Créer une migration manuelle (avancé)
```bash
docker compose exec backend alembic revision -m "Description"
```

### Revenir à une migration précédente (attention !)
```bash
docker compose exec backend alembic downgrade <revision_id>
```

## 🚨 Notes Importantes

- ✅ **Automatique** : Les migrations s'appliquent à chaque rebuild/restart
- ✅ **Sécurisé** : Le script vérifie les erreurs et arrête en cas de problème
- ✅ **Visible** : Tous les logs sont affichés pour suivre le processus
- ⚠️ **Attention** : En cas de conflit, vérifiez manuellement les migrations générées

## 🎯 Plus de Problèmes de Schéma !

Désormais, quand vous :
- Modifiez un modèle
- Créez une migration avec `./create_migration.sh`
- Redémarrez le backend avec `docker compose restart backend`

→ **La migration s'applique automatiquement !** ✨