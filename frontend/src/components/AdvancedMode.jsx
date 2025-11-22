import React from 'react';
import { Sliders } from 'lucide-react';

const AdvancedMode = ({ advancedMode, setAdvancedMode, temperatures, setTemperatures }) => {
  const translators = [
    { key: 'literary', label: 'Literary', default: 0.8, description: 'Creative content' },
    { key: 'legal', label: 'Legal', default: 0.65, description: 'Technical, precise' },
    { key: 'technical', label: 'Technical', default: 0.65, description: 'Technical specs' },
    { key: 'medical', label: 'Medical', default: 0.6, description: 'Very precise' },
    { key: 'news', label: 'News', default: 0.7, description: 'Balanced' },
    { key: 'academic', label: 'Academic', default: 0.7, description: 'Balanced' },
    { key: 'marketing', label: 'Marketing', default: 0.8, description: 'Creative' },
    { key: 'business', label: 'Business', default: 0.7, description: 'Balanced' },
    { key: 'master', label: 'Master', default: 0.7, description: 'All-purpose' },
  ];

  const handleTemperatureChange = (key, value) => {
    setTemperatures(prev => ({ ...prev, [key]: parseFloat(value) }));
  };

  return (
    <div className="bg-white dark:bg-gray-800/50 backdrop-blur-xl border border-gray-200 dark:border-gray-700/50 rounded-2xl p-6 shadow-xl transition-colors duration-300">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2 text-lg font-semibold text-gray-900 dark:text-white">
          <Sliders className="w-5 h-5 text-purple-600 dark:text-purple-400" />
          <h3>Advanced Mode (Detailed Temperature Setting)</h3>
        </div>
        <button
          onClick={() => setAdvancedMode(!advancedMode)}
          className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
            advancedMode ? 'bg-purple-600' : 'bg-gray-300 dark:bg-gray-600'
          }`}
        >
          <span
            className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
              advancedMode ? 'translate-x-6' : 'translate-x-1'
            }`}
          />
        </button>
      </div>

      {advancedMode && (
        <div className="mt-6 space-y-4">
          <div className="flex items-center justify-between">
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Fine-tune temperature settings for each specialized translator. Higher values (0.8) produce more creative translations, while lower values (0.6) are more precise.
            </p>
            <button
              onClick={() => setTemperatures({})}
              className="px-3 py-1.5 text-xs font-medium text-purple-600 dark:text-purple-400 hover:bg-purple-50 dark:hover:bg-purple-900/20 rounded-lg transition-colors border border-purple-200 dark:border-purple-800"
            >
              Reset to Defaults
            </button>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {translators.map(({ key, label, default: defaultTemp, description }) => (
              <div key={key} className="space-y-2">
                <div className="flex items-center justify-between">
                  <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    {label}
                  </label>
                  <span className="text-sm font-mono text-purple-600 dark:text-purple-400">
                    {(temperatures[key] || defaultTemp).toFixed(1)}
                  </span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.1"
                  value={temperatures[key] || defaultTemp}
                  onChange={(e) => handleTemperatureChange(key, e.target.value)}
                  className="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-lg appearance-none cursor-pointer accent-purple-600"
                />
                <p className="text-xs text-gray-500 dark:text-gray-400">{description}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default AdvancedMode;
