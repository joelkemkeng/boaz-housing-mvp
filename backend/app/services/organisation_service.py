import json
import os
from typing import Dict, Any
from datetime import datetime
import secrets
import string

class OrganisationService:
    """Service pour gérer les données statiques de l'organisation Boaz-Housing"""
    
    def __init__(self):
        self.config_file = os.path.join(os.path.dirname(__file__), "../data/organisation.json")
        self._config = None
    
    def _load_config(self) -> Dict[str, Any]:
        """Charge la configuration depuis le fichier JSON"""
        if self._config is None:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self._config = json.load(f)
        return self._config
    
    def get_organisation_info(self) -> Dict[str, Any]:
        """Retourne les informations de l'organisation"""
        config = self._load_config()
        return config["organisation"]
    
    def get_ceo_info(self) -> Dict[str, Any]:
        """Retourne les informations du CEO"""
        config = self._load_config()
        return config["ceo"]
    
    def get_documents_config(self) -> Dict[str, Any]:
        """Retourne la configuration des documents"""
        config = self._load_config()
        return config["documents"]
    
    def generate_reference_code(self) -> str:
        """Génère un code de référence unique pour les souscriptions"""
        # Format: ATT-{12_caractères_aléatoires}
        random_part = ''.join(secrets.choice(string.ascii_uppercase + string.digits) 
                             for _ in range(12))
        return f"ATT-{random_part}"
    
    def generate_qr_code_url(self, reference: str) -> str:
        """Génère l'URL du QR code pour vérification"""
        config = self._load_config()
        base_url = config["documents"]["qr_code_base_url"]
        return f"{base_url}/{reference}"
    
    def get_all_config(self) -> Dict[str, Any]:
        """Retourne toute la configuration"""
        return self._load_config()
    
    def format_address_for_document(self) -> str:
        """Formate l'adresse pour les documents PDF"""
        org = self.get_organisation_info()
        return org["adresse_siege"]
    
    def get_contact_info(self) -> Dict[str, str]:
        """Retourne les informations de contact formatées"""
        org = self.get_organisation_info()
        return {
            "email": org["email_contact"],
            "telephone": org["telephone"],
            "site_web": org["site_web"]
        }

# Instance globale pour utilisation dans l'app
organisation_service = OrganisationService()