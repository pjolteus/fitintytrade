import React from 'react';

function FilterBar({
  tickers,
  selectedTicker,
  setSelectedTicker,
  minConfidence,
  setMinConfidence,
  maxConfidence,
  setMaxConfidence,
  sortBy,
  setSortBy,
  order,
  setOrder,
  searchQuery,
  setSearchQuery,
  onExportCSV,
  onExportPDF,
  onExportExcel,
}) {
  return (
    <div className="flex flex-wrap gap-4 items-center mb-4">
      <input
        type="text"
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        placeholder="Search by ticker, model, confidence"
        className="p-2 w-full md:w-64 border rounded dark:bg-gray-700 dark:text-white"
      />

      <div>
        <label htmlFor="ticker" className="text-sm text-gray-700 dark:text-gray-300 mr-2">Filter by ticker:</label>
        <select
          id="ticker"
          className="p-2 border rounded dark:border-gray-600 dark:bg-gray-700 dark:text-white"
          value={selectedTicker}
          onChange={(e) => setSelectedTicker(e.target.value)}
        >
          <option value="all">All</option>
          {tickers.map((t) => (
            <option key={t} value={t}>{t}</option>
          ))}
        </select>
      </div>

      <div>
        <label className="text-sm text-gray-700 dark:text-gray-300 mr-2">Confidence:</label>
        <input
          type="number"
          min={0}
          max={1}
          step={0.01}
          value={minConfidence}
          onChange={(e) => setMinConfidence(parseFloat(e.target.value))}
          className="p-2 w-20 border rounded dark:border-gray-600 dark:bg-gray-700 dark:text-white"
        />
        <span className="mx-1 text-gray-500 dark:text-gray-300">to</span>
        <input
          type="number"
          min={0}
          max={1}
          step={0.01}
          value={maxConfidence}
          onChange={(e) => setMaxConfidence(parseFloat(e.target.value))}
          className="p-2 w-20 border rounded dark:border-gray-600 dark:bg-gray-700 dark:text-white"
        />
      </div>

      <div>
        <label className="text-sm text-gray-700 dark:text-gray-300 mr-2">Sort by:</label>
        <select
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
          className="p-2 border rounded dark:border-gray-600 dark:bg-gray-700 dark:text-white"
        >
          <option value="timestamp">Date</option>
          <option value="confidence">Confidence</option>
        </select>
        <select
          value={order}
          onChange={(e) => setOrder(e.target.value)}
          className="ml-2 p-2 border rounded dark:border-gray-600 dark:bg-gray-700 dark:text-white"
        >
          <option value="desc">Descending</option>
          <option value="asc">Ascending</option>
        </select>
      </div>

      <div className="ml-auto flex gap-2">
        <button onClick={onExportCSV} className="px-3 py-1 bg-green-600 text-white rounded">CSV</button>
        <button onClick={onExportPDF} className="px-3 py-1 bg-blue-600 text-white rounded">PDF</button>
        <button onClick={onExportExcel} className="px-3 py-1 bg-yellow-600 text-white rounded">Excel</button>
      </div>
    </div>
  );
}

export default FilterBar;
