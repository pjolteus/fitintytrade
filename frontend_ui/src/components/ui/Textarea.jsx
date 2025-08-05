// src/components/ui/Textarea.jsx
import React from "react";

export const Textarea = React.forwardRef(({ className = "", ...props }, ref) => {
  return (
    <textarea
      ref={ref}
      rows={4}
      className={`w-full border border-gray-300 dark:border-gray-700 rounded-md px-3 py-2 text-sm placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary transition resize-none ${className}`}
      {...props}
    />
  );
});

Textarea.displayName = "Textarea";

