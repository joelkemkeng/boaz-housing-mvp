import React, { useState } from 'react';
import LogementList from '../components/LogementList';
import LogementForm from '../components/LogementForm';
import LogementStats from '../components/LogementStats';
import LogementDetailModal from '../components/LogementDetailModal';
import { logementService } from '../services/logementService';

const LogementsPage = () => {
  const [showForm, setShowForm] = useState(false);
  const [selectedLogement, setSelectedLogement] = useState(null);
  const [isEdit, setIsEdit] = useState(false);
  const [refreshKey, setRefreshKey] = useState(0);
  const [showDetailModal, setShowDetailModal] = useState(false);
  const [logementToView, setLogementToView] = useState(null);
  const [loadingEdit, setLoadingEdit] = useState(false);

  const handleNewLogement = () => {
    setSelectedLogement(null);
    setIsEdit(false);
    setShowForm(true);
  };

  const handleEditLogement = async (logement) => {
    try {
      setLoadingEdit(true);
      
      // Fermer d'abord le formulaire s'il est ouvert pour forcer un remount
      setShowForm(false);
      setSelectedLogement(null);
      
      // Récupérer les données fraîches du logement depuis l'API
      const logementFrais = await logementService.getLogement(logement.id);
      
      // Ensuite définir le nouveau logement et ouvrir le formulaire
      setTimeout(() => {
        setSelectedLogement(logementFrais);
        setIsEdit(true);
        setShowForm(true);
        setLoadingEdit(false);
      }, 10);
    } catch (error) {
      console.error('Erreur lors de la récupération du logement:', error);
      // En cas d'erreur, utiliser les données existantes
      setTimeout(() => {
        setSelectedLogement(logement);
        setIsEdit(true);
        setShowForm(true);
        setLoadingEdit(false);
      }, 10);
    }
  };

  const handleViewLogement = (logement) => {
    setLogementToView(logement);
    setShowDetailModal(true);
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

  const handleCloseDetailModal = () => {
    setShowDetailModal(false);
    setLogementToView(null);
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
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
              refreshTrigger={refreshKey}
              onEdit={handleEditLogement}
              onView={handleViewLogement}
              onDataChange={handleDataChange}
              loadingEdit={loadingEdit}
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

        {/* Modal de détail */}
        <LogementDetailModal
          logement={logementToView}
          show={showDetailModal}
          onClose={handleCloseDetailModal}
        />
      </div>
    </div>
  );
};

export default LogementsPage;