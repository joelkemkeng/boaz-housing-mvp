from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime
import re
from app.models.user import UserRole

class UserBase(BaseModel):
    email: str
    nom: str
    prenom: str
    role: UserRole
    active: bool = True

    @validator('email')
    def validate_email(cls, v):
        if not v or not v.strip():
            raise ValueError("L'email ne peut pas être vide")
        
        v = v.strip().lower()
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError("Format d'email invalide")
        return v

    @validator('nom')
    def validate_nom(cls, v):
        if not v or not v.strip():
            raise ValueError('Le nom ne peut pas être vide')
        v = v.strip()
        if len(v) < 2:
            raise ValueError('Le nom doit contenir au moins 2 caractères')
        return v.title()

    @validator('prenom')
    def validate_prenom(cls, v):
        if not v or not v.strip():
            raise ValueError('Le prénom ne peut pas être vide')
        v = v.strip()
        if len(v) < 2:
            raise ValueError('Le prénom doit contenir au moins 2 caractères')
        return v.title()

class UserCreate(UserBase):
    password: str

    @validator('password')
    def validate_password(cls, v):
        if not v or len(v) < 4:
            raise ValueError('Le mot de passe doit contenir au moins 4 caractères')
        return v

class UserUpdate(BaseModel):
    email: Optional[str] = None
    nom: Optional[str] = None
    prenom: Optional[str] = None
    role: Optional[UserRole] = None
    active: Optional[bool] = None
    password: Optional[str] = None

    @validator('nom')
    def validate_nom(cls, v):
        if v is not None:
            if not v or not v.strip():
                raise ValueError('Le nom ne peut pas être vide')
            v = v.strip()
            if len(v) < 2:
                raise ValueError('Le nom doit contenir au moins 2 caractères')
            return v.title()
        return v

    @validator('prenom')
    def validate_prenom(cls, v):
        if v is not None:
            if not v or not v.strip():
                raise ValueError('Le prénom ne peut pas être vide')
            v = v.strip()
            if len(v) < 2:
                raise ValueError('Le prénom doit contenir au moins 2 caractères')
            return v.title()
        return v

    @validator('password')
    def validate_password(cls, v):
        if v is not None:
            if len(v) < 4:
                raise ValueError('Le mot de passe doit contenir au moins 4 caractères')
        return v

class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: str
    password: str

    @validator('email')
    def validate_email(cls, v):
        if not v or not v.strip():
            raise ValueError("L'email ne peut pas être vide")
        
        v = v.strip().lower()
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError("Format d'email invalide")
        return v

    @validator('password')
    def validate_password(cls, v):
        if not v:
            raise ValueError('Le mot de passe est requis')
        return v