import React, { useState, useEffect } from 'react';
import { logementService } from '../services/logementService';

const LogementForm = ({ logement, onSave, onCancel, isEdit = false }) => {
  const [formData, setFormData] = useState({
    titre: '',
    description: '',
    adresse: '',
    ville: '',
    code_postal: '',
    pays: 'France',
    loyer: '',
    montant_charges: '',
    statut: 'disponible'
  });
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (logement && isEdit) {
      setFormData({
        titre: logement.titre || '',
        description: logement.description || '',
        adresse: logement.adresse || '',
        ville: logement.ville || '',
        code_postal: logement.code_postal || '',
        pays: logement.pays || 'France',
        loyer: logement.loyer || '',
        montant_charges: logement.montant_charges || '',
        statut: logement.statut || 'disponible'
      });
    }
  }, [logement, isEdit]);

  const validateForm = () => {
    const newErrors = {};

    if (!formData.titre.trim()) {
      newErrors.titre = 'Le titre est requis';
    }

    if (!formData.adresse.trim()) {
      newErrors.adresse = 'L\'adresse est requise';
    }

    if (!formData.ville.trim()) {
      newErrors.ville = 'La ville est requise';
    }

    if (!formData.code_postal.trim()) {
      newErrors.code_postal = 'Le code postal est requis';
    } else if (!/^\d{5}$/.test(formData.code_postal)) {
      newErrors.code_postal = 'Le code postal doit contenir 5 chiffres';
    }

    if (!formData.pays.trim()) {
      newErrors.pays = 'Le pays est requis';
    }

    if (!formData.loyer || formData.loyer <= 0) {
      newErrors.loyer = 'Le loyer doit être supérieur à 0';
    }

    if (formData.montant_charges && formData.montant_charges < 0) {
      newErrors.montant_charges = 'Le montant des charges ne peut pas être négatif';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    
    // Nettoyer l'erreur du champ modifié
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setLoading(true);
    try {
      const dataToSend = {
        ...formData,
        loyer: parseFloat(formData.loyer),
        montant_charges: formData.montant_charges ? parseFloat(formData.montant_charges) : 0.0
      };

      let result;
      if (isEdit && logement) {
        result = await logementService.updateLogement(logement.id, dataToSend);
      } else {
        result = await logementService.createLogement(dataToSend);
      }

      onSave(result);
    } catch (err) {
      console.error('Erreur sauvegarde logement:', err);
      if (err.response?.data?.detail) {
        setErrors({ submit: err.response.data.detail });
      } else {
        setErrors({ submit: 'Erreur lors de la sauvegarde' });
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div className="relative top-20 mx-auto p-5 border w-full max-w-md shadow-lg rounded-md bg-white">
        <div className="mt-3">
          <h3 className="text-lg font-medium text-gray-900 mb-4">
            {isEdit ? 'Modifier le logement' : 'Nouveau logement'}
          </h3>
          
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Titre */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Titre *
              </label>
              <input
                type="text"
                name="titre"
                value={formData.titre}
                onChange={handleChange}
                className={`w-full border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                  errors.titre ? 'border-red-500' : 'border-gray-300'
                }`}
                placeholder="Appartement moderne centre-ville"
                maxLength={200}
              />
              {errors.titre && (
                <p className="text-red-500 text-xs mt-1">{errors.titre}</p>
              )}
            </div>

            {/* Description */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Description
              </label>
              <textarea
                name="description"
                value={formData.description}
                onChange={handleChange}
                className={`w-full border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                  errors.description ? 'border-red-500' : 'border-gray-300'
                }`}
                placeholder="Description détaillée du logement..."
                rows={3}
                maxLength={2000}
              />
              {errors.description && (
                <p className="text-red-500 text-xs mt-1">{errors.description}</p>
              )}
            </div>

            {/* Adresse */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Adresse *
              </label>
              <input
                type="text"
                name="adresse"
                value={formData.adresse}
                onChange={handleChange}
                className={`w-full border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                  errors.adresse ? 'border-red-500' : 'border-gray-300'
                }`}
                placeholder="123 Rue de la Paix"
              />
              {errors.adresse && (
                <p className="text-red-500 text-xs mt-1">{errors.adresse}</p>
              )}
            </div>

            {/* Ville */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Ville *
              </label>
              <input
                type="text"
                name="ville"
                value={formData.ville}
                onChange={handleChange}
                className={`w-full border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                  errors.ville ? 'border-red-500' : 'border-gray-300'
                }`}
                placeholder="Paris"
              />
              {errors.ville && (
                <p className="text-red-500 text-xs mt-1">{errors.ville}</p>
              )}
            </div>

            {/* Code postal */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Code postal *
              </label>
              <input
                type="text"
                name="code_postal"
                value={formData.code_postal}
                onChange={handleChange}
                className={`w-full border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                  errors.code_postal ? 'border-red-500' : 'border-gray-300'
                }`}
                placeholder="75001"
                maxLength={5}
              />
              {errors.code_postal && (
                <p className="text-red-500 text-xs mt-1">{errors.code_postal}</p>
              )}
            </div>

            {/* Pays */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Pays *
              </label>
              <input
                type="text"
                name="pays"
                value={formData.pays}
                onChange={handleChange}
                className={`w-full border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                  errors.pays ? 'border-red-500' : 'border-gray-300'
                }`}
                placeholder="France"
              />
              {errors.pays && (
                <p className="text-red-500 text-xs mt-1">{errors.pays}</p>
              )}
            </div>

            {/* Loyer */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Loyer mensuel (€) *
              </label>
              <input
                type="number"
                name="loyer"
                value={formData.loyer}
                onChange={handleChange}
                min="0"
                step="0.01"
                className={`w-full border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                  errors.loyer ? 'border-red-500' : 'border-gray-300'
                }`}
                placeholder="450.00"
              />
              {errors.loyer && (
                <p className="text-red-500 text-xs mt-1">{errors.loyer}</p>
              )}
            </div>

            {/* Montant des charges */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Montant des charges (€)
              </label>
              <input
                type="number"
                name="montant_charges"
                value={formData.montant_charges}
                onChange={handleChange}
                min="0"
                step="0.01"
                className={`w-full border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                  errors.montant_charges ? 'border-red-500' : 'border-gray-300'
                }`}
                placeholder="50.00"
              />
              {errors.montant_charges && (
                <p className="text-red-500 text-xs mt-1">{errors.montant_charges}</p>
              )}
            </div>

            {/* Statut */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Statut
              </label>
              <select
                name="statut"
                value={formData.statut}
                onChange={handleChange}
                className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="disponible">Disponible</option>
                <option value="occupe">Occupé</option>
                <option value="maintenance">Maintenance</option>
              </select>
            </div>

            {/* Erreur générale */}
            {errors.submit && (
              <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
                {errors.submit}
              </div>
            )}

            {/* Boutons */}
            <div className="flex space-x-3 pt-4">
              <button
                type="button"
                onClick={onCancel}
                className="flex-1 px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 border border-gray-300 rounded-md hover:bg-gray-200"
                disabled={loading}
              >
                Annuler
              </button>
              <button
                type="submit"
                className="flex-1 px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                disabled={loading}
              >
                {loading ? 'Sauvegarde...' : (isEdit ? 'Modifier' : 'Créer')}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default LogementForm;