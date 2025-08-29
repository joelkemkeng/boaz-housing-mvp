#!/bin/bash
# scripts/reset-env.sh

echo "🔥 Reset complet environnement Boaz-Housing..."

# Arrêt et suppression complète
docker-compose down -v --rmi all --remove-orphans

# Suppression volumes
docker volume prune -f

# Suppression réseaux
docker network prune -f

# Nettoyage images
docker image prune -f

echo "✅ Environnement complètement nettoyé!"
echo "💡 Relancez ./scripts/start-dev.sh pour redémarrer"