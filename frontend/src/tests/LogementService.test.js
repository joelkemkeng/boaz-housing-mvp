import { LogementService } from '../services/logementService';

// Mock simple de l'API
const mockApi = {
  post: jest.fn(),
  get: jest.fn(),
  put: jest.fn(),
  delete: jest.fn(),
  patch: jest.fn()
};

describe('LogementService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('createLogement', () => {
    test('should create a logement successfully', async () => {
      const mockLogement = {
        id: 1,
        adresse: '123 Rue Test',
        ville: 'Paris',
        code_postal: '75001',
        loyer: 500,
        statut: 'disponible'
      };

      mockedApi.post.mockResolvedValue({ data: mockLogement });

      const result = await logementService.createLogement({
        adresse: '123 Rue Test',
        ville: 'Paris',
        code_postal: '75001',
        loyer: 500,
        statut: 'disponible'
      });

      expect(mockedApi.post).toHaveBeenCalledWith('/logements/', {
        adresse: '123 Rue Test',
        ville: 'Paris',
        code_postal: '75001',
        loyer: 500,
        statut: 'disponible'
      });
      expect(result).toEqual(mockLogement);
    });
  });

  describe('getLogements', () => {
    test('should fetch logements with parameters', async () => {
      const mockLogements = [
        { id: 1, adresse: '123 Rue A', ville: 'Paris', loyer: 500 },
        { id: 2, adresse: '456 Rue B', ville: 'Lyon', loyer: 400 }
      ];

      mockedApi.get.mockResolvedValue({ data: mockLogements });

      const result = await logementService.getLogements({ statut: 'disponible', ville: 'Paris' });

      expect(mockedApi.get).toHaveBeenCalledWith('/logements/', { 
        params: { statut: 'disponible', ville: 'Paris' } 
      });
      expect(result).toEqual(mockLogements);
    });

    test('should fetch logements without parameters', async () => {
      const mockLogements = [];
      mockedApi.get.mockResolvedValue({ data: mockLogements });

      const result = await logementService.getLogements();

      expect(mockedApi.get).toHaveBeenCalledWith('/logements/', { params: {} });
      expect(result).toEqual(mockLogements);
    });
  });

  describe('getLogement', () => {
    test('should fetch a single logement by id', async () => {
      const mockLogement = { id: 1, adresse: '123 Rue Test', ville: 'Paris' };
      mockedApi.get.mockResolvedValue({ data: mockLogement });

      const result = await logementService.getLogement(1);

      expect(mockedApi.get).toHaveBeenCalledWith('/logements/1');
      expect(result).toEqual(mockLogement);
    });
  });

  describe('updateLogement', () => {
    test('should update a logement successfully', async () => {
      const mockUpdatedLogement = { id: 1, adresse: '123 Rue Updated', loyer: 600 };
      mockedApi.put.mockResolvedValue({ data: mockUpdatedLogement });

      const result = await logementService.updateLogement(1, { loyer: 600 });

      expect(mockedApi.put).toHaveBeenCalledWith('/logements/1', { loyer: 600 });
      expect(result).toEqual(mockUpdatedLogement);
    });
  });

  describe('deleteLogement', () => {
    test('should delete a logement successfully', async () => {
      const mockResponse = { message: 'Logement supprimé avec succès' };
      mockedApi.delete.mockResolvedValue({ data: mockResponse });

      const result = await logementService.deleteLogement(1);

      expect(mockedApi.delete).toHaveBeenCalledWith('/logements/1');
      expect(result).toEqual(mockResponse);
    });
  });

  describe('changeStatutLogement', () => {
    test('should change logement status successfully', async () => {
      const mockResponse = { 
        message: 'Statut mis à jour avec succès',
        logement: { id: 1, statut: 'occupe' }
      };
      mockedApi.patch.mockResolvedValue({ data: mockResponse });

      const result = await logementService.changeStatutLogement(1, 'occupe');

      expect(mockedApi.patch).toHaveBeenCalledWith('/logements/1/statut?nouveau_statut=occupe');
      expect(result).toEqual(mockResponse);
    });
  });

  describe('getStatsLogements', () => {
    test('should fetch logements statistics', async () => {
      const mockStats = { total: 10, disponibles: 6, occupes: 2, maintenance: 2 };
      mockedApi.get.mockResolvedValue({ data: mockStats });

      const result = await logementService.getStatsLogements();

      expect(mockedApi.get).toHaveBeenCalledWith('/logements/stats');
      expect(result).toEqual(mockStats);
    });
  });

  describe('getLogementsDisponibles', () => {
    test('should fetch available logements only', async () => {
      const mockLogements = [
        { id: 1, statut: 'disponible' },
        { id: 3, statut: 'disponible' }
      ];
      mockedApi.get.mockResolvedValue({ data: mockLogements });

      const result = await logementService.getLogementsDisponibles();

      expect(mockedApi.get).toHaveBeenCalledWith('/logements/disponibles');
      expect(result).toEqual(mockLogements);
    });
  });
});