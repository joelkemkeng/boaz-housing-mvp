from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from app.models.souscription import StatutSouscription
from app.schemas.logement import LogementResponse

class SouscriptionBase(BaseModel):
    nom_client: str
    prenom_client: str
    email_client: str
    date_naissance_client: Optional[date] = None
    ville_naissance_client: Optional[str] = None
    pays_naissance_client: Optional[str] = None
    nationalite_client: Optional[str] = None
    pays_destination: Optional[str] = None
    date_arrivee_prevue: Optional[date] = None
    
    # Informations académiques
    ecole_universite: str
    filiere: str
    pays_ecole: Optional[str] = None
    ville_ecole: Optional[str] = None
    code_postal_ecole: Optional[str] = None
    adresse_ecole: Optional[str] = None
    
    # Informations logement
    logement_id: int
    date_entree_prevue: Optional[date] = None
    duree_location_mois: int = 12

class SouscriptionCreate(SouscriptionBase):
    pass

class SouscriptionUpdate(BaseModel):
    nom_client: Optional[str] = None
    prenom_client: Optional[str] = None
    email_client: Optional[str] = None
    date_naissance_client: Optional[date] = None
    ville_naissance_client: Optional[str] = None
    pays_naissance_client: Optional[str] = None
    nationalite_client: Optional[str] = None
    pays_destination: Optional[str] = None
    date_arrivee_prevue: Optional[date] = None
    
    ecole_universite: Optional[str] = None
    filiere: Optional[str] = None
    pays_ecole: Optional[str] = None
    ville_ecole: Optional[str] = None
    code_postal_ecole: Optional[str] = None
    adresse_ecole: Optional[str] = None
    
    logement_id: Optional[int] = None
    date_entree_prevue: Optional[date] = None
    duree_location_mois: Optional[int] = None

class SouscriptionResponse(SouscriptionBase):
    id: int
    reference: str
    statut: StatutSouscription
    created_at: datetime
    updated_at: Optional[datetime]
    logement: Optional[LogementResponse] = None
    
    class Config:
        from_attributes = True

class StatutUpdate(BaseModel):
    statut: StatutSouscription