import secrets
import string
import json
from datetime import date, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
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
        query = db.query(Souscription).options(joinedload(Souscription.logement))
        if statut:
            query = query.filter(Souscription.statut == statut)
        return query.offset(skip).limit(limit).all()
    
    def get_souscription(self, db: Session, souscription_id: int) -> Optional[Souscription]:
        """Récupérer une souscription par ID"""
        return db.query(Souscription).options(joinedload(Souscription.logement)).filter(Souscription.id == souscription_id).first()
    
    def update_souscription(self, db: Session, souscription_id: int, 
                           souscription_update: SouscriptionUpdate) -> Souscription:
        """Mettre à jour une souscription"""
        db_souscription = self.get_souscription(db, souscription_id)
        if not db_souscription:
            raise ValueError("Souscription non trouvée")
        
        # Empêcher modification si statut >= livraison
        if db_souscription.statut in [StatutSouscription.LIVRE, StatutSouscription.CLOTURE]:
            raise ValueError("Modification interdite pour les souscriptions livrées ou clôturées")
        
        # Vérifier le nouveau logement s'il est fourni
        update_data = souscription_update.dict(exclude_unset=True)
        if 'logement_id' in update_data:
            nouveau_logement_id = update_data['logement_id']
            if nouveau_logement_id != db_souscription.logement_id:
                logement = db.query(Logement).filter(Logement.id == nouveau_logement_id).first()
                if not logement:
                    raise ValueError("Nouveau logement non trouvé")
                if logement.statut != StatutLogement.DISPONIBLE:
                    raise ValueError("Nouveau logement non disponible")
        
        # Mettre à jour les champs
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
        
        # Si passage à "attente livraison", le logement reste disponible jusqu'à la livraison effective
        # La logique de changement de statut du logement est gérée dans livrer_souscription()
        
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
    
    def payer_souscription(self, db: Session, souscription_id: int, preuve_paiement_path: Optional[str] = None) -> Souscription:
        """Action Payer : ATTENTE_PAIEMENT → ATTENTE_LIVRAISON"""
        db_souscription = self.get_souscription(db, souscription_id)
        if not db_souscription:
            raise ValueError("Souscription non trouvée")
        
        # Vérifier le statut actuel
        if db_souscription.statut != StatutSouscription.ATTENTE_PAIEMENT:
            raise ValueError(f"Impossible de payer: statut actuel {db_souscription.statut}")
        
        # Changer le statut
        db_souscription.statut = StatutSouscription.ATTENTE_LIVRAISON
        
        # Ajouter la preuve de paiement si fournie
        if preuve_paiement_path:
            db_souscription.preuve_paiement_path = preuve_paiement_path
        
        db.commit()
        db.refresh(db_souscription)
        return db_souscription
    
    def livrer_souscription(self, db: Session, souscription_id: int) -> Souscription:
        """Action Livrer : ATTENTE_LIVRAISON → LIVRE (+ calcul date_expiration)"""
        db_souscription = self.get_souscription(db, souscription_id)
        if not db_souscription:
            raise ValueError("Souscription non trouvée")
        
        # Vérifier le statut actuel
        if db_souscription.statut != StatutSouscription.ATTENTE_LIVRAISON:
            raise ValueError(f"Impossible de livrer: statut actuel {db_souscription.statut}")
        
        # Valider que le logement est disponible
        if not self.valider_logement_disponible(db, db_souscription.logement_id):
            raise ValueError("Logement non disponible pour livraison")
        
        # Calculer la date d'expiration selon les services
        duree_validite_jours = self._get_duree_validite_services(db_souscription.services_ids or [1])
        
        # Changer le statut et définir les dates
        db_souscription.statut = StatutSouscription.LIVRE
        db_souscription.date_livraison = date.today()
        db_souscription.date_expiration = date.today() + timedelta(days=duree_validite_jours)
        
        # Marquer le logement comme occupé si service ID 1 (attestation hébergement)
        if 1 in (db_souscription.services_ids or []):
            logement = db.query(Logement).filter(Logement.id == db_souscription.logement_id).first()
            if logement:
                logement.statut = StatutLogement.OCCUPE
        
        db.commit()
        db.refresh(db_souscription)
        return db_souscription
    
    def valider_logement_disponible(self, db: Session, logement_id: int) -> bool:
        """Vérifier qu'un logement est disponible pour livraison"""
        logement = db.query(Logement).filter(Logement.id == logement_id).first()
        if not logement:
            return False
        return logement.statut == StatutLogement.DISPONIBLE
    
    def _get_duree_validite_services(self, services_ids: List[int]) -> int:
        """Récupérer la durée de validité en jours depuis services.json"""
        try:
            with open('/app/app/data/services.json', 'r', encoding='utf-8') as f:
                services_data = json.load(f)
            
            # Par défaut 365 jours (1 an)
            duree_max = 365
            
            for service_id in services_ids:
                for service in services_data.get('services', []):
                    if service['id'] == service_id:
                        duree_service = service.get('duree_validite_jours', 365)
                        duree_max = max(duree_max, duree_service)
                        break
            
            return duree_max
        except Exception:
            # Fallback à 365 jours si erreur
            return 365

# Instance globale
souscription_service = SouscriptionService()