# Setup Docker Compose - Environnement Boaz-Housing MVP

**Objectif :** Configuration complète environnement de développement avec un seul `docker-compose up`

---

## 1. ARCHITECTURE DOCKER

### 1.1 Services Conteneurisés

```yaml
Services:
├── postgres          # Base de données PostgreSQL
├── backend           # FastAPI Python
├── frontend          # React.js
├── pgadmin          # Interface admin PostgreSQL
└── mailhog          # Serveur SMTP test emails
```

### 1.2 Réseaux et Volumes

- **Network** : `boaz-housing-network` (bridge)
- **Volumes** : 
  - `postgres_data` : persistance données PostgreSQL
  - `pgadmin_data` : configuration PgAdmin
  - `uploads` : stockage temporaire fichiers

---

## 2. STRUCTURE PROJET

### 2.1 Arborescence Recommandée

```
boaz-housing/
├── docker-compose.yml
├── docker-compose.override.yml     # Config développement
├── .env                           # Variables environnement
├── .env.example                   # Template variables
├── README.md
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routers/
│   │   ├── services/
│   │   └── data/
│   │       └── organisation.json
│   ├── alembic/
│   ├── alembic.ini
│   └── tests/
├── frontend/
│   ├── Dockerfile
│   ├── Dockerfile.dev              # Version développement
│   ├── package.json
│   ├── public/
│   └── src/
└── docs/
    └── setup.md
```

---

## 3. FICHIERS DE CONFIGURATION

### 3.1 docker-compose.yml (Production-Ready)

```yaml
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    container_name: boaz-postgres
    environment:
      - POSTGRES_DB=${POSTGRES_DB:-boaz_housing_mvp}
      - POSTGRES_USER=${POSTGRES_USER:-boaz_user}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-boaz_secure_password_2024}
      - POSTGRES_HOST_AUTH_METHOD=trust
    ports:
      - "${POSTGRES_PORT:-5432}:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backend/init-db.sql:/docker-entrypoint-initdb.d/init-db.sql:ro
    networks:
      - boaz-housing-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-boaz_user} -d ${POSTGRES_DB:-boaz_housing_mvp}"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # FastAPI Backend
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
      target: development
    container_name: boaz-backend
    environment:
      - DATABASE_URL=postgresql://${POSTGRES_USER:-boaz_user}:${POSTGRES_PASSWORD:-boaz_secure_password_2024}@postgres:5432/${POSTGRES_DB:-boaz_housing_mvp}
      - CORS_ORIGINS=${CORS_ORIGINS:-http://localhost:3000,http://frontend:3000}
      - SMTP_HOST=${SMTP_HOST:-mailhog}
      - SMTP_PORT=${SMTP_PORT:-1025}
      - SMTP_USERNAME=${SMTP_USERNAME:-}
      - SMTP_PASSWORD=${SMTP_PASSWORD:-}
      - SMTP_USE_TLS=${SMTP_USE_TLS:-false}
      - EMAIL_FROM=${EMAIL_FROM:-info@boaz-study.fr}
      - APP_ENV=${APP_ENV:-development}
      - SECRET_KEY=${SECRET_KEY:-boaz-housing-secret-key-dev-2024}
      - API_V1_PREFIX=/api
    ports:
      - "${BACKEND_PORT:-8000}:8000"
    volumes:
      - ./backend:/app:rw
      - uploads:/app/uploads
    depends_on:
      postgres:
        condition: service_healthy
      mailhog:
        condition: service_started
    networks:
      - boaz-housing-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped
    command: >
      sh -c "
        echo 'Waiting for database...' &&
        python -c 'import time; import psycopg2; 
        while True:
          try: 
            conn = psycopg2.connect(host=\"postgres\", database=\"${POSTGRES_DB:-boaz_housing_mvp}\", user=\"${POSTGRES_USER:-boaz_user}\", password=\"${POSTGRES_PASSWORD:-boaz_secure_password_2024}\")
            conn.close()
            break
          except: 
            time.sleep(1)' &&
        echo 'Database ready!' &&
        alembic upgrade head &&
        echo 'Migrations applied!' &&
        uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
      "

  # React Frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
      target: development
    container_name: boaz-frontend
    environment:
      - REACT_APP_API_URL=${REACT_APP_API_URL:-http://localhost:8000}
      - REACT_APP_ENV=${APP_ENV:-development}
      - CHOKIDAR_USEPOLLING=true
      - WATCHPACK_POLLING=true
    ports:
      - "${FRONTEND_PORT:-3000}:3000"
    volumes:
      - ./frontend:/app:rw
      - /app/node_modules
    depends_on:
      - backend
    networks:
      - boaz-housing-network
    stdin_open: true
    tty: true
    restart: unless-stopped
    command: npm start

  # PgAdmin - Interface Web PostgreSQL
  pgadmin:
    image: dpage/pgadmin4:7
    container_name: boaz-pgadmin
    environment:
      - PGADMIN_DEFAULT_EMAIL=${PGADMIN_EMAIL:-admin@boaz-housing.dev}
      - PGADMIN_DEFAULT_PASSWORD=${PGADMIN_PASSWORD:-admin_boaz_2024}
      - PGADMIN_CONFIG_SERVER_MODE=False
      - PGADMIN_CONFIG_MASTER_PASSWORD_REQUIRED=False
    ports:
      - "${PGADMIN_PORT:-5050}:80"
    volumes:
      - pgadmin_data:/var/lib/pgadmin
      - ./docker/pgadmin/servers.json:/pgadmin4/servers.json:ro
    depends_on:
      - postgres
    networks:
      - boaz-housing-network
    restart: unless-stopped

  # MailHog - Serveur SMTP Test
  mailhog:
    image: mailhog/mailhog:v1.0.1
    container_name: boaz-mailhog
    ports:
      - "${MAILHOG_SMTP_PORT:-1025}:1025"    # SMTP
      - "${MAILHOG_HTTP_PORT:-8025}:8025"    # Interface Web
    networks:
      - boaz-housing-network
    restart: unless-stopped

volumes:
  postgres_data:
    driver: local
  pgadmin_data:
    driver: local
  uploads:
    driver: local

networks:
  boaz-housing-network:
    driver: bridge
    name: boaz-housing-network
```

