# 📖 Commandes essentielles pour Docker et le projet Boaz Housing

## 🧹 Formater tout Docker (Images, Volumes, Conteneurs, Cache)
Pour nettoyer complètement Docker et supprimer toutes les ressources associées au projet :
```bash
docker-compose down --rmi all --volumes --remove-orphans
```
- **`--rmi all`** : Supprime toutes les images associées.
- **`--volumes`** : Supprime tous les volumes associés.
- **`--remove-orphans`** : Supprime les conteneurs orphelins.

---

## 🚀 Lancer tout le projet avec Docker Compose
Pour démarrer tous les services du projet :
```bash
docker-compose up -d
```
- **`-d`** : Démarre les services en arrière-plan.

---

## 🛠️ Exécuter un script dans un conteneur Docker
Pour exécuter un script Python dans le conteneur `backend` :
```bash
docker-compose exec backend python insert_fake_data.py
```
- **`exec`** : Permet d'exécuter une commande dans un conteneur en cours d'exécution.
- **`backend`** : Nom du service défini dans `docker-compose.yml`.
- **`python insert_fake_data.py`** : Commande exécutée dans le conteneur.

---

## ✅ Exécuter les tests
Pour exécuter les tests unitaires avec `pytest` dans le conteneur `backend` :
```bash
docker-compose exec backend pytest tests/ -v
```
- **`pytest tests/`** : Lance les tests situés dans le dossier `tests/`.
- **`-v`** : Affiche les résultats des tests avec plus de détails.
---

## 📌 Notes supplémentaires
- **Vérifier les logs des services** :
  ```bash
  docker-compose logs -f
  ```

- **Arrêter tous les services** :
  ```bash
  docker-compose down
  ```