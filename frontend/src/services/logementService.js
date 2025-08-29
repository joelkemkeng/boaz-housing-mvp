import api from './api';

export class LogementService {
  async createLogement(logementData) {
    const response = await api.post('/logements/', logementData);
    return response.data;
  }

  async getLogements(params = {}) {
    const response = await api.get('/logements/', { params });
    return response.data;
  }

  async getLogement(id) {
    const response = await api.get(`/logements/${id}`);
    return response.data;
  }

  async updateLogement(id, logementData) {
    const response = await api.put(`/logements/${id}`, logementData);
    return response.data;
  }

  async deleteLogement(id) {
    const response = await api.delete(`/logements/${id}`);
    return response.data;
  }

  async changeStatutLogement(id, nouveauStatut) {
    const response = await api.patch(`/logements/${id}/statut?nouveau_statut=${nouveauStatut}`);
    return response.data;
  }

  async getLogementsDisponibles() {
    const response = await api.get('/logements/disponibles');
    return response.data;
  }

  async getStatsLogements() {
    const response = await api.get('/logements/stats');
    return response.data;
  }
}

export const logementService = new LogementService();