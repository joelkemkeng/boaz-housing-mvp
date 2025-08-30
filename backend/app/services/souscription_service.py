import secrets
import string
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.souscription import Souscription, StatutSouscription
from app.models.logement import Logement, StatutLogement
from app.schemas.souscription import SouscriptionCreate, SouscriptionUpdate

def generate_reference() -> str:
    """Génère une référence unique au format ATT-XXXXXXXXXXXXXXXX"""
    random_part = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(16))
    return f"ATT-{random_part}"

class SouscriptionService:
    
    def create_souscription(self, db: Session, souscription: SouscriptionCreate) -> Souscription:
        """Créer une nouvelle souscription"""
        # Vérifier que le logement existe et est libre
        logement = db.query(Logement).filter(Logement.id == souscription.logement_id).first()
        if not logement:
            raise ValueError("Logement non trouvé")
        if logement.statut != StatutLogement.DISPONIBLE:
            raise ValueError("Logement non disponible")
        
        # Générer référence unique
        reference = generate_reference()
        while db.query(Souscription).filter(Souscription.reference == reference).first():
            reference = generate_reference()
        
        # Créer souscription
        db_souscription = Souscription(
            reference=reference,
            **souscription.dict()
        )
        
        db.add(db_souscription)
        db.commit()
        db.refresh(db_souscription)
        return db_souscription
    
    def get_souscriptions(self, db: Session, skip: int = 0, limit: int = 100, 
                         statut: Optional[StatutSouscription] = None) -> List[Souscription]:
        """Récupérer la liste des souscriptions"""
        query = db.query(Souscription)
        if statut:
            query = query.filter(Souscription.statut == statut)
        return query.offset(skip).limit(limit).all()
    
    def get_souscription(self, db: Session, souscription_id: int) -> Optional[Souscription]:
        """Récupérer une souscription par ID"""
        return db.query(Souscription).filter(Souscription.id == souscription_id).first()
    
    def update_souscription(self, db: Session, souscription_id: int, 
                           souscription_update: SouscriptionUpdate) -> Souscription:
        """Mettre à jour une souscription"""
        db_souscription = self.get_souscription(db, souscription_id)
        if not db_souscription:
            raise ValueError("Souscription non trouvée")
        
        # Empêcher modification si statut >= payé
        if db_souscription.statut in [StatutSouscription.PAYE, StatutSouscription.LIVRE, StatutSouscription.CLOTURE]:
            raise ValueError("Modification interdite pour les souscriptions payées")
        
        # Mettre à jour les champs
        update_data = souscription_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_souscription, field, value)
        
        db.commit()
        db.refresh(db_souscription)
        return db_souscription
    
    def changer_statut(self, db: Session, souscription_id: int, 
                      nouveau_statut: StatutSouscription) -> Souscription:
        """Changer le statut d'une souscription"""
        db_souscription = self.get_souscription(db, souscription_id)
        if not db_souscription:
            raise ValueError("Souscription non trouvée")
        
        # Si passage à "payé", changer statut logement
        if nouveau_statut == StatutSouscription.PAYE and db_souscription.statut == StatutSouscription.ATTENTE_PAIEMENT:
            logement = db.query(Logement).filter(Logement.id == db_souscription.logement_id).first()
            if logement:
                logement.statut = StatutLogement.OCCUPE
        
        db_souscription.statut = nouveau_statut
        db.commit()
        db.refresh(db_souscription)
        return db_souscription
    
    def delete_souscription(self, db: Session, souscription_id: int) -> bool:
        """Suppression logique d'une souscription (soft delete)"""
        db_souscription = self.get_souscription(db, souscription_id)
        if not db_souscription:
            return False
        
        # Simple soft delete en supprimant de la base pour le MVP
        db.delete(db_souscription)
        db.commit()
        return True

# Instance globale
souscription_service = SouscriptionService()