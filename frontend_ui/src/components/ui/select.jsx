import React, { useState, useRef, useEffect } from "react";

// Select root component
export const Select = ({
  children,
  value,
  onChange,
  defaultValue,
  className = "",
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [selected, setSelected] = useState(defaultValue || "");
  const selectRef = useRef(null);
  const itemRefs = useRef([]);
  const [focusedIndex, setFocusedIndex] = useState(-1);

  const isControlled = value !== undefined && onChange !== undefined;
  const currentValue = isControlled ? value : selected;

  const toggle = () => setIsOpen((prev) => !prev);
  const close = () => setIsOpen(false);

  const handleSelect = (newValue) => {
    if (isControlled) {
      onChange(newValue);
    } else {
      setSelected(newValue);
    }
    close();
  };

  const handleKeyDown = (e) => {
    if (!isOpen) return;
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setFocusedIndex((i) => Math.min(i + 1, itemRefs.current.length - 1));
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setFocusedIndex((i) => Math.max(i - 1, 0));
    } else if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      const ref = itemRefs.current[focusedIndex];
      if (ref) ref.click();
    } else if (e.key === "Escape") {
      close();
    }
  };

  // Close dropdown on outside click
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (selectRef.current && !selectRef.current.contains(event.target)) {
        close();
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div
      ref={selectRef}
      className={`relative inline-block w-full ${className}`}
      tabIndex={0}
      onKeyDown={handleKeyDown}
    >
      {React.Children.map(children, (child) =>
        React.cloneElement(child, {
          isOpen,
          toggle,
          close,
          value: currentValue,
          onSelect: handleSelect,
          focusedIndex,
          setFocusedIndex,
          itemRefs,
        })
      )}
    </div>
  );
};

// Button to trigger the dropdown
export const SelectTrigger = ({ children, toggle, className = "" }) => (
  <button
    onClick={toggle}
    className={`border p-2 rounded w-full text-left bg-white focus:outline-none focus:ring ${className}`}
    aria-haspopup="listbox"
  >
    {children}
  </button>
);

// Display current value
export const SelectValue = ({ value }) => (
  <span className="mx-2">{value || "Select an option"}</span>
);

// Dropdown content
export const SelectContent = ({ children, isOpen }) =>
  isOpen ? (
    <div
      className="absolute z-10 mt-1 w-full border rounded bg-white shadow animate-fade-in"
      role="listbox"
    >
      {children}
    </div>
  ) : null;

// Selectable item
export const SelectItem = ({
  children,
  onClick,
  onSelect,
  close,
  index,
  focusedIndex,
  itemRefs,
}) => {
  const ref = useRef(null);

  useEffect(() => {
    if (focusedIndex === index && ref.current) {
      ref.current.focus();
    }
  }, [focusedIndex, index]);

  useEffect(() => {
    itemRefs.current[index] = ref.current;
  }, [index]);

  const handleClick = () => {
    onSelect(children);
    if (onClick) onClick();
  };

  return (
    <div
      ref={ref}
      role="option"
      tabIndex={-1}
      className={`p-2 cursor-pointer hover:bg-gray-100 ${
        focusedIndex === index ? "bg-gray-100" : ""
      }`}
      onClick={handleClick}
    >
      {children}
    </div>
  );
};
