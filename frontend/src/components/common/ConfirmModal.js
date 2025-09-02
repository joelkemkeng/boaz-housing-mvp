import React from 'react';

const ConfirmModal = ({ 
  isOpen, 
  onClose, 
  onConfirm, 
  title = "Confirmation", 
  message = "Êtes-vous sûr de vouloir continuer ?",
  confirmText = "Confirmer",
  cancelText = "Annuler",
  type = "info", // info, success, warning, error
  loading = false
}) => {
  if (!isOpen) return null;

  const getTypeStyles = () => {
    switch (type) {
      case 'success':
        return {
          icon: '✅',
          bgColor: 'bg-green-50',
          borderColor: 'border-green-200',
          buttonColor: 'bg-green-600 hover:bg-green-700'
        };
      case 'warning':
        return {
          icon: '⚠️',
          bgColor: 'bg-yellow-50',
          borderColor: 'border-yellow-200',
          buttonColor: 'bg-yellow-600 hover:bg-yellow-700'
        };
      case 'error':
        return {
          icon: '❌',
          bgColor: 'bg-red-50',
          borderColor: 'border-red-200',
          buttonColor: 'bg-red-600 hover:bg-red-700'
        };
      default:
        return {
          icon: '📧',
          bgColor: 'bg-blue-50',
          borderColor: 'border-blue-200',
          buttonColor: 'bg-blue-600 hover:bg-blue-700'
        };
    }
  };

  const styles = getTypeStyles();

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Overlay */}
      <div 
        className="absolute inset-0 bg-black opacity-50"
        onClick={!loading ? onClose : undefined}
      ></div>
      
      {/* Modal */}
      <div className={`relative bg-white rounded-lg shadow-xl max-w-md w-full mx-4 ${styles.bgColor} ${styles.borderColor} border-2`}>
        {/* Header */}
        <div className="p-6 pb-4">
          <div className="flex items-center space-x-3">
            <span className="text-2xl">{styles.icon}</span>
            <h3 className="text-lg font-semibold text-gray-900">
              {title}
            </h3>
          </div>
        </div>
        
        {/* Content */}
        <div className="px-6 pb-4">
          <p className="text-gray-600">
            {message}
          </p>
        </div>
        
        {/* Actions */}
        <div className="px-6 py-4 bg-gray-50 rounded-b-lg flex justify-end space-x-3">
          <button
            onClick={onClose}
            disabled={loading}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {cancelText}
          </button>
          <button
            onClick={onConfirm}
            disabled={loading}
            className={`px-4 py-2 text-sm font-medium text-white rounded-md ${styles.buttonColor} disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2`}
          >
            {loading && (
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            )}
            <span>{loading ? 'Envoi en cours...' : confirmText}</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default ConfirmModal;