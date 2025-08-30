import React, { useState, useEffect } from 'react';
import { createSouscription, updateSouscription } from '../../services/souscriptionService';
import { getLogementsDisponibles } from '../../services/logementService';

const WizardSouscription = ({ souscriptionToEdit, onComplete, onCancel }) => {
  const [currentStep, setCurrentStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [logements, setLogements] = useState([]);
  
  const [formData, setFormData] = useState(() => {
    if (souscriptionToEdit) {
      // Mode édition : pré-remplir avec les données existantes
      return {
        nom_client: souscriptionToEdit.nom_client || '',
        prenom_client: souscriptionToEdit.prenom_client || '',
        email_client: souscriptionToEdit.email_client || '',
        date_naissance_client: souscriptionToEdit.date_naissance_client || '',
        ville_naissance_client: souscriptionToEdit.ville_naissance_client || '',
        pays_naissance_client: souscriptionToEdit.pays_naissance_client || '',
        nationalite_client: souscriptionToEdit.nationalite_client || '',
        pays_destination: souscriptionToEdit.pays_destination || '',
        date_arrivee_prevue: souscriptionToEdit.date_arrivee_prevue || '',
        
        // Informations académiques
        ecole_universite: souscriptionToEdit.ecole_universite || '',
        filiere: souscriptionToEdit.filiere || '',
        pays_ecole: souscriptionToEdit.pays_ecole || '',
        ville_ecole: souscriptionToEdit.ville_ecole || '',
        code_postal_ecole: souscriptionToEdit.code_postal_ecole || '',
        adresse_ecole: souscriptionToEdit.adresse_ecole || '',
        
        // Informations logement
        logement_id: souscriptionToEdit.logement_id || '',
        date_entree_prevue: souscriptionToEdit.date_entree_prevue || '',
        duree_location_mois: souscriptionToEdit.duree_location_mois || 12
      };
    } else {
      // Mode création : formulaire vide
      return {
        nom_client: '',
        prenom_client: '',
        email_client: '',
        date_naissance_client: '',
        ville_naissance_client: '',
        pays_naissance_client: '',
        nationalite_client: '',
        pays_destination: '',
        date_arrivee_prevue: '',
        
        // Informations académiques
        ecole_universite: '',
        filiere: '',
        pays_ecole: '',
        ville_ecole: '',
        code_postal_ecole: '',
        adresse_ecole: '',
        
        // Informations logement
        logement_id: '',
        date_entree_prevue: '',
        duree_location_mois: 12
      };
    }
  });

  useEffect(() => {
    // Charger les logements dès l'ouverture du wizard pour permettre la présélection
    loadLogements();
  }, []);

  useEffect(() => {
    if (currentStep === 3 && logements.length === 0) {
      loadLogements();
    }
  }, [currentStep]);

  const loadLogements = async () => {
    try {
      setLoading(true);
      const data = await getLogementsDisponibles();
      setLogements(data);
    } catch (error) {
      console.error('Erreur chargement logements:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleNextStep = () => {
    if (validateCurrentStep()) {
      setCurrentStep(prev => prev + 1);
    }
  };

  const handlePrevStep = () => {
    setCurrentStep(prev => prev - 1);
  };

  const validateCurrentStep = () => {
    if (currentStep === 1) {
      return formData.nom_client && formData.prenom_client && formData.email_client;
    }
    if (currentStep === 2) {
      return formData.ecole_universite && formData.filiere;
    }
    if (currentStep === 3) {
      return formData.logement_id;
    }
    return true;
  };

  const handleSubmit = async () => {
    try {
      setLoading(true);
      
      // Nettoyer les données : retirer les champs vides
      const cleanData = {};
      Object.keys(formData).forEach(key => {
        const value = formData[key];
        // Garder les champs obligatoires même vides et les valeurs non-vides
        if (value !== '' && value !== null && value !== undefined) {
          cleanData[key] = value;
        }
        // Toujours inclure les champs obligatoires
        if (['nom_client', 'prenom_client', 'email_client', 'ecole_universite', 'filiere', 'logement_id', 'duree_location_mois'].includes(key)) {
          cleanData[key] = value || (key === 'duree_location_mois' ? 12 : '');
        }
      });
      
      if (souscriptionToEdit) {
        // Mode édition : mettre à jour la souscription existante
        await updateSouscription(souscriptionToEdit.id, cleanData);
      } else {
        // Mode création : créer nouvelle souscription
        await createSouscription(cleanData);
      }
      
      onComplete();
    } catch (error) {
      const action = souscriptionToEdit ? 'modification' : 'création';
      alert(`Erreur lors de la ${action}: ` + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  const renderStepIndicator = () => (
    <div className="flex justify-center mb-8">
      {[1, 2, 3, 4].map((step) => (
        <div key={step} className="flex items-center">
          <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${
            step <= currentStep ? 'bg-blue-600 text-white' : 'bg-gray-300 text-gray-600'
          }`}>
            {step}
          </div>
          {step < 4 && (
            <div className={`w-12 h-0.5 ${
              step < currentStep ? 'bg-blue-600' : 'bg-gray-300'
            }`}></div>
          )}
        </div>
      ))}
    </div>
  );

  const renderStep1 = () => (
    <div className="space-y-4">
      <h3 className="text-lg font-medium text-gray-900 mb-4">Informations Client</h3>
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Nom *</label>
          <input
            type="text"
            name="nom_client"
            value={formData.nom_client}
            onChange={handleInputChange}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Prénom *</label>
          <input
            type="text"
            name="prenom_client"
            value={formData.prenom_client}
            onChange={handleInputChange}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Email *</label>
          <input
            type="email"
            name="email_client"
            value={formData.email_client}
            onChange={handleInputChange}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Date de naissance</label>
          <input
            type="date"
            name="date_naissance_client"
            value={formData.date_naissance_client}
            onChange={handleInputChange}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Nationalité</label>
          <input
            type="text"
            name="nationalite_client"
            value={formData.nationalite_client}
            onChange={handleInputChange}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Pays destination</label>
          <input
            type="text"
            name="pays_destination"
            value={formData.pays_destination}
            onChange={handleInputChange}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
      </div>
    </div>
  );

  const renderStep2 = () => (
    <div className="space-y-4">
      <h3 className="text-lg font-medium text-gray-900 mb-4">Informations Académiques</h3>
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">École/Université *</label>
          <input
            type="text"
            name="ecole_universite"
            value={formData.ecole_universite}
            onChange={handleInputChange}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Filière *</label>
          <input
            type="text"
            name="filiere"
            value={formData.filiere}
            onChange={handleInputChange}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Pays école</label>
          <input
            type="text"
            name="pays_ecole"
            value={formData.pays_ecole}
            onChange={handleInputChange}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Ville école</label>
          <input
            type="text"
            name="ville_ecole"
            value={formData.ville_ecole}
            onChange={handleInputChange}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Code postal</label>
          <input
            type="text"
            name="code_postal_ecole"
            value={formData.code_postal_ecole}
            onChange={handleInputChange}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Date entrée prévue</label>
          <input
            type="date"
            name="date_entree_prevue"
            value={formData.date_entree_prevue}
            onChange={handleInputChange}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700">Adresse école</label>
        <textarea
          name="adresse_ecole"
          value={formData.adresse_ecole}
          onChange={handleInputChange}
          rows="3"
          className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
        />
      </div>
    </div>
  );

  const renderStep3 = () => (
    <div className="space-y-4">
      <h3 className="text-lg font-medium text-gray-900 mb-4">Choix du Logement</h3>
      {loading ? (
        <div className="text-center">Chargement des logements...</div>
      ) : (
        <div className="grid grid-cols-1 gap-4 max-h-96 overflow-y-auto">
          {logements.map((logement) => (
            <div
              key={logement.id}
              className={`border rounded-lg p-4 cursor-pointer transition-colors ${
                formData.logement_id === logement.id
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-300 hover:border-gray-400'
              }`}
              onClick={() => setFormData(prev => ({ ...prev, logement_id: logement.id }))}
            >
              <div className="flex items-start space-x-4">
                <input
                  type="radio"
                  name="logement_id"
                  value={logement.id}
                  checked={formData.logement_id === logement.id}
                  onChange={() => {}}
                  className="mt-1"
                />
                <div className="flex-1">
                  <h4 className="font-medium text-gray-900">{logement.titre}</h4>
                  <p className="text-sm text-gray-600">{logement.adresse}</p>
                  <p className="text-sm text-gray-600">{logement.ville}, {logement.pays}</p>
                  <div className="mt-2 flex items-center space-x-4">
                    <span className="text-sm font-medium text-green-600">
                      {logement.montant_total}€/mois
                    </span>
                    <span className="text-xs text-gray-500">
                      (Loyer: {logement.loyer}€ + Charges: {logement.montant_charges}€)
                    </span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );

  const renderStep4 = () => (
    <div className="space-y-4">
      <h3 className="text-lg font-medium text-gray-900 mb-4">Récapitulatif</h3>
      <div className="bg-gray-50 p-4 rounded-lg space-y-2">
        <p><strong>Client:</strong> {formData.prenom_client} {formData.nom_client}</p>
        <p><strong>Email:</strong> {formData.email_client}</p>
        <p><strong>École:</strong> {formData.ecole_universite}</p>
        <p><strong>Filière:</strong> {formData.filiere}</p>
        {logements.find(l => l.id === formData.logement_id) && (
          <p><strong>Logement:</strong> {logements.find(l => l.id === formData.logement_id).titre}</p>
        )}
      </div>
    </div>
  );

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-xl font-semibold text-gray-900">
            {souscriptionToEdit ? `Modifier Souscription - ${souscriptionToEdit.reference}` : 'Nouvelle Souscription'}
          </h2>
        </div>
        
        <div className="p-6">
          {renderStepIndicator()}
          
          <div className="mb-8">
            {currentStep === 1 && renderStep1()}
            {currentStep === 2 && renderStep2()}
            {currentStep === 3 && renderStep3()}
            {currentStep === 4 && renderStep4()}
          </div>
          
          <div className="flex justify-between">
            <button
              onClick={onCancel}
              className="px-4 py-2 text-gray-600 hover:text-gray-800"
            >
              Annuler
            </button>
            
            <div className="space-x-2">
              {currentStep > 1 && (
                <button
                  onClick={handlePrevStep}
                  className="px-4 py-2 bg-gray-100 text-gray-800 rounded-lg hover:bg-gray-200"
                >
                  Précédent
                </button>
              )}
              
              {currentStep < 4 ? (
                <button
                  onClick={handleNextStep}
                  disabled={!validateCurrentStep()}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed"
                >
                  Suivant
                </button>
              ) : (
                <button
                  onClick={handleSubmit}
                  disabled={loading}
                  className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed"
                >
                  {loading 
                    ? (souscriptionToEdit ? 'Modification...' : 'Création...')
                    : (souscriptionToEdit ? 'Modifier la souscription' : 'Créer la souscription')
                  }
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WizardSouscription;