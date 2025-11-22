import React from 'react';
import { FileText, Upload, Languages, FileType } from 'lucide-react';

const TranslationForm = ({ formData, setFormData, onSubmit, isLoading }) => {
  const languages = [
    'English', 'Spanish', 'French', 'German', 'Italian', 'Portuguese', 'Russian',
    'Chinese (Simplified)', 'Chinese (Traditional)', 'Japanese', 'Korean', 'Arabic',
    'Hindi', 'Dutch', 'Swedish', 'Polish', 'Turkish', 'Vietnamese', 'Thai', 'Indonesian', 'Greek'
  ];

  const translationTypes = [
    'Help me to decide', 'Business', 'Legal', 'Literary', 'Technical',
    'Medical', 'News', 'Academic', 'Marketing', 'Master Translator'
  ];

  const outputFormats = [
    { value: 'docx', label: 'MS Word (.docx)' },
    { value: 'txt', label: 'Plain Text (.txt)' },
    { value: 'md', label: 'Markdown (.md)' },
    { value: 'json', label: 'JSON (.json)' },
    { value: 'html', label: 'HTML (.html)' }
  ];

  const handleFileChange = (e) => {
    setFormData(prev => ({ ...prev, file: e.target.files[0] }));
  };

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e, fileType) => {
    e.preventDefault();
    e.stopPropagation();
    
    const files = e.dataTransfer.files;
    if (files && files.length > 0) {
      if (fileType === 'main') {
        setFormData(prev => ({ ...prev, file: files[0] }));
      } else if (fileType === 'glossary') {
        setFormData(prev => ({ ...prev, glossaryFile: files[0] }));
      }
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800/50 backdrop-blur-xl border border-gray-200 dark:border-gray-700/50 rounded-2xl p-8 shadow-xl transition-colors duration-300">
      <div className="flex items-center gap-2 text-xl font-semibold text-gray-900 dark:text-white mb-6">
        <FileText className="w-5 h-5 text-purple-600 dark:text-purple-400" />
        <h2>Translation Details</h2>
      </div>

      <div className="space-y-6">
        {/* File Upload */}
        <div 
          className="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-xl p-8 text-center hover:border-purple-500 transition-colors"
          onDragOver={handleDragOver}
          onDrop={(e) => handleDrop(e, 'main')}
        >
          <input
            type="file"
            id="file-upload"
            onChange={handleFileChange}
            className="hidden"
            accept=".pdf,.docx,.pptx,.json,.html,.txt,.md"
          />
          <label htmlFor="file-upload" className="cursor-pointer">
            <Upload className="w-12 h-12 mx-auto text-gray-400 dark:text-gray-500 mb-3" />
            <p className="text-gray-700 dark:text-gray-300 font-medium">
              {formData.file ? formData.file.name : 'Click to upload or drag and drop'}
            </p>
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
              PDF, DOCX, PPTX, JSON, HTML, TXT
            </p>
          </label>
        </div>

        {/* Language Selection */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-2">
            <label className="text-sm font-medium text-gray-700 dark:text-gray-300 flex items-center gap-2">
              <Languages className="w-4 h-4" />
              Source Language
            </label>
            <select
              value={formData.sourceLang}
              onChange={(e) => handleChange('sourceLang', e.target.value)}
              className="w-full px-4 py-2.5 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            >
              {languages.map(lang => (
                <option key={lang} value={lang}>{lang}</option>
              ))}
            </select>
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium text-gray-700 dark:text-gray-300 flex items-center gap-2">
              <Languages className="w-4 h-4" />
              Target Language
            </label>
            <select
              value={formData.targetLang}
              onChange={(e) => handleChange('targetLang', e.target.value)}
              className="w-full px-4 py-2.5 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            >
              {languages.map(lang => (
                <option key={lang} value={lang}>{lang}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Translation Type */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-gray-700 dark:text-gray-300 flex items-center gap-2">
            <FileType className="w-4 h-4" />
            Translation Type
          </label>
          <select
            value={formData.translationType}
            onChange={(e) => handleChange('translationType', e.target.value)}
            className="w-full px-4 py-2.5 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-purple-500 focus:border-transparent"
          >
            {translationTypes.map(type => (
              <option key={type} value={type}>{type}</option>
            ))}
          </select>
        </div>

        {/* Manager's Brief */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
            Manager's Brief
          </label>
          <textarea
            value={formData.brief}
            onChange={(e) => handleChange('brief', e.target.value)}
            placeholder="Describe your translation needs, style preferences, and any specific requirements..."
            rows="4"
            className="w-full px-4 py-3 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none"
          />
        </div>

        {/* Output Format */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-gray-700 dark:text-gray-300 flex items-center gap-2">
            <FileText className="w-4 h-4" />
            Output Format
          </label>
          <select
            value={formData.outputFormat}
            onChange={(e) => handleChange('outputFormat', e.target.value)}
            className="w-full px-4 py-2.5 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-purple-500 focus:border-transparent"
          >
            {outputFormats.map(format => (
              <option key={format.value} value={format.value}>{format.label}</option>
            ))}
          </select>
        </div>

        {/* Glossary Upload (Optional) */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
            Terminology List (Optional)
          </label>
          <div 
            className="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-xl p-4 text-center hover:border-purple-500 transition-colors"
            onDragOver={handleDragOver}
            onDrop={(e) => handleDrop(e, 'glossary')}
          >
            <input
              type="file"
              id="glossary-upload"
              onChange={(e) => setFormData(prev => ({ ...prev, glossaryFile: e.target.files[0] }))}
              className="hidden"
              accept=".xlsx,.xls,.csv"
            />
            <label htmlFor="glossary-upload" className="cursor-pointer">
              <Upload className="w-8 h-8 mx-auto text-gray-400 dark:text-gray-500 mb-2" />
              <p className="text-gray-700 dark:text-gray-300 text-sm font-medium">
                {formData.glossaryFile ? formData.glossaryFile.name : 'Upload glossary (.xlsx, .csv)'}
              </p>
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                First column: source terms, second column: target terms
              </p>
            </label>
          </div>
        </div>

        {/* Submit Button */}
        <button
          onClick={onSubmit}
          disabled={isLoading || !formData.file}
          className="w-full py-3.5 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 disabled:from-gray-400 disabled:to-gray-500 text-white font-semibold rounded-lg transition-all duration-200 disabled:cursor-not-allowed shadow-lg"
        >
          {isLoading ? 'Translating...' : 'Start Translation'}
        </button>
      </div>
    </div>
  );
};

export default TranslationForm;
