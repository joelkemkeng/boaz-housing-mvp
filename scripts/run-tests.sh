#!/bin/bash
# scripts/run-tests.sh

echo "🧪 Lancement tests complets Boaz-Housing..."

# Tests backend
echo "🐍 Tests Backend Python..."
docker-compose exec backend python -m pytest tests/ -v --cov=app --cov-report=term-missing

# Tests frontend  
echo "⚛️ Tests Frontend React..."
docker-compose exec frontend npm test -- --coverage --watchAll=false

# Tests intégration
echo "🔗 Tests d'intégration API..."
docker-compose exec backend python -m pytest tests/integration/ -v

# Health checks
echo "❤️ Vérification santé services..."
./scripts/health-check.sh

echo "✅ Tests terminés!"