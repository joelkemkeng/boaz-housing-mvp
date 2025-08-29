from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Client(Base):
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Informations personnelles
    nom_complet = Column(String, nullable=False)
    date_naissance = Column(Date, nullable=False)
    ville_naissance = Column(String, nullable=False)
    pays_naissance = Column(String, nullable=False)
    
    # Informations de contact
    email = Column(String, nullable=False, unique=True, index=True)
    telephone = Column(String, nullable=False)
    
    # Informations académiques
    etablissement = Column(String, nullable=False)
    niveau_etude = Column(String, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())