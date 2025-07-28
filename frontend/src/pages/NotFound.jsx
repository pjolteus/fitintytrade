import React from 'react';
import { Link } from 'react-router-dom';

function NotFound() {
  return (
    <div className="min-h-[60vh] flex flex-col items-center justify-center text-center p-6">
      <h1 className="text-4xl font-bold text-purple-800 mb-2">404 - Page Not Found</h1>
      <p className="text-gray-600 mb-4">
        Sorry, the page you're looking for doesn't exist.
      </p>
      <Link
        to="/dashboard"
        className="px-4 py-2 bg-purple-700 text-white rounded hover:bg-purple-800"
      >
        Go to Dashboard
      </Link>
    </div>
  );
}

export default NotFound;


