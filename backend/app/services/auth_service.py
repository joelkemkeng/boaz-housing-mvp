from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from typing import Optional

# Configuration simple pour le hachage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hacher un mot de passe"""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Vérifier un mot de passe"""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """
        Authentifier un utilisateur avec email/password
        Retourne l'utilisateur si valide, None sinon
        """
        try:
            # Rechercher l'utilisateur par email
            user = db.query(User).filter(User.email == email.lower()).first()
            
            if not user:
                return None
            
            # Vérifier que l'utilisateur est actif
            if not user.active:
                return None
            
            # Vérifier le mot de passe
            if not AuthService.verify_password(password, user.password_hash):
                return None
            
            return user
            
        except Exception as e:
            print(f"Erreur d'authentification: {str(e)}")
            return None
    
    @staticmethod
    def create_user(db: Session, user_create: UserCreate) -> User:
        """
        Créer un nouvel utilisateur avec mot de passe haché
        """
        try:
            # Vérifier que l'email n'existe pas déjà
            existing_user = db.query(User).filter(User.email == user_create.email.lower()).first()
            if existing_user:
                raise ValueError("Un utilisateur avec cet email existe déjà")
            
            # Créer l'utilisateur avec mot de passe haché
            db_user = User(
                email=user_create.email.lower(),
                nom=user_create.nom,
                prenom=user_create.prenom,
                password_hash=AuthService.hash_password(user_create.password),
                role=user_create.role,
                active=user_create.active
            )
            
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            
            return db_user
            
        except Exception as e:
            db.rollback()
            raise e

# Instance du service pour utilisation
auth_service = AuthService()