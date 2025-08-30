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

-- Créer la base de données de test
CREATE DATABASE boaz_housing_test;

-- Log initialisation
DO $$
BEGIN
    RAISE NOTICE 'Base de données Boaz-Housing initialisée avec succès!';
    RAISE NOTICE 'Base de données de test créée: boaz_housing_test';
END $$;