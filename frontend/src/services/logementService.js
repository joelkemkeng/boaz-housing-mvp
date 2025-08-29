import api from './api';
import { logError } from '../utils/errorHandler';

export class LogementService {
  async createLogement(logementData) {
    try {
      const response = await api.post('/logements/', logementData);
      return response.data;
    } catch (error) {
      logError(error, 'LogementService.createLogement');
      throw error; // Re-lancer l'erreur pour que le composant puisse la gérer
    }
  }

  async getLogements(params = {}) {
    try {
      const response = await api.get('/logements/', { params });
      return response.data;
    } catch (error) {
      logError(error, 'LogementService.getLogements');
      throw error;
    }
  }

  async getLogement(id) {
    try {
      const response = await api.get(`/logements/${id}`);
      return response.data;
    } catch (error) {
      logError(error, 'LogementService.getLogement');
      throw error;
    }
  }

  async updateLogement(id, logementData) {
    try {
      const response = await api.put(`/logements/${id}`, logementData);
      return response.data;
    } catch (error) {
      logError(error, 'LogementService.updateLogement');
      throw error;
    }
  }

  async deleteLogement(id) {
    try {
      const response = await api.delete(`/logements/${id}`);
      return response.data;
    } catch (error) {
      logError(error, 'LogementService.deleteLogement');
      throw error;
    }
  }

  async changeStatutLogement(id, nouveauStatut) {
    try {
      const response = await api.patch(`/logements/${id}/statut?nouveau_statut=${nouveauStatut}`);
      return response.data;
    } catch (error) {
      logError(error, 'LogementService.changeStatutLogement');
      throw error;
    }
  }

  async getLogementsDisponibles() {
    try {
      const response = await api.get('/logements/disponibles');
      return response.data;
    } catch (error) {
      logError(error, 'LogementService.getLogementsDisponibles');
      throw error;
    }
  }

  async getStatsLogements() {
    try {
      const response = await api.get('/logements/stats');
      return response.data;
    } catch (error) {
      logError(error, 'LogementService.getStatsLogements');
      throw error;
    }
  }
}

export const logementService = new LogementService();