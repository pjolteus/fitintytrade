import React, { useEffect, useState } from 'react';

function Settings() {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => setLoading(false), 1200);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="bg-white rounded-lg p-6 shadow min-h-[300px]">
      <h2 className="text-2xl font-semibold text-purple-800 mb-4">Settings</h2>

      {loading ? (
        <div className="space-y-4 animate-pulse">
          <div className="h-5 bg-gray-300 rounded w-1/4" />
          <div className="h-4 bg-gray-200 rounded w-3/4" />
        </div>
      ) : (
        <p className="text-gray-600">
          User settings will be editable here.
        </p>
      )}
    </div>
  );
}

export default Settings;


