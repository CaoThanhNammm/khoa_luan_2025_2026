import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useSettings } from '../context/SettingsContext';
import { useTranslation } from '../utils/translations';
import { BiChat, BiRocket, BiShield, BiBot } from 'react-icons/bi';
import PageTransition from '../components/PageTransition';

const HomePage: React.FC = () => {
  const { user } = useAuth();
  const { settings } = useSettings();
  const { t } = useTranslation(settings.language);

  return (
    <PageTransition>
      <div className="min-h-screen">{/* ...existing code... */}
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-off-white via-beige to-lavender/20 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 py-20 px-4 transition-colors duration-300">
        <div className="max-w-6xl mx-auto text-center">
          <div className="mb-8">
            <BiChat className="h-20 w-20 text-charcoal dark:text-white mx-auto mb-6 transition-colors duration-300" />
            <h1 className="font-heading text-5xl sm:text-6xl lg:text-7xl font-bold text-charcoal dark:text-white mb-6 transition-colors duration-300">
              {t('home.title')}
            </h1>
            <p className="text-xl sm:text-2xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto leading-relaxed transition-colors duration-300">
              {t('home.subtitle')}
            </p>
          </div>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center max-w-md mx-auto">
            {user ? (
              <Link to="/chat" className="btn-primary w-full sm:w-auto text-lg px-8 py-4">
                {t('home.continue_chatting')}
              </Link>
            ) : (
              <>
                <Link to="/chat" className="btn-primary w-full sm:w-auto text-lg px-8 py-4">
                  {t('home.start_chat')}
                </Link>
                <Link to="/register" className="btn-secondary w-full sm:w-auto text-lg px-8 py-4">
                  {t('home.create_account')}
                </Link>
              </>
            )}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 bg-white dark:bg-gray-800 transition-colors duration-300">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="font-heading text-4xl font-bold text-charcoal dark:text-white mb-4 transition-colors duration-300">
              {t('home.why_choose')}
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto transition-colors duration-300">
              {t('home.why_choose_subtitle')}
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center p-8 rounded-2xl bg-beige/50 dark:bg-gray-700/50 hover:bg-beige dark:hover:bg-gray-700 transition-colors">
              <BiBot className="h-12 w-12 text-charcoal dark:text-white mx-auto mb-4 transition-colors duration-300" />
              <h3 className="font-heading text-2xl font-semibold text-charcoal dark:text-white mb-3 transition-colors duration-300">
                {t('home.feature_fast')}
              </h3>
              <p className="text-gray-600 dark:text-gray-300 leading-relaxed transition-colors duration-300">
                {t('home.feature_fast_desc')}
              </p>
            </div>

            <div className="text-center p-8 rounded-2xl bg-lavender/30 dark:bg-indigo-900/30 hover:bg-lavender/50 dark:hover:bg-indigo-900/50 transition-colors">
              <BiShield className="h-12 w-12 text-charcoal dark:text-white mx-auto mb-4 transition-colors duration-300" />
              <h3 className="font-heading text-2xl font-semibold text-charcoal dark:text-white mb-3 transition-colors duration-300">
                {t('home.feature_secure')}
              </h3>
              <p className="text-gray-600 dark:text-gray-300 leading-relaxed transition-colors duration-300">
                {t('home.feature_secure_desc')}
              </p>
            </div>

            <div className="text-center p-8 rounded-2xl bg-sky-blue/30 dark:bg-blue-900/30 hover:bg-sky-blue/50 dark:hover:bg-blue-900/50 transition-colors">
              <BiRocket className="h-12 w-12 text-charcoal dark:text-white mx-auto mb-4 transition-colors duration-300" />
              <h3 className="font-heading text-2xl font-semibold text-charcoal dark:text-white mb-3 transition-colors duration-300">
                {t('home.feature_learning')}
              </h3>
              <p className="text-gray-600 dark:text-gray-300 leading-relaxed transition-colors duration-300">
                {t('home.feature_learning_desc')}
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 bg-gradient-to-r from-charcoal to-gray-800 dark:from-gray-800 dark:to-gray-900 transition-colors duration-300">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="font-heading text-4xl font-bold text-white mb-6">
            {t('home.ready_to_start')}
          </h2>
          <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
            {t('home.ready_subtitle')}
          </p>
          {!user && (
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center max-w-md mx-auto">
              <Link to="/register" className="bg-white text-charcoal px-8 py-4 rounded-lg font-medium hover:bg-gray-100 transition-colors w-full sm:w-auto">
                {t('home.get_started')}
              </Link>
              <Link to="/login" className="border border-white text-white px-8 py-4 rounded-lg font-medium hover:bg-white hover:text-charcoal transition-colors w-full sm:w-auto">
                {t('home.sign_in')}
              </Link>
            </div>
          )}        </div>
      </section>
    </div>
    </PageTransition>
  );
};

export default HomePage;
