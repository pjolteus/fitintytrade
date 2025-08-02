import React from 'react';

type PaginationProps = {
  page: number;
  totalPages: number;
  onPageChange: (newPage: number) => void;
  variant?: 'default' | 'primary' | 'danger' | 'success';
};

const Pagination: React.FC<PaginationProps> = ({
  page,
  totalPages,
  onPageChange,
  variant = 'default',
}) => {
  const baseClasses = "px-3 py-1 rounded text-sm transition duration-150";
  const variantClasses: Record<string, string> = {
    default: "bg-gray-300 dark:bg-gray-600 text-gray-900 dark:text-white",
    primary: "bg-blue-600 hover:bg-blue-700 text-white",
    danger: "bg-red-600 hover:bg-red-700 text-white",
    success: "bg-green-600 hover:bg-green-700 text-white",
  };

  const buttonClass = `${baseClasses} ${variantClasses[variant]} disabled:opacity-50`;

  const pageNumbers = Array.from({ length: totalPages }, (_, i) => i + 1);

  return (
    <div className="flex flex-wrap items-center justify-center gap-2 mt-4">
      <button
        disabled={page === 1}
        onClick={() => onPageChange(1)}
        className={buttonClass}
      >
        First
      </button>
      <button
        disabled={page === 1}
        onClick={() => onPageChange(page - 1)}
        className={buttonClass}
      >
        Previous
      </button>

      {pageNumbers.map((num) => (
        <button
          key={num}
          onClick={() => onPageChange(num)}
          className={`${buttonClass} ${
            num === page
              ? 'ring-2 ring-offset-1 ring-purple-500 font-bold'
              : ''
          }`}
        >
          {num}
        </button>
      ))}

      <button
        disabled={page === totalPages}
        onClick={() => onPageChange(page + 1)}
        className={buttonClass}
      >
        Next
      </button>
      <button
        disabled={page === totalPages}
        onClick={() => onPageChange(totalPages)}
        className={buttonClass}
      >
        Last
      </button>
    </div>
  );
};

export default Pagination;
