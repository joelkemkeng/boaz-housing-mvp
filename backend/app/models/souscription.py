from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import func
from app.database import Base
import enum

class StatutSouscription(str, enum.Enum):
    ATTENTE_PAIEMENT = "ATTENTE_PAIEMENT"
    ATTENTE_LIVRAISON = "ATTENTE_LIVRAISON"
    LIVRE = "LIVRE"
    CLOTURE = "CLOTURE"

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
    
    # Services sélectionnés (stockage des IDs des services depuis services.json)
    services_ids = Column(JSON, nullable=True, default=lambda: [1])  # Par défaut, service ID 1
    
    # Dates de suivi
    date_livraison = Column(Date, nullable=True)
    date_expiration = Column(Date, nullable=True)
    preuve_paiement_path = Column(String, nullable=True)
    cree_par_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Statut et tracking
    statut = Column(Enum(StatutSouscription, values_callable=lambda obj: [e.value for e in obj]), default=StatutSouscription.ATTENTE_PAIEMENT)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    logement = relationship("Logement", backref="souscriptions")
    createur = relationship("User", foreign_keys=[cree_par_user_id])
    
    @validates('statut')
    def validate_statut(self, key, statut):
        # Si c'est déjà une instance StatutSouscription, l'accepter
        if isinstance(statut, StatutSouscription):
            return statut
        
        # Si c'est un string, vérifier qu'il correspond à une valeur valide et le convertir
        if isinstance(statut, str):
            valid_values = [s.value for s in StatutSouscription]
            if statut not in valid_values:
                raise ValueError(f"Statut invalide. Statuts valides: {', '.join(valid_values)}")
            # Convertir le string en enum
            for s in StatutSouscription:
                if s.value == statut:
                    return s
        
        # Cas par défaut - erreur
        valid_statuts = [s.value for s in StatutSouscription]
        raise ValueError(f"Statut invalide. Type: {type(statut)}, Valeur: {statut}. Statuts valides: {', '.join(valid_statuts)}")