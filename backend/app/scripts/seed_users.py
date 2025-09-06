#!/usr/bin/env python3
"""
Script de seed pour créer les 3 utilisateurs par défaut
"""
import sys
import os
sys.path.append('/app')

from app.database import get_db
from app.models.user import User, UserRole
from app.services.auth_service import auth_service

def seed_default_users():
    """Créer les 3 utilisateurs par défaut"""
    
    print("🌱 Seed des utilisateurs par défaut...")
    
    # Utilisateurs par défaut selon les spécifications
    default_users = [
        {
            "email": "agent@boaz-study.com",
            "nom": "AGENT",
            "prenom": "Boaz",
            "password": "agent1234",
            "role": "agent-boaz"
        },
        {
            "email": "bailleur@boaz-study.com", 
            "nom": "BAILLEUR",
            "prenom": "Boaz",
            "password": "bailleur1234",
            "role": "bailleur"
        },
        {
            "email": "ceo@boaz-study.com",
            "nom": "CEO",
            "prenom": "Admin",
            "password": "ceo1234", 
            "role": "admin-generale"
        }
    ]
    
    db = next(get_db())
    
    try:
        created_count = 0
        updated_count = 0
        
        for user_data in default_users:
            # Vérifier si l'utilisateur existe déjà
            existing_user = db.query(User).filter(User.email == user_data["email"]).first()
            
            if existing_user:
                print(f"📧 {user_data['email']} existe déjà - mise à jour du mot de passe")
                # Mettre à jour le mot de passe
                existing_user.password_hash = auth_service.hash_password(user_data["password"])
                existing_user.role = user_data["role"]
                existing_user.active = True
                updated_count += 1
            else:
                print(f"➕ Création de {user_data['email']}...")
                
                # Créer l'utilisateur directement (évite le service qui peut avoir des validations)
                db_user = User(
                    email=user_data["email"],
                    nom=user_data["nom"],
                    prenom=user_data["prenom"],
                    password_hash=auth_service.hash_password(user_data["password"]),
                    role=user_data["role"],
                    active=True
                )
                db.add(db_user)
                db.flush()
                new_user = db_user
                created_count += 1
                
                print(f"✅ {new_user.email} créé (ID: {new_user.id})")
        
        db.commit()
        
        print(f"\n🎉 Seed terminé !")
        print(f"   ➕ {created_count} utilisateurs créés")
        print(f"   🔄 {updated_count} utilisateurs mis à jour")
        
        # Afficher les utilisateurs créés
        print(f"\n👥 Utilisateurs disponibles :")
        users = db.query(User).all()
        for user in users:
            status = "🟢" if user.active else "🔴"
            print(f"   {status} {user.email} - {user.role.value} ({user.prenom} {user.nom})")
            
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du seed: {str(e)}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = seed_default_users()
    exit(0 if success else 1)