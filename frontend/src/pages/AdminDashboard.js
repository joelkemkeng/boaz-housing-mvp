import React, { useState } from 'react';
import ServicesSection from '../components/admin/ServicesSection';
import HistoriqueSection from '../components/admin/HistoriqueSection';

const AdminDashboard = () => {
  const [refreshKey, setRefreshKey] = useState(0);

  const handleDataChange = () => {
    setRefreshKey(prev => prev + 1);
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Boaz-Housing Admin</h1>
              <p className="text-gray-600 mt-2">Gestion des souscriptions et services</p>
            </div>
          </div>
        </div>

        {/* Section Services */}
        <ServicesSection onDataChange={handleDataChange} />

        {/* Section Historique */}
        <HistoriqueSection key={refreshKey} onDataChange={handleDataChange} />
      </div>
    </div>
  );
};

export default AdminDashboard;