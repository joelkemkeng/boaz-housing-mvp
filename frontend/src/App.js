import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LogementsPage from './pages/LogementsPage';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Navigate to="/logements" replace />} />
          <Route path="/logements" element={<LogementsPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
