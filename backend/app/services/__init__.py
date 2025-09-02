# Import uniquement ce qui ne dépend pas de SQLAlchemy
try:
    from .organisation_service import organisation_service, OrganisationService
    from .logement_service import logement_service, LogementService
    __all__ = ["organisation_service", "OrganisationService", "logement_service", "LogementService"]
except ImportError:
    # En cas d'erreur (dépendances manquantes), imports limités
    __all__ = []