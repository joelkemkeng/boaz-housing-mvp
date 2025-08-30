#!/bin/bash

# Script pour créer une nouvelle migration Alembic automatiquement
# Usage: ./create_migration.sh "description de la migration"

set -e

if [ -z "$1" ]; then
    echo "❌ Erreur: Veuillez fournir une description pour la migration"
    echo "Usage: $0 \"description de la migration\""
    exit 1
fi

DESCRIPTION="$1"

echo "📝 Création d'une nouvelle migration: $DESCRIPTION"

# Générer la migration automatiquement en comparant les modèles avec la DB
alembic revision --autogenerate -m "$DESCRIPTION"

if [ $? -eq 0 ]; then
    echo "✅ Migration créée avec succès!"
    echo "📋 Pour appliquer la migration:"
    echo "   docker compose restart backend"
    echo "   ou"
    echo "   docker compose exec backend alembic upgrade head"
else
    echo "❌ Erreur lors de la création de la migration"
    exit 1
fi