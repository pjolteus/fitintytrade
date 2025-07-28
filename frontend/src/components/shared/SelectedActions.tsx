// 📁 components/shared/SelectedActions.tsx
import React from 'react';

type SelectedActionsProps = {
  selectedCount: number;
  onClear: () => void;
  onSend: () => void;
  isSending?: boolean;
  variant?: 'default' | 'primary' | 'danger';
};

const SelectedActions: React.FC<SelectedActionsProps> = ({
  selectedCount,
  onClear,
  onSend,
  isSending = false,
  variant = 'primary',
}) => {
  if (selectedCount === 0) return null;

  const baseBtn = 'px-3 py-1 rounded text-sm transition duration-150';
  const styles = {
    default: 'bg-gray-500 hover:bg-gray-600 text-white',
    primary: 'bg-blue-600 hover:bg-blue-700 text-white',
    danger: 'bg-red-600 hover:bg-red-700 text-white',
  };

  return (
    <div className="mb-4 flex gap-2 items-center bg-purple-50 dark:bg-gray-700 p-3 rounded">
      <span className="text-sm font-medium text-purple-800 dark:text-white">
        {selectedCount} selected
      </span>
      <button onClick={onSend} disabled={isSending} className={`${baseBtn} ${styles[variant]}`}>
        {isSending ? 'Sending...' : 'Email Selected'}
      </button>
      <button onClick={onClear} className={`${baseBtn} ${styles.default}`}>Clear</button>
    </div>
  );
};

export default SelectedActions;

// 📘 SelectedActions.stories.tsx
import React, { useState } from 'react';
import SelectedActions from './SelectedActions';

export default {
  title: 'Shared/SelectedActions',
  component: SelectedActions,
};

export const Primary = () => {
  const [count, setCount] = useState(3);
  return (
    <SelectedActions
      selectedCount={count}
      isSending={false}
      onSend={() => alert('Send Email')}
      onClear={() => setCount(0)}
      variant="primary"
    />
  );
};

// 📁 components/filters/FilterBar.tsx
import React from 'react';

type FilterBarProps = {
  tickers: string[];
  selectedTicker: string;
  setSelectedTicker: (val: string) => void;
  minConfidence: number;
  maxConfidence: number;
  setMinConfidence: (val: number) => void;
  setMaxConfidence: (val: number) => void;
  sortBy: string;
  order: string;
  setSortBy: (val: string) => void;
  setOrder: (val: string) => void;
  searchQuery: string;
  setSearchQuery: (val: string) => void;
  onExportCSV: () => void;
  onExportPDF: () => void;
  onExportExcel: () => void;
};

const FilterBar: React.FC<FilterBarProps> = ({
  tickers,
  selectedTicker,
  setSelectedTicker,
  minConfidence,
  maxConfidence,
  setMinConfidence,
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
}) => {
  return (
    <div className="flex flex-wrap gap-4 items-center mb-4">
      <input
        type="text"
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        placeholder="Search..."
        className="p-2 w-full md:w-64 border rounded dark:bg-gray-700 dark:text-white"
      />

      <select
        className="p-2 border rounded dark:border-gray-600 dark:bg-gray-700 dark:text-white"
        value={selectedTicker}
        onChange={(e) => setSelectedTicker(e.target.value)}
      >
        <option value="all">All Tickers</option>
        {tickers.map((t) => <option key={t} value={t}>{t}</option>)}
      </select>

      <div className="flex items-center">
        <input type="number" step={0.01} min={0} max={1} value={minConfidence} onChange={(e) => setMinConfidence(parseFloat(e.target.value))} className="p-2 w-20 border rounded dark:bg-gray-700 dark:text-white" />
        <span className="mx-1 text-gray-500 dark:text-white">to</span>
        <input type="number" step={0.01} min={0} max={1} value={maxConfidence} onChange={(e) => setMaxConfidence(parseFloat(e.target.value))} className="p-2 w-20 border rounded dark:bg-gray-700 dark:text-white" />
      </div>

      <div className="flex gap-2">
        <select value={sortBy} onChange={(e) => setSortBy(e.target.value)} className="p-2 border rounded dark:bg-gray-700 dark:text-white">
          <option value="timestamp">Date</option>
          <option value="confidence">Confidence</option>
        </select>
        <select value={order} onChange={(e) => setOrder(e.target.value)} className="p-2 border rounded dark:bg-gray-700 dark:text-white">
          <option value="desc">Desc</option>
          <option value="asc">Asc</option>
        </select>
      </div>

      <div className="flex gap-2 ml-auto">
        <button onClick={onExportCSV} className="px-3 py-1 bg-green-600 text-white rounded">CSV</button>
        <button onClick={onExportPDF} className="px-3 py-1 bg-blue-600 text-white rounded">PDF</button>
        <button onClick={onExportExcel} className="px-3 py-1 bg-yellow-600 text-white rounded">Excel</button>
      </div>
    </div>
  );
};

