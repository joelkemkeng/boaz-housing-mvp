import json
import os
from typing import List, Optional, Dict, Any
from pathlib import Path

class ServicesDataService:
    """Service pour gérer les données des services depuis des fichiers JSON"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent / "data"
        self.services_file = self.base_path / "services.json"
        self.organisation_file = self.base_path / "organisation_details.json"
    
    def _load_json(self, file_path: Path) -> Dict[str, Any]:
        """Charger un fichier JSON de manière sécurisée"""
        try:
            if not file_path.exists():
                return {}
            
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erreur lors du chargement de {file_path}: {str(e)}")
            return {}
    
    def get_all_services(self, active_only: bool = True) -> List[Dict[str, Any]]:
        """Récupérer tous les services"""
        try:
            data = self._load_json(self.services_file)
            services = data.get('services', [])
            
            if active_only:
                services = [s for s in services if s.get('active', True)]
            
            return services
        except Exception as e:
            print(f"Erreur lors de la récupération des services: {str(e)}")
            return []
    
    def get_service_by_id(self, service_id: int) -> Optional[Dict[str, Any]]:
        """Récupérer un service par ID"""
        try:
            services = self.get_all_services(active_only=False)
            for service in services:
                if service.get('id') == service_id:
                    return service
            return None
        except Exception as e:
            print(f"Erreur lors de la récupération du service {service_id}: {str(e)}")
            return None
    
    def get_service_by_slug(self, slug: str) -> Optional[Dict[str, Any]]:
        """Récupérer un service par slug"""
        try:
            services = self.get_all_services(active_only=False)
            clean_slug = slug.lower().strip()
            
            for service in services:
                if service.get('slug', '').lower().strip() == clean_slug:
                    return service
            return None
        except Exception as e:
            print(f"Erreur lors de la récupération du service par slug {slug}: {str(e)}")
            return None
    
    def get_services_by_ids(self, service_ids: List[int]) -> List[Dict[str, Any]]:
        """Récupérer plusieurs services par IDs"""
        try:
            services = []
            for service_id in service_ids:
                service = self.get_service_by_id(service_id)
                if service:
                    services.append(service)
            return services
        except Exception as e:
            print(f"Erreur lors de la récupération des services par IDs: {str(e)}")
            return []
    
    def get_organisation_details(self) -> Dict[str, Any]:
        """Récupérer les détails de l'organisation"""
        try:
            data = self._load_json(self.organisation_file)
            return data.get('organisation', {})
        except Exception as e:
            print(f"Erreur lors de la récupération de l'organisation: {str(e)}")
            return {}
    
    def calculate_services_total(self, service_ids: List[int]) -> float:
        """Calculer le total des services sélectionnés"""
        try:
            services = self.get_services_by_ids(service_ids)
            total = sum(service.get('tarif', 0) for service in services)
            return float(total)
        except Exception as e:
            print(f"Erreur lors du calcul du total: {str(e)}")
            return 0.0