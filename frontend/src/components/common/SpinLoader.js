import React from 'react';

const SpinLoader = ({ size = 'md', text = '', className = '' }) => {
  const sizeClasses = {
    sm: 'h-6 w-6',
    md: 'h-8 w-8', 
    lg: 'h-12 w-12',
    xl: 'h-16 w-16'
  };
  
  const textSizeClasses = {
    sm: 'text-sm',
    md: 'text-base',
    lg: 'text-lg', 
    xl: 'text-xl'
  };
  
  return (
    <div className={`flex flex-col items-center justify-center space-y-3 ${className}`}>
      <div className={`animate-spin rounded-full border-2 border-gray-200 border-t-blue-600 ${sizeClasses[size]}`}></div>
      {text && (
        <p className={`text-gray-600 ${textSizeClasses[size]} animate-pulse`}>
          {text}
        </p>
      )}
    </div>
  );
};

export default SpinLoader;