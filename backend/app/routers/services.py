from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any
from app.services.services_data import ServicesDataService

router = APIRouter(
    prefix="/services",
    tags=["services"]
)

# Instance du service
services_data = ServicesDataService()

@router.get("/", response_model=List[Dict[str, Any]])
def get_services(active_only: bool = True):
    """Récupérer la liste des services"""
    try:
        services = services_data.get_all_services(active_only=active_only)
        return services
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des services: {str(e)}"
        )

@router.get("/{service_id}", response_model=Dict[str, Any])
def get_service(service_id: int):
    """Récupérer un service par ID"""
    try:
        service = services_data.get_service_by_id(service_id)
        if not service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service non trouvé"
            )
        return service
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération du service: {str(e)}"
        )

@router.get("/slug/{slug}", response_model=Dict[str, Any])
def get_service_by_slug(slug: str):
    """Récupérer un service par slug"""
    try:
        service = services_data.get_service_by_slug(slug)
        if not service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service non trouvé"
            )
        return service
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération du service: {str(e)}"
        )

@router.post("/calculate-total")
def calculate_services_total(service_ids: List[int]):
    """Calculer le total pour une liste de services"""
    try:
        total = services_data.calculate_services_total(service_ids)
        services = services_data.get_services_by_ids(service_ids)
        
        return {
            "service_ids": service_ids,
            "services": services,
            "total": total,
            "currency": "FCFA"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors du calcul: {str(e)}"
        )

@router.get("/organisation/details", response_model=Dict[str, Any])
def get_organisation_details():
    """Récupérer les détails de l'organisation"""
    try:
        details = services_data.get_organisation_details()
        if not details:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Détails de l'organisation non trouvés"
            )
        return details
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des détails: {str(e)}"
        )