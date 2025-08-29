#!/usr/bin/env python3
"""
Script pour mettre à jour les données existantes après la migration
"""
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://boaz_user:boaz_secure_password_2024@postgres:5432/boaz_housing_mvp")

def update_existing_data():
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as connection:
        # Mettre à jour les colonnes ajoutées avec des valeurs par défaut appropriées
        connection.execute(text("""
            UPDATE logements 
            SET 
                titre = COALESCE(ville, 'Logement') || ' - ' || COALESCE(adresse, 'Adresse non spécifiée'),
                montant_total = COALESCE(loyer, 0.0),
                pays = COALESCE(pays, 'France')
            WHERE titre = '' OR titre IS NULL OR montant_total = 0.0
        """))
        
        connection.commit()
        print("✅ Données mises à jour avec succès!")

if __name__ == "__main__":
    try:
        update_existing_data()
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour des données: {e}")
        exit(1)