import React from 'react';
import { Settings as SettingsIcon } from 'lucide-react';

const Settings = ({ settings, setSettings }) => {
  const PROVIDERS = ['OpenRouter', 'OpenAI', 'Anthropic', 'Google', 'xAI'];
  
  const MODELS = {
    openrouter: ['google/gemini-flash-1.5', 'openai/gpt-4o', 'anthropic/claude-3-opus', 'custom'],
    openai: ['gpt-4o', 'gpt-4', 'gpt-3.5-turbo', 'custom'],
    anthropic: ['claude-3-opus-20240229', 'claude-3-sonnet-20240229', 'custom'],
    google: ['gemini-1.5-pro', 'gemini-1.5-flash', 'custom'],
    xai: ['grok-2', 'custom']
  };

  const handleChange = (field, value) => {
    setSettings(prev => ({ ...prev, [field]: value }));
  };

  return (
    <div className="bg-white dark:bg-gray-800/50 backdrop-blur-xl border border-gray-200 dark:border-gray-700/50 rounded-2xl p-8 shadow-xl transition-colors duration-300">
      <div className="flex items-center gap-2 text-xl font-semibold text-gray-900 dark:text-white mb-6">
        <SettingsIcon className="w-5 h-5 text-purple-600 dark:text-purple-400" />
        <h2>Configuration</h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* AI Provider */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-gray-700 dark:text-gray-300 flex items-center gap-2">
            <span className="text-purple-600 dark:text-purple-400">⚡</span>
            AI Provider
          </label>
          <select
            value={settings.provider}
            onChange={(e) => handleChange('provider', e.target.value.toLowerCase())}
            className="w-full px-4 py-2.5 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-colors"
          >
            {PROVIDERS.map(provider => (
              <option key={provider} value={provider.toLowerCase()}>{provider}</option>
            ))}
          </select>
        </div>

        {/* Model */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-gray-700 dark:text-gray-300 flex items-center gap-2">
            <span className="text-purple-600 dark:text-purple-400">🎯</span>
            Model
          </label>
          <select
            value={settings.model}
            onChange={(e) => handleChange('model', e.target.value)}
            className="w-full px-4 py-2.5 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-colors"
          >
            {MODELS[settings.provider]?.map(model => (
              <option key={model} value={model}>{model}</option>
            ))}
          </select>
          {settings.provider === 'openrouter' && (
            <a 
              href="https://openrouter.ai/models" 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-xs text-purple-600 dark:text-purple-400 hover:underline"
            >
              View model list →
            </a>
          )}
        </div>

        {/* API Key */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-gray-700 dark:text-gray-300 flex items-center gap-2">
            <span className="text-purple-600 dark:text-purple-400">🔑</span>
            API Key
          </label>
          <input
            type="password"
            value={settings.apiKey}
            onChange={(e) => handleChange('apiKey', e.target.value)}
            placeholder="Enter your OpenRouter API key"
            className="w-full px-4 py-2.5 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-colors"
          />
          <p className="text-xs text-gray-500 dark:text-gray-400">Securely passed, never stored</p>
        </div>
      </div>

      {/* Custom Model Input */}
      {settings.model === 'custom' && (
        <div className="mt-4 space-y-2">
          <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
            Custom Model ID
          </label>
          <input
            type="text"
            value={settings.customModel || ''}
            onChange={(e) => handleChange('customModel', e.target.value)}
            placeholder="e.g., gpt-4-turbo"
            className="w-full px-4 py-2.5 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-colors"
          />
        </div>
      )}
    </div>
  );
};

export default Settings;
