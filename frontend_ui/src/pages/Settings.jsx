// frontend_ui/src/pages/Settings.jsx

import React, { useEffect, useState } from 'react';
import { Card } from '../components/ui/card';
import LoadingSpinner from '../components/shared/LoadingSpinner';

function Settings() {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => setLoading(false), 1200);
    return () => clearTimeout(timer);
  }, []);

  return (
    <Card className="min-h-[300px]">
      <h2 className="text-2xl font-semibold text-purple-800 mb-4">Settings</h2>

      {loading ? (
        <div className="flex justify-center items-center h-32">
          <LoadingSpinner />
        </div>
      ) : (
        <div className="space-y-4 text-gray-700">
          <p>This page will soon allow you to update:</p>
          <ul className="list-disc pl-6">
            <li>Notification preferences</li>
            <li>Theme (Light/Dark)</li>
            <li>Account details and email</li>
            <li>Connected brokers</li>
          </ul>
        </div>
      )}
    </Card>
  );
}

export default Settings;
