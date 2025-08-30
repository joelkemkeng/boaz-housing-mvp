#!/usr/bin/env python3
"""
Script pour vider toutes les données des logements

⚠️ ATTENTION: Ce script supprime TOUTES les données des logements !
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://boaz_user:boaz_secure_password_2024@postgres:5432/boaz_housing_mvp")

def clear_all_data():
    """Supprime toutes les données des logements"""
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as connection:
        # Compter les logements avant suppression
        result = connection.execute(text("SELECT COUNT(*) FROM logements"))
        count = result.scalar()
        
        if count == 0:
            print("ℹ️  Aucun logement à supprimer.")
            return
        
        print(f"⚠️  {count} logements vont être supprimés.")
        
        # Demander confirmation
        confirmation = input("Tapez 'CONFIRMER' pour continuer: ")
        if confirmation != 'CONFIRMER':
            print("❌ Opération annulée.")
            return
        
        # Supprimer toutes les données
        connection.execute(text("DELETE FROM logements"))
        connection.commit()
        
        print(f"✅ {count} logements supprimés avec succès!")

if __name__ == "__main__":
    try:
        print("🗑️  Script de suppression des données Boaz-Housing")
        print("=" * 50)
        
        clear_all_data()
        
        print("\n🎉 Script terminé avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution: {e}")
        exit(1)