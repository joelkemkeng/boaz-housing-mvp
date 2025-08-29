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
    
    # Relations
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    logement_id = Column(Integer, ForeignKey("logements.id"), nullable=False)
    
    # Informations souscription
    date_entree = Column(Date, nullable=False)
    duree_location = Column(Integer, nullable=False)  # en mois
    statut = Column(Enum(StatutSouscription), default=StatutSouscription.ATTENTE_PAIEMENT)
    
    # Référence unique
    reference = Column(String, nullable=False, unique=True, index=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    client = relationship("Client", backref="souscriptions")
    logement = relationship("Logement", backref="souscriptions")