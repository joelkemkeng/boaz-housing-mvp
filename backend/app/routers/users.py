from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.auth_service import auth_service

router = APIRouter(prefix="/users", tags=["Utilisateurs"])

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Créer un nouvel utilisateur"""
    try:
        return auth_service.create_user(db=db, user_create=user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création: {str(e)}")

@router.get("/")
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lister tous les utilisateurs"""
    try:
        # Utiliser SQL direct pour éviter le problème enum
        result = db.execute(text("""
            SELECT id, email, nom, prenom, role, active, created_at, updated_at
            FROM users 
            ORDER BY created_at DESC
            LIMIT :limit OFFSET :skip
        """), {"limit": limit, "skip": skip})
        
        users = []
        for row in result:
            users.append({
                "id": row.id,
                "email": row.email,
                "nom": row.nom,
                "prenom": row.prenom,
                "role": row.role,
                "active": row.active,
                "created_at": row.created_at.isoformat() if row.created_at else None,
                "updated_at": row.updated_at.isoformat() if row.updated_at else None
            })
        
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    """Modifier un utilisateur"""
    try:
        # Vérifier que l'utilisateur existe
        check_result = db.execute(text("""
            SELECT id FROM users WHERE id = :user_id
        """), {"user_id": user_id})
        
        if not check_result.fetchone():
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        
        # Préparer les champs à mettre à jour
        update_fields = []
        update_params = {"user_id": user_id}
        
        if user_update.nom is not None:
            update_fields.append("nom = :nom")
            update_params["nom"] = user_update.nom
            
        if user_update.prenom is not None:
            update_fields.append("prenom = :prenom")
            update_params["prenom"] = user_update.prenom
            
        if user_update.email is not None:
            update_fields.append("email = :email")
            update_params["email"] = user_update.email.lower()
            
        if user_update.role is not None:
            update_fields.append("role = :role")
            update_params["role"] = user_update.role.value
            
        if user_update.active is not None:
            update_fields.append("active = :active")
            update_params["active"] = user_update.active
            
        if user_update.password is not None:
            hashed_password = auth_service.hash_password(user_update.password)
            update_fields.append("password_hash = :password_hash")
            update_params["password_hash"] = hashed_password
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="Aucun champ à mettre à jour")
        
        # Ajouter updated_at
        update_fields.append("updated_at = CURRENT_TIMESTAMP")
        
        # Construire et exécuter la requête de mise à jour
        update_query = f"""
            UPDATE users 
            SET {', '.join(update_fields)}
            WHERE id = :user_id
        """
        
        db.execute(text(update_query), update_params)
        db.commit()
        
        # Récupérer l'utilisateur mis à jour
        result = db.execute(text("""
            SELECT id, email, nom, prenom, role, active, created_at, updated_at
            FROM users 
            WHERE id = :user_id
        """), {"user_id": user_id})
        
        user_row = result.fetchone()
        
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
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur lors de la mise à jour: {str(e)}")

@router.get("/by-email/{email}", response_model=UserResponse)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    """Récupérer un utilisateur par email (pour connexion simple)"""
    try:
        result = db.execute(text("""
            SELECT id, email, nom, prenom, role, active, created_at, updated_at
            FROM users 
            WHERE email = :email
        """), {"email": email.lower()})
        
        user_row = result.fetchone()
        if not user_row:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        
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
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    """Modifier un utilisateur"""
    try:
        # Vérifier que l'utilisateur existe
        check_result = db.execute(text("""
            SELECT id FROM users WHERE id = :user_id
        """), {"user_id": user_id})
        
        if not check_result.fetchone():
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        
        # Préparer les champs à mettre à jour
        update_fields = []
        update_params = {"user_id": user_id}
        
        if user_update.nom is not None:
            update_fields.append("nom = :nom")
            update_params["nom"] = user_update.nom
            
        if user_update.prenom is not None:
            update_fields.append("prenom = :prenom")
            update_params["prenom"] = user_update.prenom
            
        if user_update.email is not None:
            update_fields.append("email = :email")
            update_params["email"] = user_update.email.lower()
            
        if user_update.role is not None:
            update_fields.append("role = :role")
            update_params["role"] = user_update.role.value
            
        if user_update.active is not None:
            update_fields.append("active = :active")
            update_params["active"] = user_update.active
            
        if user_update.password is not None:
            hashed_password = auth_service.hash_password(user_update.password)
            update_fields.append("password_hash = :password_hash")
            update_params["password_hash"] = hashed_password
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="Aucun champ à mettre à jour")
        
        # Ajouter updated_at
        update_fields.append("updated_at = CURRENT_TIMESTAMP")
        
        # Construire et exécuter la requête de mise à jour
        update_query = f"""
            UPDATE users 
            SET {', '.join(update_fields)}
            WHERE id = :user_id
        """
        
        db.execute(text(update_query), update_params)
        db.commit()
        
        # Récupérer l'utilisateur mis à jour
        result = db.execute(text("""
            SELECT id, email, nom, prenom, role, active, created_at, updated_at
            FROM users 
            WHERE id = :user_id
        """), {"user_id": user_id})
        
        user_row = result.fetchone()
        
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
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur lors de la mise à jour: {str(e)}")

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Récupérer un utilisateur par ID"""
    try:
        result = db.execute(text("""
            SELECT id, email, nom, prenom, role, active, created_at, updated_at
            FROM users 
            WHERE id = :user_id
        """), {"user_id": user_id})
        
        user_row = result.fetchone()
        if not user_row:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        
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
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    """Modifier un utilisateur"""
    try:
        # Vérifier que l'utilisateur existe
        check_result = db.execute(text("""
            SELECT id FROM users WHERE id = :user_id
        """), {"user_id": user_id})
        
        if not check_result.fetchone():
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        
        # Préparer les champs à mettre à jour
        update_fields = []
        update_params = {"user_id": user_id}
        
        if user_update.nom is not None:
            update_fields.append("nom = :nom")
            update_params["nom"] = user_update.nom
            
        if user_update.prenom is not None:
            update_fields.append("prenom = :prenom")
            update_params["prenom"] = user_update.prenom
            
        if user_update.email is not None:
            update_fields.append("email = :email")
            update_params["email"] = user_update.email.lower()
            
        if user_update.role is not None:
            update_fields.append("role = :role")
            update_params["role"] = user_update.role.value
            
        if user_update.active is not None:
            update_fields.append("active = :active")
            update_params["active"] = user_update.active
            
        if user_update.password is not None:
            hashed_password = auth_service.hash_password(user_update.password)
            update_fields.append("password_hash = :password_hash")
            update_params["password_hash"] = hashed_password
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="Aucun champ à mettre à jour")
        
        # Ajouter updated_at
        update_fields.append("updated_at = CURRENT_TIMESTAMP")
        
        # Construire et exécuter la requête de mise à jour
        update_query = f"""
            UPDATE users 
            SET {', '.join(update_fields)}
            WHERE id = :user_id
        """
        
        db.execute(text(update_query), update_params)
        db.commit()
        
        # Récupérer l'utilisateur mis à jour
        result = db.execute(text("""
            SELECT id, email, nom, prenom, role, active, created_at, updated_at
            FROM users 
            WHERE id = :user_id
        """), {"user_id": user_id})
        
        user_row = result.fetchone()
        
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
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur lors de la mise à jour: {str(e)}")