### 3.2 docker-compose.override.yml (Développement)

```yaml
version: '3.8'

services:
  backend:
    build:
      target: development
    volumes:
      - ./backend:/app:rw
      - uploads:/app/uploads
    environment:
      - DEBUG=true
      - LOG_LEVEL=debug
      - RELOAD=true
    command: >
      sh -c "
        echo 'Development mode - Installing dependencies...' &&
        pip install -r requirements-dev.txt &&
        echo 'Running database migrations...' &&
        alembic upgrade head &&
        echo 'Starting development server with hot reload...' &&
        uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --log-level debug
      "

  frontend:
    build:
      target: development
    volumes:
      - ./frontend:/app:rw
      - /app/node_modules
    environment:
      - FAST_REFRESH=true
      - REACT_APP_DEBUG=true

  # Redis pour cache développement (optionnel)
  redis:
    image: redis:7-alpine
    container_name: boaz-redis-dev
    ports:
      - "6379:6379"
    networks:
      - boaz-housing-network
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data

volumes:
  redis_data:
```

### 3.3 Fichier .env (Variables Environnement)

```bash
# Base de données PostgreSQL
POSTGRES_DB=boaz_housing_mvp
POSTGRES_USER=boaz_user
POSTGRES_PASSWORD=boaz_secure_password_2024
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# Backend FastAPI
BACKEND_PORT=8000
SECRET_KEY=boaz-housing-secret-key-dev-2024-ultra-secure
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
API_V1_PREFIX=/api
APP_ENV=development
DEBUG=true
LOG_LEVEL=info

# Frontend React
FRONTEND_PORT=3000
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENV=development

# Configuration Email SMTP
SMTP_HOST=mailhog
SMTP_PORT=1025
SMTP_USERNAME=
SMTP_PASSWORD=
SMTP_USE_TLS=false
EMAIL_FROM=info@boaz-study.fr

# PgAdmin
PGADMIN_EMAIL=admin@boaz-housing.dev
PGLADMIN_PASSWORD=admin_boaz_2024
PGADMIN_PORT=5050

# MailHog Ports
MAILHOG_SMTP_PORT=1025
MAILHOG_HTTP_PORT=8025

# Organisation Boaz-Housing (utilisé par backend)
ORGANISATION_NAME=Boaz-Housing
ORGANISATION_WEBSITE=www.boaz-study.com
CEO_NAME=Benjamin YOHO BATOMO
CEO_BIRTH_CITY=Douala
CEO_BIRTH_COUNTRY=Cameroun
ORGANISATION_ADDRESS=14 Rue Jean Piestre, Corbeil-Essonnes, 91100, France
ORGANISATION_RCS_CITY=Corbeil-Essonnes
ORGANISATION_EMAIL=info@boaz-study.fr
ORGANISATION_PHONE=+33 01 84 18 02 67

# Développement uniquement
RELOAD=true
CHOKIDAR_USEPOLLING=true
WATCHPACK_POLLING=true
```

