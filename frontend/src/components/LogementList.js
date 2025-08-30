import React, { useState, useEffect, useRef } from 'react';
import { logementService } from '../services/logementService';
import { handleError } from '../utils/errorHandler';
import Alert from './Alert';

const LogementList = ({ onEdit, onView, onDataChange, refreshTrigger, loadingEdit = false }) => {
  const [logements, setLogements] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    statut: '',
    ville: '',
    skip: 0,
    limit: 20
  });

  // État séparé pour l'input de ville (pour éviter la perte de focus)
  const [villeInput, setVilleInput] = useState('');
  
  // Pour le debounce de la recherche par ville
  const debounceTimeoutRef = useRef(null);

  const statutColors = {
    disponible: 'bg-green-100 text-green-800',
    occupe: 'bg-red-100 text-red-800',
    maintenance: 'bg-yellow-100 text-yellow-800'
  };

  const loadLogements = async () => {
    try {
      setLoading(true);
      const params = {};
      if (filters.statut) params.statut = filters.statut;
      if (filters.ville) params.ville = filters.ville;
      params.skip = filters.skip;
      params.limit = filters.limit;

      const data = await logementService.getLogements(params);
      setLogements(data);
      setError(null);
    } catch (err) {
      const errorMsg = 'Erreur lors du chargement des logements';
      setError(errorMsg);
      handleError(err, 'Chargement des logements', errorMsg);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadLogements();
  }, [filters]); // eslint-disable-line react-hooks/exhaustive-deps

  // Écouter les mises à jour externes (après création/modification/suppression)
  useEffect(() => {
    if (refreshTrigger > 0) {
      loadLogements();
    }
  }, [refreshTrigger]); // eslint-disable-line react-hooks/exhaustive-deps

  // Nettoyage du timeout au démontage du composant
  useEffect(() => {
    return () => {
      if (debounceTimeoutRef.current) {
        clearTimeout(debounceTimeoutRef.current);
      }
    };
  }, []);

  const handleFilterChange = (key, value) => {
    if (key === 'ville') {
      // Mise à jour immédiate de l'input seulement (garde le focus)
      setVilleInput(value);
      
      // Debounce pour mettre à jour le filtre et déclencher la recherche
      if (debounceTimeoutRef.current) {
        clearTimeout(debounceTimeoutRef.current);
      }
      
      debounceTimeoutRef.current = setTimeout(() => {
        setFilters(prev => ({ ...prev, ville: value, skip: 0 }));
      }, 300);
    } else {
      // Pour les autres filtres (statut), pas de debounce
      setFilters(prev => ({ ...prev, [key]: value, skip: 0 }));
    }
  };

  const handleVilleReset = () => {
    setVilleInput('');
    setFilters({ statut: '', ville: '', skip: 0, limit: 20 });
    if (debounceTimeoutRef.current) {
      clearTimeout(debounceTimeoutRef.current);
    }
  };


  const handleDelete = async (id) => {
    if (!window.confirm('Êtes-vous sûr de vouloir supprimer ce logement ?')) {
      return;
    }

    try {
      await logementService.deleteLogement(id);
      await loadLogements();
      // Notifier le parent que les données ont changé
      if (onDataChange) {
        onDataChange();
      }
    } catch (err) {
      const errorMsg = 'Erreur lors de la suppression';
      setError(errorMsg);
      handleError(err, 'Suppression logement', errorMsg);
    }
  };

  const handleChangeStatut = async (id, nouveauStatut) => {
    try {
      await logementService.changeStatutLogement(id, nouveauStatut);
      await loadLogements();
      // Notifier le parent que les données ont changé
      if (onDataChange) {
        onDataChange();
      }
    } catch (err) {
      const errorMsg = 'Erreur lors du changement de statut';
      setError(errorMsg);
      handleError(err, 'Changement statut', errorMsg);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Filtres */}
      <div className="bg-white p-4 rounded-lg shadow">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Filtrer par statut
            </label>
            <select
              value={filters.statut}
              onChange={(e) => handleFilterChange('statut', e.target.value)}
              className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Tous les statuts</option>
              <option value="disponible">Disponible</option>
              <option value="occupe">Occupé</option>
              <option value="maintenance">Maintenance</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Filtrer par ville
            </label>
            <input
              type="text"
              value={villeInput}
              onChange={(e) => handleFilterChange('ville', e.target.value)}
              placeholder="Rechercher une ville..."
              className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div className="flex items-end">
            <button
              onClick={handleVilleReset}
              className="px-4 py-2 text-sm text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50"
            >
              Réinitialiser
            </button>
          </div>
        </div>
      </div>

      {/* Message d'erreur */}
      {error && (
        <Alert
          type="error"
          message={error}
          onClose={() => setError(null)}
        />
      )}

      {/* Liste des logements */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        {logements.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-500">Aucun logement trouvé</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Logement
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Localisation
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Prix total
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
                {logements.map((logement) => (
                  <tr key={logement.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div>
                        <div className="text-sm font-medium text-gray-900">
                          {logement.titre}
                        </div>
                        <div className="text-sm text-gray-500">
                          {logement.adresse}
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div>
                        <div className="text-sm text-gray-900">{logement.ville}</div>
                        <div className="text-xs text-gray-500">{logement.code_postal}, {logement.pays}</div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      <div>
                        <div className="font-semibold">{logement.montant_total}€</div>
                        <div className="text-xs text-gray-500">
                          Loyer: {logement.loyer}€{logement.montant_charges > 0 ? ` + Charges: ${logement.montant_charges}€` : ''}
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${statutColors[logement.statut]}`}>
                        {logement.statut}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                      <button
                        onClick={() => onView(logement)}
                        className="text-blue-600 hover:text-blue-900"
                      >
                        Voir
                      </button>
                      <button
                        onClick={() => onEdit(logement)}
                        disabled={loadingEdit}
                        className="text-indigo-600 hover:text-indigo-900 disabled:text-gray-400 disabled:cursor-not-allowed"
                      >
                        {loadingEdit ? 'Chargement...' : 'Modifier'}
                      </button>
                      <select
                        value={logement.statut}
                        onChange={(e) => handleChangeStatut(logement.id, e.target.value)}
                        className="text-sm border border-gray-300 rounded px-2 py-1"
                      >
                        <option value="disponible">Disponible</option>
                        <option value="occupe">Occupé</option>
                        <option value="maintenance">Maintenance</option>
                      </select>
                      <button
                        onClick={() => handleDelete(logement.id)}
                        className="text-red-600 hover:text-red-900"
                      >
                        Supprimer
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Pagination */}
      <div className="flex justify-between items-center">
        <button
          onClick={() => handleFilterChange('skip', Math.max(0, filters.skip - filters.limit))}
          disabled={filters.skip === 0}
          className="px-4 py-2 text-sm bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Précédent
        </button>
        <span className="text-sm text-gray-500">
          Affichage de {filters.skip + 1} à {filters.skip + logements.length}
        </span>
        <button
          onClick={() => handleFilterChange('skip', filters.skip + filters.limit)}
          disabled={logements.length < filters.limit}
          className="px-4 py-2 text-sm bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Suivant
        </button>
      </div>
    </div>
  );
};

export default LogementList;