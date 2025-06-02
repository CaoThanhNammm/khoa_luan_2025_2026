import React from 'react';
import { useSettings } from '../context/SettingsContext';
import { useTranslation } from '../utils/translations';
import { BiBot, BiRocket, BiShield, BiHeart, BiUser, BiStar, BiCode, BiGlobe } from 'react-icons/bi';

const AboutPage: React.FC = () => {
  const { settings } = useSettings();
  const { t } = useTranslation(settings.language);

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-off-white via-beige to-lavender/20 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 py-20 px-4 transition-colors duration-300">
        <div className="max-w-6xl mx-auto text-center">
          <div className="mb-8">
            <BiBot className="h-20 w-20 text-charcoal dark:text-white mx-auto mb-6 transition-colors duration-300" />
            <h1 className="font-heading text-5xl sm:text-6xl lg:text-7xl font-bold text-charcoal dark:text-white mb-6 transition-colors duration-300">
              {t('about.title')}
            </h1>
            <p className="text-xl sm:text-2xl text-gray-600 dark:text-gray-300 max-w-4xl mx-auto leading-relaxed transition-colors duration-300">
              {t('about.subtitle')}
            </p>
          </div>
        </div>
      </section>

      {/* Mission Section */}
      <section className="py-20 px-4 bg-white dark:bg-gray-800 transition-colors duration-300">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="font-heading text-4xl font-bold text-charcoal dark:text-white mb-6 transition-colors duration-300">
              {t('about.our_mission')}
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-4xl mx-auto leading-relaxed transition-colors duration-300">
              {t('about.mission_text')}
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <h3 className="font-heading text-3xl font-semibold text-charcoal dark:text-white mb-6 transition-colors duration-300">
                {t('about.vision_title')}
              </h3>
              <p className="text-lg text-gray-600 dark:text-gray-300 leading-relaxed mb-6 transition-colors duration-300">
                {t('about.vision_text')}
              </p>
              <div className="flex items-center gap-4">
                <BiHeart className="h-8 w-8 text-red-500" />
                <span className="text-lg font-medium text-charcoal dark:text-white transition-colors duration-300">
                  {t('about.made_with_love')}
                </span>
              </div>
            </div>
            <div className="bg-gradient-to-br from-lavender/30 to-sky-blue/30 dark:from-indigo-900/30 dark:to-blue-900/30 rounded-2xl p-8 transition-colors duration-300">
              <div className="grid grid-cols-2 gap-6">
                <div className="text-center">
                  <BiUser className="h-12 w-12 text-charcoal dark:text-white mx-auto mb-4 transition-colors duration-300" />
                  <h4 className="text-2xl font-bold text-charcoal dark:text-white transition-colors duration-300">10K+</h4>
                  <p className="text-gray-600 dark:text-gray-300 transition-colors duration-300">{t('about.stat_users')}</p>
                </div>
                <div className="text-center">
                  <BiBot className="h-12 w-12 text-charcoal dark:text-white mx-auto mb-4 transition-colors duration-300" />
                  <h4 className="text-2xl font-bold text-charcoal dark:text-white transition-colors duration-300">1M+</h4>
                  <p className="text-gray-600 dark:text-gray-300 transition-colors duration-300">{t('about.stat_conversations')}</p>
                </div>
                <div className="text-center">
                  <BiStar className="h-12 w-12 text-charcoal dark:text-white mx-auto mb-4 transition-colors duration-300" />
                  <h4 className="text-2xl font-bold text-charcoal dark:text-white transition-colors duration-300">4.9/5</h4>
                  <p className="text-gray-600 dark:text-gray-300 transition-colors duration-300">{t('about.stat_rating')}</p>
                </div>
                <div className="text-center">
                  <BiGlobe className="h-12 w-12 text-charcoal dark:text-white mx-auto mb-4 transition-colors duration-300" />
                  <h4 className="text-2xl font-bold text-charcoal dark:text-white transition-colors duration-300">50+</h4>
                  <p className="text-gray-600 dark:text-gray-300 transition-colors duration-300">{t('about.stat_countries')}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Technology Section */}
      <section className="py-20 px-4 bg-beige/30 dark:bg-gray-900 transition-colors duration-300">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="font-heading text-4xl font-bold text-charcoal dark:text-white mb-6 transition-colors duration-300">
              {t('about.our_technology')}
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto leading-relaxed transition-colors duration-300">
              {t('about.technology_subtitle')}
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center p-8 rounded-2xl bg-white dark:bg-gray-800 shadow-lg hover:shadow-xl transition-all duration-300">
              <BiCode className="h-16 w-16 text-blue-500 mx-auto mb-6" />
              <h3 className="font-heading text-2xl font-semibold text-charcoal dark:text-white mb-4 transition-colors duration-300">
                {t('about.tech_nlu')}
              </h3>
              <p className="text-gray-600 dark:text-gray-300 leading-relaxed transition-colors duration-300">
                {t('about.tech_nlu_desc')}
              </p>
            </div>

            <div className="text-center p-8 rounded-2xl bg-white dark:bg-gray-800 shadow-lg hover:shadow-xl transition-all duration-300">
              <BiRocket className="h-16 w-16 text-green-500 mx-auto mb-6" />
              <h3 className="font-heading text-2xl font-semibold text-charcoal dark:text-white mb-4 transition-colors duration-300">
                {t('about.tech_ml')}
              </h3>
              <p className="text-gray-600 dark:text-gray-300 leading-relaxed transition-colors duration-300">
                {t('about.tech_ml_desc')}
              </p>
            </div>

            <div className="text-center p-8 rounded-2xl bg-white dark:bg-gray-800 shadow-lg hover:shadow-xl transition-all duration-300">
              <BiShield className="h-16 w-16 text-purple-500 mx-auto mb-6" />
              <h3 className="font-heading text-2xl font-semibold text-charcoal dark:text-white mb-4 transition-colors duration-300">
                {t('about.tech_security')}
              </h3>
              <p className="text-gray-600 dark:text-gray-300 leading-relaxed transition-colors duration-300">
                {t('about.tech_security_desc')}
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Values Section */}
      <section className="py-20 px-4 bg-gradient-to-r from-charcoal to-gray-800 dark:from-gray-800 dark:to-gray-900 transition-colors duration-300">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="font-heading text-4xl font-bold text-white mb-6">
              {t('about.our_values')}
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto leading-relaxed">
              {t('about.values_subtitle')}
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="text-center p-6">
              <div className="bg-blue-500 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <BiBot className="h-8 w-8 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-3">
                {t('about.value_innovation')}
              </h3>
              <p className="text-gray-300 text-sm leading-relaxed">
                {t('about.value_innovation_desc')}
              </p>
            </div>

            <div className="text-center p-6">
              <div className="bg-green-500 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <BiShield className="h-8 w-8 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-3">
                {t('about.value_privacy')}
              </h3>
              <p className="text-gray-300 text-sm leading-relaxed">
                {t('about.value_privacy_desc')}
              </p>
            </div>

            <div className="text-center p-6">
              <div className="bg-purple-500 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <BiUser className="h-8 w-8 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-3">
                {t('about.value_accessibility')}
              </h3>
              <p className="text-gray-300 text-sm leading-relaxed">
                {t('about.value_accessibility_desc')}
              </p>
            </div>

            <div className="text-center p-6">
              <div className="bg-orange-500 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <BiHeart className="h-8 w-8 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-3">
                {t('about.value_community')}
              </h3>
              <p className="text-gray-300 text-sm leading-relaxed">
                {t('about.value_community_desc')}
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default AboutPage;
