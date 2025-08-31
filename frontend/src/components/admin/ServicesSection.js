import React, { useState, useEffect } from 'react';
import WizardSouscription from './WizardSouscription';
import { getAllServices } from '../../services/serviceService';

const ServicesSection = ({ onDataChange }) => {
  const [showWizard, setShowWizard] = useState(false);
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadServices();
  }, []);

  const loadServices = async () => {
    try {
      setLoading(true);
      setError('');
      const data = await getAllServices(true);
      setServices(data);
    } catch (err) {
      setError('Impossible de charger les services');
      console.error('Erreur chargement services:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSouscrire = () => {
    setShowWizard(true);
  };

  const handleWizardComplete = () => {
    setShowWizard(false);
    onDataChange();
  };

  const handleWizardCancel = () => {
    setShowWizard(false);
  };

  const formatPrice = (price) => {
    return new Intl.NumberFormat('fr-FR').format(price);
  };

  return (
    <>
      <div className="bg-white rounded-lg shadow mb-8">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-medium text-gray-900">Services Disponibles</h2>
          <p className="text-sm text-gray-600">Choisissez un service à souscrire</p>
        </div>
        
        <div className="p-6">
          {loading && (
            <div className="flex items-center justify-center py-12">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              <span className="ml-2 text-gray-600">Chargement des services...</span>
            </div>
          )}

          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
              <div className="flex items-center">
                <svg className="w-5 h-5 text-red-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
                <span className="text-red-800 text-sm">{error}</span>
                <button
                  onClick={loadServices}
                  className="ml-4 px-3 py-1 bg-red-100 hover:bg-red-200 text-red-800 text-xs rounded-md"
                >
                  Réessayer
                </button>
              </div>
            </div>
          )}

          {!loading && !error && services.length === 0 && (
            <div className="text-center py-12">
              <p className="text-gray-500">Aucun service disponible pour le moment</p>
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {services.map((service) => (
              <div 
                key={service.id} 
                className="bg-white border border-gray-200 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300"
              >
                <div className="p-6">
                  <div className="flex items-start mb-4">
                    <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center flex-shrink-0">
                      <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                      </svg>
                    </div>
                    <div className="ml-4 flex-1">
                      <h3 className="text-lg font-semibold text-gray-900 leading-tight">
                        {service.nom}
                      </h3>
                    </div>
                  </div>
                  
                  <p className="text-gray-600 text-sm mb-4 line-clamp-3">
                    {service.description}
                  </p>
                  
                  <div className="mb-4">
                    <div className="text-2xl font-bold text-gray-900 mb-1">
                      {formatPrice(service.tarif)} FCFA
                    </div>
                    <div className="text-sm text-gray-500">
                      + frais logement selon sélection
                    </div>
                  </div>
                  
                  <button
                    onClick={handleSouscrire}
                    className="w-full bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors duration-200 font-medium"
                  >
                    Souscrire
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Wizard Modal */}
      {showWizard && (
        <WizardSouscription
          onComplete={handleWizardComplete}
          onCancel={handleWizardCancel}
        />
      )}
    </>
  );
};

export default ServicesSection;