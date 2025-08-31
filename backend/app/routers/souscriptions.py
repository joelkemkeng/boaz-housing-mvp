from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app.database import get_db
from app.schemas.souscription import SouscriptionCreate, SouscriptionUpdate, SouscriptionResponse, StatutUpdate
from app.services.souscription_service import souscription_service
from app.services.proforma_generator import ProformaGenerator
from app.services.services_data import ServicesDataService
from app.models.souscription import StatutSouscription
from pydantic import BaseModel
import os

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

@router.get("/generated-pdfs")
def list_generated_pdfs():
    """Lister tous les PDFs de proforma générés"""
    import os
    import glob
    
    pdf_files = []
    pdf_pattern = "/tmp/proforma_*.pdf"
    
    for pdf_path in glob.glob(pdf_pattern):
        if os.path.exists(pdf_path):
            filename = os.path.basename(pdf_path)
            file_size = os.path.getsize(pdf_path)
            file_time = os.path.getctime(pdf_path)
            
            pdf_files.append({
                "filename": filename,
                "path": pdf_path,
                "size": file_size,
                "created_at": file_time,
                "download_url": f"/api/souscriptions/pdf/{filename}"
            })
    
    return {"pdfs": pdf_files, "count": len(pdf_files)}

@router.get("/pdf/{filename}")
def download_pdf(filename: str):
    """Télécharger un PDF de proforma par nom de fichier"""
    import os
    
    # Sécurité: vérifier que le fichier existe et est un PDF de proforma
    if not filename.startswith("proforma_") or not filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Nom de fichier invalide")
    
    file_path = f"/tmp/{filename}"
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Fichier PDF non trouvé")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/pdf"
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

class ProformaRequest(BaseModel):
    """Modèle pour la génération de proforma"""
    client_data: Dict[str, Any]
    service_ids: List[int]
    logement_data: Dict[str, Any]

@router.post("/generate-proforma")
def generate_proforma(
    proforma_request: ProformaRequest
):
    """Générer une proforma PDF pour une souscription"""
    try:
        # Initialiser les services
        proforma_generator = ProformaGenerator()
        services_data_service = ServicesDataService()
        
        # Récupérer les données des services
        services = services_data_service.get_services_by_ids(proforma_request.service_ids)
        if not services:
            raise HTTPException(status_code=400, detail="Aucun service trouvé pour les IDs fournis")
        
        # Récupérer les détails de l'organisation
        organisation_data = services_data_service.get_organisation_details()
        if not organisation_data:
            raise HTTPException(status_code=500, detail="Détails de l'organisation non disponibles")
        
        # Générer la proforma PDF
        pdf_path = proforma_generator.generate_proforma(
            client_data=proforma_request.client_data,
            services_data=services,
            logement_data=proforma_request.logement_data,
            organisation_data=organisation_data
        )
        
        # Vérifier que le fichier a été créé
        if not os.path.exists(pdf_path):
            raise HTTPException(status_code=500, detail="Erreur lors de la génération du PDF")
        
        # Retourner le fichier PDF
        return FileResponse(
            path=pdf_path,
            filename=f"proforma_{proforma_request.client_data.get('nom', 'client')}.pdf",
            media_type="application/pdf"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la génération de la proforma: {str(e)}"
        )