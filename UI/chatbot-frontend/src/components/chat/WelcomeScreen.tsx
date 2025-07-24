import React from 'react';
import { BiFile, BiPlus, BiChat, BiRocket } from 'react-icons/bi';
import { useSettings } from '../../context/SettingsContext';
import { useTranslation } from '../../utils/translations';

interface WelcomeScreenProps {
  onCreateNewSession: (type: 'default' | 'upload') => void;
}

const WelcomeScreen: React.FC<WelcomeScreenProps> = ({ onCreateNewSession }) => {
  const { settings } = useSettings();
  const { t } = useTranslation(settings.language);

  return (
    <div className="flex-1 flex items-center justify-center p-8 bg-gradient-to-br from-slate-50 via-purple-50/30 to-blue-50/40 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900">
      <div className="max-w-2xl w-full text-center">
        {/* Welcome Header */}
        <div className="mb-12">
          <div className="mb-6">
            <BiChat className="h-20 w-20 text-blue-600 dark:text-blue-400 mx-auto mb-4" />
          </div>
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
            {t('chat.welcome_title')}
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-lg mx-auto">
            {t('chat.welcome_subtitle')}
          </p>
        </div>

        {/* Options */}
        <div className="grid md:grid-cols-2 gap-6 mb-8">
          {/* Chat with Student Handbook */}
          <button
            onClick={() => onCreateNewSession('default')}
            className="group p-8 bg-white dark:bg-slate-800 rounded-3xl shadow-lg hover:shadow-xl border-2 border-transparent hover:border-green-200 dark:hover:border-green-700 transition-all duration-300 hover:-translate-y-1"
          >
            <div className="mb-6">
              <div className="w-16 h-16 bg-gradient-to-br from-green-500 to-emerald-600 rounded-2xl flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform duration-300">
                <BiFile className="h-8 w-8 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">
                {t('chat.with_handbook')}
              </h3>
              <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                {t('chat.handbook_description')}
              </p>
            </div>
            <div className="flex items-center justify-center text-green-600 dark:text-green-400 font-semibold">
              <span>{t('chat.start_now')}</span>
              <BiRocket className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform duration-300" />
            </div>
          </button>

          {/* Chat with Document */}
          <button
            onClick={() => onCreateNewSession('upload')}
            className="group p-8 bg-white dark:bg-slate-800 rounded-3xl shadow-lg hover:shadow-xl border-2 border-transparent hover:border-blue-200 dark:hover:border-blue-700 transition-all duration-300 hover:-translate-y-1"
          >
            <div className="mb-6">
              <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-2xl flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform duration-300">
                <BiPlus className="h-8 w-8 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">
                {t('chat.with_document')}
              </h3>
              <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                {t('chat.document_description')}
              </p>
            </div>
            <div className="flex items-center justify-center text-blue-600 dark:text-blue-400 font-semibold">
              <span>{t('chat.upload_document_btn')}</span>
              <BiRocket className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform duration-300" />
            </div>
          </button>
        </div>

      </div>
    </div>
  );
};

export default WelcomeScreen;