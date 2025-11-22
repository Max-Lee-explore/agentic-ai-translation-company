import React from 'react';
import { CheckCircle2, Circle, Loader2 } from 'lucide-react';

const steps = [
  { id: 1, name: 'Analysis', description: 'Selecting translators' },
  { id: 2, name: 'Translation', description: 'Creating initial translation' },
  { id: 3, name: 'Review', description: 'Refining translation' },
  { id: 4, name: 'Finalization', description: 'Checking terminology' }
];

const StatusBar = ({ currentStatus, isComplete }) => {
  // Map backend status to step number
  const getStepFromStatus = (status) => {
    if (!status || status === 'Starting...') return 1;
    if (status.includes('Analyzing') || status === 'analysis_complete') return 1;
    if (status === 'Initial translation' || status.includes('Creating')) return 2;
    if (status === 'Reflection' || status === 'Improvement' || status.includes('Reviewing') || status.includes('Refining')) return 3;
    if (status === 'Terminology check' || status.includes('Checking terminology') || status.includes('Finalizing')) return 4;
    if (status === 'completed') return 4;
    if (status.includes('chunk')) return 2; // Processing chunks = translation phase
    return 1;
  };

  const currentStep = isComplete ? 4 : getStepFromStatus(currentStatus);

  return (
    <div className="w-full max-w-3xl mx-auto mb-8">
      <div className="relative flex justify-between items-center">
        {/* Progress Bar Background */}
        <div className="absolute top-1/2 left-0 w-full h-1 bg-gray-200 dark:bg-gray-700 -z-10 transform -translate-y-1/2 rounded-full" />
        
        {/* Active Progress Bar */}
        <div 
          className="absolute top-1/2 left-0 h-1 bg-purple-600 dark:bg-purple-500 -z-10 transform -translate-y-1/2 rounded-full transition-all duration-500 ease-in-out"
          style={{ width: `${((currentStep - 1) / (steps.length - 1)) * 100}%` }}
        />

        {steps.map((step) => {
          const isActive = currentStep === step.id;
          const isPast = currentStep > step.id || isComplete;
          
          return (
            <div key={step.id} className="flex flex-col items-center group">
              <div 
                className={`
                  w-10 h-10 rounded-full flex items-center justify-center border-4 transition-all duration-300 bg-white dark:bg-[#0f1117]
                  ${isPast || isComplete
                    ? 'border-purple-600 dark:border-purple-500 text-purple-600 dark:text-purple-500' 
                    : isActive 
                      ? 'border-purple-600 dark:border-purple-500 text-purple-600 dark:text-purple-500 scale-110 shadow-[0_0_15px_rgba(147,51,234,0.3)]' 
                      : 'border-gray-300 dark:border-gray-600 text-gray-300 dark:text-gray-600'
                  }
                `}
              >
                {isPast || isComplete ? (
                  <CheckCircle2 className="w-5 h-5" />
                ) : isActive ? (
                  <Loader2 className="w-5 h-5 animate-spin" />
                ) : (
                  <Circle className="w-5 h-5" />
                )}
              </div>
              
              <div className="absolute mt-12 flex flex-col items-center w-32 text-center">
                <span 
                  className={`
                    text-sm font-medium transition-colors duration-300
                    ${isActive || isPast || isComplete
                      ? 'text-purple-700 dark:text-purple-300' 
                      : 'text-gray-400 dark:text-gray-600'
                    }
                  `}
                >
                  {step.name}
                </span>
                {isActive && !isComplete && (
                  <span className="text-xs text-gray-500 dark:text-gray-400 animate-pulse mt-1">
                    {step.description}
                  </span>
                )}
              </div>
            </div>
          );
        })}
      </div>
      {/* Spacing for the text labels below */}
      <div className="h-16" />
    </div>
  );
};

export default StatusBar;
