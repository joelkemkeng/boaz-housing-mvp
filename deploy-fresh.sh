#!/bin/bash

# Script de déploiement complet pour éviter tous les problèmes de cache Docker

echo "🛑 Arrêt de tous les services..."
docker-compose down

echo "🧹 Nettoyage complet des images et volumes..."
docker-compose down --rmi all --volumes --remove-orphans

echo "🔧 Suppression du cache Docker..."
docker system prune -f

echo "🏗️ Reconstruction complète de tous les services..."
docker-compose build --no-cache

echo "🚀 Démarrage des services..."
docker-compose up -d

echo "⏳ Attente du démarrage des services (30s)..."
sleep 30

echo "🏥 Vérification de la santé des services..."
echo "📊 Backend:"
curl -f http://localhost:8000/api/logements/stats > /dev/null && echo "✅ Backend OK" || echo "❌ Backend KO"

echo "🌐 Frontend:"
curl -f http://localhost:3000 > /dev/null && echo "✅ Frontend OK" || echo "❌ Frontend KO"

echo ""
echo "🎉 Déploiement terminé !"
echo "🌐 Frontend: http://localhost:3000"
echo "📊 Backend: http://localhost:8000"
echo "🗄️ PgAdmin: http://localhost:5050"