import api from './api';

const SERVICE_BASE_URL = '/services';

// Service pour gérer les services (attestation, etc.)
export const getAllServices = async (activeOnly = true) => {
  try {
    const response = await api.get(`${SERVICE_BASE_URL}?active_only=${activeOnly}`);
    return response.data;
  } catch (error) {
    console.error('Erreur lors de la récupération des services:', error);
    throw new Error(error.response?.data?.detail || 'Erreur lors de la récupération des services');
  }
};

export const getServiceById = async (serviceId) => {
  try {
    const response = await api.get(`${SERVICE_BASE_URL}/${serviceId}`);
    return response.data;
  } catch (error) {
    console.error('Erreur lors de la récupération du service:', error);
    throw new Error(error.response?.data?.detail || 'Erreur lors de la récupération du service');
  }
};

export const getServiceBySlug = async (slug) => {
  try {
    const response = await api.get(`${SERVICE_BASE_URL}/slug/${slug}`);
    return response.data;
  } catch (error) {
    console.error('Erreur lors de la récupération du service par slug:', error);
    throw new Error(error.response?.data?.detail || 'Erreur lors de la récupération du service');
  }
};

export const calculateServicesTotal = async (serviceIds) => {
  try {
    const response = await api.post(`${SERVICE_BASE_URL}/calculate-total`, serviceIds);
    return response.data;
  } catch (error) {
    console.error('Erreur lors du calcul du total:', error);
    throw new Error(error.response?.data?.detail || 'Erreur lors du calcul du total');
  }
};

export const getOrganisationDetails = async () => {
  try {
    const response = await api.get(`${SERVICE_BASE_URL}/organisation/details`);
    return response.data;
  } catch (error) {
    console.error('Erreur lors de la récupération des détails organisation:', error);
    throw new Error(error.response?.data?.detail || 'Erreur lors de la récupération des détails');
  }
};