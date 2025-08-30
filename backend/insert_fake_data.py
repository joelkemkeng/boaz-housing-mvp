#!/usr/bin/env python3
"""
Script pour insérer les données fictives depuis le fichier JSON

Ce script lit le fichier data/logements_fictifs.json et insère tous les logements
dans la base de données.
"""
import json
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://boaz_user:boaz_secure_password_2024@postgres:5432/boaz_housing_mvp")

def load_fake_data():
    """Charge les données fictives depuis le fichier JSON"""
    json_file = os.path.join(os.path.dirname(__file__), "data", "logements_fictifs.json")
    
    if not os.path.exists(json_file):
        raise FileNotFoundError(f"Fichier de données non trouvé: {json_file}")
    
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def insert_fake_data():
    """Insère les données fictives en base"""
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as connection:
        # Vérifier s'il y a déjà des données
        result = connection.execute(text("SELECT COUNT(*) FROM logements"))
        count = result.scalar()
        
        print(f"📊 {count} logements existants en base.")
        
        # Charger les données JSON
        logements_data = load_fake_data()
        print(f"📁 {len(logements_data)} logements chargés depuis le fichier JSON.")
        
        # Préparer la requête d'insertion
        insert_query = text("""
            INSERT INTO logements (titre, description, adresse, ville, code_postal, pays, 
                                 loyer, montant_charges, montant_total, statut, created_at)
            VALUES (:titre, :description, :adresse, :ville, :code_postal, :pays, 
                   :loyer, :montant_charges, :montant_total, :statut, NOW())
        """)
        
        # Insérer tous les logements un par un
        inserted_count = 0
        for logement in logements_data:
            try:
                # Calculer montant_total
                logement['montant_total'] = logement['loyer'] + logement.get('montant_charges', 0)
                
                connection.execute(insert_query, logement)
                connection.commit()
                inserted_count += 1
                print(f"✅ Inséré: {logement['titre']} ({logement['ville']} - {logement['statut']})")
                
            except Exception as e:
                connection.rollback()
                print(f"❌ Erreur pour {logement['titre']}: {e}")
                continue
        
        # Afficher les statistiques finales
        result = connection.execute(text("""
            SELECT statut, COUNT(*) as count 
            FROM logements 
            GROUP BY statut 
            ORDER BY statut
        """))
        
        stats = dict(result.fetchall())
        total = sum(stats.values())
        
        print(f"\n✅ {inserted_count} logements fictifs insérés avec succès!")
        print(f"📈 Statistiques totales ({total} logements):")
        print(f"   🟢 Disponibles: {stats.get('DISPONIBLE', 0)}")
        print(f"   🔴 Occupés: {stats.get('OCCUPE', 0)}")
        print(f"   🟡 Maintenance: {stats.get('MAINTENANCE', 0)}")

if __name__ == "__main__":
    try:
        print("🏠 Script d'insertion de données fictives Boaz-Housing")
        print("=" * 55)
        
        insert_fake_data()
        
        print("\n🎉 Script terminé avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution: {e}")
        exit(1)