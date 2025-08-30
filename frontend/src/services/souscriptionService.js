import api from './api';

export const getSouscriptions = async (params = {}) => {
  try {
    const response = await api.get('/souscriptions/', { params });
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getSouscription = async (id) => {
  try {
    const response = await api.get(`/souscriptions/${id}`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const createSouscription = async (souscriptionData) => {
  try {
    const response = await api.post('/souscriptions/', souscriptionData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const updateSouscription = async (id, souscriptionData) => {
  try {
    const response = await api.put(`/souscriptions/${id}`, souscriptionData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const changerStatutSouscription = async (id, statut) => {
  try {
    const response = await api.patch(`/souscriptions/${id}/statut`, { statut });
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const deleteSouscription = async (id) => {
  try {
    const response = await api.delete(`/souscriptions/${id}`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

// Énums pour les statuts
export const STATUT_SOUSCRIPTION = {
  ATTENTE_PAIEMENT: 'attente_paiement',
  PAYE: 'paye',
  LIVRE: 'livre',
  CLOTURE: 'cloture'
};