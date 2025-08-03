// src/components/ui/button.jsx
import React from "react";

export const Button = ({ children, className = "", ...props }) => {
  return (
    <button
      className={`bg-purple-700 text-white px-4 py-2 rounded hover:bg-purple-800 transition duration-200 ${className}`}
      {...props}
    >
      {children}
    </button>
  );
};
