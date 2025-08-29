from fastapi import HTTPException

class LogementException(Exception):
    """Exception de base pour les logements"""
    pass

class LogementValidationError(LogementException):
    """Erreur de validation des données logement"""
    def __init__(self, message: str, field: str = None):
        self.message = message
        self.field = field
        super().__init__(self.message)

class LogementBusinessRuleError(LogementException):
    """Erreur de règle métier pour les logements"""
    def __init__(self, message: str, rule: str = None):
        self.message = message
        self.rule = rule
        super().__init__(self.message)

class LogementNotFoundError(LogementException):
    """Logement non trouvé"""
    def __init__(self, logement_id: int):
        self.logement_id = logement_id
        self.message = f"Logement avec l'ID {logement_id} non trouvé"
        super().__init__(self.message)

class LogementStatutError(LogementException):
    """Erreur liée au changement de statut"""
    def __init__(self, message: str, current_statut: str, target_statut: str):
        self.message = message
        self.current_statut = current_statut
        self.target_statut = target_statut
        super().__init__(self.message)

def convert_to_http_exception(exc: LogementException) -> HTTPException:
    """Convertir une exception métier en HTTPException FastAPI"""
    if isinstance(exc, LogementValidationError):
        return HTTPException(
            status_code=422,
            detail={
                "type": "validation_error",
                "message": exc.message,
                "field": exc.field
            }
        )
    elif isinstance(exc, LogementBusinessRuleError):
        return HTTPException(
            status_code=400,
            detail={
                "type": "business_rule_error", 
                "message": exc.message,
                "rule": exc.rule
            }
        )
    elif isinstance(exc, LogementNotFoundError):
        return HTTPException(
            status_code=404,
            detail={
                "type": "not_found_error",
                "message": exc.message,
                "logement_id": exc.logement_id
            }
        )
    elif isinstance(exc, LogementStatutError):
        return HTTPException(
            status_code=409,
            detail={
                "type": "statut_error",
                "message": exc.message,
                "current_statut": exc.current_statut,
                "target_statut": exc.target_statut
            }
        )
    else:
        return HTTPException(
            status_code=500,
            detail={
                "type": "internal_error",
                "message": "Erreur interne du serveur"
            }
        )