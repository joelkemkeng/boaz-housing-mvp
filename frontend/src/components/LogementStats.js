import React, { useState, useEffect } from 'react';
import { logementService } from '../services/logementService';

const LogementStats = () => {
  const [stats, setStats] = useState({
    total: 0,
    disponibles: 0,
    occupes: 0,
    maintenance: 0
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadStats = async () => {
    try {
      setLoading(true);
      const data = await logementService.getStatsLogements();
      setStats(data);
      setError(null);
    } catch (err) {
      setError('Erreur lors du chargement des statistiques');
      console.error('Erreur stats:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadStats();
    
    // Actualiser les stats toutes les 30 secondes
    const interval = setInterval(loadStats, 30000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        {[1, 2, 3, 4].map(i => (
          <div key={i} className="bg-white p-6 rounded-lg shadow animate-pulse">
            <div className="h-4 bg-gray-200 rounded mb-2"></div>
            <div className="h-8 bg-gray-200 rounded"></div>
          </div>
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div className="mb-6">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      </div>
    );
  }

  const statCards = [
    {
      title: 'Total logements',
      value: stats.total,
      color: 'bg-blue-500',
      icon: '🏠'
    },
    {
      title: 'Disponibles',
      value: stats.disponibles,
      color: 'bg-green-500',
      icon: '✅',
      percentage: stats.total > 0 ? Math.round((stats.disponibles / stats.total) * 100) : 0
    },
    {
      title: 'Occupés',
      value: stats.occupes,
      color: 'bg-red-500',
      icon: '🏘️',
      percentage: stats.total > 0 ? Math.round((stats.occupes / stats.total) * 100) : 0
    },
    {
      title: 'En maintenance',
      value: stats.maintenance,
      color: 'bg-yellow-500',
      icon: '🔧',
      percentage: stats.total > 0 ? Math.round((stats.maintenance / stats.total) * 100) : 0
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
      {statCards.map((stat, index) => (
        <div key={index} className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center">
            <div className={`${stat.color} text-white rounded-full w-12 h-12 flex items-center justify-center text-xl mr-4`}>
              {stat.icon}
            </div>
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-600">{stat.title}</p>
              <div className="flex items-baseline">
                <p className="text-2xl font-semibold text-gray-900">{stat.value}</p>
                {stat.percentage !== undefined && (
                  <p className="ml-2 text-sm text-gray-500">({stat.percentage}%)</p>
                )}
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default LogementStats;