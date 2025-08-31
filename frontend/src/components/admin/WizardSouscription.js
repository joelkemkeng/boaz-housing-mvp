import React, { useState, useEffect } from 'react';
import { createSouscription, updateSouscription } from '../../services/souscriptionService';
import { getLogementsDisponibles } from '../../services/logementService';
import { generateProforma, downloadPdf, previewPdf } from '../../services/proformaService';
import { getAllServices } from '../../services/serviceService';
import SpinLoader from '../common/SpinLoader';

const WizardSouscription = ({ souscriptionToEdit, onComplete, onCancel }) => {
  const [currentStep, setCurrentStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [logements, setLogements] = useState([]);
  const [errors, setErrors] = useState({});
  const [generalError, setGeneralError] = useState('');
  const [services, setServices] = useState([]);
  const [selectedServices, setSelectedServices] = useState([]);
  const [proformaLoading, setProformaLoading] = useState(false);
  const [proformaData, setProformaData] = useState(null);
  
  const [formData, setFormData] = useState(() => {
    if (souscriptionToEdit) {
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
        ecole_universite: souscriptionToEdit.ecole_universite || '',
        filiere: souscriptionToEdit.filiere || '',
        pays_ecole: souscriptionToEdit.pays_ecole || '',
        ville_ecole: souscriptionToEdit.ville_ecole || '',
        code_postal_ecole: souscriptionToEdit.code_postal_ecole || '',
        adresse_ecole: souscriptionToEdit.adresse_ecole || '',
        logement_id: souscriptionToEdit.logement_id || '',
        date_entree_prevue: souscriptionToEdit.date_entree_prevue || '',
        duree_location_mois: souscriptionToEdit.duree_location_mois || 12
      };
    } else {
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
        ecole_universite: '',
        filiere: '',
        pays_ecole: '',
        ville_ecole: '',
        code_postal_ecole: '',
        adresse_ecole: '',
        logement_id: '',
        date_entree_prevue: '',
        duree_location_mois: 12
      };
    }
  });

  // Auto-chargement des logements à l'étape 3 et des services/logements à l'étape 4
  useEffect(() => {
    if (currentStep === 3) {
      // Charger les logements automatiquement à l'étape 3
      if (logements.length === 0) {
        loadLogements();
      }
    } else if (currentStep === 4) {
      // Charger les données si nécessaire à l'étape 4
      if (services.length === 0) {
        loadServices();
      }
      if (logements.length === 0) {
        loadLogements();
      }
    }
  }, [currentStep]);

  // Déclencher la génération automatique quand les données sont prêtes à l'étape 4
  useEffect(() => {
    if (currentStep === 4 && services.length > 0 && logements.length > 0) {
      const selectedLogement = logements.find(l => l.id === parseInt(formData.logement_id));
      
      if (!proformaData && !proformaLoading && selectedServices.length > 0 && selectedLogement) {
        // Petite temporisation pour éviter les appels trop rapides
        const timer = setTimeout(() => {
          handleGenerateProforma();
        }, 300);
        
        return () => clearTimeout(timer);
      }
    }
  }, [currentStep, services.length, logements.length, proformaData, proformaLoading, selectedServices.length, formData.logement_id]);

  const loadLogements = async () => {
    if (loading) return;
    try {
      setLoading(true);
      setGeneralError('');
      const data = await getLogementsDisponibles();
      setLogements(data);
    } catch (error) {
      console.error('Erreur chargement logements:', error);
      setGeneralError('Impossible de charger les logements disponibles.');
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
    
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
    
    if (generalError) {
      setGeneralError('');
    }
  };

  const validateCurrentStep = () => {
    const newErrors = {};
    let isValid = true;

    if (currentStep === 1) {
      if (!formData.nom_client?.trim()) {
        newErrors.nom_client = 'Le nom est requis';
        isValid = false;
      }
      if (!formData.prenom_client?.trim()) {
        newErrors.prenom_client = 'Le prénom est requis';
        isValid = false;
      }
      if (!formData.email_client?.trim()) {
        newErrors.email_client = 'L\'email est requis';
        isValid = false;
      }
    }

    if (currentStep === 2) {
      if (!formData.ecole_universite?.trim()) {
        newErrors.ecole_universite = 'L\'école/université est requise';
        isValid = false;
      }
      if (!formData.filiere?.trim()) {
        newErrors.filiere = 'La filière est requise';
        isValid = false;
      }
    }

    if (currentStep === 3) {
      if (!formData.logement_id) {
        setGeneralError('Veuillez sélectionner un logement');
        isValid = false;
      }
    }

    setErrors(newErrors);
    return isValid;
  };

  const handleNextStep = () => {
    if (currentStep === 3 && logements.length === 0) {
      loadLogements();
    }
    if (validateCurrentStep()) {
      setCurrentStep(prev => prev + 1);
    }
  };

  const handlePrevStep = () => {
    setCurrentStep(prev => prev - 1);
  };

  const handleSubmit = async () => {
    try {
      setLoading(true);
      setGeneralError('');
      
      const cleanData = {};
      Object.keys(formData).forEach(key => {
        const value = formData[key];
        if (value !== '' && value !== null && value !== undefined) {
          cleanData[key] = value;
        }
        if (['nom_client', 'prenom_client', 'email_client', 'ecole_universite', 'filiere', 'logement_id', 'duree_location_mois'].includes(key)) {
          cleanData[key] = value || (key === 'duree_location_mois' ? 12 : '');
        }
      });
      
      if (souscriptionToEdit) {
        await updateSouscription(souscriptionToEdit.id, cleanData);
      } else {
        await createSouscription(cleanData);
      }
      
      onComplete();
    } catch (error) {
      console.error('Erreur lors de la soumission:', error);
      setGeneralError('Une erreur s\'est produite. Veuillez réessayer.');
    } finally {
      setLoading(false);
    }
  };

  const renderErrorMessage = () => {
    if (!generalError) return null;
    
    return (
      <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <svg className="w-5 h-5 text-red-400 mr-3" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
            <p className="text-sm text-red-800">{generalError}</p>
          </div>
          {generalError.includes('logements') && (
            <button
              onClick={() => loadLogements()}
              disabled={loading}
              className="ml-4 px-3 py-1 bg-red-100 hover:bg-red-200 text-red-800 text-xs font-medium rounded-md transition-colors duration-200 disabled:opacity-50"
            >
              {loading ? 'Chargement...' : 'Réessayer'}
            </button>
          )}
        </div>
      </div>
    );
  };

  const renderInput = (name, label, type = 'text', placeholder = '', required = false) => (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-2">
        {label} {required && <span className="text-red-500">*</span>}
      </label>
      <input
        type={type}
        name={name}
        value={formData[name] || ''}
        onChange={handleInputChange}
        className={`block w-full px-4 py-3 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:border-transparent transition-all duration-200 ${
          errors[name] 
            ? 'border-red-300 focus:ring-red-400 bg-red-50' 
            : 'border-gray-300 focus:ring-blue-400'
        }`}
        placeholder={placeholder}
        required={required}
      />
      {errors[name] && (
        <p className="mt-1 text-sm text-red-600">{errors[name]}</p>
      )}
    </div>
  );

  const renderStepIndicator = () => (
    <div className="flex justify-center mb-10">
      <div className="flex items-center space-x-4">
        {[
          { num: 1, label: 'Client' },
          { num: 2, label: 'Académique' },
          { num: 3, label: 'Logement' },
          { num: 4, label: 'Récapitulatif' }
        ].map((step, index) => (
          <div key={step.num} className="flex items-center">
            <div className="flex flex-col items-center">
              <div className={`w-10 h-10 rounded-full flex items-center justify-center text-sm font-semibold transition-all duration-300 ${
                step.num <= currentStep 
                  ? 'bg-blue-400 text-white shadow-lg' 
                  : 'bg-gray-200 text-gray-500'
              }`}>
                {step.num <= currentStep ? (
                  step.num < currentStep ? '✓' : step.num
                ) : step.num}
              </div>
              <span className={`text-xs mt-2 font-medium transition-colors ${
                step.num <= currentStep ? 'text-blue-600' : 'text-gray-400'
              }`}>
                {step.label}
              </span>
            </div>
            {index < 3 && (
              <div className={`w-16 h-0.5 mx-4 transition-colors duration-300 ${
                step.num < currentStep ? 'bg-blue-400' : 'bg-gray-200'
              }`}></div>
            )}
          </div>
        ))}
      </div>
    </div>
  );

  const renderStep1 = () => (
    <div className="space-y-6">
      <h3 className="text-xl font-semibold text-gray-800 mb-6">Informations Client</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {renderInput('nom_client', 'Nom', 'text', 'Nom de famille', true)}
        {renderInput('prenom_client', 'Prénom', 'text', 'Prénom', true)}
        {renderInput('email_client', 'Email', 'email', 'email@exemple.com', true)}
        {renderInput('date_naissance_client', 'Date de naissance', 'date')}
        {renderInput('ville_naissance_client', 'Ville de naissance', 'text', 'Ville de naissance')}
        {renderInput('pays_naissance_client', 'Pays de naissance', 'text', 'Pays de naissance')}
        {renderInput('nationalite_client', 'Nationalité', 'text', 'Nationalité')}
        {renderInput('pays_destination', 'Pays de destination', 'text', 'Pays de destination')}
        {renderInput('date_arrivee_prevue', 'Date d\'arrivée prévue', 'date')}
      </div>
    </div>
  );

  const renderStep2 = () => (
    <div className="space-y-6">
      <h3 className="text-xl font-semibold text-gray-800 mb-6">Informations Académiques</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {renderInput('ecole_universite', 'École/Université', 'text', 'Nom de l\'école ou université', true)}
        {renderInput('filiere', 'Filière', 'text', 'Filière d\'études', true)}
        {renderInput('pays_ecole', 'Pays de l\'école', 'text', 'Pays')}
        {renderInput('ville_ecole', 'Ville de l\'école', 'text', 'Ville')}
        {renderInput('code_postal_ecole', 'Code postal de l\'école', 'text', 'Code postal')}
        {renderInput('date_entree_prevue', 'Date d\'entrée prévue', 'date')}
        {renderInput('duree_location_mois', 'Durée de location (mois)', 'number', '12')}
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">Adresse complète de l'école</label>
        <textarea
          name="adresse_ecole"
          value={formData.adresse_ecole}
          onChange={handleInputChange}
          rows="3"
          className="block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent"
          placeholder="Adresse complète de l'école ou université..."
        />
      </div>
    </div>
  );

  const renderStep3 = () => (
    <div className="space-y-6">
      <h3 className="text-xl font-semibold text-gray-800 mb-6">Choix du Logement</h3>
      
      {loading ? (
        <div className="text-center py-8">
          <SpinLoader size="lg" text="Chargement des logements disponibles..." />
        </div>
      ) : logements.length === 0 ? (
        <div className="text-center py-8">
          <div className="text-gray-500">
            <svg className="w-12 h-12 mx-auto mb-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
            </svg>
            <p className="text-lg font-medium mb-2">Aucun logement disponible</p>
            <p className="text-sm">Aucun logement n'a été trouvé pour le moment.</p>
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {logements.map(logement => (
            <div
              key={logement.id}
              className={`border-2 rounded-lg p-4 cursor-pointer transition-all duration-200 ${
                parseInt(formData.logement_id) === logement.id
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-200 hover:border-gray-300'
              }`}
              onClick={() => setFormData(prev => ({ ...prev, logement_id: logement.id }))}
            >
              <h4 className="font-semibold text-lg">{logement.titre}</h4>
              <p className="text-gray-600 text-sm mb-2">{logement.adresse}</p>
              <p className="text-blue-600 font-semibold">{logement.loyer}€/mois</p>
              {logement.montant_charges && (
                <p className="text-gray-500 text-sm">+ {logement.montant_charges}€ de charges</p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );

  const loadServices = async () => {
    try {
      const servicesData = await getAllServices(true);
      setServices(servicesData);
      // Sélectionner par défaut le service "Attestation de logement"
      const defaultService = servicesData.find(s => s.slug === 'attestation-logement-prise-charge');
      if (defaultService) {
        setSelectedServices([defaultService.id]);
      }
    } catch (error) {
      console.error('Erreur chargement services:', error);
    }
  };

  const handleServiceToggle = (serviceId) => {
    setSelectedServices(prev => 
      prev.includes(serviceId) 
        ? prev.filter(id => id !== serviceId)
        : [...prev, serviceId]
    );
  };

  const handleGenerateProforma = async () => {
    try {
      setProformaLoading(true);
      setGeneralError('');
      
      // Récupérer le logement sélectionné
      const selectedLogement = logements.find(l => l.id === parseInt(formData.logement_id));
      if (!selectedLogement) {
        setGeneralError('Veuillez sélectionner un logement');
        return;
      }
      
      // Préparer les données client
      const clientData = {
        nom: formData.nom_client,
        prenom: formData.prenom_client,
        email: formData.email_client,
        date_naissance: formData.date_naissance_client,
        ville_naissance_client: formData.ville_naissance_client,
        pays_naissance_client: formData.pays_naissance_client,
        nationalite: formData.nationalite_client,
        numero_passeport: formData.numero_passeport || '',
        telephone: formData.telephone_client || '',
        date_arrivee_prevue: formData.date_arrivee_prevue
      };
      
      // Préparer les données logement
      const logementData = {
        type_logement: selectedLogement.type_logement,
        adresse: selectedLogement.adresse,
        ville: selectedLogement.ville,
        prix_mois: selectedLogement.prix_mois,
        caution: selectedLogement.caution,
        frais_agence: selectedLogement.frais_agence || 0
      };
      
      const result = await generateProforma(clientData, selectedServices, logementData);
      
      if (result.success) {
        setProformaData(result);
      } else {
        setGeneralError(result.error || 'Erreur lors de la génération de la proforma');
      }
      
    } catch (error) {
      console.error('Erreur génération proforma:', error);
      setGeneralError('Erreur lors de la génération de la proforma');
    } finally {
      setProformaLoading(false);
    }
  };

  const handleDownloadProforma = () => {
    if (proformaData?.pdfBlob) {
      try {
        downloadPdf(proformaData.pdfBlob, proformaData.filename);
      } catch (error) {
        setGeneralError('Erreur lors du téléchargement');
      }
    }
  };

  const handlePreviewProforma = () => {
    if (proformaData?.pdfUrl) {
      try {
        previewPdf(proformaData.pdfUrl);
      } catch (error) {
        setGeneralError('Erreur lors de l\'ouverture de la prévisualisation');
      }
    }
  };

  const renderStep4 = () => {
    // Charger les services si pas encore fait
    if (services.length === 0) {
      loadServices();
    }

    const selectedLogement = logements.find(l => l.id === parseInt(formData.logement_id));
    const selectedServicesData = services.filter(s => selectedServices.includes(s.id));
    const totalServices = selectedServicesData.reduce((total, service) => total + service.tarif, 0);
    const totalLogement = selectedLogement ? 
      (selectedLogement.prix_mois + selectedLogement.caution + (selectedLogement.frais_agence || 0)) : 0;
    const totalGeneral = totalServices + totalLogement;

    return (
      <div className="space-y-6">
        <h3 className="text-xl font-semibold text-gray-800 mb-6">Récapitulatif et Proforma</h3>
        
        {/* Récapitulatif */}
        <div className="bg-gradient-to-r from-blue-50 to-orange-50 rounded-lg p-6 border border-blue-200">
          <h4 className="font-semibold text-blue-800 mb-4">Récapitulatif de la Souscription</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-sm">
            <div>
              <p><strong>Client:</strong> {formData.prenom_client} {formData.nom_client}</p>
              <p><strong>Email:</strong> {formData.email_client}</p>
              <p><strong>Nationalité:</strong> {formData.nationalite_client}</p>
            </div>
            <div>
              <p><strong>École:</strong> {formData.ecole_universite}</p>
              <p><strong>Filière:</strong> {formData.filiere}</p>
              <p><strong>Arrivée prévue:</strong> {formData.date_arrivee_prevue}</p>
            </div>
          </div>
          {selectedLogement && (
            <div className="mt-4 pt-4 border-t border-blue-200">
              <p><strong>Logement:</strong> {selectedLogement.type_logement} - {selectedLogement.ville}</p>
              <p><strong>Adresse:</strong> {selectedLogement.adresse}</p>
            </div>
          )}
        </div>



        {/* Section Proforma */}
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h4 className="font-semibold text-gray-800 mb-4">Proforma</h4>
          
          {proformaLoading ? (
            <div className="text-center py-8">
              <SpinLoader size="lg" text="Génération de la proforma en cours..." />
            </div>
          ) : proformaData ? (
            <div className="space-y-4">
              <div className="flex items-center p-4 bg-green-50 border border-green-200 rounded-lg">
                <svg className="w-6 h-6 text-green-600 mr-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                <span className="text-green-800">Proforma générée avec succès !</span>
              </div>
              
              <div className="flex space-x-3">
                <button
                  onClick={handlePreviewProforma}
                  className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200"
                >
                  📄 Prévisualiser
                </button>
                <button
                  onClick={handleDownloadProforma}
                  className="flex-1 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors duration-200"
                >
                  📥 Télécharger
                </button>
              </div>
            </div>
          ) : (
            <div className="text-center py-8">
              <div className="text-gray-500 mb-4">
                <svg className="w-12 h-12 mx-auto mb-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <p>Une erreur est survenue lors de la génération automatique de la proforma.</p>
              </div>
              <button
                onClick={handleGenerateProforma}
                className="px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors duration-200"
              >
                🔄 Régénérer la Proforma
              </button>
            </div>
          )}
        </div>
      </div>
    );
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-2xl max-w-4xl w-full max-h-[90vh] shadow-2xl flex flex-col">
        {/* Header fixe avec titre et indicateur d'étapes */}
        <div className="flex-shrink-0">
          <div className="px-8 py-6 border-b border-gray-100">
            <h2 className="text-2xl font-bold text-gray-800">
              {souscriptionToEdit ? (
                <>
                  <span className="text-blue-600">Modifier</span> Souscription
                </>
              ) : (
                <>
                  <span className="text-blue-600">Nouvelle</span> Souscription
                </>
              )}
            </h2>
          </div>
          
          <div className="px-8 pt-6 pb-4 border-b border-gray-100">
            {renderStepIndicator()}
            {renderErrorMessage()}
          </div>
        </div>
        
        {/* Contenu scrollable - seul le contenu du step actuel */}
        <div className="flex-1 overflow-y-auto">
          <div className="p-8">
            {currentStep === 1 && renderStep1()}
            {currentStep === 2 && renderStep2()}
            {currentStep === 3 && renderStep3()}
            {currentStep === 4 && renderStep4()}
          </div>
        </div>
        
        {/* Footer fixe */}
        <div className="px-8 py-6 border-t border-gray-100 flex-shrink-0 bg-white rounded-b-2xl">
          <div className="flex justify-between">
            <button
              onClick={onCancel}
              className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors duration-200"
            >
              Annuler
            </button>
            
            <div className="flex space-x-3">
              {currentStep > 1 && (
                <button
                  onClick={handlePrevStep}
                  className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors duration-200"
                >
                  Précédent
                </button>
              )}
              
              {currentStep < 4 ? (
                <button
                  onClick={handleNextStep}
                  className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200"
                >
                  Suivant
                </button>
              ) : (
                <button
                  onClick={handleSubmit}
                  disabled={loading}
                  className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 transition-colors duration-200"
                >
                  {loading ? 'Enregistrement...' : 'Finaliser'}
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