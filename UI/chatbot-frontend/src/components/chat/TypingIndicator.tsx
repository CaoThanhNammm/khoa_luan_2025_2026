import React from 'react';
import { BiBot } from 'react-icons/bi';
import { useSettings } from '../../context/SettingsContext';
import { useTranslation } from '../../utils/translations';

const TypingIndicator: React.FC = () => {
  const { settings } = useSettings();
  const { t } = useTranslation(settings.language);

  return (
    <div className="flex items-start space-x-4 opacity-0 animate-fade-in">
      <div className="h-10 w-10 bg-gradient-to-br from-lavender via-purple-200 to-sky-blue dark:from-indigo-500 dark:via-purple-500 dark:to-blue-500 rounded-2xl flex items-center justify-center flex-shrink-0 shadow-lg animate-pulse transition-colors duration-300">
        <BiBot className="h-5 w-5 text-charcoal dark:text-white" />
      </div>
      <div className="bg-white/95 dark:bg-gray-700/95 backdrop-blur-sm px-5 py-4 rounded-2xl shadow-lg border border-white/50 dark:border-gray-600/50 relative transition-colors duration-300">
        <div className="flex space-x-2 items-center">
          <span className="text-sm text-gray-600 dark:text-gray-300 mr-3 font-medium transition-colors duration-300">
            {t('chat.ai_thinking')}
          </span>
          <div className="flex space-x-1">
            <div className="w-2 h-2 bg-gradient-to-r from-lavender to-sky-blue dark:from-indigo-400 dark:to-blue-400 rounded-full animate-bounce shadow-sm"></div>
            <div className="w-2 h-2 bg-gradient-to-r from-lavender to-sky-blue dark:from-indigo-400 dark:to-blue-400 rounded-full animate-bounce shadow-sm" style={{ animationDelay: '0.2s' }}></div>
            <div className="w-2 h-2 bg-gradient-to-r from-lavender to-sky-blue dark:from-indigo-400 dark:to-blue-400 rounded-full animate-bounce shadow-sm" style={{ animationDelay: '0.4s' }}></div>
          </div>
        </div>
        <div className="absolute top-4 w-3 h-3 bg-white/95 dark:bg-gray-700/95 border-l border-b border-white/50 dark:border-gray-600/50 transform rotate-45 -left-1.5"></div>
      </div>
    </div>
  );
};

export default TypingIndicator;
