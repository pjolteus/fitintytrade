// src/components/ui/InputWithDropdown.jsx
import React from "react";

export const InputWithDropdown = ({ options = [], onSelect, ...props }) => {
  return (
    <div className="relative">
      <input
        className="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-primary"
        {...props}
      />
      {options.length > 0 && (
        <ul className="absolute z-10 mt-1 w-full bg-white dark:bg-gray-900 border border-gray-300 dark:border-gray-700 rounded-md shadow-md max-h-48 overflow-auto">
          {options.map((option, idx) => (
            <li
              key={idx}
              className="px-3 py-2 hover:bg-gray-100 dark:hover:bg-gray-800 cursor-pointer"
              onClick={() => onSelect(option)}
            >
              {option}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};



