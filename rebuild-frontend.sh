#!/bin/bash

# Script pour reconstruire complètement le frontend avec les nouvelles dépendances

echo "🔄 Arrêt du container frontend..."
docker stop boaz-frontend

echo "🗑️ Suppression du container frontend..."
docker rm boaz-frontend

echo "🗑️ Suppression de l'image frontend..."
docker rmi $(docker images -q --filter "reference=*frontend*") 2>/dev/null || true

echo "🏗️ Reconstruction complète du frontend..."
docker-compose build --no-cache frontend

echo "🚀 Redémarrage des services..."
docker-compose up -d

echo "✅ Frontend reconstruit avec succès !"
echo "🌐 Application disponible sur http://localhost:3000"