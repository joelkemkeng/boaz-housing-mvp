import React, { useState } from 'react';
import LogementList from '../components/LogementList';
import LogementForm from '../components/LogementForm';
import LogementStats from '../components/LogementStats';

const LogementsPage = () => {
  const [showForm, setShowForm] = useState(false);
  const [selectedLogement, setSelectedLogement] = useState(null);
  const [isEdit, setIsEdit] = useState(false);
  const [refreshKey, setRefreshKey] = useState(0);

  const handleNewLogement = () => {
    setSelectedLogement(null);
    setIsEdit(false);
    setShowForm(true);
  };

  const handleEditLogement = (logement) => {
    setSelectedLogement(logement);
    setIsEdit(true);
    setShowForm(true);
  };

  const handleViewLogement = (logement) => {
    const description = logement.description ? `\nDescription: ${logement.description}` : '';
    alert(`Détails du logement:\n\nTitre: ${logement.titre}${description}\nAdresse: ${logement.adresse}\nVille: ${logement.ville}\nCode postal: ${logement.code_postal}\nPays: ${logement.pays}\nLoyer: ${logement.loyer}€\nStatut: ${logement.statut}\n\nCréé le: ${new Date(logement.created_at).toLocaleDateString('fr-FR')}`);
  };

  const handleFormSave = (logement) => {
    setShowForm(false);
    setSelectedLogement(null);
    setRefreshKey(prev => prev + 1);
  };

  const handleFormCancel = () => {
    setShowForm(false);
    setSelectedLogement(null);
  };

  const handleDataChange = () => {
    // Forcer la mise à jour des statistiques et de la liste
    setRefreshKey(prev => prev + 1);
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Gestion des logements</h1>
              <p className="text-gray-600 mt-2">Gérez le parc locatif Boaz-Housing</p>
            </div>
            <button
              onClick={handleNewLogement}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200 font-medium"
            >
              + Nouveau logement
            </button>
          </div>
        </div>

        {/* Statistiques */}
        <LogementStats key={`stats-${refreshKey}`} />

        {/* Liste des logements */}
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-medium text-gray-900">Liste des logements</h2>
          </div>
          <div className="p-6">
            <LogementList
              key={`list-${refreshKey}`}
              onEdit={handleEditLogement}
              onView={handleViewLogement}
              onDataChange={handleDataChange}
            />
          </div>
        </div>

        {/* Formulaire modal */}
        {showForm && (
          <LogementForm
            logement={selectedLogement}
            onSave={handleFormSave}
            onCancel={handleFormCancel}
            isEdit={isEdit}
          />
        )}
      </div>
    </div>
  );
};

export default LogementsPage;