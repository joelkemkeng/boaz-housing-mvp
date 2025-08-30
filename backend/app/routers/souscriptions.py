from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas.souscription import SouscriptionCreate, SouscriptionUpdate, SouscriptionResponse, StatutUpdate
from app.services.souscription_service import souscription_service
from app.models.souscription import StatutSouscription

router = APIRouter(prefix="/souscriptions", tags=["Souscriptions"])

@router.post("/", response_model=SouscriptionResponse)
def create_souscription(
    souscription: SouscriptionCreate,
    db: Session = Depends(get_db)
):
    """Créer une nouvelle souscription"""
    try:
        return souscription_service.create_souscription(db=db, souscription=souscription)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[SouscriptionResponse])
def list_souscriptions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    statut: Optional[StatutSouscription] = Query(None),
    db: Session = Depends(get_db)
):
    """Récupérer la liste des souscriptions"""
    return souscription_service.get_souscriptions(
        db=db, skip=skip, limit=limit, statut=statut
    )

@router.get("/{souscription_id}", response_model=SouscriptionResponse)
def get_souscription(
    souscription_id: int,
    db: Session = Depends(get_db)
):
    """Récupérer une souscription par ID"""
    db_souscription = souscription_service.get_souscription(db=db, souscription_id=souscription_id)
    if not db_souscription:
        raise HTTPException(status_code=404, detail="Souscription non trouvée")
    return db_souscription

@router.put("/{souscription_id}", response_model=SouscriptionResponse)
def update_souscription(
    souscription_id: int,
    souscription_update: SouscriptionUpdate,
    db: Session = Depends(get_db)
):
    """Mettre à jour une souscription"""
    try:
        return souscription_service.update_souscription(
            db=db, souscription_id=souscription_id, souscription_update=souscription_update
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{souscription_id}/statut")
def changer_statut_souscription(
    souscription_id: int,
    statut_update: StatutUpdate,
    db: Session = Depends(get_db)
):
    """Changer le statut d'une souscription"""
    try:
        db_souscription = souscription_service.changer_statut(
            db=db, souscription_id=souscription_id, nouveau_statut=statut_update.statut
        )
        return {"message": f"Statut changé vers {statut_update.statut.value}", "souscription": db_souscription}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{souscription_id}")
def delete_souscription(
    souscription_id: int,
    db: Session = Depends(get_db)
):
    """Supprimer une souscription"""
    success = souscription_service.delete_souscription(db=db, souscription_id=souscription_id)
    if not success:
        raise HTTPException(status_code=404, detail="Souscription non trouvée")
    return {"message": "Souscription supprimée avec succès"}