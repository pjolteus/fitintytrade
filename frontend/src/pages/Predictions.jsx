import {
  ChartTabs,
  FilterBar,
  PredictionModal,
  Pagination,
  SelectedActions,
  EmailAuditLog,
  LoadingSpinner,
  ErrorBanner,
} from '../components';
import React, { useEffect, useState } from 'react';
import { fetchPredictionHistory } from '../api/api';
import { sendEmailReport } from '../api/email';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';
import * as XLSX from 'xlsx';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const ITEMS_PER_PAGE = 5;
const REFRESH_INTERVAL = 60000; // 60 seconds

function Predictions() {
  const [predictions, setPredictions] = useState([]);
  const [tickers, setTickers] = useState([]);
  const [selectedTicker, setSelectedTicker] = useState(() => localStorage.getItem('selectedTicker') || 'all');
  const [minConfidence, setMinConfidence] = useState(() => parseFloat(localStorage.getItem('minConfidence')) || 0);
  const [maxConfidence, setMaxConfidence] = useState(() => parseFloat(localStorage.getItem('maxConfidence')) || 1);
  const [searchQuery, setSearchQuery] = useState('');
  const [page, setPage] = useState(() => parseInt(localStorage.getItem('page')) || 1);
  const [total, setTotal] = useState(0);
  const [sortBy, setSortBy] = useState(() => localStorage.getItem('sortBy') || 'timestamp');
  const [order, setOrder] = useState(() => localStorage.getItem('order') || 'desc');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedIds, setSelectedIds] = useState([]);
  const [isSendingEmail, setIsSendingEmail] = useState(false);
  const [recentEmails, setRecentEmails] = useState(() => JSON.parse(localStorage.getItem('recentEmails') || '[]'));
  const [auditLog, setAuditLog] = useState(() => JSON.parse(localStorage.getItem('emailAudit') || '[]'));
  const [selectedPrediction, setSelectedPrediction] = useState(null);
  const userRole = 'admin';

  useEffect(() => {
    const fetchData = () => {
      setLoading(true);
      fetchPredictionHistory({ page, limit: ITEMS_PER_PAGE, sortBy, order })
        .then((data) => {
          setPredictions(data.items || []);
          setTotal(data.total || 0);
          const uniqueTickers = [...new Set(data.items.map((p) => p.ticker))];
          setTickers(uniqueTickers);
        })
        .catch((err) => setError(err.message || 'Unknown error'))
        .finally(() => setLoading(false));
    };

    fetchData();
    const interval = setInterval(fetchData, REFRESH_INTERVAL);
    return () => clearInterval(interval);
  }, [page, sortBy, order]);

  useEffect(() => {
    localStorage.setItem('selectedTicker', selectedTicker);
    localStorage.setItem('minConfidence', minConfidence);
    localStorage.setItem('maxConfidence', maxConfidence);
    localStorage.setItem('page', page);
    localStorage.setItem('sortBy', sortBy);
    localStorage.setItem('order', order);
  }, [selectedTicker, minConfidence, maxConfidence, page, sortBy, order]);

  const filtered = predictions.filter((p) => {
    const matchTicker = selectedTicker === 'all' || p.ticker.toLowerCase() === selectedTicker.toLowerCase();
    const matchConfidence = p.confidence >= minConfidence && p.confidence <= maxConfidence;
    const matchSearch = [p.ticker, p.model_name, p.confidence.toString()].some(field => field.toLowerCase().includes(searchQuery.toLowerCase()));
    return matchTicker && matchConfidence && matchSearch;
  });

  const totalPages = Math.ceil(total / ITEMS_PER_PAGE);

  const exportCSV = () => {
    const csvRows = [
      ['Ticker', 'Prediction', 'Confidence (%)', 'Model', 'Timestamp'],
      ...filtered.map(p => [
        p.ticker,
        p.prediction === 1 ? 'Bullish (Call)' : 'Bearish (Put)',
        (p.confidence * 100).toFixed(2),
        p.model_name,
        new Date(p.timestamp).toLocaleString()
      ])
    ];
    const blob = new Blob([csvRows.map(row => row.join(',')).join('\n')], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'predictions.csv';
    a.click();
  };

  const exportPDF = () => {
    const doc = new jsPDF();
    doc.setFontSize(16);
    doc.text('Prediction Report', 14, 20);
    autoTable(doc, {
      startY: 30,
      head: [['Ticker', 'Prediction', 'Confidence (%)', 'Model', 'Timestamp']],
      body: filtered.map(p => [
        p.ticker,
        p.prediction === 1 ? 'Bullish (Call)' : 'Bearish (Put)',
        (p.confidence * 100).toFixed(2),
        p.model_name,
        new Date(p.timestamp).toLocaleString()
      ])
    });
    doc.save('predictions.pdf');
  };

  const exportExcel = () => {
    const worksheet = XLSX.utils.json_to_sheet(
      filtered.map(p => ({
        Ticker: p.ticker,
        Prediction: p.prediction === 1 ? 'Bullish (Call)' : 'Bearish (Put)',
        'Confidence (%)': (p.confidence * 100).toFixed(2),
        Model: p.model_name,
        Timestamp: new Date(p.timestamp).toLocaleString()
      }))
    );
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, 'Predictions');
    XLSX.writeFile(workbook, 'predictions.xlsx');
  };

  const handleEmailSelected = async () => {
    const selectedItems = filtered.filter(p => selectedIds.includes(p.id));
    const email = prompt(`Enter recipient email:\n${recentEmails.length > 0 ? 'Recent: ' + recentEmails.join(', ') : ''}`);
    if (!email) return;

    setIsSendingEmail(true);
    try {
      await sendEmailReport(selectedItems.map(p => p.id), email);
      toast.success('Email sent successfully.');
      setSelectedIds([]);

      const updatedEmails = [email, ...recentEmails.filter(e => e !== email)].slice(0, 5);
      setRecentEmails(updatedEmails);
      localStorage.setItem('recentEmails', JSON.stringify(updatedEmails));

      const newAudit = { time: new Date().toISOString(), email, count: selectedItems.length };
      const updatedAudit = [newAudit, ...auditLog].slice(0, 5);
      setAuditLog(updatedAudit);
      localStorage.setItem('emailAudit', JSON.stringify(updatedAudit));
    } catch (err) {
      toast.error('Failed to send email.');
    } finally {
      setIsSendingEmail(false);
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow min-h-[300px]">
      <ToastContainer position="top-right" autoClose={3000} />
      <h2 className="text-2xl font-semibold text-purple-800 dark:text-purple-200 mb-4">Predictions</h2>

      <FilterBar
        tickers={tickers}
        selectedTicker={selectedTicker}
        setSelectedTicker={setSelectedTicker}
        minConfidence={minConfidence}
        setMinConfidence={setMinConfidence}
        maxConfidence={maxConfidence}
        setMaxConfidence={setMaxConfidence}
        sortBy={sortBy}
        setSortBy={setSortBy}
        order={order}
        setOrder={setOrder}
        searchQuery={searchQuery}
        setSearchQuery={setSearchQuery}
        onExportCSV={exportCSV}
        onExportPDF={exportPDF}
        onExportExcel={exportExcel}
      />

      {selectedIds.length > 0 && (
        <div className="mb-4 flex gap-2 items-center bg-purple-50 dark:bg-gray-700 p-3 rounded">
          <span className="text-sm font-medium text-purple-800 dark:text-white">{selectedIds.length} selected</span>
          <button className="px-3 py-1 bg-blue-600 text-white rounded text-sm" onClick={handleEmailSelected} disabled={isSendingEmail}>
            {isSendingEmail ? 'Sending...' : 'Email Selected'}
          </button>
          <button className="px-3 py-1 bg-gray-500 text-white rounded text-sm" onClick={() => setSelectedIds([])}>Clear</button>
        </div>
      )}

      {filtered.length > 0 && (
        <ChartTabs
          data={filtered}
          comparisonMode={true}
          toggleEnabled={true}
          selectedIds={selectedIds}
          onSelectRow={setSelectedIds}
          onClickRow={(row) => setSelectedPrediction(row)}
        />
      )}

      <PredictionModal
        prediction={selectedPrediction}
        onClose={() => setSelectedPrediction(null)}
      />

<Pagination
  page={page}
  totalPages={totalPages}
  onPageChange={(newPage) => setPage(newPage)}
/>

      {userRole === 'admin' && auditLog.length > 0 && (
        <div className="mt-8">
          <h3 className="text-lg font-semibold text-purple-800 dark:text-purple-200 mb-2">Recent Email Audit</h3>
          <ul className="text-sm text-gray-800 dark:text-white list-disc ml-4">
            {auditLog.map((entry, i) => (
              <li key={i}>
                {new Date(entry.time).toLocaleString()} — Sent to {entry.email} ({entry.count} items)
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default Predictions;
