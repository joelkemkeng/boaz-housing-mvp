// Utilitaire pour gérer les erreurs de manière centralisée et simple

/**
 * Extrait un message d'erreur lisible depuis différents formats d'erreur
 * @param {Error|Object|string} error - L'erreur à traiter
 * @returns {string} - Message d'erreur lisible
 */
export const getErrorMessage = (error) => {
  // Si c'est déjà une string, la retourner
  if (typeof error === 'string') {
    return error;
  }

  // Si c'est une erreur avec response (erreur Axios)
  if (error?.response?.data) {
    const data = error.response.data;
    
    // Si c'est un objet avec detail (FastAPI)
    if (data.detail) {
      // Si detail est un array d'erreurs de validation
      if (Array.isArray(data.detail)) {
        return data.detail.map(err => {
          const field = err.loc?.join(' > ') || 'Champ';
          return `${field}: ${err.msg}`;
        }).join('\n');
      }
      // Si detail est une string
      if (typeof data.detail === 'string') {
        return data.detail;
      }
    }
    
    // Si c'est un message direct
    if (data.message) {
      return data.message;
    }
    
    // Si c'est juste le data en string
    if (typeof data === 'string') {
      return data;
    }
  }

  // Erreur réseau (vérifier avant les messages génériques)
  if (error?.code === 'NETWORK_ERROR' || error?.message?.includes('Network')) {
    return 'Erreur de connexion. Vérifiez votre connexion internet.';
  }

  // Gestion des codes d'état HTTP
  const status = error?.response?.status;
  if (status) {
    switch (status) {
      case 400:
        return 'Données invalides. Veuillez vérifier vos informations.';
      case 401:
        return 'Non autorisé. Veuillez vous reconnecter.';
      case 403:
        return 'Accès interdit.';
      case 404:
        return 'Ressource non trouvée.';
      case 422:
        return 'Données de validation incorrectes.';
      case 500:
        return 'Erreur serveur. Veuillez réessayer plus tard.';
      default:
        return `Erreur ${status}. Veuillez réessayer.`;
    }
  }

  // Si c'est un objet Error standard (après avoir vérifié les erreurs réseau)
  if (error?.message) {
    return error.message;
  }

  // Fallback par défaut
  return 'Une erreur inattendue s\'est produite. Veuillez réessayer.';
};

/**
 * Affiche une alerte simple avec le message d'erreur
 * @param {Error|Object|string} error - L'erreur à afficher
 * @param {string} title - Titre de l'alerte (optionnel)
 */
export const showErrorAlert = (error, title = 'Erreur') => {
  const message = getErrorMessage(error);
  
  // Pour le MVP, on utilise alert() simple
  // Plus tard on pourra remplacer par un composant modal plus joli
  alert(`${title}\n\n${message}`);
};

/**
 * Console log l'erreur pour le debug
 * @param {Error|Object|string} error - L'erreur à logger
 * @param {string} context - Contexte où l'erreur s'est produite
 */
export const logError = (error, context = 'Unknown') => {
  console.error(`[${context}] Error:`, error);
  
  // En production, on pourrait envoyer à un service de monitoring
  // comme Sentry, LogRocket, etc.
};

/**
 * Gestionnaire d'erreur complet : log + affiche l'alerte
 * @param {Error|Object|string} error - L'erreur à traiter
 * @param {string} context - Contexte (ex: 'Création logement')
 * @param {string} title - Titre de l'alerte
 */
export const handleError = (error, context, title) => {
  logError(error, context);
  showErrorAlert(error, title || context);
};