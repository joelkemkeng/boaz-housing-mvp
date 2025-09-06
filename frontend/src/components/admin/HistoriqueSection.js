import React, { useState, useEffect } from 'react';
import { getSouscriptions, deleteSouscription, changerStatutSouscription, payerSouscription, livrerSouscription } from '../../services/souscriptionService';
import { previewAttestation, previewPdf, sendProformaEmail } from '../../services/proformaService';
import WizardSouscription from './WizardSouscription';
import SouscriptionViewModal from './SouscriptionViewModal';
import ConfirmModal from '../common/ConfirmModal';
import { useAuth } from '../../contexts/AuthContext';

const HistoriqueSection = ({ onDataChange }) => {
  const { user } = useAuth();
  const [souscriptions, setSouscriptions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedSouscription, setSelectedSouscription] = useState(null);
  const [showViewModal, setShowViewModal] = useState(false);
  const [souscriptionToEdit, setSouscriptionToEdit] = useState(null);
  const [showEditWizard, setShowEditWizard] = useState(false);
  
  // États pour l'envoi de proforma
  const [showEmailModal, setShowEmailModal] = useState(false);
  const [emailLoading, setEmailLoading] = useState(false);
  const [emailModalConfig, setEmailModalConfig] = useState({
    type: 'info',
    title: '',
    message: '',
    onConfirm: null
  });

  useEffect(() => {
    loadSouscriptions();
  }, []);

  const loadSouscriptions = async () => {
    try {
      setLoading(true);
      const data = await getSouscriptions();
      setSouscriptions(data);
      
      // DEBUG: Afficher les statuts des souscriptions et le rôle utilisateur
      console.log('🔍 DEBUG - Utilisateur actuel:', user);
      console.log('🔍 DEBUG - Souscriptions chargées:', data);
      data.forEach(souscription => {
        console.log(`🔍 DEBUG - Souscription ${souscription.id}: statut = "${souscription.statut}"`);
      });
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
        await payerSouscription(souscription.id);
        await loadSouscriptions();
        onDataChange();
      } catch (error) {
        alert('Erreur lors du paiement: ' + error.message);
      }
    }
  };

  const handleLivrer = async (souscription) => {
    if (window.confirm('Confirmer la livraison de cette souscription ?')) {
      try {
        await livrerSouscription(souscription.id);
        await loadSouscriptions();
        onDataChange();
        alert('Souscription livrée avec succès !');
      } catch (error) {
        if (error.response?.status === 400) {
          alert('Erreur de livraison: ' + (error.response.data.detail || error.message));
        } else {
          alert('Erreur lors de la livraison: ' + error.message);
        }
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

  const handlePreviewAttestation = async (souscription) => {
    try {
      const result = await previewAttestation(souscription.id);
      if (result.success) {
        previewPdf(result.pdfUrl);
      } else {
        alert('Erreur lors de la génération: ' + result.error);
      }
    } catch (error) {
      alert('Erreur lors de la génération de l\'attestation: ' + error.message);
    }
  };

  const handleSendProforma = (souscription) => {
    // Configuration du modal de confirmation
    setEmailModalConfig({
      type: 'info',
      title: 'Envoyer Proforma',
      message: `Envoyer le proforma pour ${souscription.prenom_client} ${souscription.nom_client} à l'adresse ${souscription.email_client} ?`,
      onConfirm: () => performSendProforma(souscription)
    });
    setShowEmailModal(true);
  };

  const performSendProforma = async (souscription) => {
    try {
      setEmailLoading(true);
      
      const result = await sendProformaEmail(souscription.id);
      
      if (result.success) {
        // Modal de succès
        setEmailModalConfig({
          type: 'success',
          title: 'Envoi réussi !',
          message: `Le proforma a été envoyé avec succès à ${result.recipient}. Référence: ${result.reference}`,
          onConfirm: () => setShowEmailModal(false)
        });
      } else {
        // Modal d'erreur
        setEmailModalConfig({
          type: 'error',
          title: 'Erreur d\'envoi',
          message: result.error || 'Une erreur est survenue lors de l\'envoi du proforma.',
          onConfirm: () => setShowEmailModal(false)
        });
      }
      
    } catch (error) {
      // Modal d'erreur pour les exceptions
      setEmailModalConfig({
        type: 'error',
        title: 'Erreur système',
        message: `Erreur inattendue: ${error.message}`,
        onConfirm: () => setShowEmailModal(false)
      });
    } finally {
      setEmailLoading(false);
    }
  };

  const getStatutBadge = (statut) => {
    const styles = {
      'ATTENTE_PAIEMENT': 'bg-red-100 text-red-800',
      'ATTENTE_LIVRAISON': 'bg-blue-100 text-blue-800',
      'LIVRE': 'bg-green-100 text-green-800',
      'CLOTURE': 'bg-gray-100 text-gray-800'
    };
    
    const labels = {
      'ATTENTE_PAIEMENT': 'Attente paiement',
      'ATTENTE_LIVRAISON': 'Attente livraison',
      'LIVRE': 'Livré',
      'CLOTURE': 'Clôturé'
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
                    Logement
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
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div>
                        <div className="text-sm font-medium text-gray-900">
                          {souscription.logement?.titre || 'Non défini'}
                        </div>
                        <div className="text-sm text-gray-500">
                          {souscription.logement?.loyer ? `${souscription.logement.loyer}€/mois` : ''}
                        </div>
                        <div className="text-xs text-gray-400 mt-1">
                          {souscription.logement?.adresse ? (
                            <>
                              {souscription.logement.adresse}
                              <br />
                              {souscription.logement?.ville || ''} {souscription.logement?.code_postal || ''}
                            </>
                          ) : (
                            'Adresse non définie'
                          )}
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
                      <div className="flex flex-wrap gap-2">
                        <button
                          onClick={() => handleView(souscription)}
                          className="inline-flex items-center px-2.5 py-1.5 border border-transparent text-xs font-medium rounded text-blue-700 bg-blue-100 hover:bg-blue-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
                        >
                          <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                          </svg>
                          Voir
                        </button>
                        {/* DEBUG: Afficher les conditions */}
                        {console.log(`🔍 DEBUG Souscription ${souscription.id}:`, {
                          statut: souscription.statut,
                          userRole: user?.role,
                          modifierVisible: (souscription.statut === 'ATTENTE_PAIEMENT' || souscription.statut === 'ATTENTE_LIVRAISON'),
                          payerVisible: souscription.statut === 'ATTENTE_PAIEMENT',
                          livrerVisible: user?.role === 'admin-generale' && souscription.statut === 'ATTENTE_LIVRAISON',
                          previewAttestationVisible: user?.role === 'admin-generale'
                        })}
                        {/* Bouton MODIFIER selon les nouvelles règles :
                            - ATTENTE_PAIEMENT : visible
                            - ATTENTE_LIVRAISON : visible  
                            - LIVRE : masqué */}
                        {(souscription.statut === 'ATTENTE_PAIEMENT' || souscription.statut === 'ATTENTE_LIVRAISON') && (
                          <button
                            onClick={() => handleModifier(souscription)}
                            className="inline-flex items-center px-2.5 py-1.5 border border-transparent text-xs font-medium rounded text-orange-700 bg-orange-100 hover:bg-orange-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500 transition-colors"
                          >
                            <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                            </svg>
                            Modifier
                          </button>
                        )}
                        {/* Bouton ACTION PAYER selon les règles clarifiées :
                            - ATTENTE_PAIEMENT : visible (pour effectuer le paiement)
                            - PAYE : masqué (déjà payé)
                            - LIVRE : masqué */}
                        {souscription.statut === 'ATTENTE_PAIEMENT' && (
                          <button
                            onClick={() => handlePayer(souscription)}
                            className="inline-flex items-center px-2.5 py-1.5 border border-transparent text-xs font-medium rounded text-green-700 bg-green-100 hover:bg-green-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-colors"
                          >
                            <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"></path>
                            </svg>
                            Payer
                          </button>
                        )}
                        {/* Bouton ACTION LIVRER selon les nouvelles règles :
                            - ATTENTE_PAIEMENT : masqué
                            - ATTENTE_LIVRAISON : visible UNIQUEMENT pour ADMIN-GENERALE
                            - LIVRE : masqué (déjà livré) */}
                        {user?.role === 'admin-generale' && souscription.statut === 'ATTENTE_LIVRAISON' && (
                          <button
                            onClick={() => handleLivrer(souscription)}
                            className="inline-flex items-center px-2.5 py-1.5 border border-transparent text-xs font-medium rounded text-purple-700 bg-purple-100 hover:bg-purple-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 transition-colors"
                          >
                            <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                            </svg>
                            Livrer
                          </button>
                        )}
                        <button
                          onClick={() => handleSendProforma(souscription)}
                          className="inline-flex items-center px-2.5 py-1.5 border border-transparent text-xs font-medium rounded text-indigo-700 bg-indigo-100 hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors"
                        >
                          <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207"></path>
                          </svg>
                          Envoyer Proforma
                        </button>
                        {/* Bouton Preview Attestation - EXCLUSIVEMENT pour ADMIN-GENERALE */}
                        {user?.role === 'admin-generale' && (
                          <button
                            onClick={() => handlePreviewAttestation(souscription)}
                            className="inline-flex items-center px-2.5 py-1.5 border border-transparent text-xs font-medium rounded text-purple-700 bg-purple-100 hover:bg-purple-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 transition-colors"
                          >
                            <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                            </svg>
                            Preview Attestation
                          </button>
                        )}
                        {/* Bouton Supprimer selon les règles :
                            - Attente paiement : visible pour tous
                            - Payé : visible pour tous
                            - Livré : visible pour tous */}
                        <button
                          onClick={() => handleDelete(souscription)}
                          className="inline-flex items-center px-2.5 py-1.5 border border-transparent text-xs font-medium rounded text-red-700 bg-red-100 hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-colors"
                        >
                          <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                          </svg>
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

      {/* Modal Envoi Email */}
      <ConfirmModal
        isOpen={showEmailModal}
        onClose={() => setShowEmailModal(false)}
        onConfirm={emailModalConfig.onConfirm}
        title={emailModalConfig.title}
        message={emailModalConfig.message}
        type={emailModalConfig.type}
        loading={emailLoading}
        confirmText={emailModalConfig.type === 'success' ? 'OK' : emailModalConfig.type === 'error' ? 'OK' : 'Envoyer'}
        cancelText="Annuler"
      />
    </>
  );
};

export default HistoriqueSection;