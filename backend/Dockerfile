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
# Rendre le script entrypoint exécutable AVANT le changement d'utilisateur
RUN chmod +x entrypoint.sh && \
    chown -R appuser:appuser /app
USER appuser
EXPOSE 8000
ENTRYPOINT ["./entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Target production
FROM base as production
COPY . .
# Rendre le script entrypoint exécutable AVANT le changement d'utilisateur
RUN chmod +x entrypoint.sh && \
    chown -R appuser:appuser /app
USER appuser
EXPOSE 8000
ENTRYPOINT ["./entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]