### 3.4 Fichier .env.example (Template)

```bash
# Copiez ce fichier vers .env et adaptez les valeurs

# ==============================================
# CONFIGURATION BASE DE DONNÉES
# ==============================================
POSTGRES_DB=boaz_housing_mvp
POSTGRES_USER=boaz_user
POSTGRES_PASSWORD=CHANGEZ_MOI_EN_PRODUCTION
POSTGRES_PORT=5432

# ==============================================
# CONFIGURATION BACKEND
# ==============================================
BACKEND_PORT=8000
SECRET_KEY=GENEREZ_UNE_CLE_SECRETE_FORTE
APP_ENV=development

# ==============================================
# CONFIGURATION FRONTEND  
# ==============================================
FRONTEND_PORT=3000
REACT_APP_API_URL=http://localhost:8000

# ==============================================
# CONFIGURATION EMAIL
# ==============================================
SMTP_HOST=mailhog
SMTP_PORT=1025
EMAIL_FROM=info@boaz-study.fr

# En production, utilisez un vrai serveur SMTP :
# SMTP_HOST=smtp.gmail.com
# SMTP_PORT=587
# SMTP_USERNAME=votre-email@gmail.com
# SMTP_PASSWORD=votre-mot-de-passe-app
# SMTP_USE_TLS=true

# ==============================================
# OUTILS DÉVELOPPEMENT
# ==============================================
PGADMIN_EMAIL=admin@boaz-housing.dev
PGADMIN_PASSWORD=admin_password
MAILHOG_HTTP_PORT=8025
```

---

## 4. DOCKERFILES

### 4.1 Backend Dockerfile

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim as base

# Variables environnement
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Installation dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Création utilisateur non-root
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Répertoire de travail
WORKDIR /app

# Copie requirements et installation dépendances Python
COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Target développement
FROM base as development
RUN pip install --no-cache-dir -r requirements-dev.txt
COPY . .
RUN chown -R appuser:appuser /app
USER appuser
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Target production
FROM base as production
COPY . .
RUN chown -R appuser:appuser /app
USER appuser
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 4.2 Frontend Dockerfile

```dockerfile
# frontend/Dockerfile.dev
FROM node:18-alpine as base

# Variables environnement
ENV NODE_ENV=development

# Installation dépendances système
RUN apk add --no-cache git

# Répertoire de travail
WORKDIR /app

# Copie package.json et installation dépendances
COPY package*.json ./
RUN npm ci --only=development

# Target développement
FROM base as development
COPY . .
EXPOSE 3000
CMD ["npm", "start"]

# Target production  
FROM base as production
ENV NODE_ENV=production
RUN npm ci --only=production
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npx", "serve", "-s", "build", "-l", "3000"]
```

---

## 5. FICHIERS DE CONFIGURATION SUPPLÉMENTAIRES

### 5.1 Configuration PgAdmin

```json
# docker/pgladmin/servers.json
{
    "Servers": {
        "1": {
            "Name": "Boaz-Housing PostgreSQL",
            "Group": "Servers",
            "Host": "postgres",
            "Port": 5432,
            "MaintenanceDB": "boaz_housing_mvp",
            "Username": "boaz_user",
            "Password": "boaz_secure_password_2024",
            "SSLMode": "prefer",
            "Favorite": true
        }
    }
}
```

### 5.2 Script Initialisation Base

```sql
-- backend/init-db.sql
-- Script exécuté automatiquement au premier démarrage PostgreSQL

-- Extension UUID pour génération identifiants uniques
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Extension pour recherche full-text si nécessaire
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Utilisateur application (déjà créé via POSTGRES_USER)
-- Aucune action supplémentaire requise

-- Schema par défaut suffisant pour MVP
-- Les tables seront créées par Alembic

-- Log initialisation
DO $$
BEGIN
    RAISE NOTICE 'Base de données Boaz-Housing initialisée avec succès!';
END $$;
```

### 5.3 Configuration Alembic

```ini
# backend/alembic.ini
[alembic]
script_location = alembic
prepend_sys_path = .
version_path_separator = os
sqlalchemy.url = postgresql://%(POSTGRES_USER)s:%(POSTGRES_PASSWORD)s@%(POSTGRES_HOST)s:5432/%(POSTGRES_DB)s

[post_write_hooks]
hooks = black
black.type = console_scripts
black.entrypoint = black
black.options = --line-length 88

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```

---

## 6. SCRIPTS D'AUTOMATISATION

### 6.1 Script Démarrage Complet

```bash
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
```

### 6.2 Script Tests Complets

```bash
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
```

### 6.3 Script Reset Environnement

```bash
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
```

---

