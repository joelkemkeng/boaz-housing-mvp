import React from 'react';

const LogementDetailModal = ({ logement, onClose, show = false }) => {
  if (!show || !logement) return null;

  const statutColors = {
    disponible: 'bg-green-100 text-green-800 border-green-200',
    occupe: 'bg-red-100 text-red-800 border-red-200',
    maintenance: 'bg-yellow-100 text-yellow-800 border-yellow-200'
  };

  const statutIcons = {
    disponible: '🟢',
    occupe: '🔴',
    maintenance: '🟡'
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Non renseigné';
    return new Date(dateString).toLocaleDateString('fr-FR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 overflow-y-auto h-full w-full z-50 flex items-center justify-center p-4">
      <div className="relative bg-white rounded-xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 rounded-t-xl">
          <div className="flex justify-between items-start">
            <div className="flex-1">
              <h2 className="text-2xl font-bold text-gray-900 mb-2">{logement.titre}</h2>
              <div className="flex items-center space-x-3">
                <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium border ${statutColors[logement.statut]}`}>
                  <span className="mr-2">{statutIcons[logement.statut]}</span>
                  {logement.statut.charAt(0).toUpperCase() + logement.statut.slice(1)}
                </span>
                <span className="text-3xl font-bold text-blue-600">{logement.montant_total}€/mois</span>
              </div>
            </div>
            <button
              onClick={onClose}
              className="ml-4 text-gray-400 hover:text-gray-600 text-2xl font-bold w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-100"
              aria-label="Fermer"
            >
              ×
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="p-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            
            {/* Section Localisation */}
            <div className="bg-gray-50 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <span className="mr-2">📍</span>
                Localisation
              </h3>
              <div className="space-y-3">
                <div className="flex items-start">
                  <span className="text-gray-500 font-medium w-24 flex-shrink-0">Adresse:</span>
                  <span className="text-gray-900">{logement.adresse}</span>
                </div>
                <div className="flex items-center">
                  <span className="text-gray-500 font-medium w-24 flex-shrink-0">Ville:</span>
                  <span className="text-gray-900 font-medium">{logement.ville}</span>
                </div>
                <div className="flex items-center">
                  <span className="text-gray-500 font-medium w-24 flex-shrink-0">Code postal:</span>
                  <span className="text-gray-900">{logement.code_postal}</span>
                </div>
                <div className="flex items-center">
                  <span className="text-gray-500 font-medium w-24 flex-shrink-0">Pays:</span>
                  <span className="text-gray-900">{logement.pays}</span>
                </div>
              </div>
            </div>

            {/* Section Prix */}
            <div className="bg-blue-50 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <span className="mr-2">💰</span>
                Tarification
              </h3>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-gray-500 font-medium">Loyer mensuel:</span>
                  <span className="text-lg font-semibold text-blue-600">{logement.loyer}€</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-500 font-medium">Charges:</span>
                  <span className="text-lg font-semibold text-gray-700">
                    {logement.montant_charges > 0 ? `${logement.montant_charges}€` : 'Incluses'}
                  </span>
                </div>
                <hr className="border-gray-300" />
                <div className="flex justify-between items-center">
                  <span className="text-gray-900 font-bold">Total mensuel:</span>
                  <span className="text-2xl font-bold text-blue-600">{logement.montant_total}€</span>
                </div>
                
                {/* Calcul annuel */}
                <div className="mt-4 p-3 bg-blue-100 rounded-md">
                  <div className="flex justify-between items-center">
                    <span className="text-blue-800 font-medium">Coût annuel:</span>
                    <span className="text-lg font-bold text-blue-800">{(logement.montant_total * 12).toLocaleString()}€</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Section Description */}
            <div className="lg:col-span-2">
              <div className="bg-white border border-gray-200 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                  <span className="mr-2">📝</span>
                  Description
                </h3>
                <div className="prose prose-sm max-w-none">
                  <p className="text-gray-700 leading-relaxed whitespace-pre-line">
                    {logement.description || 'Aucune description fournie pour ce logement.'}
                  </p>
                </div>
              </div>
            </div>

            {/* Section Informations administratives */}
            <div className="bg-gray-50 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <span className="mr-2">📊</span>
                Informations
              </h3>
              <div className="space-y-3">
                <div className="flex items-center">
                  <span className="text-gray-500 font-medium w-32 flex-shrink-0">ID Logement:</span>
                  <span className="text-gray-900 font-mono">#{logement.id}</span>
                </div>
                <div className="flex items-center">
                  <span className="text-gray-500 font-medium w-32 flex-shrink-0">Statut actuel:</span>
                  <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${statutColors[logement.statut]}`}>
                    {statutIcons[logement.statut]} {logement.statut}
                  </span>
                </div>
                <div className="flex items-start">
                  <span className="text-gray-500 font-medium w-32 flex-shrink-0">Créé le:</span>
                  <span className="text-gray-900 text-sm">{formatDate(logement.created_at)}</span>
                </div>
                <div className="flex items-start">
                  <span className="text-gray-500 font-medium w-32 flex-shrink-0">Modifié le:</span>
                  <span className="text-gray-900 text-sm">{formatDate(logement.updated_at)}</span>
                </div>
              </div>
            </div>

            {/* Section Résumé rapide */}
            <div className="bg-green-50 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <span className="mr-2">🏠</span>
                Résumé
              </h3>
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">📍 Localisation:</span>
                  <span className="font-medium text-gray-900">{logement.ville}, {logement.pays}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">💰 Prix/mois:</span>
                  <span className="font-bold text-green-600">{logement.montant_total}€</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">📋 Statut:</span>
                  <span className={`font-medium ${logement.statut === 'disponible' ? 'text-green-600' : logement.statut === 'occupe' ? 'text-red-600' : 'text-yellow-600'}`}>
                    {logement.statut.charAt(0).toUpperCase() + logement.statut.slice(1)}
                  </span>
                </div>
                {logement.montant_charges > 0 && (
                  <div className="flex items-center justify-between">
                    <span className="text-gray-600">📊 Charges:</span>
                    <span className="font-medium text-gray-900">{logement.montant_charges}€</span>
                  </div>
                )}
              </div>
              
              {logement.statut === 'disponible' && (
                <div className="mt-4 p-3 bg-green-100 rounded-md border border-green-200">
                  <div className="flex items-center">
                    <span className="text-green-800 font-medium">✅ Ce logement est actuellement disponible à la location</span>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="sticky bottom-0 bg-gray-50 border-t border-gray-200 px-6 py-4 rounded-b-xl">
          <div className="flex justify-end space-x-3">
            <button
              onClick={onClose}
              className="px-6 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              Fermer
            </button>
            <button
              onClick={() => {
                navigator.clipboard.writeText(`Logement #${logement.id} - ${logement.titre} - ${logement.ville} - ${logement.montant_total}€/mois`);
                alert('Informations copiées dans le presse-papiers !');
              }}
              className="px-6 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              📋 Copier le résumé
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LogementDetailModal;