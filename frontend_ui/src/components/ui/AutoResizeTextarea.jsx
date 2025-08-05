// src/components/ui/AutoResizeTextarea.jsx
import React, { useEffect, useRef } from "react";

export const AutoResizeTextarea = ({ className = "", ...props }) => {
  const textareaRef = useRef(null);

  useEffect(() => {
    const el = textareaRef.current;
    if (el) {
      const resize = () => {
        el.style.height = "auto";
        el.style.height = el.scrollHeight + "px";
      };
      resize();
      el.addEventListener("input", resize);
      return () => el.removeEventListener("input", resize);
    }
  }, []);

  return (
    <textarea
      ref={textareaRef}
      className={`w-full border border-gray-300 dark:border-gray-700 rounded-md px-3 py-2 text-sm placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary transition resize-none overflow-hidden ${className}`}
      rows={1}
      {...props}
    />
  );
};




