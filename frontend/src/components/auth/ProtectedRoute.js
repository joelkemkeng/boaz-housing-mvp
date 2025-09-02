import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

const ProtectedRoute = ({ children, requiredRole = null, redirectTo = '/login' }) => {
  const { isAuthenticated, user, loading } = useAuth();

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

  if (!isAuthenticated) {
    return <Navigate to={redirectTo} replace />;
  }

  if (requiredRole && user.role !== requiredRole) {
    const userRedirectUrl = user.role === 'agent-boaz' ? '/agent-dashboard' :
                           user.role === 'bailleur' ? '/bailleur-dashboard' :
                           user.role === 'admin-generale' ? '/admin-dashboard' :
                           user.role === 'client' ? '/client-dashboard' : '/';
    return <Navigate to={userRedirectUrl} replace />;
  }

  return children;
};

export default ProtectedRoute;