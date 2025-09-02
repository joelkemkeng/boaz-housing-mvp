import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import LoginForm from './components/auth/LoginForm';
import ProtectedRoute from './components/auth/ProtectedRoute';
import LogementsPage from './pages/LogementsPage';
import AdminDashboard from './pages/AdminDashboard';
import Navigation from './components/Navigation';
import './App.css';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <Routes>
            <Route path="/login" element={<LoginForm />} />
            <Route 
              path="/" 
              element={
                <ProtectedRoute>
                  <div>
                    <Navigation />
                    <Navigate to="/admin-dashboard" replace />
                  </div>
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/logements" 
              element={
                <ProtectedRoute>
                  <div>
                    <Navigation />
                    <LogementsPage />
                  </div>
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/admin" 
              element={<Navigate to="/admin-dashboard" replace />} 
            />
            <Route 
              path="/admin-dashboard" 
              element={
                <ProtectedRoute requiredRole="admin-generale">
                  <div>
                    <Navigation />
                    <AdminDashboard />
                  </div>
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/agent-dashboard" 
              element={
                <ProtectedRoute requiredRole="agent-boaz">
                  <div>
                    <Navigation />
                    <div className="p-8">
                      <h1 className="text-2xl font-bold mb-4">Dashboard Agent Boaz</h1>
                      <p>Interface réservée aux agents Boaz</p>
                    </div>
                  </div>
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/bailleur-dashboard" 
              element={
                <ProtectedRoute requiredRole="bailleur">
                  <div>
                    <Navigation />
                    <div className="p-8">
                      <h1 className="text-2xl font-bold mb-4">Dashboard Bailleur</h1>
                      <p>Interface réservée aux bailleurs</p>
                    </div>
                  </div>
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/client-dashboard" 
              element={
                <ProtectedRoute requiredRole="client">
                  <div>
                    <Navigation />
                    <div className="p-8">
                      <h1 className="text-2xl font-bold mb-4">Dashboard Client</h1>
                      <p>Interface réservée aux clients</p>
                    </div>
                  </div>
                </ProtectedRoute>
              } 
            />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
