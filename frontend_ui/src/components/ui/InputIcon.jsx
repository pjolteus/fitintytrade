// src/components/ui/InputIcon.jsx
import React from "react";

export const InputIcon = ({ icon, className = "", ...props }) => {
  return (
    <div className={`relative ${className}`}>
      <span className="absolute inset-y-0 left-0 flex items-center pl-3 text-gray-400">
        {icon}
      </span>
      <input
        className="w-full pl-10 pr-3 py-2 border border-gray-300 dark:border-gray-700 rounded-md text-sm placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary transition bg-white dark:bg-gray-900"
        {...props}
      />
    </div>
  );
};

