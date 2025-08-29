from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas.logement import LogementCreate, LogementUpdate, LogementResponse
from app.services.logement_service import logement_service
from app.models.logement import StatutLogement
from app.exceptions.logement_exceptions import LogementException, convert_to_http_exception

router = APIRouter(prefix="/logements", tags=["Logements"])

@router.post("/", response_model=LogementResponse)
def create_logement(
    logement: LogementCreate,
    db: Session = Depends(get_db)
):
    """Créer un nouveau logement"""
    try:
        return logement_service.create_logement(db=db, logement=logement)
    except LogementException as e:
        raise convert_to_http_exception(e)

@router.get("/", response_model=List[LogementResponse])
def list_logements(
    skip: int = Query(0, ge=0, description="Nombre d'éléments à ignorer"),
    limit: int = Query(100, ge=1, le=1000, description="Nombre maximum d'éléments à retourner"),
    statut: Optional[StatutLogement] = Query(None, description="Filtrer par statut"),
    ville: Optional[str] = Query(None, description="Filtrer par ville"),
    db: Session = Depends(get_db)
):
    """Récupérer la liste des logements avec filtres optionnels"""
    return logement_service.get_logements(
        db=db, 
        skip=skip, 
        limit=limit, 
        statut=statut, 
        ville=ville
    )

@router.get("/disponibles", response_model=List[LogementResponse])
def list_logements_disponibles(db: Session = Depends(get_db)):
    """Récupérer tous les logements disponibles"""
    return logement_service.get_logements_disponibles(db=db)

@router.get("/stats")
def get_stats_logements(db: Session = Depends(get_db)):
    """Obtenir les statistiques des logements"""
    return logement_service.get_stats_logements(db=db)

@router.get("/{logement_id}", response_model=LogementResponse)
def get_logement(
    logement_id: int,
    db: Session = Depends(get_db)
):
    """Récupérer un logement par son ID"""
    try:
        db_logement = logement_service.get_logement(db=db, logement_id=logement_id)
        if db_logement is None:
            raise HTTPException(status_code=404, detail="Logement non trouvé")
        return db_logement
    except LogementException as e:
        raise convert_to_http_exception(e)

@router.put("/{logement_id}", response_model=LogementResponse)
def update_logement(
    logement_id: int,
    logement_update: LogementUpdate,
    db: Session = Depends(get_db)
):
    """Mettre à jour un logement"""
    try:
        return logement_service.update_logement(
            db=db, 
            logement_id=logement_id, 
            logement_update=logement_update
        )
    except LogementException as e:
        raise convert_to_http_exception(e)

@router.patch("/{logement_id}/statut")
def changer_statut_logement(
    logement_id: int,
    nouveau_statut: StatutLogement,
    db: Session = Depends(get_db)
):
    """Changer le statut d'un logement"""
    try:
        db_logement = logement_service.changer_statut_logement(
            db=db, 
            logement_id=logement_id, 
            nouveau_statut=nouveau_statut
        )
        return {"message": f"Statut changé vers {nouveau_statut.value}", "logement": db_logement}
    except LogementException as e:
        raise convert_to_http_exception(e)

@router.delete("/{logement_id}")
def delete_logement(
    logement_id: int,
    db: Session = Depends(get_db)
):
    """Supprimer un logement"""
    success = logement_service.delete_logement(db=db, logement_id=logement_id)
    if not success:
        raise HTTPException(status_code=404, detail="Logement non trouvé")
    return {"message": "Logement supprimé avec succès"}