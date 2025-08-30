import React, { useState, useEffect } from 'react';
import { getLogement } from '../../services/logementService';

const SouscriptionViewModal = ({ souscription, show, onClose }) => {
  const [logement, setLogement] = useState(null);
  const [loadingLogement, setLoadingLogement] = useState(false);
  const [expandedSections, setExpandedSections] = useState({
    client: true,
    academique: true,
    logement: true,
    administrative: true
  });

  useEffect(() => {
    if (show && souscription) {
      loadLogementDetails();
    }
  }, [show, souscription]);

  const loadLogementDetails = async () => {
    if (souscription.logement_id) {
      try {
        setLoadingLogement(true);
        const logementData = await getLogement(souscription.logement_id);
        setLogement(logementData);
      } catch (error) {
        console.error('Erreur chargement logement:', error);
      } finally {
        setLoadingLogement(false);
      }
    }
  };

  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Non renseigné';
    return new Date(dateString).toLocaleDateString('fr-FR');
  };

  const getStatutBadge = (statut) => {
    const configs = {
      'attente_paiement': {
        style: 'bg-orange-100 text-orange-800 border-orange-200',
        icon: '⏳',
        label: 'En attente de paiement'
      },
      'paye': {
        style: 'bg-blue-100 text-blue-800 border-blue-200',
        icon: '💳',
        label: 'Payé'
      },
      'livre': {
        style: 'bg-green-100 text-green-800 border-green-200',
        icon: '✅',
        label: 'Livré'
      },
      'cloture': {
        style: 'bg-gray-100 text-gray-800 border-gray-200',
        icon: '📋',
        label: 'Clôturé'
      }
    };
    
    const config = configs[statut] || {
      style: 'bg-gray-100 text-gray-800 border-gray-200',
      icon: '❓',
      label: statut
    };

    return (
      <span className={`px-3 py-1 text-sm font-medium rounded-full border flex items-center space-x-1 ${config.style} shadow-sm`}>
        <span>{config.icon}</span>
        <span>{config.label}</span>
      </span>
    );
  };

  const renderSection = (title, icon, sectionKey, content) => {
    const isExpanded = expandedSections[sectionKey];
    const isLogementSection = sectionKey === 'logement';
    
    return (
      <div className="border border-orange-200 rounded-lg overflow-hidden mb-4 shadow-sm">
        <button
          onClick={() => toggleSection(sectionKey)}
          className="w-full px-6 py-4 bg-gradient-to-r from-blue-50 to-orange-50 hover:from-blue-100 hover:to-orange-100 transition-all duration-200 flex items-center justify-between"
        >
          <div className="flex items-center space-x-3">
            <div className="text-blue-600">{icon}</div>
            <h3 className="text-lg font-medium text-gray-900">{title}</h3>
          </div>
          <svg 
            className={`w-5 h-5 text-orange-500 transform transition-transform duration-200 ${isExpanded ? 'rotate-180' : ''}`}
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path>
          </svg>
        </button>
        
        <div className={`overflow-hidden transition-all duration-300 ${isExpanded ? (isLogementSection ? 'max-h-[600px]' : 'max-h-[500px]') + ' opacity-100' : 'max-h-0 opacity-0'}`}>
          <div className={`px-6 py-4 bg-white ${isLogementSection ? 'overflow-y-auto max-h-[550px]' : ''}`}>
            {content}
          </div>
        </div>
      </div>
    );
  };

  const renderInfoField = (label, value, fullWidth = false) => (
    <div className={fullWidth ? "col-span-2" : ""}>
      <dt className="text-sm font-medium text-blue-600 mb-1">{label}</dt>
      <dd className="text-sm text-gray-900 bg-gradient-to-r from-blue-50 to-orange-50 px-3 py-2 rounded border border-blue-200 shadow-sm">
        {value || 'Non renseigné'}
      </dd>
    </div>
  );

  if (!show || !souscription) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50 animate-fadeIn">
      <div className="bg-white rounded-lg max-w-4xl w-full max-h-[95vh] overflow-y-auto shadow-2xl transform animate-slideIn">
        {/* Header */}
        <div className="px-6 py-4 border-b border-orange-200 bg-gradient-to-r from-blue-50 via-blue-100 to-orange-100">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-semibold text-blue-900">
                Détails de la Souscription
              </h2>
              <p className="text-sm text-blue-600 mt-1">
                Référence : <span className="font-mono font-medium text-orange-600">{souscription.reference}</span>
              </p>
            </div>
            <div className="flex items-center space-x-4">
              {getStatutBadge(souscription.statut)}
              <button
                onClick={onClose}
                className="text-orange-400 hover:text-orange-600 transition-colors duration-200 bg-white rounded-full p-2 shadow-md"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
              </button>
            </div>
          </div>
        </div>

        {/* Content */}
        <div className="p-6">
          {/* Section Informations Client */}
          {renderSection(
            "Informations Client",
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
            </svg>,
            "client",
            <dl className="grid grid-cols-2 gap-4">
              {renderInfoField("Nom complet", `${souscription.prenom_client} ${souscription.nom_client}`, true)}
              {renderInfoField("Email", souscription.email_client)}
              {renderInfoField("Date de naissance", formatDate(souscription.date_naissance_client))}
              {renderInfoField("Ville de naissance", souscription.ville_naissance_client)}
              {renderInfoField("Pays de naissance", souscription.pays_naissance_client)}
              {renderInfoField("Nationalité", souscription.nationalite_client)}
              {renderInfoField("Pays de destination", souscription.pays_destination)}
              {renderInfoField("Date d'arrivée prévue", formatDate(souscription.date_arrivee_prevue))}
            </dl>
          )}

          {/* Section Informations Académiques */}
          {renderSection(
            "Informations Académiques",
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 14l9-5-9-5-9 5 9 5z"></path>
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z"></path>
            </svg>,
            "academique",
            <dl className="grid grid-cols-2 gap-4">
              {renderInfoField("École/Université", souscription.ecole_universite, true)}
              {renderInfoField("Filière", souscription.filiere, true)}
              {renderInfoField("Pays de l'école", souscription.pays_ecole)}
              {renderInfoField("Ville de l'école", souscription.ville_ecole)}
              {renderInfoField("Code postal", souscription.code_postal_ecole)}
              {renderInfoField("Adresse complète", souscription.adresse_ecole, true)}
            </dl>
          )}

          {/* Section Informations Logement */}
          {renderSection(
            "Informations Logement",
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path>
            </svg>,
            "logement",
            loadingLogement ? (
              <div className="text-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                <p className="text-gray-500 mt-2">Chargement des informations du logement...</p>
              </div>
            ) : logement ? (
              <div className="space-y-4">
                <dl className="grid grid-cols-2 gap-4">
                  {renderInfoField("Titre", logement.titre, true)}
                  {renderInfoField("Adresse", logement.adresse, true)}
                  {renderInfoField("Ville", logement.ville)}
                  {renderInfoField("Code postal", logement.code_postal)}
                  {renderInfoField("Pays", logement.pays)}
                  {renderInfoField("Statut du logement", logement.statut)}
                </dl>
                
                <div className="bg-gradient-to-r from-orange-50 to-blue-50 border border-orange-300 rounded-lg p-4 shadow-sm">
                  <h4 className="font-medium text-orange-800 mb-3 flex items-center space-x-2">
                    <svg className="w-5 h-5 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"></path>
                    </svg>
                    <span>Informations Financières</span>
                  </h4>
                  <dl className="grid grid-cols-2 gap-4">
                    {renderInfoField("Loyer", `${logement.loyer}€`)}
                    {renderInfoField("Charges", `${logement.montant_charges}€`)}
                    {renderInfoField("Total mensuel", `${logement.montant_total}€`, true)}
                  </dl>
                </div>

                {logement.description && (
                  <div>
                    <dt className="text-sm font-medium text-gray-500 mb-1">Description</dt>
                    <dd className="text-sm text-gray-900 bg-gray-50 px-3 py-3 rounded border">
                      {logement.description}
                    </dd>
                  </div>
                )}
              </div>
            ) : (
              <p className="text-gray-500 text-center py-4">Aucune information de logement disponible</p>
            )
          )}

          {/* Section Informations Administratives */}
          {renderSection(
            "Informations Administratives",
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>,
            "administrative",
            <dl className="grid grid-cols-2 gap-4">
              {renderInfoField("Date d'entrée prévue", formatDate(souscription.date_entree_prevue))}
              {renderInfoField("Durée de location", `${souscription.duree_location_mois} mois`)}
              {renderInfoField("Date de création", formatDate(souscription.created_at))}
              {renderInfoField("Dernière modification", formatDate(souscription.updated_at))}
            </dl>
          )}
        </div>

        {/* Footer */}
        <div className="px-6 py-4 border-t border-orange-200 bg-gradient-to-r from-blue-50 to-orange-50 flex justify-end">
          <button
            onClick={onClose}
            className="px-6 py-2 bg-gradient-to-r from-orange-500 to-blue-500 text-white rounded-lg hover:from-orange-600 hover:to-blue-600 transition-all duration-200 shadow-md font-medium"
          >
            Fermer
          </button>
        </div>
      </div>
    </div>
  );
};

export default SouscriptionViewModal;