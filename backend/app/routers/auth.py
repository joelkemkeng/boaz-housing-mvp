from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.schemas.user import UserLogin
from app.services.auth_service import auth_service
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["Authentification"])

@router.post("/login")
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    """
    Connexion utilisateur avec email/password
    Retourne les informations utilisateur si la connexion réussit
    """
    try:
        # Recherche utilisateur via SQL direct (évite le problème enum SQLAlchemy)
        result = db.execute(text("""
            SELECT id, email, nom, prenom, password_hash, role, active, created_at, updated_at
            FROM users 
            WHERE email = :email AND active = true
        """), {"email": user_login.email.lower()})
        
        user_row = result.fetchone()
        
        if not user_row:
            raise HTTPException(
                status_code=401,
                detail="Email ou mot de passe incorrect"
            )
        
        # Vérifier le mot de passe
        if not auth_service.verify_password(user_login.password, user_row.password_hash):
            raise HTTPException(
                status_code=401,
                detail="Email ou mot de passe incorrect"
            )
        
        # Retourner les informations utilisateur (sans password_hash)
        return {
            "id": user_row.id,
            "email": user_row.email,
            "nom": user_row.nom,
            "prenom": user_row.prenom,
            "role": user_row.role,
            "active": user_row.active,
            "created_at": user_row.created_at.isoformat() if user_row.created_at else None,
            "updated_at": user_row.updated_at.isoformat() if user_row.updated_at else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la connexion: {str(e)}"
        )