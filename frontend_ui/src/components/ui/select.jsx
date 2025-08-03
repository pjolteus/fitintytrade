// src/components/ui/select.jsx
import React from "react";

export const Select = ({ options, value, onChange, className = "", ...props }) => {
  return (
    <select
      className={`border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-600 ${className}`}
      value={value}
      onChange={onChange}
      {...props}
    >
      {options.map((opt) => (
        <option key={opt.value} value={opt.value}>
          {opt.label}
        </option>
      ))}
    </select>
  );
};
