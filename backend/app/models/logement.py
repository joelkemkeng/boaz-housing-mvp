from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, Text, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import validates
from app.database import Base
import enum
import re

class StatutLogement(str, enum.Enum):
    DISPONIBLE = "disponible"
    OCCUPE = "occupe"
    MAINTENANCE = "maintenance"

class Logement(Base):
    __tablename__ = "logements"
    
    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    adresse = Column(String(500), nullable=False)
    ville = Column(String(100), nullable=False)
    code_postal = Column(String(20), nullable=False)
    pays = Column(String(100), nullable=False, default="France")
    loyer = Column(Float, nullable=False)
    montant_charges = Column(Float, nullable=False, default=0.0)
    montant_total = Column(Float, nullable=False)
    statut = Column(Enum(StatutLogement), default=StatutLogement.DISPONIBLE, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Contraintes de base de données
    __table_args__ = (
        CheckConstraint('loyer > 0', name='check_loyer_positive'),
        CheckConstraint('montant_charges >= 0', name='check_charges_positive_ou_nulle'),
        CheckConstraint('montant_total > 0', name='check_montant_total_positive'),
        CheckConstraint('montant_total = loyer + montant_charges', name='check_coherence_montant_total'),
        CheckConstraint("trim(titre) != ''", name='check_titre_non_vide'),
        CheckConstraint("trim(adresse) != ''", name='check_adresse_non_vide'),
        CheckConstraint("trim(ville) != ''", name='check_ville_non_vide'),
        CheckConstraint("trim(code_postal) != ''", name='check_code_postal_non_vide'),
    )
    
    @validates('titre')
    def validate_titre(self, key, titre):
        if not titre or not titre.strip():
            raise ValueError("Le titre ne peut pas être vide")
        if len(titre.strip()) < 3:
            raise ValueError("Le titre doit contenir au moins 3 caractères")
        return titre.strip()
    
    @validates('adresse')
    def validate_adresse(self, key, adresse):
        if not adresse or not adresse.strip():
            raise ValueError("L'adresse ne peut pas être vide")
        if len(adresse.strip()) < 5:
            raise ValueError("L'adresse doit contenir au moins 5 caractères")
        return adresse.strip()
    
    @validates('ville')
    def validate_ville(self, key, ville):
        if not ville or not ville.strip():
            raise ValueError("La ville ne peut pas être vide")
        if len(ville.strip()) < 2:
            raise ValueError("La ville doit contenir au moins 2 caractères")
        # Autoriser uniquement les lettres, espaces, tirets et apostrophes
        if not re.match(r"^[a-zA-ZÀ-ÿ\s\-']+$", ville.strip()):
            raise ValueError("La ville ne doit contenir que des lettres, espaces, tirets et apostrophes")
        return ville.strip().title()
    
    @validates('code_postal')
    def validate_code_postal(self, key, code_postal):
        if not code_postal or not code_postal.strip():
            raise ValueError("Le code postal ne peut pas être vide")
        code_postal = code_postal.strip()
        
        # Validation pour différents formats de codes postaux
        patterns = {
            'France': r'^\d{5}$',
            'Belgique': r'^\d{4}$',
            'Suisse': r'^\d{4}$',
            'Canada': r'^[A-Za-z]\d[A-Za-z] \d[A-Za-z]\d$',
            'USA': r'^\d{5}(-\d{4})?$'
        }
        
        # Par défaut, validation française si pas spécifiée
        if not any(re.match(pattern, code_postal) for pattern in patterns.values()):
            raise ValueError("Format de code postal invalide")
            
        return code_postal.upper()
    
    @validates('pays')
    def validate_pays(self, key, pays):
        if not pays or not pays.strip():
            return "France"  # Valeur par défaut
        
        pays_valides = {
            'france', 'belgique', 'suisse', 'luxembourg', 'canada', 
            'usa', 'etats-unis', 'allemagne', 'italie', 'espagne'
        }
        
        if pays.strip().lower() not in pays_valides:
            raise ValueError(f"Pays non supporté. Pays valides: {', '.join(pays_valides)}")
            
        return pays.strip().title()
    
    @validates('loyer')
    def validate_loyer(self, key, loyer):
        if loyer is None or loyer <= 0:
            raise ValueError("Le loyer doit être supérieur à 0")
        if loyer > 50000:  # Limite raisonnable pour éviter les erreurs de saisie
            raise ValueError("Le loyer semble anormalement élevé (max 50 000€)")
        return round(float(loyer), 2)
    
    @validates('montant_charges')
    def validate_montant_charges(self, key, montant_charges):
        if montant_charges is None:
            return 0.0
        if montant_charges < 0:
            raise ValueError("Le montant des charges ne peut pas être négatif")
        if montant_charges > 10000:  # Limite raisonnable
            raise ValueError("Le montant des charges semble anormalement élevé (max 10 000€)")
        return round(float(montant_charges), 2)
    
    @validates('statut')
    def validate_statut(self, key, statut):
        if statut not in StatutLogement:
            raise ValueError(f"Statut invalide. Statuts valides: {[s.value for s in StatutLogement]}")
        return statut
    
    def __repr__(self):
        return f"<Logement(id={self.id}, titre='{self.titre}', ville='{self.ville}', statut='{self.statut}')>"