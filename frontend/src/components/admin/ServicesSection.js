import React, { useState } from 'react';
import WizardSouscription from './WizardSouscription';

const ServicesSection = ({ onDataChange }) => {
  const [showWizard, setShowWizard] = useState(false);

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

  return (
    <>
      <div className="bg-white rounded-lg shadow mb-8">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-medium text-gray-900">Services Disponibles</h2>
          <p className="text-sm text-gray-600">Choisissez un service à souscrire</p>
        </div>
        
        <div className="p-6">
          {/* Card Service Unique */}
          <div className="max-w-sm bg-white border border-gray-200 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300">
            <div className="p-6">
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                  <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                  </svg>
                </div>
                <div className="ml-4">
                  <h3 className="text-lg font-semibold text-gray-900">
                    Attestation de Logement et de Prise en Charge
                  </h3>
                </div>
              </div>
              
              <p className="text-gray-600 text-sm mb-4">
                Service complet d'attestation de logement avec prise en charge administrative pour étudiants étrangers.
              </p>
              
              <div className="mb-4">
                <div className="text-2xl font-bold text-gray-900 mb-1">
                  À partir de 50€
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