import { getErrorMessage } from './errorHandler';

describe('errorHandler', () => {
  describe('getErrorMessage', () => {
    test('should handle string errors', () => {
      const result = getErrorMessage('Simple error');
      expect(result).toBe('Simple error');
    });

    test('should handle FastAPI validation errors', () => {
      const mockError = {
        response: {
          data: {
            detail: [
              {
                loc: ['body', 'adresse'],
                msg: 'L\'adresse doit contenir au moins 5 caractères',
                type: 'value_error'
              },
              {
                loc: ['body', 'loyer'],
                msg: 'Le loyer doit être supérieur à 0',
                type: 'value_error'
              }
            ]
          }
        }
      };

      const result = getErrorMessage(mockError);
      expect(result).toContain('body > adresse: L\'adresse doit contenir au moins 5 caractères');
      expect(result).toContain('body > loyer: Le loyer doit être supérieur à 0');
    });

    test('should handle simple FastAPI detail string', () => {
      const mockError = {
        response: {
          data: {
            detail: 'Logement non trouvé'
          }
        }
      };

      const result = getErrorMessage(mockError);
      expect(result).toBe('Logement non trouvé');
    });

    test('should handle HTTP status codes', () => {
      const mockError = {
        response: {
          status: 404
        }
      };

      const result = getErrorMessage(mockError);
      expect(result).toBe('Ressource non trouvée.');
    });

    test('should handle network errors', () => {
      const mockError = {
        code: 'NETWORK_ERROR',
        message: 'Network Error'
      };

      const result = getErrorMessage(mockError);
      expect(result).toBe('Erreur de connexion. Vérifiez votre connexion internet.');
    });

    test('should handle unknown errors', () => {
      const mockError = { unknown: 'property' };

      const result = getErrorMessage(mockError);
      expect(result).toBe('Une erreur inattendue s\'est produite. Veuillez réessayer.');
    });
  });
});