## 7. DOCUMENTATION SETUP

### 7.1 README.md Principal

```markdown
# Boaz-Housing MVP

Plateforme de souscription et gestion de services de logement étudiant à l'étranger.

## 🚀 Démarrage Rapide

### Prérequis
- Docker 20.10+
- Docker Compose 2.0+
- Git

### Installation One-Click
```bash
git clone [repository-url] boaz-housing
cd boaz-housing
chmod +x scripts/*.sh
./scripts/start-dev.sh
```

L'environnement complet sera disponible en 2-3 minutes !

## 📱 Accès Services

| Service | URL | Credentials |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | - |
| **API Backend** | http://localhost:8000 | - |
| **API Docs** | http://localhost:8000/docs | - |
| **PgAdmin** | http://localhost:5050 | admin@boaz-housing.dev / admin_boaz_2024 |
| **MailHog** | http://localhost:8025 | - |

## 🛠️ Développement

### Commandes Utiles
```bash
# Démarrage
docker-compose up -d

# Logs temps réel
docker-compose logs -f backend
docker-compose logs -f frontend

# Shell dans conteneur
docker-compose exec backend bash
docker-compose exec frontend sh

# Tests
./scripts/run-tests.sh

# Reset complet
./scripts/reset-env.sh
```

### Hot Reload
- ✅ Backend FastAPI : Auto-reload activé
- ✅ Frontend React : Hot refresh activé
- ✅ Base données : Persistance garantie

## 📁 Structure Projet
```
boaz-housing/
├── backend/          # FastAPI Python
├── frontend/         # React.js  
├── docker/          # Configurations Docker
├── scripts/         # Scripts automatisation
└── docs/           # Documentation
```

## 🧪 Tests et Qualité

- **Backend** : pytest + coverage
- **Frontend** : Jest + React Testing Library  
- **API** : Tests intégration automatisés
- **E2E** : Procédures manuelles documentées

## 🚢 Production

Variables à modifier pour production dans `.env` :
- `POSTGRES_PASSWORD` : Mot de passe fort
- `SECRET_KEY` : Clé secrète unique
- `SMTP_*` : Configuration SMTP réelle

## 📞 Support

- Documentation complète : `./docs/`
- Issues : [GitHub Issues]
- Contact : info@boaz-study.fr
```

---

## 8. HEALTH CHECKS ET MONITORING

### 8.1 Script Health Check

```bash
#!/bin/bash
# scripts/health-check.sh

echo "🔍 Vérification santé Boaz-Housing..."

# Couleurs pour output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonction test service
check_service() {
    local name=$1
    local url=$2
    local expected_code=${3:-200}
    
    echo -n "Checking $name... "
    
    if response=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null); then
        if [ "$response" = "$expected_code" ]; then
            echo -e "${GREEN}✅ OK${NC} ($response)"
            return 0
        else
            echo -e "${RED}❌ ERROR${NC} (HTTP $response)"
            return 1
        fi
    else
        echo -e "${RED}❌ UNREACHABLE${NC}"
        return 1
    fi
}

# Tests services
echo ""
echo "=== SERVICES HEALTH CHECK ==="

check_service "Frontend React" "http://localhost:3000" 200
check_service "Backend API" "http://localhost:8000/health" 200
check_service "API Docs" "http://localhost:8000/docs" 200
check_service "PgAdmin" "http://localhost:5050" 200
check_service "MailHog" "http://localhost:8025" 200

echo ""
echo "=== DATABASE CHECK ==="
if docker-compose exec -T postgres pg_isready -U boaz_user -d boaz_housing_mvp >/dev/null 2>&1; then
    echo -e "PostgreSQL... ${GREEN}✅ OK${NC}"
else
    echo -e "PostgreSQL... ${RED}❌ ERROR${NC}"
fi

echo ""
echo "=== CONTAINERS STATUS ==="
docker-compose ps

echo ""
echo "=== VOLUMES STATUS ==="
docker volume ls | grep boaz

echo ""
echo "Health check terminé!"
```

---

Cette configuration Docker Compose permet un démarrage complet de l'environnement Boaz-Housing en une seule commande, avec tous les services configurés et prêts à l'emploi pour le développement et les tests.

**Avantages de ce setup :**
- ✅ **Zero-config** : Un seul `docker-compose up` suffit
- ✅ **Hot-reload** : Backend et Frontend se rechargent automatiquement
- ✅ **Services complets** : BDD, API, Frontend, Outils admin
- ✅ **Production-ready** : Configuration adaptable production
- ✅ **Debugging facile** : Logs, health checks, outils admin
- ✅ **Tests intégrés** : Environnement de test automatisé