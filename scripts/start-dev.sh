#!/bin/bash
# scripts/start-dev.sh

echo "🚀 Démarrage environnement Boaz-Housing MVP..."

# Vérification Docker et Docker Compose
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé"
    exit 1
fi

# Création fichier .env si inexistant
if [ ! -f .env ]; then
    echo "📝 Création fichier .env depuis template..."
    cp .env.example .env
    echo "⚠️  Pensez à personnaliser le fichier .env créé"
fi

# Nettoyage conteneurs existants
echo "🧹 Nettoyage environnement précédent..."
docker-compose down -v --remove-orphans 2>/dev/null

# Construction images
echo "🏗️  Construction des images Docker..."
docker-compose build --no-cache

# Démarrage services
echo "🔄 Démarrage des services..."
docker-compose up -d

# Attente démarrage services
echo "⏳ Attente démarrage complet des services..."
sleep 10

# Vérification santé services
echo "🔍 Vérification santé des services..."

# PostgreSQL
if docker-compose exec postgres pg_isready -U boaz_user -d boaz_housing_mvp >/dev/null 2>&1; then
    echo "✅ PostgreSQL : OK"
else
    echo "❌ PostgreSQL : Erreur"
fi

# Backend
if curl -f http://localhost:8000/health >/dev/null 2>&1; then
    echo "✅ Backend FastAPI : OK"
else
    echo "❌ Backend FastAPI : Erreur"
fi

# Frontend
if curl -f http://localhost:3000 >/dev/null 2>&1; then
    echo "✅ Frontend React : OK"
else
    echo "❌ Frontend React : Erreur"
fi

echo ""
echo "🎉 Environnement Boaz-Housing prêt !"
echo ""
echo "📱 Accès aux services :"
echo "   • Application Frontend : http://localhost:3000"
echo "   • API Backend : http://localhost:8000"
echo "   • Documentation API : http://localhost:8000/docs"
echo "   • PgAdmin : http://localhost:5050"
echo "   • MailHog (Emails) : http://localhost:8025"
echo ""
echo "🔧 Commandes utiles :"
echo "   • Logs : docker-compose logs -f [service]"
echo "   • Shell backend : docker-compose exec backend bash"
echo "   • Shell frontend : docker-compose exec frontend sh"
echo "   • Arrêt : docker-compose down"
echo ""