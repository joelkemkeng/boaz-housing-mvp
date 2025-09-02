#!/usr/bin/env python3
"""
Test de simulation CRON pour vérifier la logique de clôture
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from datetime import date, timedelta
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models.souscription import StatutSouscription
from app.models.logement import StatutLogement

# Configuration base de données (utiliser postgres depuis le conteneur Docker)
DATABASE_URL = "postgresql://boaz_user:boaz_secure_password_2024@postgres:5432/boaz_housing_mvp"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def simulate_cron_closure():
    """Simuler la clôture automatique des souscriptions expirées"""
    db = SessionLocal()
    
    try:
        print(f"=== Simulation CRON Clôture - {date.today()} ===")
        
        # 1. Identifier les souscriptions expirées (LIVRE + date_expiration < aujourd'hui)
        expired_query = text("""
            SELECT id, reference, date_expiration, services_ids, logement_id
            FROM souscriptions 
            WHERE statut = :statut_livre
            AND date_expiration < :today
            AND date_expiration IS NOT NULL
        """)
        
        expired_souscriptions = db.execute(expired_query, {
            "statut_livre": "LIVRE",  # Utiliser la constante enum directement
            "today": date.today()
        }).fetchall()
        
        print(f"Souscriptions expirées trouvées: {len(expired_souscriptions)}")
        
        for souscription in expired_souscriptions:
            print(f"- ID {souscription.id}: {souscription.reference} (expire: {souscription.date_expiration})")
            
            # 2. Changer statut LIVRE → CLOTURE
            update_statut_query = text("""
                UPDATE souscriptions 
                SET statut = :statut_cloture, updated_at = CURRENT_TIMESTAMP
                WHERE id = :souscription_id
            """)
            
            db.execute(update_statut_query, {
                "statut_cloture": "CLOTURE",  # Utiliser la constante enum directement
                "souscription_id": souscription.id
            })
            
            # 3. Si service ID 1 (attestation hébergement), libérer le logement
            services_ids = souscription.services_ids or []
            if 1 in services_ids and souscription.logement_id:
                update_logement_query = text("""
                    UPDATE logements 
                    SET statut = :statut_disponible, updated_at = CURRENT_TIMESTAMP
                    WHERE id = :logement_id
                """)
                
                db.execute(update_logement_query, {
                    "statut_disponible": "DISPONIBLE",  # Utiliser la constante enum directement
                    "logement_id": souscription.logement_id
                })
                
                print(f"  → Logement {souscription.logement_id} libéré (DISPONIBLE)")
            
            print(f"  → Statut: LIVRE → CLOTURE")
        
        db.commit()
        
        if expired_souscriptions:
            print(f"\\n✅ {len(expired_souscriptions)} souscription(s) clôturée(s) avec succès")
        else:
            print("\\n✅ Aucune souscription à clôturer aujourd'hui")
            
    except Exception as e:
        db.rollback()
        print(f"❌ Erreur lors de la clôture: {e}")
    finally:
        db.close()

def create_test_expired_souscription():
    """Créer une souscription expirée pour tester"""
    db = SessionLocal()
    
    try:
        # Créer une souscription avec date d'expiration dans le passé
        insert_query = text("""
            INSERT INTO souscriptions (
                reference, nom_client, prenom_client, email_client,
                ecole_universite, filiere, logement_id, duree_location_mois,
                services_ids, statut, date_livraison, date_expiration,
                created_at
            ) VALUES (
                'ATT-TEST-EXPIRED-001', 'TEST', 'Expired', 'test@expired.com',
                'Test University', 'Test Program', 3, 12,
                '[1]'::json, :statut_livre, '2025-08-01', '2025-08-31',
                CURRENT_TIMESTAMP
            ) RETURNING id
        """)
        
        result = db.execute(insert_query, {
            "statut_livre": "LIVRE"  # Utiliser la constante enum directement
        })
        
        new_id = result.fetchone()[0]
        db.commit()
        
        print(f"✅ Souscription de test expirée créée - ID {new_id}")
        return new_id
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erreur création test: {e}")
        return None
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "create-test":
        create_test_expired_souscription()
    else:
        simulate_cron_closure()