export default FilterBar;

// 📘 FilterBar.stories.tsx
import React, { useState } from 'react';
import FilterBar from './FilterBar';

export default {
  title: 'Filters/FilterBar',
  component: FilterBar,
};

export const Default = () => {
  const [ticker, setTicker] = useState('all');
  const [minConf, setMinConf] = useState(0);
  const [maxConf, setMaxConf] = useState(1);
  const [sortBy, setSortBy] = useState('timestamp');
  const [order, setOrder] = useState('desc');
  const [query, setQuery] = useState('');

  return (
    <FilterBar
      tickers={["AAPL", "TSLA"]}
      selectedTicker={ticker}
      setSelectedTicker={setTicker}
      minConfidence={minConf}
      maxConfidence={maxConf}
      setMinConfidence={setMinConf}
      setMaxConfidence={setMaxConf}
      sortBy={sortBy}
      order={order}
      setSortBy={setSortBy}
      setOrder={setOrder}
      searchQuery={query}
      setSearchQuery={setQuery}
      onExportCSV={() => alert('Export CSV')}
      onExportPDF={() => alert('Export PDF')}
      onExportExcel={() => alert('Export Excel')}
    />
  );
};


// 📁 components/charts/ChartTabs.tsx
import React from 'react';

type ChartTabsProps = {
  data: any[];
  selectedIds: string[];
  onSelectRow: (ids: string[]) => void;
  onClickRow?: (row: any) => void;
};

const ChartTabs: React.FC<ChartTabsProps> = ({ data, selectedIds, onSelectRow, onClickRow }) => {
  const toggle = (id: string) => {
    const updated = selectedIds.includes(id)
      ? selectedIds.filter((i) => i !== id)
      : [...selectedIds, id];
    onSelectRow(updated);
  };

  return (
    <div className="overflow-x-auto">
      <table className="w-full table-auto border-collapse">
        <thead className="bg-gray-200 dark:bg-gray-700">
          <tr>
            <th className="p-2">Select</th>
            <th className="p-2">Ticker</th>
            <th className="p-2">Prediction</th>
            <th className="p-2">Confidence</th>
            <th className="p-2">Model</th>
            <th className="p-2">Timestamp</th>
          </tr>
        </thead>
        <tbody>
          {data.map((p) => (
            <tr
              key={p.id}
              className="hover:bg-gray-100 dark:hover:bg-gray-800 cursor-pointer"
              onClick={() => onClickRow?.(p)}
            >
              <td className="p-2">
                <input
                  type="checkbox"
                  checked={selectedIds.includes(p.id)}
                  onChange={() => toggle(p.id)}
                  onClick={(e) => e.stopPropagation()}
                />
              </td>
              <td className="p-2">{p.ticker}</td>
              <td className="p-2">{p.prediction === 1 ? 'Bullish' : 'Bearish'}</td>
              <td className="p-2">{(p.confidence * 100).toFixed(2)}%</td>
              <td className="p-2">{p.model_name}</td>
              <td className="p-2">{new Date(p.timestamp).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ChartTabs;

// 📘 ChartTabs.stories.tsx
import React, { useState } from 'react';
import ChartTabs from './ChartTabs';

export default {
  title: 'Charts/ChartTabs',
  component: ChartTabs,
};

export const Basic = () => {
  const [selected, setSelected] = useState<string[]>([]);
  return (
    <ChartTabs
      data={[
        { id: '1', ticker: 'AAPL', prediction: 1, confidence: 0.76, model_name: 'XGBoost', timestamp: new Date().toISOString() },
        { id: '2', ticker: 'TSLA', prediction: 0, confidence: 0.45, model_name: 'RandomForest', timestamp: new Date().toISOString() },
      ]}
      selectedIds={selected}
      onSelectRow={setSelected}
      onClickRow={(row) => console.log('Clicked', row)}
    />
  );
};
