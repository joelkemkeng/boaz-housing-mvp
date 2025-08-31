# backend/Dockerfile
FROM python:3.11-slim as base

# Variables environnement
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Installation dépendances système et wkhtmltopdf -- old
# RUN apt-get update && apt-get install -y \
#     gcc \
#     libpq-dev \
#     curl \
#     wget \
#     xz-utils \
#     fontconfig \
#     libxrender1 \
#     libxtst6 \
#     xfonts-75dpi \
#     xfonts-base \
#     libjpeg62-turbo \
#     libxext6 \
#     ca-certificates \
#     && apt-get clean \
#     && mkdir -p /tmp/wkhtml \
#     && cd /tmp/wkhtml \
#     && wget -q https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.stretch_amd64.deb \
#     && ar x wkhtmltox_0.12.6-1.stretch_amd64.deb \
#     && tar -xf data.tar.xz \
#     && cp usr/local/bin/wkhtmltopdf /usr/local/bin/ \
#     && cp usr/local/bin/wkhtmltoimage /usr/local/bin/ \
#     && chmod +x /usr/local/bin/wkhtmltopdf /usr/local/bin/wkhtmltoimage \
#     && cd / && rm -rf /tmp/wkhtml \
#     && rm -rf /var/lib/apt/lists/* \
#     && wkhtmltopdf --version







# (joel copilot) Installation dépendances système et wkhtmltopdf
# Installation dépendances système et wkhtmltopdf
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    wget \
    xz-utils \
    fontconfig \
    libxrender1 \
    libxtst6 \
    xfonts-75dpi \
    xfonts-base \
    libjpeg62-turbo \
    libxext6 \
    ca-certificates \
    && mkdir -p /tmp/wkhtml \
    && cd /tmp/wkhtml \
    # Installation directe de wkhtmltopdf depuis le dépôt officiel
    && wget -q https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-3/wkhtmltox_0.12.6.1-3.bookworm_amd64.deb \
    && apt-get install -y ./wkhtmltox_0.12.6.1-3.bookworm_amd64.deb \
    && rm -rf /tmp/wkhtml \
    && apt-get clean \
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