import api from './api';

class AuthService {
  constructor() {
    this.API_URL = '/auth';
    this.STORAGE_KEY = 'boaz_user';
  }

  /**
   * Connexion utilisateur
   */
  async login(email, password) {
    try {
      const response = await api.post(`${this.API_URL}/login`, {
        email,
        password
      });

      const user = response.data;
      
      // Stocker l'utilisateur en localStorage
      localStorage.setItem(this.STORAGE_KEY, JSON.stringify(user));
      
      return {
        success: true,
        user: user
      };
    } catch (error) {
      console.error('Erreur de connexion:', error);
      
      // Gestion des erreurs
      let errorMessage = 'Erreur de connexion';
      
      if (error.response) {
        if (error.response.status === 401) {
          errorMessage = 'Email ou mot de passe incorrect';
        } else if (error.response.data?.detail) {
          errorMessage = error.response.data.detail;
        }
      } else if (error.request) {
        errorMessage = 'Impossible de contacter le serveur';
      }
      
      return {
        success: false,
        error: errorMessage
      };
    }
  }

  /**
   * Déconnexion
   */
  logout() {
    localStorage.removeItem(this.STORAGE_KEY);
  }

  /**
   * Récupérer l'utilisateur actuel
   */
  getCurrentUser() {
    try {
      const userStr = localStorage.getItem(this.STORAGE_KEY);
      return userStr ? JSON.parse(userStr) : null;
    } catch (error) {
      console.error('Erreur de récupération utilisateur:', error);
      return null;
    }
  }

  /**
   * Vérifier si l'utilisateur est connecté
   */
  isAuthenticated() {
    return this.getCurrentUser() !== null;
  }

  /**
   * Vérifier le rôle de l'utilisateur
   */
  hasRole(role) {
    const user = this.getCurrentUser();
    return user && user.role === role;
  }

  /**
   * Obtenir l'URL de redirection selon le rôle
   */
  getRedirectUrl(user) {
    if (!user || !user.role) {
      return '/';
    }

    switch (user.role) {
      case 'agent-boaz':
        return '/agent-dashboard';
      case 'bailleur':
        return '/bailleur-dashboard';
      case 'admin-generale':
        return '/admin-dashboard';
      case 'client':
        return '/client-dashboard';
      default:
        return '/';
    }
  }

  /**
   * Récupérer le nom d'affichage du rôle
   */
  getRoleDisplayName(role) {
    const roleNames = {
      'agent-boaz': 'Agent Boaz',
      'bailleur': 'Bailleur',
      'admin-generale': 'Administrateur Général',
      'client': 'Client'
    };
    
    return roleNames[role] || role;
  }

  /**
   * Vérifier la validité du token (simulation pour MVP)
   */
  isTokenValid() {
    // Pour le MVP, on considère que si l'utilisateur est en localStorage, c'est valide
    // Dans une vraie app, on vérifierait l'expiration d'un JWT
    return this.isAuthenticated();
  }

  /**
   * Rafraîchir les données utilisateur depuis le serveur
   */
  async refreshUser() {
    const currentUser = this.getCurrentUser();
    if (!currentUser) {
      return null;
    }

    try {
      // Récupérer les données à jour depuis le serveur
      const response = await api.get(`/users/by-email/${currentUser.email}`);
      const updatedUser = response.data;
      
      // Mettre à jour le localStorage
      localStorage.setItem(this.STORAGE_KEY, JSON.stringify(updatedUser));
      
      return updatedUser;
    } catch (error) {
      console.error('Erreur de rafraîchissement utilisateur:', error);
      // En cas d'erreur, déconnecter l'utilisateur
      this.logout();
      return null;
    }
  }
}

// Export d'une instance unique (singleton)
const authService = new AuthService();
export default authService;