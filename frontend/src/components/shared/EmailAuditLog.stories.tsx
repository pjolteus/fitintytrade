import React from 'react';
import EmailAuditLog from './EmailAuditLog';

export default {
  title: 'Shared/EmailAuditLog',
  component: EmailAuditLog,
};

const sampleAuditLog = [
  {
    time: new Date().toISOString(),
    email: 'test@example.com',
    count: 3,
  },
  {
    time: new Date(Date.now() - 86400000).toISOString(),
    email: 'admin@example.com',
    count: 2,
  },
];

export const WithData = () => (
  <EmailAuditLog auditLog={sampleAuditLog} />
);

export const Empty = () => (
  <EmailAuditLog auditLog={[]} />
);
