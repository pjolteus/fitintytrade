import React, { useState } from 'react';
import { Link, Outlet, useLocation } from 'react-router-dom';
import {
  Menu,
  X,
  LayoutDashboard,
  TrendingUp,
  ArrowRightLeft,
  Settings as SettingsIcon,
  Moon,
  Sun,
  Banknote,
  Globe,
  Bitcoin,
  ChevronDown,
  ChevronUp,
} from 'lucide-react';
import toast from 'react-hot-toast';
import useTheme from '../hooks/useTheme';

function Layout() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const { isDark, toggleTheme } = useTheme();
  const [selectedBroker, setSelectedBroker] = useState(localStorage.getItem('selectedBroker') || 'Alpaca');
  const location = useLocation();

const routeTitles = {
  '/dashboard': 'Dashboard',
  '/predictions': 'Predictions',
  '/trade-dashboard': 'Trade',
  '/settings': 'Settings',
  '/stocks': 'Stocks Dashboard',
  '/currencies': 'Currency Dashboard',
  '/crypto': 'Crypto Dashboard',
};

const pageLabel =
  Object.keys(routeTitles).find((key) => location.pathname.startsWith(key)) || '';


  const [assetMenuOpen, setAssetMenuOpen] = useState(() => {
    const saved = localStorage.getItem('assetMenuOpen');
    return saved === null ? true : saved === 'true';
  });

  const toggleSidebar = () => setSidebarOpen(!sidebarOpen);

  const toggleAssetMenu = () => {
    const newState = !assetMenuOpen;
    setAssetMenuOpen(newState);
    localStorage.setItem('assetMenuOpen', newState.toString());
  };

  const handleBrokerChange = (e) => {
    const newBroker = e.target.value;
    setSelectedBroker(newBroker);
    localStorage.setItem('selectedBroker', newBroker);
    toast.success(`🔗 Broker switched to ${newBroker}`);
  };

  const navItems = [
    { label: 'Dashboard', path: '/dashboard', icon: <LayoutDashboard size={18} /> },
    { label: 'Predictions', path: '/predictions', icon: <TrendingUp size={18} /> },
    { label: 'Trade', path: '/trade-dashboard', icon: <ArrowRightLeft size={18} /> },
    { label: 'Settings', path: '/settings', icon: <SettingsIcon size={18} /> },
  ];

  const assetDashboards = [
    { label: 'Crypto', path: '/crypto', icon: <Bitcoin size={18} /> },
    { label: 'Currencies', path: '/currencies', icon: <Globe size={18} /> },
    { label: 'Stocks', path: '/stocks', icon: <Banknote size={18} /> },
  ].sort((a, b) => a.label.localeCompare(b.label));

  const currentPage = navItems.find((item) => location.pathname.startsWith(item.path))?.label || '';

  return (
    <div className="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-900 text-gray-800 dark:text-gray-100 transition-colors">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow p-4 flex items-center justify-between md:justify-start md:gap-8">
        <button onClick={toggleSidebar} className="md:hidden text-purple-800 dark:text-purple-300">
          {sidebarOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
        <h1 className="text-xl font-bold text-purple-800 dark:text-purple-300">FitintyTrade</h1>
        <span className="text-sm text-gray-500 dark:text-gray-300 ml-auto hidden md:block">
          {pageLabel && `» ${routeTitles[pageLabel]}`}
        </span>

        {/* Broker Selector */}
        <select
          value={selectedBroker}
          onChange={handleBrokerChange}
          className="ml-4 border border-gray-300 dark:border-gray-700 rounded px-2 py-1 text-sm bg-white dark:bg-gray-800 dark:text-white"
        >
          <option>Alpaca</option>
          <option>OANDA</option>
          <option>FXCM</option>
          <option>IBR</option>
          <option>Binance</option>
          <option>Bybit</option>
          <option>Coinbase</option>
        </select>

        {/* Theme Toggle */}
        <button
          onClick={() => {
            toggleTheme();
            toast(isDark ? '☀️ Light mode enabled' : '🌙 Dark mode enabled');
          }}
          className="ml-4 transition-transform duration-300 hover:scale-110 text-purple-700 dark:text-yellow-300"
          title={isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
        >
          {isDark ? <Sun size={20} className="animate-spin-slow" /> : <Moon size={20} />}
        </button>
      </header>

      <div className="flex flex-1">
        {/* Sidebar */}
        <aside
          className={`fixed md:static z-20 top-0 left-0 w-64 h-full bg-purple-900 text-white p-6 transform transition-transform duration-200 ease-in-out ${
            sidebarOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'
          }`}
        >
          <nav className="space-y-4 pt-14 md:pt-0">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                onClick={() => setSidebarOpen(false)}
                className={`flex items-center gap-2 px-3 py-2 rounded-md text-sm font-medium ${
                  location.pathname.startsWith(item.path)
                    ? 'bg-purple-700'
                    : 'hover:bg-purple-800'
                }`}
              >
                {item.icon}
                {item.label}
              </Link>
            ))}

            {/* Collapsible Asset Dashboards */}
            <div>
              <button
                onClick={toggleAssetMenu}
                className="w-full flex items-center justify-between px-3 py-2 rounded-md text-sm font-medium hover:bg-purple-800"
              >
                <span className="flex items-center gap-2">
                  <TrendingUp size={18} />
                  Asset Dashboards
                </span>
                {assetMenuOpen ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
              </button>

              {assetMenuOpen && (
                <div className="mt-1 pl-6 space-y-1">
                  {assetDashboards.map((item) => (
                    <Link
                      key={item.path}
                      to={item.path}
                      onClick={() => setSidebarOpen(false)}
                      className={`flex items-center gap-2 px-3 py-2 rounded-md text-sm font-medium ${
                        location.pathname.startsWith(item.path)
                          ? 'bg-purple-700'
                          : 'hover:bg-purple-800'
                      }`}
                    >
                      {item.icon}
                      {item.label}
                    </Link>
                  ))}
                </div>
              )}
            </div>
          </nav>
        </aside>

        {/* Main content */}
        <main className="flex-1 p-6 mt-4 md:mt-0">
          <Outlet />
        </main>
      </div>

      {/* Footer */}
      <footer className="bg-white dark:bg-gray-800 shadow text-center p-4 text-sm text-gray-500 dark:text-gray-400">
        &copy; {new Date().getFullYear()} FitintyTrade. All rights reserved.
      </footer>
    </div>
  );
}

export default Layout;
