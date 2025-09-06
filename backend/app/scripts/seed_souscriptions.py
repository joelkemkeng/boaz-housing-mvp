#!/usr/bin/env python3
"""
Script de seed pour créer des souscriptions fictives
"""
import sys
import os
sys.path.append('/app')

import json
from datetime import datetime, date
from app.database import get_db
from app.models.souscription import Souscription, StatutSouscription
from app.models.logement import Logement
from app.models.user import User

def load_souscriptions_data():
    """Charger les données depuis le fichier JSON"""
    json_path = "/app/data/souscriptions_fictives.json"
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Fichier {json_path} non trouvé")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ Erreur de lecture JSON: {e}")
        return []

def convert_date_string(date_string):
    """Convertir une chaîne de date en objet date"""
    if not date_string:
        return None
    try:
        return datetime.strptime(date_string, "%Y-%m-%d").date()
    except ValueError:
        print(f"⚠️  Format de date invalide: {date_string}")
        return None

def seed_souscriptions():
    """Créer les souscriptions fictives"""
    
    print("🌱 Script d'insertion de souscriptions fictives Boaz-Housing")
    print("=" * 65)
    
    db = next(get_db())
    
    try:
        # Compter les souscriptions existantes
        existing_count = db.query(Souscription).count()
        print(f"📊 {existing_count} souscriptions existantes en base.")
        
        # Charger les données
        souscriptions_data = load_souscriptions_data()
        if not souscriptions_data:
            print("❌ Aucune donnée à insérer")
            return False
            
        print(f"📁 {len(souscriptions_data)} souscriptions chargées depuis le fichier JSON.")
        
        # Récupérer les mappings pour les relations
        users_by_email = {user.email: user for user in db.query(User).all()}
        logements_by_id = {logement.id: logement for logement in db.query(Logement).all()}
        
        created_count = 0
        updated_count = 0
        
        for souscription_data in souscriptions_data:
            # Vérifier si la souscription existe déjà
            existing_souscription = db.query(Souscription).filter(
                Souscription.reference == souscription_data["reference"]
            ).first()
            
            if existing_souscription:
                print(f"📧 {souscription_data['reference']} existe déjà - ignoré")
                continue
            
            # Vérifier que le logement existe
            logement_id = souscription_data.get("logement_id")
            if logement_id not in logements_by_id:
                print(f"⚠️  Logement ID {logement_id} non trouvé pour {souscription_data['reference']} - ignoré")
                continue
            
            # Trouver l'utilisateur créateur
            cree_par_user_email = souscription_data.get("cree_par_user_email")
            cree_par_user_id = None
            if cree_par_user_email and cree_par_user_email in users_by_email:
                cree_par_user_id = users_by_email[cree_par_user_email].id
            
            # Créer la souscription
            try:
                nouvelle_souscription = Souscription(
                    reference=souscription_data["reference"],
                    nom_client=souscription_data["nom_client"],
                    prenom_client=souscription_data["prenom_client"],
                    email_client=souscription_data["email_client"],
                    date_naissance_client=convert_date_string(souscription_data.get("date_naissance_client")),
                    ville_naissance_client=souscription_data.get("ville_naissance_client"),
                    pays_naissance_client=souscription_data.get("pays_naissance_client"),
                    nationalite_client=souscription_data.get("nationalite_client"),
                    pays_destination=souscription_data.get("pays_destination"),
                    date_arrivee_prevue=convert_date_string(souscription_data.get("date_arrivee_prevue")),
                    ecole_universite=souscription_data["ecole_universite"],
                    filiere=souscription_data["filiere"],
                    pays_ecole=souscription_data.get("pays_ecole"),
                    ville_ecole=souscription_data.get("ville_ecole"),
                    code_postal_ecole=souscription_data.get("code_postal_ecole"),
                    adresse_ecole=souscription_data.get("adresse_ecole"),
                    logement_id=logement_id,
                    date_entree_prevue=convert_date_string(souscription_data.get("date_entree_prevue")),
                    duree_location_mois=souscription_data.get("duree_location_mois", 12),
                    services_ids=souscription_data.get("services_ids", [1]),
                    statut=souscription_data.get("statut", "ATTENTE_PAIEMENT"),
                    cree_par_user_id=cree_par_user_id
                )
                
                db.add(nouvelle_souscription)
                db.flush()
                
                logement = logements_by_id[logement_id]
                user_info = f" par {cree_par_user_email}" if cree_par_user_email else ""
                print(f"✅ Inséré: {nouvelle_souscription.reference} - {nouvelle_souscription.prenom_client} {nouvelle_souscription.nom_client} → {logement.titre} ({nouvelle_souscription.statut}){user_info}")
                created_count += 1
                
            except Exception as e:
                print(f"❌ Erreur lors de l'insertion de {souscription_data['reference']}: {str(e)}")
                continue
        
        db.commit()
        
        print(f"\n✅ {created_count} souscriptions fictives insérées avec succès!")
        
        # Statistiques par statut
        total_souscriptions = db.query(Souscription).count()
        print(f"📈 Statistiques totales ({total_souscriptions} souscriptions):")
        
        for statut in StatutSouscription:
            count = db.query(Souscription).filter(Souscription.statut == statut).count()
            if count > 0:
                icon = {
                    "ATTENTE_PAIEMENT": "🟡",
                    "ATTENTE_LIVRAISON": "🟠", 
                    "PAYE": "🔵",
                    "LIVRE": "🟢",
                    "CLOTURE": "⚫"
                }.get(statut.value, "📋")
                print(f"   {icon} {statut.value}: {count}")
        
        # Statistiques par utilisateur créateur
        print(f"\n👥 Répartition par créateur:")
        from sqlalchemy import func
        user_stats = db.query(User.email, func.count(Souscription.id).label('count'))\
                      .join(Souscription, User.id == Souscription.cree_par_user_id, isouter=True)\
                      .group_by(User.email)\
                      .having(func.count(Souscription.id) > 0)\
                      .all()
        
        for email, count in user_stats:
            print(f"   📧 {email}: {count} souscriptions")
        
        print(f"\n🎉 Script terminé avec succès!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du seed: {str(e)}")
        db.rollback()
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = seed_souscriptions()
    exit(0 if success else 1)
