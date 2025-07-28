import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import OverviewDashboard from './pages/OverviewDashboard';
import Predictions from './pages/Predictions';
import Settings from './pages/Settings';
import NotFound from './pages/NotFound';
import Layout from './components/Layout';
import TradeDashboard from './pages/TradeDashboard';

function App() {
  return (
    <>
      {/* Global toast notifications */}
      <Toaster
        position="bottom-center"
        toastOptions={{
          duration: 2000,
          style: {
            background: '#1f2937', // Tailwind dark gray
            color: '#fff',
          },
        }}
      />

      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Navigate to="/dashboard" />} />
          <Route path="dashboard" element={<OverviewDashboard />} />
          <Route path="predictions" element={<Predictions />} />
          <Route path="settings" element={<Settings />} />
          <Route path="trade-dashboard" element={<TradeDashboard />} />
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </>
  );
}

export default App;




