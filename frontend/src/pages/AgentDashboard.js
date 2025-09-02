import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import SouscriptionForm from '../components/agent/SouscriptionForm';
import PaymentUpload from '../components/agent/PaymentUpload';
import SouscriptionStats from '../components/agent/SouscriptionStats';
import api from '../services/api';

const AgentDashboard = () => {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState('souscriptions');
  const [souscriptions, setSouscriptions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSouscriptions();
  }, []);

  const fetchSouscriptions = async () => {
    try {
      const response = await api.get('/souscriptions');
      setSouscriptions(response.data);
    } catch (error) {
      console.error('Erreur lors du chargement des souscriptions:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSouscriptionCreated = () => {
    fetchSouscriptions();
    setActiveTab('souscriptions');
  };

  const tabs = [
    { id: 'souscriptions', label: 'Souscriptions', icon: '📋' },
    { id: 'new', label: 'Nouvelle Souscription', icon: '➕' },
    { id: 'payment', label: 'Paiements', icon: '💳' },
    { id: 'stats', label: 'Statistiques', icon: '📊' }
  ];

  const getStatutColor = (statut) => {
    const colors = {
      'BROUILLON': 'bg-gray-100 text-gray-800',
      'EN_ATTENTE': 'bg-yellow-100 text-yellow-800',
      'ATTENTE_PAIEMENT': 'bg-orange-100 text-orange-800',
      'ATTENTE_LIVRAISON': 'bg-blue-100 text-blue-800',
      'LIVRE': 'bg-green-100 text-green-800',
      'CLOTURE': 'bg-gray-100 text-gray-600'
    };
    return colors[statut] || 'bg-gray-100 text-gray-800';
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-2 text-gray-600">Chargement...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Dashboard Agent Boaz
          </h1>
          <p className="mt-2 text-gray-600">
            Bienvenue {user?.prenom} {user?.nom}
          </p>
        </div>

        {/* Navigation Tabs */}
        <div className="bg-white rounded-lg shadow mb-6">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8 px-6">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`py-4 px-1 border-b-2 font-medium text-sm whitespace-nowrap ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <span className="mr-2">{tab.icon}</span>
                  {tab.label}
                </button>
              ))}
            </nav>
          </div>
        </div>

        {/* Tab Content */}
        <div className="bg-white rounded-lg shadow">
          {activeTab === 'souscriptions' && (
            <div className="p-6">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-xl font-semibold">Liste des Souscriptions</h2>
                <button
                  onClick={() => setActiveTab('new')}
                  className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
                >
                  + Nouvelle Souscription
                </button>
              </div>
              
              {souscriptions.length === 0 ? (
                <div className="text-center py-8">
                  <p className="text-gray-500">Aucune souscription trouvée</p>
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          ID
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Client
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Service
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Statut
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Montant
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Date
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {souscriptions.map((souscription) => (
                        <tr key={souscription.id} className="hover:bg-gray-50">
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                            #{souscription.id}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            {souscription.nom_client} {souscription.prenom_client}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            {souscription.service_nom}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatutColor(souscription.statut)}`}>
                              {souscription.statut}
                            </span>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            {souscription.montant_total}€
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {new Date(souscription.created_at).toLocaleDateString('fr-FR')}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          )}

          {activeTab === 'new' && (
            <div className="p-6">
              <h2 className="text-xl font-semibold mb-6">Nouvelle Souscription</h2>
              <SouscriptionForm onSouscriptionCreated={handleSouscriptionCreated} />
            </div>
          )}

          {activeTab === 'payment' && (
            <div className="p-6">
              <h2 className="text-xl font-semibold mb-6">Gestion des Paiements</h2>
              <PaymentUpload souscriptions={souscriptions} onPaymentProcessed={fetchSouscriptions} />
            </div>
          )}

          {activeTab === 'stats' && (
            <div className="p-6">
              <h2 className="text-xl font-semibold mb-6">Statistiques</h2>
              <SouscriptionStats souscriptions={souscriptions} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AgentDashboard;