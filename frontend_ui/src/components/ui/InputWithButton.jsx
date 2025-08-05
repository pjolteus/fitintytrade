// src/components/ui/InputWithButton.jsx
import React from "react";

export const InputWithButton = ({ placeholder, buttonLabel, onButtonClick, className = "", ...props }) => {
  return (
    <div className={`flex rounded-md shadow-sm ${className}`}>
      <input
        type="text"
        placeholder={placeholder}
        className="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-l-md text-sm focus:outline-none focus:ring-2 focus:ring-primary"
        {...props}
      />
      <button
        type="button"
        onClick={onButtonClick}
        className="px-4 py-2 bg-primary text-white rounded-r-md hover:bg-primary-dark transition"
      >
        {buttonLabel}
      </button>
    </div>
  );
};


