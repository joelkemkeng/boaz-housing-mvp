from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import validates
from app.database import Base
import enum
import re

class UserRole(str, enum.Enum):
    CLIENT = "client"
    AGENT_BOAZ = "agent-boaz"
    ADMIN_GENERALE = "admin-generale"
    BAILLEUR = "bailleur"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    @validates('email')
    def validate_email(self, key, email):
        if not email or not email.strip():
            raise ValueError("L'email ne peut pas être vide")
        
        email = email.strip().lower()
        
        # Validation regex email
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise ValueError("Format d'email invalide")
        
        return email
    
    @validates('nom')
    def validate_nom(self, key, nom):
        if not nom or not nom.strip():
            raise ValueError("Le nom ne peut pas être vide")
        
        nom = nom.strip()
        if len(nom) < 2:
            raise ValueError("Le nom doit contenir au moins 2 caractères")
        
        # Autoriser lettres, espaces, tirets, apostrophes
        if not re.match(r"^[a-zA-ZÀ-ÿ\s\-']+$", nom):
            raise ValueError("Le nom ne doit contenir que des lettres, espaces, tirets et apostrophes")
        
        return nom.title()
    
    @validates('prenom')
    def validate_prenom(self, key, prenom):
        if not prenom or not prenom.strip():
            raise ValueError("Le prénom ne peut pas être vide")
        
        prenom = prenom.strip()
        if len(prenom) < 2:
            raise ValueError("Le prénom doit contenir au moins 2 caractères")
        
        # Autoriser lettres, espaces, tirets, apostrophes
        if not re.match(r"^[a-zA-ZÀ-ÿ\s\-']+$", prenom):
            raise ValueError("Le prénom ne doit contenir que des lettres, espaces, tirets et apostrophes")
        
        return prenom.title()
    
    @validates('role')
    def validate_role(self, key, role):
        # Si c'est déjà une instance UserRole, l'accepter
        if isinstance(role, UserRole):
            return role
        
        # Si c'est un string, vérifier qu'il correspond à une valeur valide et le convertir
        if isinstance(role, str):
            valid_values = [r.value for r in UserRole]
            if role not in valid_values:
                raise ValueError(f"Rôle invalide. Rôles valides: {', '.join(valid_values)}")
            # Convertir le string en enum
            for r in UserRole:
                if r.value == role:
                    return r
        
        # Cas par défaut - erreur
        valid_roles = [r.value for r in UserRole]
        raise ValueError(f"Rôle invalide. Type: {type(role)}, Valeur: {role}. Rôles valides: {', '.join(valid_roles)}")
    
    @validates('password_hash')
    def validate_password_hash(self, key, password_hash):
        if not password_hash or not password_hash.strip():
            raise ValueError("Le hash du mot de passe ne peut pas être vide")
        return password_hash
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role.value}', active={self.active})>"