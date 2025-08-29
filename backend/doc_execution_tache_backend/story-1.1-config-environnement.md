# Story 1.1 - Configuration environnement de développement

## ✅ Tâche complétée
**Durée estimée :** 45min  
**Statut :** TERMINÉ  

## 🎯 Objectifs
Configuration complète de l'environnement de développement avec :
- Backend FastAPI avec toutes les dépendances
- Frontend React avec Tailwind CSS, React Router et Axios
- Base de données PostgreSQL
- Services auxiliaires (Redis, MailHog, PgAdmin)
- Docker Compose pour l'orchestration

## 🛠️ Implémentation réalisée - Détail technique

### 1. Configuration Backend FastAPI

**Création du fichier principal `backend/app/main.py` :**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(
    title="Boaz Housing API",
    description="API pour la gestion des logements et souscriptions Boaz Housing",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Boaz Housing API v1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
```

**Procédure technique :**
1. Configuration du middleware CORS pour autoriser les appels du frontend sur localhost:3000
2. Utilisation d'un lifespan manager pour les opérations startup/shutdown
3. Endpoints de base pour tester la connectivité
4. Chargement automatique des variables d'environnement avec python-dotenv

**Création du fichier d'environnement `.env` :**
```bash
DATABASE_URL=postgresql://admin:admin@localhost/boaz_housing_db
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EMAIL_FROM=info@boaz-study.fr
```

### 2. Configuration Frontend React

**Installation des dépendances essentielles :**
```bash
# Dans le répertoire frontend/
npm install react-router-dom axios
npm install -D tailwindcss autoprefixer postcss
npx tailwindcss init -p
```

**Configuration Tailwind CSS `tailwind.config.js` :**
```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",  // Chemin pour scanner les fichiers
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

**Integration Tailwind dans `src/index.css` :**
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
/* Rest du CSS existant conservé */
```

**Procédure technique :**
1. Installation de react-router-dom pour la navigation SPA
2. Installation d'axios pour les appels API vers le backend
3. Configuration Tailwind avec PostCSS pour le processing automatique
4. Inclusion des directives Tailwind dans le point d'entrée CSS

### 3. Orchestration Docker

**Démarrage de l'environnement :**
```bash
bash scripts/start-dev.sh
```

**Ce script exécute :**
1. `docker-compose down --volumes --remove-orphans` - Nettoyage
2. `docker-compose build` - Construction des images
3. `docker-compose up -d` - Démarrage en arrière-plan
4. Vérifications de santé des services

**Services configurés automatiquement :**
- **PostgreSQL** : Base de données principale avec utilisateur admin/admin
- **PgAdmin** : Interface web de gestion PostgreSQL
- **Backend FastAPI** : API avec hot-reload en mode développement
- **Frontend React** : Serveur de développement avec hot-reload
- **MailHog** : Capture des emails en développement
- **Redis** : Cache et sessions (préparé pour usage futur)

## 🧪 Tests de validation
```bash
# Test API Backend
curl http://localhost:8000/
# Résultat : {"message":"Boaz Housing API v1.0.0"}

curl http://localhost:8000/health
# Résultat : {"status":"ok"}

# Test Frontend
curl -I http://localhost:3000/
# Résultat : HTTP/1.1 200 OK
```

## 📊 Services opérationnels
- ✅ PostgreSQL : OK
- ✅ Backend FastAPI : OK  
- ✅ Frontend React : OK
- ✅ PgAdmin : OK
- ✅ MailHog : OK

## 🔗 Points d'accès configurés
- **Application Frontend :** http://localhost:3000
- **API Backend :** http://localhost:8000
- **Documentation API :** http://localhost:8000/docs
- **PgAdmin :** http://localhost:5050
- **MailHog (Emails) :** http://localhost:8025

## 🐛 Problèmes résolus
1. **Erreur module `app.main`** - Résolu en déplaçant `main.py` dans le dossier `app/`
2. **Permissions npm** - Résolu en supprimant/réinstallant `node_modules`
3. **Configuration Tailwind** - Ajout des paths de contenu corrects

## 📝 Commandes utiles
```bash
# Démarrage environnement
bash scripts/start-dev.sh

# Logs des services
docker-compose logs -f [service]

# Shell backend/frontend
docker-compose exec backend bash
docker-compose exec frontend sh

# Arrêt environnement
docker-compose down
```

## 🎯 Prochaine étape
Story 1.2 - Création des modèles de base de données