import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useSettings } from '../context/SettingsContext';
import { useTranslation } from '../utils/translations';
import { BiChat, BiRocket, BiShield, BiBot } from 'react-icons/bi';
import PageTransition from '../components/PageTransition';
import ScrollReveal from '../components/ScrollReveal';

const HomePage: React.FC = () => {
  const { user } = useAuth();
  const { settings } = useSettings();
  const { t } = useTranslation(settings.language);

  return (
    <PageTransition>
      <div className="min-h-screen">
        {/* Hero Section */}
        <section className="bg-gradient-to-br from-off-white via-beige to-lavender/20 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 py-20 px-4 transition-colors duration-300">
          <div className="max-w-6xl mx-auto text-center">
            <ScrollReveal>
              <div className="mb-8">
                <BiChat className="h-20 w-20 text-charcoal dark:text-white mx-auto mb-6 transition-colors duration-300" />
                <h1 className="font-heading text-5xl sm:text-6xl lg:text-7xl font-bold text-charcoal dark:text-white mb-6 transition-colors duration-300">
                  {t('home.title')}
                </h1>
                <p className="text-xl sm:text-2xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto leading-relaxed transition-colors duration-300">
                  {t('home.subtitle')}
                </p>
              </div>
            </ScrollReveal>
            
            <ScrollReveal delay={200}>
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
            </ScrollReveal>
          </div>
        </section>

        {/* University Introduction Section */}
        <section className="py-20 px-4 bg-white dark:bg-gray-800 transition-colors duration-300">
          <div className="max-w-6xl mx-auto">
            <ScrollReveal>
              <div className="text-center mb-16">
                <h2 className="font-heading text-4xl font-bold text-charcoal dark:text-white mb-4 transition-colors duration-300">
                  {t('home.university_intro')}
                </h2>
                <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto transition-colors duration-300">
                  {t('home.university_intro_subtitle')}
                </p>
              </div>
            </ScrollReveal>

            <ScrollReveal delay={100}>
              <div className="bg-gradient-to-r from-green-50 to-blue-50 dark:from-green-900/20 dark:to-blue-900/20 rounded-2xl p-8 mb-12">
                <h3 className="font-heading text-3xl font-semibold text-charcoal dark:text-white mb-6 text-center">
                  {t('home.university_about')}
                </h3>
                <p className="text-lg text-gray-700 dark:text-gray-300 leading-relaxed text-center max-w-4xl mx-auto">
                  {t('home.university_about_desc')}
                </p>
              </div>
            </ScrollReveal>
          </div>
        </section>

        {/* AI Features Section */}
        <section className="py-20 px-4 bg-beige/30 dark:bg-gray-900 transition-colors duration-300">
          <div className="max-w-6xl mx-auto">
            <ScrollReveal>
              <div className="text-center mb-16">
                <h2 className="font-heading text-4xl font-bold text-charcoal dark:text-white mb-4 transition-colors duration-300">
                  {t('home.ai_features')}
                </h2>
                <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto transition-colors duration-300">
                  {t('home.ai_features_subtitle')}
                </p>
              </div>
            </ScrollReveal>

            <div className="grid md:grid-cols-3 gap-8">
              <ScrollReveal delay={100}>
                <div className="text-center p-8 rounded-2xl bg-white dark:bg-gray-800 shadow-lg hover:shadow-xl transition-all duration-300">
                  <BiBot className="h-16 w-16 text-green-600 dark:text-green-400 mx-auto mb-6" />
                  <h3 className="font-heading text-2xl font-semibold text-charcoal dark:text-white mb-4">
                    {t('home.feature_academic')}
                  </h3>
                  <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                    {t('home.feature_academic_desc')}
                  </p>
                </div>
              </ScrollReveal>

              <ScrollReveal delay={200}>
                <div className="text-center p-8 rounded-2xl bg-white dark:bg-gray-800 shadow-lg hover:shadow-xl transition-all duration-300">
                  <BiShield className="h-16 w-16 text-blue-600 dark:text-blue-400 mx-auto mb-6" />
                  <h3 className="font-heading text-2xl font-semibold text-charcoal dark:text-white mb-4">
                    {t('home.feature_research')}
                  </h3>
                  <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                    {t('home.feature_research_desc')}
                  </p>
                </div>
              </ScrollReveal>

              <ScrollReveal delay={300}>
                <div className="text-center p-8 rounded-2xl bg-white dark:bg-gray-800 shadow-lg hover:shadow-xl transition-all duration-300">
                  <BiRocket className="h-16 w-16 text-purple-600 dark:text-purple-400 mx-auto mb-6" />
                  <h3 className="font-heading text-2xl font-semibold text-charcoal dark:text-white mb-4">
                    {t('home.feature_campus')}
                  </h3>
                  <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                    {t('home.feature_campus_desc')}
                  </p>
                </div>
              </ScrollReveal>
            </div>
          </div>
        </section>

        {/* Departments Section */}
        <section className="py-20 px-4 bg-white dark:bg-gray-800 transition-colors duration-300">
          <div className="max-w-6xl mx-auto">
            <ScrollReveal>
              <div className="text-center mb-16">
                <h2 className="font-heading text-4xl font-bold text-charcoal dark:text-white mb-4 transition-colors duration-300">
                  {t('home.departments')}
                </h2>
                <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto transition-colors duration-300">
                  {t('home.departments_subtitle')}
                </p>
              </div>
            </ScrollReveal>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              <ScrollReveal delay={100}>
                <div className="p-6 rounded-xl bg-green-50 dark:bg-green-900/20 hover:bg-green-100 dark:hover:bg-green-900/30 transition-colors">
                  <h4 className="font-heading text-xl font-semibold text-green-800 dark:text-green-300 mb-3">
                    {t('home.dept_agriculture')}
                  </h4>
                  <p className="text-green-700 dark:text-green-400 text-sm">
                    {t('home.dept_agriculture_desc')}
                  </p>
                </div>
              </ScrollReveal>

              <ScrollReveal delay={150}>
                <div className="p-6 rounded-xl bg-emerald-50 dark:bg-emerald-900/20 hover:bg-emerald-100 dark:hover:bg-emerald-900/30 transition-colors">
                  <h4 className="font-heading text-xl font-semibold text-emerald-800 dark:text-emerald-300 mb-3">
                    {t('home.dept_forestry')}
                  </h4>
                  <p className="text-emerald-700 dark:text-emerald-400 text-sm">
                    {t('home.dept_forestry_desc')}
                  </p>
                </div>
              </ScrollReveal>

              <ScrollReveal delay={200}>
                <div className="p-6 rounded-xl bg-blue-50 dark:bg-blue-900/20 hover:bg-blue-100 dark:hover:bg-blue-900/30 transition-colors">
                  <h4 className="font-heading text-xl font-semibold text-blue-800 dark:text-blue-300 mb-3">
                    {t('home.dept_aquaculture')}
                  </h4>
                  <p className="text-blue-700 dark:text-blue-400 text-sm">
                    {t('home.dept_aquaculture_desc')}
                  </p>
                </div>
              </ScrollReveal>

              <ScrollReveal delay={250}>
                <div className="p-6 rounded-xl bg-orange-50 dark:bg-orange-900/20 hover:bg-orange-100 dark:hover:bg-orange-900/30 transition-colors">
                  <h4 className="font-heading text-xl font-semibold text-orange-800 dark:text-orange-300 mb-3">
                    {t('home.dept_veterinary')}
                  </h4>
                  <p className="text-orange-700 dark:text-orange-400 text-sm">
                    {t('home.dept_veterinary_desc')}
                  </p>
                </div>
              </ScrollReveal>

              <ScrollReveal delay={300}>
                <div className="p-6 rounded-xl bg-purple-50 dark:bg-purple-900/20 hover:bg-purple-100 dark:hover:bg-purple-900/30 transition-colors">
                  <h4 className="font-heading text-xl font-semibold text-purple-800 dark:text-purple-300 mb-3">
                    {t('home.dept_biotechnology')}
                  </h4>
                  <p className="text-purple-700 dark:text-purple-400 text-sm">
                    {t('home.dept_biotechnology_desc')}
                  </p>
                </div>
              </ScrollReveal>

              <ScrollReveal delay={350}>
                <div className="p-6 rounded-xl bg-red-50 dark:bg-red-900/20 hover:bg-red-100 dark:hover:bg-red-900/30 transition-colors">
                  <h4 className="font-heading text-xl font-semibold text-red-800 dark:text-red-300 mb-3">
                    {t('home.dept_food_technology')}
                  </h4>
                  <p className="text-red-700 dark:text-red-400 text-sm">
                    {t('home.dept_food_technology_desc')}
                  </p>
                </div>
              </ScrollReveal>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="py-20 px-4 bg-beige/30 dark:bg-gray-900 transition-colors duration-300">
          <div className="max-w-6xl mx-auto">
            <ScrollReveal>
              <div className="text-center mb-16">
                <h2 className="font-heading text-4xl font-bold text-charcoal dark:text-white mb-4 transition-colors duration-300">
                  {t('home.why_choose')}
                </h2>
                <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto transition-colors duration-300">
                  {t('home.why_choose_subtitle')}
                </p>
              </div>
            </ScrollReveal>

            <div className="grid md:grid-cols-3 gap-8">
              <ScrollReveal delay={100}>
                <div className="text-center p-8 rounded-2xl bg-beige/50 dark:bg-gray-700/50 hover:bg-beige dark:hover:bg-gray-700 transition-colors">
                  <BiBot className="h-12 w-12 text-charcoal dark:text-white mx-auto mb-4 transition-colors duration-300" />
                  <h3 className="font-heading text-2xl font-semibold text-charcoal dark:text-white mb-3 transition-colors duration-300">
                    {t('home.feature_fast')}
                  </h3>
                  <p className="text-gray-600 dark:text-gray-300 leading-relaxed transition-colors duration-300">
                    {t('home.feature_fast_desc')}
                  </p>
                </div>
              </ScrollReveal>

              <ScrollReveal delay={200}>
                <div className="text-center p-8 rounded-2xl bg-lavender/30 dark:bg-indigo-900/30 hover:bg-lavender/50 dark:hover:bg-indigo-900/50 transition-colors">
                  <BiShield className="h-12 w-12 text-charcoal dark:text-white mx-auto mb-4 transition-colors duration-300" />
                  <h3 className="font-heading text-2xl font-semibold text-charcoal dark:text-white mb-3 transition-colors duration-300">
                    {t('home.feature_secure')}
                  </h3>
                  <p className="text-gray-600 dark:text-gray-300 leading-relaxed transition-colors duration-300">
                    {t('home.feature_secure_desc')}
                  </p>
                </div>
              </ScrollReveal>

              <ScrollReveal delay={300}>
                <div className="text-center p-8 rounded-2xl bg-sky-blue/30 dark:bg-blue-900/30 hover:bg-sky-blue/50 dark:hover:bg-blue-900/50 transition-colors">
                  <BiRocket className="h-12 w-12 text-charcoal dark:text-white mx-auto mb-4 transition-colors duration-300" />
                  <h3 className="font-heading text-2xl font-semibold text-charcoal dark:text-white mb-3 transition-colors duration-300">
                    {t('home.feature_learning')}
                  </h3>
                  <p className="text-gray-600 dark:text-gray-300 leading-relaxed transition-colors duration-300">
                    {t('home.feature_learning_desc')}
                  </p>
                </div>
              </ScrollReveal>
            </div>
          </div>
        </section>

        {/* Creators Section */}
        <section className="py-20 px-4 bg-white dark:bg-gray-800 transition-colors duration-300">
          <div className="max-w-6xl mx-auto">
            <ScrollReveal>
              <div className="text-center mb-16">
                <h2 className="font-heading text-4xl font-bold text-charcoal dark:text-white mb-4 transition-colors duration-300">
                  {t('home.creators')}
                </h2>
                <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto transition-colors duration-300">
                  {t('home.creators_subtitle')}
                </p>
              </div>
            </ScrollReveal>

            <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
              <ScrollReveal delay={100}>
                <div className="text-center p-8 rounded-2xl bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 shadow-lg">
                  <div className="w-24 h-24 bg-blue-500 rounded-full mx-auto mb-6 flex items-center justify-center">
                    <span className="text-white font-bold text-2xl">VP</span>
                  </div>
                  <h3 className="font-heading text-2xl font-semibold text-charcoal dark:text-white mb-2">
                    {t('home.creator_pha')}
                  </h3>
                  <p className="text-blue-600 dark:text-blue-400 font-medium mb-3">
                    {t('home.creator_pha_id')}
                  </p>
                  <p className="text-gray-600 dark:text-gray-300">
                    {t('home.creator_pha_role')}
                  </p>
                </div>
              </ScrollReveal>

              <ScrollReveal delay={200}>
                <div className="text-center p-8 rounded-2xl bg-gradient-to-br from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 shadow-lg">
                  <div className="w-24 h-24 bg-green-500 rounded-full mx-auto mb-6 flex items-center justify-center">
                    <span className="text-white font-bold text-2xl">CN</span>
                  </div>
                  <h3 className="font-heading text-2xl font-semibold text-charcoal dark:text-white mb-2">
                    {t('home.creator_nam')}
                  </h3>
                  <p className="text-green-600 dark:text-green-400 font-medium mb-3">
                    {t('home.creator_nam_id')}
                  </p>
                  <p className="text-gray-600 dark:text-gray-300">
                    {t('home.creator_nam_role')}
                  </p>
                </div>
              </ScrollReveal>
            </div>

            <ScrollReveal delay={300}>
              <div className="text-center mt-12">
                <p className="text-lg text-gray-600 dark:text-gray-300 font-medium">
                  {t('home.thesis_project')}
                </p>
              </div>
            </ScrollReveal>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-20 px-4 bg-gradient-to-r from-charcoal to-gray-800 dark:from-gray-800 dark:to-gray-900 transition-colors duration-300">
          <div className="max-w-4xl mx-auto text-center">
            <ScrollReveal>
              <h2 className="font-heading text-4xl font-bold text-white mb-6">
                {t('home.ready_to_start')}
              </h2>
              <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
                {t('home.ready_subtitle')}
              </p>
            </ScrollReveal>
            
            {!user && (
              <ScrollReveal delay={100}>
                <div className="flex flex-col sm:flex-row gap-4 justify-center items-center max-w-md mx-auto">
                  <Link to="/register" className="bg-white text-charcoal px-8 py-4 rounded-lg font-medium hover:bg-gray-100 transition-colors w-full sm:w-auto">
                    {t('home.get_started')}
                  </Link>
                  <Link to="/login" className="border border-white text-white px-8 py-4 rounded-lg font-medium hover:bg-white hover:text-charcoal transition-colors w-full sm:w-auto">
                    {t('home.sign_in')}
                  </Link>
                </div>
              </ScrollReveal>
            )}
          </div>
        </section>
      </div>
    </PageTransition>
  );
};

export default HomePage;
