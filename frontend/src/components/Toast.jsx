import React, { useEffect } from 'react';
import './Toast.css';

const Toast = ({ message, type, status, onClose }) => {
  useEffect(() => {
    if (type === 'success') {
      const timer = setTimeout(() => {
        onClose();
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [type, onClose]);

  const getStatusIcon = () => {
    switch (type) {
      case 'loading':
        return <div className="toast-spinner" />;
      case 'success':
        return <span className="toast-icon">✓</span>;
      case 'error':
        return <span className="toast-icon">✕</span>;
      default:
        return null;
    }
  };

  const getStatusText = () => {
    if (status === 'pending') return 'Queued...';
    if (status === 'processing') return 'Processing document...';
    return message;
  };

  return (
    <div className={`toast toast-${type}`}>
      {getStatusIcon()}
      <span className="toast-message">{getStatusText()}</span>
      {type !== 'loading' && (
        <button className="toast-close" onClick={onClose}>
          ×
        </button>
      )}
    </div>
  );
};

export default Toast;
