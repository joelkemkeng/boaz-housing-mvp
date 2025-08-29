from fastapi import APIRouter
from app.services.organisation_service import organisation_service

router = APIRouter(prefix="/organisation", tags=["Organisation"])

@router.get("/info")
def get_organisation_info():
    """Récupère les informations de l'organisation Boaz-Housing"""
    return organisation_service.get_organisation_info()

@router.get("/ceo")
def get_ceo_info():
    """Récupère les informations du CEO"""
    return organisation_service.get_ceo_info()

@router.get("/contact")
def get_contact_info():
    """Récupère les informations de contact"""
    return organisation_service.get_contact_info()

@router.get("/config")
def get_full_config():
    """Récupère toute la configuration (pour développement)"""
    return organisation_service.get_all_config()

@router.post("/generate-reference")
def generate_reference():
    """Génère un code de référence unique pour les souscriptions"""
    reference = organisation_service.generate_reference_code()
    qr_url = organisation_service.generate_qr_code_url(reference)
    return {
        "reference": reference,
        "qr_code_url": qr_url
    }