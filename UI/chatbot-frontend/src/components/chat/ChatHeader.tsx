import React from 'react';
import { BiBot } from 'react-icons/bi';
import { useSettings } from '../../context/SettingsContext';
import { useTranslation, formatDate, formatMonthDay } from '../../utils/translations';

interface ChatHeaderProps {
  isTyping: boolean;
}

const ChatHeader: React.FC<ChatHeaderProps> = ({ isTyping }) => {
  const { settings } = useSettings();
  const { t } = useTranslation(settings.language);

  const currentDate = new Date();

  return (
    <div className="bg-white/95 dark:bg-slate-800/95 backdrop-blur-xl border-b border-gray-200/50 dark:border-slate-600/30 px-6 py-4 shadow-lg dark:shadow-2xl transition-all duration-300">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <div className="relative group">
            <div className="h-12 w-12 bg-gradient-to-br from-lavender via-purple-200 to-sky-blue dark:from-indigo-500 dark:via-purple-500 dark:to-blue-500 rounded-2xl flex items-center justify-center shadow-lg shadow-lavender/20 dark:shadow-indigo-500/30 group-hover:shadow-xl group-hover:shadow-lavender/30 dark:group-hover:shadow-indigo-500/50 transition-all duration-300 group-hover:scale-105 hover-lift glow-effect">
              <BiBot className="h-6 w-6 text-charcoal dark:text-white" />
            </div>
            <div className="absolute -bottom-1 -right-1 h-4 w-4 bg-emerald-500 dark:bg-emerald-400 rounded-full border-2 border-white dark:border-slate-800 shadow-lg animate-pulse"></div>
          </div>
          <div>
            <h1 className="font-heading text-2xl font-bold text-charcoal dark:text-slate-100 tracking-wide transition-colors duration-300">
              {t('chat.title')}
            </h1>
            <p className="text-sm text-gray-600 dark:text-slate-300 flex items-center space-x-2 font-medium transition-colors duration-300">
              <span className="h-2 w-2 bg-emerald-500 dark:bg-emerald-400 rounded-full animate-pulse shadow-sm"></span>
              <span>{isTyping ? t('chat.thinking') : t('chat.ready')}</span>
            </p>
          </div>
        </div>
        <div className="text-right">
          <div className="text-xs text-gray-500 dark:text-slate-400 font-semibold uppercase tracking-wider transition-colors duration-300">
            {formatDate(currentDate, settings.language, 'short')}
          </div>
          <div className="text-sm text-gray-700 dark:text-slate-200 font-bold transition-colors duration-300">
            {formatMonthDay(currentDate, settings.language)}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatHeader;
