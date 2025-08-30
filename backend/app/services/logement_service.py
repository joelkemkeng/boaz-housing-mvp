from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, timedelta
from app.models.logement import Logement, StatutLogement
from app.schemas.logement import LogementCreate, LogementUpdate
from app.exceptions.logement_exceptions import (
    LogementValidationError,
    LogementBusinessRuleError,
    LogementNotFoundError,
    LogementStatutError
)

class LogementService:
    """Service pour la gestion CRUD des logements"""
    
    # Règles métier configurables
    LOYER_MIN = 50.0          # Loyer minimum acceptable
    LOYER_MAX = 50000.0       # Loyer maximum acceptable
    CHARGES_MAX = 10000.0     # Charges maximum acceptables
    MONTANT_TOTAL_MAX = 60000.0  # Montant total maximum
    
    
    def _validate_business_rules(self, logement_data: dict) -> None:
        """Valider les règles métier"""
        loyer = logement_data.get('loyer', 0)
        charges = logement_data.get('montant_charges', 0)
        
        # Règle: loyer dans une fourchette acceptable
        if loyer < self.LOYER_MIN:
            raise LogementBusinessRuleError(
                f"Le loyer doit être d'au moins {self.LOYER_MIN}€", 
                "loyer_minimum"
            )
        
        if loyer > self.LOYER_MAX:
            raise LogementBusinessRuleError(
                f"Le loyer ne peut pas dépasser {self.LOYER_MAX}€", 
                "loyer_maximum"
            )
        
        # Règle: charges raisonnables
        if charges > self.CHARGES_MAX:
            raise LogementBusinessRuleError(
                f"Les charges ne peuvent pas dépasser {self.CHARGES_MAX}€", 
                "charges_maximum"
            )
        
        # Règle: ratio charges/loyer acceptable (charges max 80% du loyer)
        if charges > 0 and charges > (loyer * 0.8):
            raise LogementBusinessRuleError(
                "Les charges ne peuvent pas dépasser 80% du loyer", 
                "ratio_charges_loyer"
            )
        
        # Règle: montant total cohérent
        montant_total = loyer + charges
        if montant_total > self.MONTANT_TOTAL_MAX:
            raise LogementBusinessRuleError(
                f"Le montant total ne peut pas dépasser {self.MONTANT_TOTAL_MAX}€", 
                "montant_total_maximum"
            )
    
    def _check_duplicate_logement(self, db: Session, adresse: str, ville: str, exclude_id: Optional[int] = None) -> None:
        """Vérifier qu'il n'y a pas de doublon sur adresse + ville"""
        query = db.query(Logement).filter(
            Logement.adresse == adresse.strip(),
            Logement.ville == ville.strip()
        )
        
        if exclude_id:
            query = query.filter(Logement.id != exclude_id)
        
        existing = query.first()
        if existing:
            raise LogementBusinessRuleError(
                f"Un logement existe déjà à cette adresse: {adresse}, {ville}",
                "duplicate_adresse"
            )
    
    def create_logement(self, db: Session, logement: LogementCreate) -> Logement:
        """Créer un nouveau logement avec validations métier"""
        try:
            logement_data = logement.dict()
            
            # Validation des règles métier
            self._validate_business_rules(logement_data)
            
            # Vérification des doublons
            self._check_duplicate_logement(db, logement_data['adresse'], logement_data['ville'])
            
            # Calculer le montant total (loyer + charges)
            logement_data['montant_total'] = logement_data['loyer'] + logement_data.get('montant_charges', 0.0)
            
            db_logement = Logement(**logement_data)
            db.add(db_logement)
            db.commit()
            db.refresh(db_logement)
            return db_logement
            
        except IntegrityError as e:
            db.rollback()
            if "check_" in str(e):
                raise LogementValidationError("Données invalides: contrainte de base de données violée")
            raise LogementValidationError("Erreur d'intégrité des données")
    
    def get_logement(self, db: Session, logement_id: int) -> Optional[Logement]:
        """Récupérer un logement par ID"""
        return db.query(Logement).filter(Logement.id == logement_id).first()
    
    def get_logements(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        statut: Optional[StatutLogement] = None,
        ville: Optional[str] = None
    ) -> List[Logement]:
        """Récupérer une liste de logements avec filtres optionnels"""
        query = db.query(Logement)
        
        if statut:
            query = query.filter(Logement.statut == statut)
        
        if ville:
            query = query.filter(Logement.ville.ilike(f"%{ville}%"))
        
        # Tri : dernière activité en premier (création OU modification)
        # COALESCE prend updated_at si présent, sinon created_at
        query = query.order_by(
            func.coalesce(Logement.updated_at, Logement.created_at).desc()
        )
        
        return query.offset(skip).limit(limit).all()
    
    def update_logement(
        self, 
        db: Session, 
        logement_id: int, 
        logement_update: LogementUpdate
    ) -> Logement:
        """Mettre à jour un logement avec validations métier"""
        try:
            db_logement = self.get_logement(db, logement_id)
            if not db_logement:
                raise LogementNotFoundError(logement_id)
            
            # Mise à jour des champs fournis
            update_data = logement_update.dict(exclude_unset=True)
            
            if not update_data:
                raise LogementValidationError("Aucune donnée fournie pour la mise à jour")
            
            # Créer un dictionnaire avec les nouvelles valeurs pour validation
            validation_data = {
                'loyer': update_data.get('loyer', db_logement.loyer),
                'montant_charges': update_data.get('montant_charges', db_logement.montant_charges)
            }
            
            # Validation des règles métier sur les nouvelles valeurs
            self._validate_business_rules(validation_data)
            
            # Vérification des doublons si adresse ou ville changée
            if 'adresse' in update_data or 'ville' in update_data:
                new_adresse = update_data.get('adresse', db_logement.adresse)
                new_ville = update_data.get('ville', db_logement.ville)
                self._check_duplicate_logement(db, new_adresse, new_ville, exclude_id=logement_id)
            
            # Application des modifications
            for field, value in update_data.items():
                setattr(db_logement, field, value)
            
            # Recalculer le montant total si loyer ou charges ont changé
            if 'loyer' in update_data or 'montant_charges' in update_data:
                db_logement.montant_total = db_logement.loyer + db_logement.montant_charges
            
            db.commit()
            db.refresh(db_logement)
            return db_logement
            
        except IntegrityError as e:
            db.rollback()
            if "check_" in str(e):
                raise LogementValidationError("Données invalides: contrainte de base de données violée")
            raise LogementValidationError("Erreur d'intégrité des données")
    
    def delete_logement(self, db: Session, logement_id: int) -> bool:
        """Supprimer un logement"""
        db_logement = self.get_logement(db, logement_id)
        if not db_logement:
            return False
        
        db.delete(db_logement)
        db.commit()
        return True
    
    def get_logements_disponibles(self, db: Session) -> List[Logement]:
        """Récupérer tous les logements disponibles"""
        return self.get_logements(db, statut=StatutLogement.DISPONIBLE)
    
    def _validate_statut_change(self, db_logement: Logement, nouveau_statut: StatutLogement) -> None:
        """Validation simple pour le MVP - aucune restriction"""
        # MVP: Aucune validation, tous les changements de statut sont permis
        pass
    
    def changer_statut_logement(
        self, 
        db: Session, 
        logement_id: int, 
        nouveau_statut: StatutLogement
    ) -> Logement:
        """Changer le statut d'un logement avec validations métier"""
        db_logement = self.get_logement(db, logement_id)
        if not db_logement:
            raise LogementNotFoundError(logement_id)
        
        # MVP: Permettre même statut (pas de restriction)
        if db_logement.statut == nouveau_statut:
            # On fait quand même le changement pour simplifier l'interface
            pass
        
        # Validation des règles de changement de statut
        self._validate_statut_change(db_logement, nouveau_statut)
        
        db_logement.statut = nouveau_statut
        db.commit()
        db.refresh(db_logement)
        return db_logement
    
    def get_stats_logements(self, db: Session) -> dict:
        """Obtenir les statistiques des logements"""
        total = db.query(Logement).count()
        disponibles = db.query(Logement).filter(Logement.statut == StatutLogement.DISPONIBLE).count()
        occupes = db.query(Logement).filter(Logement.statut == StatutLogement.OCCUPE).count()
        maintenance = db.query(Logement).filter(Logement.statut == StatutLogement.MAINTENANCE).count()
        
        return {
            "total": total,
            "disponibles": disponibles,
            "occupes": occupes,
            "maintenance": maintenance
        }

# Instance globale du service
logement_service = LogementService()