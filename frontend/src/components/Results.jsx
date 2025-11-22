import React from 'react';
import { CheckCircle, Download, FileText, AlertCircle, Zap, Activity, Bot } from 'lucide-react';

const Results = ({ result, error }) => {
  if (error) {
    return (
      <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-500/20 rounded-2xl p-8 text-center space-y-4">
        <div className="inline-flex p-3 bg-red-100 dark:bg-red-500/20 rounded-full text-red-600 dark:text-red-400 mb-2">
          <AlertCircle className="w-8 h-8" />
        </div>
        <h3 className="text-xl font-semibold text-red-900 dark:text-red-200">Translation Failed</h3>
        <p className="text-red-700 dark:text-red-300 max-w-md mx-auto">{error}</p>
      </div>
    );
  }

  if (!result) return null;

  return (
    <div className="bg-white dark:bg-gray-800/50 backdrop-blur-xl border border-gray-200 dark:border-gray-700/50 rounded-2xl p-8 space-y-6 shadow-xl transition-colors duration-300">
      <div className="flex items-center gap-2 text-xl font-semibold text-gray-900 dark:text-white mb-2">
        <CheckCircle className="w-6 h-6 text-green-500" />
        <h2>Translation Complete</h2>
      </div>

      {/* Download Buttons */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <a 
          href={`http://localhost:8000/api/download/${result.output_file}`}
          className="flex items-center justify-center gap-3 p-5 bg-gradient-to-br from-purple-500/10 to-blue-500/10 border border-purple-200 dark:border-purple-500/20 rounded-xl hover:bg-purple-50 dark:hover:bg-purple-500/20 transition-all group"
        >
          <Download className="w-7 h-7 text-purple-600 dark:text-purple-400 group-hover:scale-110 transition-transform" />
          <div className="text-left">
            <p className="font-semibold text-gray-900 dark:text-white">Download Translation</p>
            <p className="text-sm text-gray-500 dark:text-gray-400">Translated document</p>
          </div>
        </a>

        <a 
          href={`http://localhost:8000/api/download/${result.output_file.replace('_translated', '_details').replace(/\.\w+$/, '.json')}`}
          className="flex items-center justify-center gap-3 p-5 bg-gray-50 dark:bg-gray-900/50 border border-gray-200 dark:border-gray-700 rounded-xl hover:bg-gray-100 dark:hover:bg-gray-800 transition-all group"
        >
          <FileText className="w-7 h-7 text-gray-500 dark:text-gray-400 group-hover:scale-110 transition-transform" />
          <div className="text-left">
            <p className="font-semibold text-gray-900 dark:text-white">Download Report</p>
            <p className="text-sm text-gray-500 dark:text-gray-400">Detailed analysis</p>
          </div>
        </a>
      </div>

      {/* Stats Row */}
      <div className="grid grid-cols-3 gap-4">
        <div className="p-4 bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 rounded-xl border border-blue-100 dark:border-blue-800/30">
          <div className="flex items-center gap-2 text-sm text-blue-600 dark:text-blue-400 mb-1">
            <Activity className="w-4 h-4" />
            Chunks Processed
          </div>
          <p className="text-2xl font-bold text-blue-900 dark:text-blue-100">{result.details?.chunks?.length || 1}</p>
        </div>
        <div className="p-4 bg-gradient-to-br from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 rounded-xl border border-green-100 dark:border-green-800/30">
          <div className="flex items-center gap-2 text-sm text-green-600 dark:text-green-400 mb-1">
            <Zap className="w-4 h-4" />
            Tokens Used
          </div>
          <p className="text-2xl font-bold text-green-900 dark:text-green-100">
            {result.details?.total_tokens?.toLocaleString() || 'N/A'}
          </p>
        </div>
        <div className="p-4 bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 rounded-xl border border-purple-100 dark:border-purple-800/30">
          <div className="flex items-center gap-2 text-sm text-purple-600 dark:text-purple-400 mb-1">
            <Bot className="w-4 h-4" />
            AI Model
          </div>
          <p className="text-xs font-semibold text-purple-900 dark:text-purple-100 truncate" title={result.details?.model}>
            {result.details?.model || 'Unknown'}
          </p>
          {result.details?.provider && (
            <p className="text-xs text-purple-700 dark:text-purple-300 mt-1">
              via {result.details.provider}
            </p>
          )}
        </div>
      </div>

      {/* Manager's Strategy */}
      {result.details?.analysis?.reasoning && (
        <div className="space-y-3">
          <h3 className="text-base font-semibold text-gray-900 dark:text-white flex items-center gap-2">
            <Bot className="w-5 h-5 text-blue-500" />
            Translation Strategy
          </h3>
          <div className="bg-gradient-to-br from-blue-50 to-cyan-50 dark:from-blue-900/20 dark:to-cyan-900/20 rounded-xl p-4 border border-blue-100 dark:border-blue-800/30">
            <p className="text-gray-700 dark:text-gray-200 text-sm leading-relaxed">
              {result.details.analysis.reasoning}
            </p>
          </div>
        </div>
      )}

      {/* Specialist Translators Used */}
      {result.details?.selected_translators && result.details.selected_translators.length > 0 && (
        <div className="space-y-3">
          <h3 className="text-base font-semibold text-gray-900 dark:text-white flex items-center gap-2">
            <Activity className="w-5 h-5 text-purple-500" />
            Specialist Translators Used
          </h3>
          <div className="flex flex-wrap gap-2">
            {result.details.selected_translators.map((translator, i) => (
              <div 
                key={i} 
                className="group relative px-4 py-2 bg-gradient-to-r from-purple-500/10 to-pink-500/10 border border-purple-200 dark:border-purple-500/30 rounded-lg hover:shadow-md transition-all"
              >
                <span className="text-sm font-medium text-purple-700 dark:text-purple-300">
                  {translator}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Results;
