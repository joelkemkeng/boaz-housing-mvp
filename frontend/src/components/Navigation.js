import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Navigation = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const getNavItems = () => {
    if (!user) return [];
    
    switch (user.role) {
      case 'admin-generale':
        return [
          { path: '/admin-dashboard', label: 'Souscriptions', icon: '👥' },
          { path: '/logements', label: 'Logements', icon: '🏠' }
        ];
      case 'agent-boaz':
        return [
          { path: '/agent-dashboard', label: 'Dashboard Agent', icon: '👨‍💼' },
          { path: '/logements', label: 'Logements', icon: '🏠' }
        ];
      case 'bailleur':
        return [
          { path: '/bailleur-dashboard', label: 'Dashboard Bailleur', icon: '🏢' },
          { path: '/logements', label: 'Mes Logements', icon: '🏠' }
        ];
      case 'client':
        return [
          { path: '/client-dashboard', label: 'Mon Compte', icon: '👤' },
          { path: '/logements', label: 'Rechercher', icon: '🔍' }
        ];
      default:
        return [];
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navItems = getNavItems();

  return (
    <nav className="bg-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between items-center py-4">
          <div className="flex items-center space-x-2">
            <div className="text-xl font-bold text-blue-600">Boaz-Housing</div>
            <div className="text-sm text-gray-500">MVP</div>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="flex space-x-1">
              {navItems.map(({ path, label, icon }) => (
                <Link
                  key={path}
                  to={path}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-200 ${
                    location.pathname === path
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                  }`}
                >
                  <span className="mr-2">{icon}</span>
                  {label}
                </Link>
              ))}
            </div>
            
            {user && (
              <div className="flex items-center space-x-3 border-l pl-4">
                <span className="text-sm text-gray-600">
                  {user.prenom} {user.nom}
                </span>
                <span className="text-xs bg-gray-100 px-2 py-1 rounded">
                  {user.role === 'admin-generale' ? 'Admin' :
                   user.role === 'agent-boaz' ? 'Agent' :
                   user.role === 'bailleur' ? 'Bailleur' : 'Client'}
                </span>
                <button
                  onClick={handleLogout}
                  className="text-sm text-red-600 hover:text-red-800 font-medium"
                >
                  Déconnexion
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;