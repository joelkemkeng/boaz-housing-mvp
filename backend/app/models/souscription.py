from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class StatutSouscription(str, enum.Enum):
    ATTENTE_PAIEMENT = "attente_paiement"
    PAYE = "paye"
    LIVRE = "livre"
    CLOTURE = "cloture"

class Souscription(Base):
    __tablename__ = "souscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    reference = Column(String, nullable=False, unique=True, index=True)
    
    # Informations client
    nom_client = Column(String, nullable=False)
    prenom_client = Column(String, nullable=False)
    email_client = Column(String, nullable=False)
    date_naissance_client = Column(Date, nullable=True)
    ville_naissance_client = Column(String, nullable=True)
    pays_naissance_client = Column(String, nullable=True)
    nationalite_client = Column(String, nullable=True)
    pays_destination = Column(String, nullable=True)
    date_arrivee_prevue = Column(Date, nullable=True)
    
    # Informations académiques
    ecole_universite = Column(String, nullable=False)
    filiere = Column(String, nullable=False)
    pays_ecole = Column(String, nullable=True)
    ville_ecole = Column(String, nullable=True)
    code_postal_ecole = Column(String, nullable=True)
    adresse_ecole = Column(String, nullable=True)
    
    # Informations logement
    logement_id = Column(Integer, ForeignKey("logements.id"), nullable=False)
    date_entree_prevue = Column(Date, nullable=True)
    duree_location_mois = Column(Integer, nullable=False, default=12)
    
    # Statut et tracking
    statut = Column(Enum(StatutSouscription), default=StatutSouscription.ATTENTE_PAIEMENT)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relation
    logement = relationship("Logement", backref="souscriptions")