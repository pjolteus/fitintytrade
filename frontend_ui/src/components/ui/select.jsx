// src/components/ui/select.jsx
import React from "react";

export const SelectTrigger = ({ children, className = "" }) => (
  <button className={`border p-2 rounded ${className}`}>{children}</button>
);

export const SelectValue = ({ value }) => (
  <span className="mx-2">{value}</span>
);

export const SelectContent = ({ children }) => (
  <div className="border rounded mt-1">{children}</div>
);

export const SelectItem = ({ children, onClick }) => (
  <div className="p-2 hover:bg-gray-100 cursor-pointer" onClick={onClick}>
    {children}
  </div>
);
