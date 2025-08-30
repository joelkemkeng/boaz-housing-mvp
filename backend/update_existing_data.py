#!/usr/bin/env python3
"""
Script de mise à jour des données après migration Boaz-Housing

Ce script met à jour les données existantes après une migration.
Il corrige les colonnes qui pourraient avoir des valeurs nulles ou incohérentes.
"""
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://boaz_user:boaz_secure_password_2024@postgres:5432/boaz_housing_mvp")

def update_existing_data():
    """Met à jour les données existantes si nécessaire"""
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as connection:
        # Mettre à jour les colonnes ajoutées avec des valeurs par défaut appropriées
        result = connection.execute(text("""
            UPDATE logements 
            SET 
                titre = COALESCE(ville, 'Logement') || ' - ' || COALESCE(adresse, 'Adresse non spécifiée'),
                montant_total = COALESCE(loyer, 0.0) + COALESCE(montant_charges, 0.0),
                pays = COALESCE(pays, 'France')
            WHERE titre = '' OR titre IS NULL OR montant_total = 0.0 OR pays IS NULL
        """))
        
        if result.rowcount > 0:
            connection.commit()
            print(f"✅ {result.rowcount} logements existants mis à jour!")

if __name__ == "__main__":
    try:
        print("🏠 Script de mise à jour des données Boaz-Housing")
        print("=" * 50)
        
        # Mettre à jour les données existantes
        update_existing_data()
        
        print("🎉 Script terminé avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution: {e}")
        exit(1)