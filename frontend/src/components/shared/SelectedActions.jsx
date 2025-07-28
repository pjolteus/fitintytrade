import React from 'react';

function SelectedActions({ selectedIds, isSendingEmail, onEmail, onClear }) {
  if (selectedIds.length === 0) return null;

  return (
    <div className="mb-4 flex gap-2 items-center bg-purple-50 dark:bg-gray-700 p-3 rounded">
      <span className="text-sm font-medium text-purple-800 dark:text-white">
        {selectedIds.length} selected
      </span>
      <button
        className="px-3 py-1 bg-blue-600 text-white rounded text-sm"
        onClick={onEmail}
        disabled={isSendingEmail}
      >
        {isSendingEmail ? 'Sending...' : 'Email Selected'}
      </button>
      <button
        className="px-3 py-1 bg-gray-500 text-white rounded text-sm"
        onClick={onClear}
      >
        Clear
      </button>
    </div>
  );
}

export default SelectedActions;

