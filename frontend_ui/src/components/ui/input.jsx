// src/components/ui/input.jsx
import React from "react";

// Reusable input field component with consistent styling
export const Input = React.forwardRef(
  ({ type = "text", className = "", ...props }, ref) => {
    return (
      <input
        ref={ref}
        type={type}
        className={`w-full border border-gray-300 dark:border-gray-700 rounded-md px-3 py-2 text-sm placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition ${className}`}
        {...props}
      />
    );
  }
);

Input.displayName = "Input";

