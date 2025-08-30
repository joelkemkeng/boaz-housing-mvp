import React, { useState, useEffect } from 'react';
import { getSouscriptions, deleteSouscription, changerStatutSouscription } from '../../services/souscriptionService';
import WizardSouscription from './WizardSouscription';
import SouscriptionViewModal from './SouscriptionViewModal';

const HistoriqueSection = ({ onDataChange }) => {
  const [souscriptions, setSouscriptions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedSouscription, setSelectedSouscription] = useState(null);
  const [showViewModal, setShowViewModal] = useState(false);
  const [souscriptionToEdit, setSouscriptionToEdit] = useState(null);
  const [showEditWizard, setShowEditWizard] = useState(false);

  useEffect(() => {
    loadSouscriptions();
  }, []);

  const loadSouscriptions = async () => {
    try {
      setLoading(true);
      const data = await getSouscriptions();
      setSouscriptions(data);
    } catch (error) {
      console.error('Erreur lors du chargement des souscriptions:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleView = (souscription) => {
    setSelectedSouscription(souscription);
    setShowViewModal(true);
  };

  const handleModifier = (souscription) => {
    setSouscriptionToEdit(souscription);
    setShowEditWizard(true);
  };

  const handleEditComplete = () => {
    setShowEditWizard(false);
    setSouscriptionToEdit(null);
    loadSouscriptions();
    onDataChange();
  };

  const handleEditCancel = () => {
    setShowEditWizard(false);
    setSouscriptionToEdit(null);
  };

  const handlePayer = async (souscription) => {
    if (window.confirm('Confirmer le paiement de cette souscription ?')) {
      try {
        await changerStatutSouscription(souscription.id, 'paye');
        await loadSouscriptions();
        onDataChange();
      } catch (error) {
        alert('Erreur lors du changement de statut: ' + error.message);
      }
    }
  };

  const handleDelete = async (souscription) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer cette souscription ?')) {
      try {
        await deleteSouscription(souscription.id);
        await loadSouscriptions();
        onDataChange();
      } catch (error) {
        alert('Erreur lors de la suppression: ' + error.message);
      }
    }
  };

  const getStatutBadge = (statut) => {
    const styles = {
      'attente_paiement': 'bg-red-100 text-red-800',
      'paye': 'bg-blue-100 text-blue-800',
      'livre': 'bg-green-100 text-green-800',
      'cloture': 'bg-gray-100 text-gray-800'
    };
    
    const labels = {
      'attente_paiement': 'Attente paiement',
      'paye': 'Payé',
      'livre': 'Livré',
      'cloture': 'Clôturé'
    };

    return (
      <span className={`px-2 py-1 text-xs font-medium rounded-full ${styles[statut] || 'bg-gray-100 text-gray-800'}`}>
        {labels[statut] || statut}
      </span>
    );
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('fr-FR');
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-medium text-gray-900">Historique des Souscriptions</h2>
        </div>
        <div className="p-6">
          <div className="text-center">Chargement...</div>
        </div>
      </div>
    );
  }

  return (
    <>
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-medium text-gray-900">Historique des Souscriptions</h2>
          <p className="text-sm text-gray-600">Gérez vos souscriptions existantes</p>
        </div>
        
        <div className="overflow-x-auto">
          {souscriptions.length === 0 ? (
            <div className="p-6 text-center text-gray-500">
              <div className="w-12 h-12 mx-auto mb-4 text-gray-400">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
              </div>
              <p>Aucune souscription pour le moment</p>
              <p className="text-sm">Utilisez le service ci-dessus pour créer votre première souscription</p>
            </div>
          ) : (
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Client
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Référence
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Date création
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Statut
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {souscriptions.map((souscription) => (
                  <tr key={souscription.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div>
                        <div className="text-sm font-medium text-gray-900">
                          {souscription.prenom_client} {souscription.nom_client}
                        </div>
                        <div className="text-sm text-gray-500">
                          {souscription.email_client}
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {souscription.reference}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {formatDate(souscription.created_at)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {getStatutBadge(souscription.statut)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <div className="flex space-x-2">
                        <button
                          onClick={() => handleView(souscription)}
                          className="text-blue-600 hover:text-blue-900"
                        >
                          Voir
                        </button>
                        {souscription.statut === 'attente_paiement' && (
                          <>
                            <button
                              onClick={() => handleModifier(souscription)}
                              className="text-orange-600 hover:text-orange-900"
                            >
                              Modifier
                            </button>
                            <button
                              onClick={() => handlePayer(souscription)}
                              className="text-green-600 hover:text-green-900"
                            >
                              Payer
                            </button>
                          </>
                        )}
                        <button
                          onClick={() => handleDelete(souscription)}
                          className="text-red-600 hover:text-red-900"
                        >
                          Supprimer
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>

      {/* Modal Voir Détails */}
      <SouscriptionViewModal
        souscription={selectedSouscription}
        show={showViewModal}
        onClose={() => {
          setShowViewModal(false);
          setSelectedSouscription(null);
        }}
      />

      {/* Wizard Edition */}
      {showEditWizard && souscriptionToEdit && (
        <WizardSouscription
          souscriptionToEdit={souscriptionToEdit}
          onComplete={handleEditComplete}
          onCancel={handleEditCancel}
        />
      )}
    </>
  );
};

export default HistoriqueSection;