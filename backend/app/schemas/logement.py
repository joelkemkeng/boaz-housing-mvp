from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, Any
from datetime import datetime
from app.models.logement import StatutLogement
import re

class LogementBase(BaseModel):
    """Schéma de base pour un logement"""
    titre: str = Field(..., min_length=3, max_length=200, description="Titre du logement")
    description: Optional[str] = Field(None, max_length=2000, description="Description détaillée du logement")
    adresse: str = Field(..., min_length=5, max_length=500, description="Adresse complète du logement")
    ville: str = Field(..., min_length=2, max_length=100, description="Ville du logement")
    code_postal: str = Field(..., min_length=4, max_length=20, description="Code postal")
    pays: str = Field("France", max_length=100, description="Pays du logement")
    loyer: float = Field(..., gt=0, le=50000, description="Montant du loyer mensuel en euros")
    montant_charges: float = Field(0.0, ge=0, le=10000, description="Montant des charges mensuelles en euros")
    statut: Optional[StatutLogement] = Field(StatutLogement.DISPONIBLE, description="Statut du logement")
    
    @field_validator('titre')
    @classmethod
    def validate_titre(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Le titre ne peut pas être vide')
        v = v.strip()
        if len(v) < 3:
            raise ValueError('Le titre doit contenir au moins 3 caractères')
        if len(v) > 200:
            raise ValueError('Le titre ne peut pas dépasser 200 caractères')
        return v
    
    @field_validator('description')
    @classmethod
    def validate_description(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and len(v.strip()) == 0:
            return None  # Convertir chaîne vide en None
        return v.strip() if v else None
    
    @field_validator('adresse')
    @classmethod
    def validate_adresse(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('L\'adresse ne peut pas être vide')
        v = v.strip()
        if len(v) < 5:
            raise ValueError('L\'adresse doit contenir au moins 5 caractères')
        return v
    
    @field_validator('ville')
    @classmethod
    def validate_ville(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('La ville ne peut pas être vide')
        v = v.strip()
        if len(v) < 2:
            raise ValueError('La ville doit contenir au moins 2 caractères')
        if not re.match(r"^[a-zA-ZÀ-ÿ\s\-']+$", v):
            raise ValueError('La ville ne doit contenir que des lettres, espaces, tirets et apostrophes')
        return v.title()
    
    @field_validator('code_postal')
    @classmethod
    def validate_code_postal(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Le code postal ne peut pas être vide')
        v = v.strip()
        
        # Formats de codes postaux supportés
        patterns = [
            r'^\d{5}$',  # France
            r'^\d{4}$',  # Belgique, Suisse
            r'^[A-Za-z]\d[A-Za-z] \d[A-Za-z]\d$',  # Canada
            r'^\d{5}(-\d{4})?$'  # USA
        ]
        
        if not any(re.match(pattern, v) for pattern in patterns):
            raise ValueError('Format de code postal invalide')
        return v.upper()
    
    @field_validator('pays')
    @classmethod
    def validate_pays(cls, v: str) -> str:
        if not v or not v.strip():
            return "France"
        
        pays_valides = {
            'france', 'belgique', 'suisse', 'luxembourg', 'canada', 
            'usa', 'etats-unis', 'allemagne', 'italie', 'espagne'
        }
        
        if v.strip().lower() not in pays_valides:
            raise ValueError(f'Pays non supporté. Pays valides: {", ".join(sorted(pays_valides))}')
        return v.strip().title()
    
    @field_validator('loyer')
    @classmethod
    def validate_loyer(cls, v: float) -> float:
        if v <= 0:
            raise ValueError('Le loyer doit être supérieur à 0')
        if v > 50000:
            raise ValueError('Le loyer semble anormalement élevé (max 50 000€)')
        return round(float(v), 2)
    
    @field_validator('montant_charges')
    @classmethod
    def validate_montant_charges(cls, v: float) -> float:
        if v < 0:
            raise ValueError('Le montant des charges ne peut pas être négatif')
        if v > 10000:
            raise ValueError('Le montant des charges semble anormalement élevé (max 10 000€)')
        return round(float(v), 2)
    
    @model_validator(mode='after')
    def validate_coherence_prix(self) -> 'LogementBase':
        """Validation de la cohérence des prix"""
        loyer = self.loyer if hasattr(self, 'loyer') else 0
        charges = self.montant_charges if hasattr(self, 'montant_charges') else 0
        
        if loyer and charges:
            montant_total = loyer + charges
            if montant_total > 60000:  # Limite raisonnable pour le total
                raise ValueError('Le montant total (loyer + charges) semble anormalement élevé')
                
        return self

class LogementCreate(LogementBase):
    """Schéma pour créer un logement"""
    pass

class LogementUpdate(BaseModel):
    """Schéma pour mettre à jour un logement"""
    titre: Optional[str] = Field(None, min_length=1, max_length=200, description="Titre du logement")
    description: Optional[str] = Field(None, max_length=2000, description="Description détaillée du logement")
    adresse: Optional[str] = Field(None, description="Adresse complète du logement")
    ville: Optional[str] = Field(None, description="Ville du logement")
    code_postal: Optional[str] = Field(None, description="Code postal")
    pays: Optional[str] = Field(None, description="Pays du logement")
    loyer: Optional[float] = Field(None, gt=0, description="Montant du loyer mensuel en euros")
    montant_charges: Optional[float] = Field(None, ge=0, description="Montant des charges mensuelles en euros")
    statut: Optional[StatutLogement] = Field(None, description="Statut du logement")

class LogementResponse(LogementBase):
    """Schéma de réponse pour un logement"""
    id: int
    montant_total: float = Field(..., description="Montant total (loyer + charges)")
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True