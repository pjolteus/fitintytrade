import React from 'react';

function EmailAuditLog({ auditLog }) {
  if (!auditLog || auditLog.length === 0) return null;

  return (
    <div className="mt-8">
      <h3 className="text-lg font-semibold text-purple-800 dark:text-purple-200 mb-2">
        Recent Email Audit
      </h3>
      <ul className="text-sm text-gray-800 dark:text-white list-disc ml-4">
        {auditLog.map((entry, i) => (
          <li key={i}>
            {new Date(entry.time).toLocaleString()} — Sent to {entry.email} ({entry.count} items)
          </li>
        ))}
      </ul>
    </div>
  );
}

export default EmailAuditLog;
