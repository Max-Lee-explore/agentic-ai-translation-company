import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Settings from './components/Settings';
import AdvancedMode from './components/AdvancedMode';
import TranslationForm from './components/TranslationForm';
import Results from './components/Results';
import { Sparkles, Sun, Moon } from 'lucide-react';
import StatusBar from './components/StatusBar';

function App() {
  const [settings, setSettings] = useState({
    apiKey: '',
    provider: 'openrouter',
    model: 'google/gemini-flash-1.5',
    customModel: ''
  });

  const [advancedMode, setAdvancedMode] = useState(false);
  const [temperatures, setTemperatures] = useState({});

  // Theme state
  const [theme, setTheme] = useState(() => {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('theme') || 'dark';
    }
    return 'dark';
  });

  // Apply theme
  useEffect(() => {
    const root = window.document.documentElement;
    if (theme === 'dark') {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
    localStorage.setItem('theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => prev === 'dark' ? 'light' : 'dark');
  };

  const [formData, setFormData] = useState({
    file: null,
    glossaryFile: null,
    sourceLang: 'English',
    targetLang: 'Spanish',
    translationType: 'Business',
    brief: '',
    outputFormat: 'docx'
  });

  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [currentStatus, setCurrentStatus] = useState('');

  const handleSubmit = async () => {
    if (!settings.apiKey) {
      setError("Please enter an API Key in the settings.");
      return;
    }

    if (!formData.file) {
      setError("Please upload a file to translate.");
      return;
    }

    setIsLoading(true);
    setError(null);
    setResult(null);
    setCurrentStatus('Starting...');

    const data = new FormData();
    data.append('file', formData.file);
    if (formData.glossaryFile) {
      data.append('glossary_file', formData.glossaryFile);
    }
    data.append('source_lang', formData.sourceLang);
    data.append('target_lang', formData.targetLang);
    data.append('translation_type', formData.translationType);
    data.append('brief', formData.brief);
    data.append('output_format', formData.outputFormat);
    data.append('api_key', settings.apiKey);
    data.append('provider', settings.provider);
    data.append('model', settings.model === 'custom' ? settings.customModel : settings.model);
    data.append('temperature', 0.7);

    // Add advanced temperatures if enabled
    if (advancedMode && Object.keys(temperatures).length > 0) {
      Object.entries(temperatures).forEach(([key, value]) => {
        data.append(`temp_${key}`, value);
      });
    }

    try {
      const response = await fetch('http://localhost:8000/api/translate', {
        method: 'POST',
        body: data,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        
        if (done) break;
        
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        
        // Keep the last incomplete line in the buffer
        buffer = lines.pop() || '';
        
        for (const line of lines) {
          if (line.trim()) {
            try {
              const event = JSON.parse(line);
              
              // Update status
              if (event.status) {
                setCurrentStatus(event.status);
              }
              
              // Handle completion
              if (event.status === 'completed' && event.result) {
                setResult(event.result);
                setIsLoading(false);
              }
              
              // Handle errors
              if (event.status === 'error') {
                setError(event.message || 'Translation failed');
                setIsLoading(false);
              }
            } catch (e) {
              console.error('Error parsing event:', e, line);
            }
          }
        }
      }
    } catch (err) {
      console.error(err);
      setError(err.message || "An error occurred during translation. Please check your API key and try again.");
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen transition-colors duration-300 bg-gray-50 dark:bg-[#0f1117] text-gray-900 dark:text-gray-100 font-sans selection:bg-purple-500/30">
      {/* Background Gradients - Dark Mode Only */}
      <div className="fixed inset-0 z-0 pointer-events-none opacity-0 dark:opacity-100 transition-opacity duration-300">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-purple-900/20 blur-[120px]" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-blue-900/20 blur-[120px]" />
      </div>

      <div className="relative z-10 max-w-4xl mx-auto px-4 py-12 space-y-8">
        {/* Header */}
        <header className="flex flex-col items-center justify-center space-y-4 mb-12 relative">
          <div className="absolute right-0 top-0">
            <button 
              onClick={toggleTheme}
              className="p-2 rounded-full bg-gray-200 dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-700 transition-colors"
              aria-label="Toggle theme"
            >
              {theme === 'dark' ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
            </button>
          </div>
          
          <div className="inline-flex items-center justify-center p-3 bg-gradient-to-br from-purple-500/20 to-blue-500/20 rounded-2xl border border-gray-200 dark:border-white/10 mb-4 shadow-2xl shadow-purple-500/10">
            <Sparkles className="w-8 h-8 text-purple-600 dark:text-purple-400" />
          </div>
          <h1 className="text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-gray-900 via-purple-800 to-blue-800 dark:from-white dark:via-purple-200 dark:to-blue-200 tracking-tight text-center pb-2">
            Agentic AI Translator
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-400 max-w-2xl mx-auto font-light text-center">
            From Manager to Proofreader: An autonomous multi-agent system for professional translation.
          </p>
        </header>

        {/* Main Content - Single Column */}
        <div className="space-y-8">
          {/* Settings Section */}
          <Settings settings={settings} setSettings={setSettings} />

          {/* Advanced Mode */}
          <AdvancedMode 
            advancedMode={advancedMode}
            setAdvancedMode={setAdvancedMode}
            temperatures={temperatures}
            setTemperatures={setTemperatures}
          />

          {/* Translation Form */}
          <TranslationForm 
            formData={formData} 
            setFormData={setFormData} 
            onSubmit={handleSubmit}
            isLoading={isLoading}
          />

          {/* Status Bar */}
          {(isLoading || result) && (
            <StatusBar currentStatus={currentStatus} isComplete={!!result} />
          )}
          
          {/* Results */}
          {(result || error) && (
            <Results result={result} error={error} />
          )}
        </div>
        
        <footer className="text-center text-gray-500 dark:text-gray-600 text-sm pt-12 pb-6">
          <p>© 2025 Agentic AI Translation System. Created by Max Lee.</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
