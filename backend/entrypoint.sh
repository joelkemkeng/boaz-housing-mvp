#!/bin/bash
set -e

echo "🚀 Démarrage du backend Boaz-Housing..."

# Attendre que la base de données soit prête
echo "⏳ Attente de la base de données..."
python -c "
import time
import sys
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://boaz_user:boaz_secure_password_2024@postgres:5432/boaz_housing_mvp')

max_retries = 30
retry_count = 0

while retry_count < max_retries:
    try:
        engine = create_engine(DATABASE_URL)
        connection = engine.connect()
        connection.close()
        print('✅ Base de données prête!')
        break
    except OperationalError:
        retry_count += 1
        print(f'⏳ Tentative {retry_count}/{max_retries} - Attente de la base de données...')
        time.sleep(2)
        
if retry_count >= max_retries:
    print('❌ Impossible de se connecter à la base de données')
    sys.exit(1)
"

# Appliquer les migrations automatiquement
echo "🔄 Application des migrations Alembic..."
alembic upgrade head

# Vérifier si les migrations ont réussi
if [ $? -eq 0 ]; then
    echo "✅ Migrations appliquées avec succès"
else
    echo "❌ Erreur lors de l'application des migrations"
    exit 1
fi

# Exécuter le script de mise à jour des données
echo "📊 Exécution du script de mise à jour des données..."
python update_existing_data.py

# Vérifier si le script a réussi
if [ $? -eq 0 ]; then
    echo "✅ Script de données exécuté avec succès"
else
    echo "❌ Erreur lors de l'exécution du script de données"
    exit 1
fi

echo "🎉 Initialisation terminée. Démarrage du serveur..."

# Démarrer l'application
exec "$@"