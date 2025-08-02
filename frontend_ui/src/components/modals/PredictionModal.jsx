import React, { useEffect } from 'react';

function PredictionModal({ prediction, onClose, onConfirm, showConfirm = false, variant = 'danger' }) {
  if (!prediction) return null;

  useEffect(() => {
    const escListener = (e) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', escListener);
    return () => window.removeEventListener('keydown', escListener);
  }, [onClose]);

  const buttonBase = "px-4 py-1 rounded text-sm transition duration-150";
  const variants = {
    default: "bg-gray-500 hover:bg-gray-600 text-white",
    danger: "bg-red-600 hover:bg-red-700 text-white",
    primary: "bg-blue-600 hover:bg-blue-700 text-white",
  };

  const closeBtnClass = `${buttonBase} ${variants[variant]}`;

  return (
    <div
      className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50"
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
    >
      <div className="bg-white dark:bg-gray-900 p-6 rounded shadow-lg max-w-md w-full">
        <h3 id="modal-title" className="text-xl font-bold text-purple-800 dark:text-purple-200 mb-2">
          Prediction Details
        </h3>
        <div className="space-y-2 text-sm text-gray-800 dark:text-white">
          <p><strong>Ticker:</strong> {prediction.ticker}</p>
          <p><strong>Prediction:</strong> {prediction.prediction === 1 ? 'Bullish (Call)' : 'Bearish (Put)'}</p>
          <p><strong>Confidence:</strong> {(prediction.confidence * 100).toFixed(2)}%</p>
          <p><strong>Model:</strong> {prediction.model_name}</p>
          <p><strong>Timestamp:</strong> {new Date(prediction.timestamp).toLocaleString()}</p>
        </div>

        <div className="mt-4 text-right space-x-2">
          {showConfirm && (
            <button
              onClick={onConfirm}
              className={`${buttonBase} ${variants.primary}`}
            >
              Confirm
            </button>
          )}
          <button onClick={onClose} className={closeBtnClass}>
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

export default PredictionModal;
