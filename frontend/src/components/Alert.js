import React from 'react';

const Alert = ({ type = 'error', title, message, onClose, show = true }) => {
  if (!show || !message) return null;

  const styles = {
    error: 'bg-red-100 border-red-400 text-red-700',
    success: 'bg-green-100 border-green-400 text-green-700',
    warning: 'bg-yellow-100 border-yellow-400 text-yellow-700',
    info: 'bg-blue-100 border-blue-400 text-blue-700'
  };

  const icons = {
    error: '❌',
    success: '✅',
    warning: '⚠️',
    info: 'ℹ️'
  };

  return (
    <div className={`border px-4 py-3 rounded mb-4 relative ${styles[type]}`}>
      {onClose && (
        <button
          onClick={onClose}
          className="absolute top-0 right-0 px-4 py-3 text-xl leading-none cursor-pointer hover:bg-black hover:bg-opacity-10 rounded"
          aria-label="Fermer"
        >
          ×
        </button>
      )}
      
      <div className="flex items-start">
        <div className="mr-2 text-lg">
          {icons[type]}
        </div>
        <div className="flex-1">
          {title && (
            <div className="font-bold mb-1">
              {title}
            </div>
          )}
          <div style={{ whiteSpace: 'pre-line' }}>
            {message}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Alert;