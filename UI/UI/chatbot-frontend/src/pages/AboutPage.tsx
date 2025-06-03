import React from 'react';
import { useSettings } from '../context/SettingsContext';
import { useTranslation } from '../utils/translations';
import { BiBot, BiRocket, BiShield, BiHeart, BiUser, BiStar, BiCode, BiGlobe, BiCalendar, BiBookmark, BiTrendingUp, BiBrain } from 'react-icons/bi';
import PageTransition from '../components/PageTransition';
import ScrollReveal from '../components/ScrollReveal';

const AboutPage: React.FC = () => {
  const { settings } = useSettings();
  const { t } = useTranslation(settings.language);

  return (
    <PageTransition>
      <div className="min-h-screen">      {/* Hero Section */}
      <section className="bg-gradient-to-br from-off-white via-beige to-lavender/20 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 py-20 px-4 transition-colors duration-300">
        <div className="max-w-6xl mx-auto text-center">
          <ScrollReveal>
            <div className="mb-8">
              <BiBot className="h-20 w-20 text-charcoal dark:text-white mx-auto mb-6 transition-colors duration-300" />
              <h1 className="font-heading text-5xl sm:text-6xl lg:text-7xl font-bold text-charcoal dark:text-white mb-6 transition-colors duration-300">
                {t('about.title')}
              </h1>
              <p className="text-xl sm:text-2xl text-gray-600 dark:text-gray-300 max-w-4xl mx-auto leading-relaxed transition-colors duration-300">
                {t('about.subtitle')}
              </p>
            </div>
          </ScrollReveal>
        </div>
      </section>      {/* Mission Section */}
      <section className="py-20 px-4 bg-white dark:bg-gray-800 transition-colors duration-300">
        <div className="max-w-6xl mx-auto">
          <ScrollReveal>
            <div className="text-center mb-16">
              <h2 className="font-heading text-4xl font-bold text-charcoal dark:text-white mb-6 transition-colors duration-300">
                {t('about.our_mission')}
              </h2>
              <p className="text-xl text-gray-600 dark:text-gray-300 max-w-4xl mx-auto leading-relaxed transition-colors duration-300">
                {t('about.mission_text')}
              </p>
            </div>
          </ScrollReveal>

          <div className="grid md:grid-cols-2 gap-12 items-center">
            <ScrollReveal delay={100}>
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
            </ScrollReveal>
            <ScrollReveal delay={200}>
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
            </ScrollReveal>
          </div>
        </div>
      </section>      {/* Technology Section */}
      <section className="py-20 px-4 bg-beige/30 dark:bg-gray-900 transition-colors duration-300">
        <div className="max-w-6xl mx-auto">
          <ScrollReveal>
            <div className="text-center mb-16">
              <h2 className="font-heading text-4xl font-bold text-charcoal dark:text-white mb-6 transition-colors duration-300">
                {t('about.our_technology')}
              </h2>
              <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto leading-relaxed transition-colors duration-300">
                {t('about.technology_subtitle')}
              </p>
            </div>
          </ScrollReveal>

          <div className="grid md:grid-cols-3 gap-8">
            <ScrollReveal delay={100}>
              <div className="text-center p-8 rounded-2xl bg-white dark:bg-gray-800 shadow-lg hover:shadow-xl transition-all duration-300">
                <BiCode className="h-16 w-16 text-blue-500 mx-auto mb-6" />
                <h3 className="font-heading text-2xl font-semibold text-charcoal dark:text-white mb-4 transition-colors duration-300">
                  {t('about.tech_nlu')}
                </h3>
                <p className="text-gray-600 dark:text-gray-300 leading-relaxed transition-colors duration-300">
                  {t('about.tech_nlu_desc')}
                </p>
              </div>
            </ScrollReveal>

            <ScrollReveal delay={200}>
              <div className="text-center p-8 rounded-2xl bg-white dark:bg-gray-800 shadow-lg hover:shadow-xl transition-all duration-300">
                <BiRocket className="h-16 w-16 text-green-500 mx-auto mb-6" />
                <h3 className="font-heading text-2xl font-semibold text-charcoal dark:text-white mb-4 transition-colors duration-300">
                  {t('about.tech_ml')}
                </h3>
                <p className="text-gray-600 dark:text-gray-300 leading-relaxed transition-colors duration-300">
                  {t('about.tech_ml_desc')}
                </p>
              </div>
            </ScrollReveal>

            <ScrollReveal delay={300}>
              <div className="text-center p-8 rounded-2xl bg-white dark:bg-gray-800 shadow-lg hover:shadow-xl transition-all duration-300">
                <BiShield className="h-16 w-16 text-purple-500 mx-auto mb-6" />
                <h3 className="font-heading text-2xl font-semibold text-charcoal dark:text-white mb-4 transition-colors duration-300">
                  {t('about.tech_security')}
                </h3>
                <p className="text-gray-600 dark:text-gray-300 leading-relaxed transition-colors duration-300">
                  {t('about.tech_security_desc')}
                </p>
              </div>
            </ScrollReveal>
          </div>
        </div>
      </section>      {/* University Section */}
      <section className="py-20 px-4 bg-gradient-to-br from-green-50 to-blue-50 dark:from-green-900/20 dark:to-blue-900/20 transition-colors duration-300">
        <div className="max-w-6xl mx-auto">
          <ScrollReveal>
            <div className="text-center mb-16">
              <h2 className="font-heading text-4xl font-bold text-charcoal dark:text-white mb-6 transition-colors duration-300">
                {t('home.university_intro')}
              </h2>
              <p className="text-xl text-gray-600 dark:text-gray-300 max-w-4xl mx-auto leading-relaxed transition-colors duration-300">
                {t('home.university_intro_subtitle')}
              </p>
            </div>
          </ScrollReveal>

          <div className="grid lg:grid-cols-2 gap-12 items-center mb-16">
            <ScrollReveal delay={100}>
              <div>
                <h3 className="font-heading text-3xl font-semibold text-charcoal dark:text-white mb-6 transition-colors duration-300">
                  {t('home.university_about')}
                </h3>
                <p className="text-lg text-gray-600 dark:text-gray-300 leading-relaxed mb-6 transition-colors duration-300">
                  {t('home.university_about_desc')}
                </p>
              </div>
            </ScrollReveal>
            <ScrollReveal delay={200}>
              <div className="bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-lg transition-colors duration-300">
                <h4 className="font-heading text-2xl font-semibold text-charcoal dark:text-white mb-6 transition-colors duration-300">
                  {t('home.ai_features')}
                </h4>
                <div className="space-y-4">
                  <div className="flex items-start gap-4">
                    <BiBot className="h-6 w-6 text-blue-500 mt-1 flex-shrink-0" />
                    <div>
                      <h5 className="font-semibold text-charcoal dark:text-white transition-colors duration-300">{t('home.feature_academic')}</h5>
                      <p className="text-gray-600 dark:text-gray-300 text-sm transition-colors duration-300">{t('home.feature_academic_desc')}</p>
                    </div>
                  </div>
                  <div className="flex items-start gap-4">
                    <BiRocket className="h-6 w-6 text-green-500 mt-1 flex-shrink-0" />
                    <div>
                      <h5 className="font-semibold text-charcoal dark:text-white transition-colors duration-300">{t('home.feature_research')}</h5>
                      <p className="text-gray-600 dark:text-gray-300 text-sm transition-colors duration-300">{t('home.feature_research_desc')}</p>
                    </div>
                  </div>
                  <div className="flex items-start gap-4">
                    <BiGlobe className="h-6 w-6 text-purple-500 mt-1 flex-shrink-0" />
                    <div>
                      <h5 className="font-semibold text-charcoal dark:text-white transition-colors duration-300">{t('home.feature_campus')}</h5>
                      <p className="text-gray-600 dark:text-gray-300 text-sm transition-colors duration-300">{t('home.feature_campus_desc')}</p>
                    </div>
                  </div>
                </div>
              </div>
            </ScrollReveal>
          </div>
        </div>
      </section>      {/* Departments Section */}
      <section className="py-20 px-4 bg-white dark:bg-gray-800 transition-colors duration-300">
        <div className="max-w-6xl mx-auto">
          <ScrollReveal>
            <div className="text-center mb-16">
              <h2 className="font-heading text-4xl font-bold text-charcoal dark:text-white mb-6 transition-colors duration-300">
                {t('home.departments')}
              </h2>
              <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto leading-relaxed transition-colors duration-300">
                {t('home.departments_subtitle')}
              </p>
            </div>
          </ScrollReveal>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <ScrollReveal delay={100}>
              <div className="bg-gradient-to-br from-green-100 to-green-200 dark:from-green-900/30 dark:to-green-800/30 rounded-2xl p-6 transition-colors duration-300">
                <div className="bg-green-500 rounded-full w-12 h-12 flex items-center justify-center mb-4">
                  <BiBot className="h-6 w-6 text-white" />
                </div>
                <h3 className="font-heading text-xl font-semibold text-charcoal dark:text-white mb-3 transition-colors duration-300">
                  {t('home.dept_agriculture')}
                </h3>
                <p className="text-gray-600 dark:text-gray-300 text-sm leading-relaxed transition-colors duration-300">
                  {t('home.dept_agriculture_desc')}
                </p>
              </div>
            </ScrollReveal>

            <ScrollReveal delay={150}>
              <div className="bg-gradient-to-br from-green-100 to-green-200 dark:from-green-900/30 dark:to-green-800/30 rounded-2xl p-6 transition-colors duration-300">
                <div className="bg-green-600 rounded-full w-12 h-12 flex items-center justify-center mb-4">
                  <BiBot className="h-6 w-6 text-white" />
                </div>
                <h3 className="font-heading text-xl font-semibold text-charcoal dark:text-white mb-3 transition-colors duration-300">
                  {t('home.dept_forestry')}
                </h3>
                <p className="text-gray-600 dark:text-gray-300 text-sm leading-relaxed transition-colors duration-300">
                  {t('home.dept_forestry_desc')}
                </p>
              </div>
            </ScrollReveal>

            <ScrollReveal delay={200}>
              <div className="bg-gradient-to-br from-blue-100 to-blue-200 dark:from-blue-900/30 dark:to-blue-800/30 rounded-2xl p-6 transition-colors duration-300">
                <div className="bg-blue-500 rounded-full w-12 h-12 flex items-center justify-center mb-4">
                  <BiBot className="h-6 w-6 text-white" />
                </div>
                <h3 className="font-heading text-xl font-semibold text-charcoal dark:text-white mb-3 transition-colors duration-300">
                  {t('home.dept_aquaculture')}
                </h3>
                <p className="text-gray-600 dark:text-gray-300 text-sm leading-relaxed transition-colors duration-300">
                  {t('home.dept_aquaculture_desc')}
                </p>
              </div>
            </ScrollReveal>

            <ScrollReveal delay={250}>
              <div className="bg-gradient-to-br from-red-100 to-red-200 dark:from-red-900/30 dark:to-red-800/30 rounded-2xl p-6 transition-colors duration-300">
                <div className="bg-red-500 rounded-full w-12 h-12 flex items-center justify-center mb-4">
                  <BiHeart className="h-6 w-6 text-white" />
                </div>
                <h3 className="font-heading text-xl font-semibold text-charcoal dark:text-white mb-3 transition-colors duration-300">
                  {t('home.dept_veterinary')}
                </h3>
                <p className="text-gray-600 dark:text-gray-300 text-sm leading-relaxed transition-colors duration-300">
                  {t('home.dept_veterinary_desc')}
                </p>
              </div>
            </ScrollReveal>

            <ScrollReveal delay={300}>
              <div className="bg-gradient-to-br from-purple-100 to-purple-200 dark:from-purple-900/30 dark:to-purple-800/30 rounded-2xl p-6 transition-colors duration-300">
                <div className="bg-purple-500 rounded-full w-12 h-12 flex items-center justify-center mb-4">
                  <BiCode className="h-6 w-6 text-white" />
                </div>
                <h3 className="font-heading text-xl font-semibold text-charcoal dark:text-white mb-3 transition-colors duration-300">
                  {t('home.dept_biotechnology')}
                </h3>
                <p className="text-gray-600 dark:text-gray-300 text-sm leading-relaxed transition-colors duration-300">
                  {t('home.dept_biotechnology_desc')}
                </p>
              </div>
            </ScrollReveal>

            <ScrollReveal delay={350}>
              <div className="bg-gradient-to-br from-orange-100 to-orange-200 dark:from-orange-900/30 dark:to-orange-800/30 rounded-2xl p-6 transition-colors duration-300">
                <div className="bg-orange-500 rounded-full w-12 h-12 flex items-center justify-center mb-4">
                  <BiRocket className="h-6 w-6 text-white" />
                </div>
                <h3 className="font-heading text-xl font-semibold text-charcoal dark:text-white mb-3 transition-colors duration-300">
                  {t('home.dept_food_technology')}
                </h3>
                <p className="text-gray-600 dark:text-gray-300 text-sm leading-relaxed transition-colors duration-300">
                  {t('home.dept_food_technology_desc')}
                </p>
              </div>
            </ScrollReveal>
          </div>
        </div>
      </section>      {/* Values Section */}
      <section className="py-20 px-4 bg-gradient-to-r from-charcoal to-gray-800 dark:from-gray-800 dark:to-gray-900 transition-colors duration-300">
        <div className="max-w-6xl mx-auto">
          <ScrollReveal>
            <div className="text-center mb-16">
              <h2 className="font-heading text-4xl font-bold text-white mb-6">
                {t('about.our_values')}
              </h2>
              <p className="text-xl text-gray-300 max-w-3xl mx-auto leading-relaxed">
                {t('about.values_subtitle')}
              </p>
            </div>
          </ScrollReveal>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <ScrollReveal delay={100}>
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
            </ScrollReveal>

            <ScrollReveal delay={150}>
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
            </ScrollReveal>

            <ScrollReveal delay={200}>
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
            </ScrollReveal>

            <ScrollReveal delay={250}>
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
            </ScrollReveal>
          </div>        </div>
      </section>      {/* Development Milestones Section */}
      <section className="py-20 px-4 bg-gradient-to-br from-indigo-50 to-purple-50 dark:from-indigo-900/20 dark:to-purple-900/20 transition-colors duration-300">
        <div className="max-w-6xl mx-auto">
          <ScrollReveal>
            <div className="text-center mb-16">
              <h2 className="font-heading text-4xl font-bold text-charcoal dark:text-white mb-6 transition-colors duration-300">
                {t('milestones.title')}
              </h2>
              <p className="text-xl text-gray-600 dark:text-gray-300 max-w-4xl mx-auto leading-relaxed transition-colors duration-300">
                {t('milestones.subtitle')}
              </p>
            </div>
          </ScrollReveal>

          {/* University Milestones */}
          <div className="mb-16">
            <ScrollReveal delay={100}>
              <div className="text-center mb-12">
                <h3 className="font-heading text-3xl font-semibold text-charcoal dark:text-white mb-4 transition-colors duration-300">
                  {t('milestones.university_section')}
                </h3>
                <div className="w-24 h-1 bg-gradient-to-r from-green-500 to-blue-500 mx-auto rounded-full"></div>
              </div>
            </ScrollReveal>

            <div className="relative">
              {/* Timeline line */}
              <div className="absolute left-1/2 transform -translate-x-1/2 w-1 h-full bg-gradient-to-b from-green-500 to-blue-500 rounded-full"></div>
              
              {/* University Milestone Items */}
              <div className="space-y-12">
                {/* 1963 */}
                <ScrollReveal delay={150}>
                  <div className="flex items-center">
                    <div className="w-1/2 pr-8 text-right">
                      <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-lg hover:shadow-xl transition-all duration-300">
                        <div className="flex items-center justify-end mb-4">
                          <BiCalendar className="h-6 w-6 text-green-500 mr-2" />
                          <h4 className="font-heading text-xl font-semibold text-charcoal dark:text-white">
                            {t('milestones.university_1963')}
                          </h4>
                        </div>
                        <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                          {t('milestones.university_1963_desc')}
                        </p>
                      </div>
                    </div>
                    <div className="w-8 h-8 bg-green-500 rounded-full border-4 border-white dark:border-gray-900 z-10 flex items-center justify-center">
                      <BiBookmark className="h-4 w-4 text-white" />
                    </div>
                    <div className="w-1/2 pl-8"></div>
                  </div>
                </ScrollReveal>

                {/* 1976 */}
                <ScrollReveal delay={200}>
                  <div className="flex items-center">
                    <div className="w-1/2 pr-8"></div>
                    <div className="w-8 h-8 bg-blue-500 rounded-full border-4 border-white dark:border-gray-900 z-10 flex items-center justify-center">
                      <BiTrendingUp className="h-4 w-4 text-white" />
                    </div>
                    <div className="w-1/2 pl-8">
                      <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-lg hover:shadow-xl transition-all duration-300">
                        <div className="flex items-center mb-4">
                          <BiCalendar className="h-6 w-6 text-blue-500 mr-2" />
                          <h4 className="font-heading text-xl font-semibold text-charcoal dark:text-white">
                            {t('milestones.university_1976')}
                          </h4>
                        </div>
                        <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                          {t('milestones.university_1976_desc')}
                        </p>
                      </div>
                    </div>
                  </div>
                </ScrollReveal>

                {/* 1995 */}
                <ScrollReveal delay={250}>
                  <div className="flex items-center">
                    <div className="w-1/2 pr-8 text-right">
                      <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-lg hover:shadow-xl transition-all duration-300">
                        <div className="flex items-center justify-end mb-4">
                          <BiCalendar className="h-6 w-6 text-purple-500 mr-2" />
                          <h4 className="font-heading text-xl font-semibold text-charcoal dark:text-white">
                            {t('milestones.university_1995')}
                          </h4>
                        </div>
                        <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                          {t('milestones.university_1995_desc')}
                        </p>
                      </div>
                    </div>
                    <div className="w-8 h-8 bg-purple-500 rounded-full border-4 border-white dark:border-gray-900 z-10 flex items-center justify-center">
                      <BiStar className="h-4 w-4 text-white" />
                    </div>
                    <div className="w-1/2 pl-8"></div>
                  </div>
                </ScrollReveal>

                {/* 2010 */}
                <ScrollReveal delay={300}>
                  <div className="flex items-center">
                    <div className="w-1/2 pr-8"></div>
                    <div className="w-8 h-8 bg-orange-500 rounded-full border-4 border-white dark:border-gray-900 z-10 flex items-center justify-center">
                      <BiRocket className="h-4 w-4 text-white" />
                    </div>
                    <div className="w-1/2 pl-8">
                      <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-lg hover:shadow-xl transition-all duration-300">
                        <div className="flex items-center mb-4">
                          <BiCalendar className="h-6 w-6 text-orange-500 mr-2" />
                          <h4 className="font-heading text-xl font-semibold text-charcoal dark:text-white">
                            {t('milestones.university_2010')}
                          </h4>
                        </div>
                        <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                          {t('milestones.university_2010_desc')}
                        </p>
                      </div>
                    </div>
                  </div>
                </ScrollReveal>

                {/* 2020 */}
                <ScrollReveal delay={350}>
                  <div className="flex items-center">
                    <div className="w-1/2 pr-8 text-right">
                      <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-lg hover:shadow-xl transition-all duration-300">
                        <div className="flex items-center justify-end mb-4">
                          <BiCalendar className="h-6 w-6 text-teal-500 mr-2" />
                          <h4 className="font-heading text-xl font-semibold text-charcoal dark:text-white">
                            {t('milestones.university_2020')}
                          </h4>
                        </div>
                        <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                          {t('milestones.university_2020_desc')}
                        </p>
                      </div>
                    </div>
                    <div className="w-8 h-8 bg-teal-500 rounded-full border-4 border-white dark:border-gray-900 z-10 flex items-center justify-center">
                      <BiBrain className="h-4 w-4 text-white" />
                    </div>
                    <div className="w-1/2 pl-8"></div>
                  </div>
                </ScrollReveal>
              </div>
            </div>
          </div>

          {/* AI Project Milestones */}
          <div>
            <ScrollReveal delay={100}>
              <div className="text-center mb-12">
                <h3 className="font-heading text-3xl font-semibold text-charcoal dark:text-white mb-4 transition-colors duration-300">
                  {t('milestones.project_section')}
                </h3>
                <div className="w-24 h-1 bg-gradient-to-r from-blue-500 to-purple-500 mx-auto rounded-full"></div>
              </div>
            </ScrollReveal>

            <div className="relative">
              {/* Timeline line */}
              <div className="absolute left-1/2 transform -translate-x-1/2 w-1 h-full bg-gradient-to-b from-blue-500 to-purple-500 rounded-full"></div>
              
              {/* AI Project Milestone Items */}
              <div className="space-y-12">
                {/* Q1 2024 */}
                <ScrollReveal delay={150}>
                  <div className="flex items-center">
                    <div className="w-1/2 pr-8 text-right">
                      <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-lg hover:shadow-xl transition-all duration-300">
                        <div className="flex items-center justify-end mb-4">
                          <BiCalendar className="h-6 w-6 text-blue-500 mr-2" />
                          <h4 className="font-heading text-xl font-semibold text-charcoal dark:text-white">
                            {t('milestones.project_2024_q1')}
                          </h4>
                        </div>
                        <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                          {t('milestones.project_2024_q1_desc')}
                        </p>
                      </div>
                    </div>
                    <div className="w-8 h-8 bg-blue-500 rounded-full border-4 border-white dark:border-gray-900 z-10 flex items-center justify-center">
                      <BiRocket className="h-4 w-4 text-white" />
                    </div>
                    <div className="w-1/2 pl-8"></div>
                  </div>
                </ScrollReveal>

                {/* Q2 2024 */}
                <ScrollReveal delay={200}>
                  <div className="flex items-center">
                    <div className="w-1/2 pr-8"></div>
                    <div className="w-8 h-8 bg-indigo-500 rounded-full border-4 border-white dark:border-gray-900 z-10 flex items-center justify-center">
                      <BiCode className="h-4 w-4 text-white" />
                    </div>
                    <div className="w-1/2 pl-8">
                      <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-lg hover:shadow-xl transition-all duration-300">
                        <div className="flex items-center mb-4">
                          <BiCalendar className="h-6 w-6 text-indigo-500 mr-2" />
                          <h4 className="font-heading text-xl font-semibold text-charcoal dark:text-white">
                            {t('milestones.project_2024_q2')}
                          </h4>
                        </div>
                        <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                          {t('milestones.project_2024_q2_desc')}
                        </p>
                      </div>
                    </div>
                  </div>
                </ScrollReveal>

                {/* Q3 2024 */}
                <ScrollReveal delay={250}>
                  <div className="flex items-center">
                    <div className="w-1/2 pr-8 text-right">
                      <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-lg hover:shadow-xl transition-all duration-300">
                        <div className="flex items-center justify-end mb-4">
                          <BiCalendar className="h-6 w-6 text-purple-500 mr-2" />
                          <h4 className="font-heading text-xl font-semibold text-charcoal dark:text-white">
                            {t('milestones.project_2024_q3')}
                          </h4>
                        </div>
                        <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                          {t('milestones.project_2024_q3_desc')}
                        </p>
                      </div>
                    </div>
                    <div className="w-8 h-8 bg-purple-500 rounded-full border-4 border-white dark:border-gray-900 z-10 flex items-center justify-center">
                      <BiBrain className="h-4 w-4 text-white" />
                    </div>
                    <div className="w-1/2 pl-8"></div>
                  </div>
                </ScrollReveal>

                {/* Q4 2024 */}
                <ScrollReveal delay={300}>
                  <div className="flex items-center">
                    <div className="w-1/2 pr-8"></div>
                    <div className="w-8 h-8 bg-pink-500 rounded-full border-4 border-white dark:border-gray-900 z-10 flex items-center justify-center">
                      <BiShield className="h-4 w-4 text-white" />
                    </div>
                    <div className="w-1/2 pl-8">
                      <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-lg hover:shadow-xl transition-all duration-300">
                        <div className="flex items-center mb-4">
                          <BiCalendar className="h-6 w-6 text-pink-500 mr-2" />
                          <h4 className="font-heading text-xl font-semibold text-charcoal dark:text-white">
                            {t('milestones.project_2024_q4')}
                          </h4>
                        </div>
                        <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                          {t('milestones.project_2024_q4_desc')}
                        </p>
                      </div>
                    </div>
                  </div>
                </ScrollReveal>

                {/* Q1 2025 */}
                <ScrollReveal delay={350}>
                  <div className="flex items-center">
                    <div className="w-1/2 pr-8 text-right">
                      <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-lg hover:shadow-xl transition-all duration-300 border-2 border-yellow-400">
                        <div className="flex items-center justify-end mb-4">
                          <BiCalendar className="h-6 w-6 text-yellow-500 mr-2" />
                          <h4 className="font-heading text-xl font-semibold text-charcoal dark:text-white">
                            {t('milestones.project_2025_q1')}
                          </h4>
                          <BiStar className="h-5 w-5 text-yellow-500 ml-2" />
                        </div>
                        <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                          {t('milestones.project_2025_q1_desc')}
                        </p>
                      </div>
                    </div>
                    <div className="w-8 h-8 bg-yellow-500 rounded-full border-4 border-white dark:border-gray-900 z-10 flex items-center justify-center animate-pulse">
                      <BiHeart className="h-4 w-4 text-white" />
                    </div>
                    <div className="w-1/2 pl-8"></div>
                  </div>
                </ScrollReveal>
              </div>
            </div>
          </div>
        </div>
      </section>      {/* Development Team Section */}
      <section className="py-20 px-4 bg-beige/30 dark:bg-gray-900 transition-colors duration-300">
        <div className="max-w-6xl mx-auto">
          <ScrollReveal>
            <div className="text-center mb-16">
              <h2 className="font-heading text-4xl font-bold text-charcoal dark:text-white mb-6 transition-colors duration-300">
                {t('home.creators')}
              </h2>
              <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto leading-relaxed transition-colors duration-300">
                {t('home.creators_subtitle')}
              </p>
            </div>
          </ScrollReveal>

          <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            <ScrollReveal delay={100}>
              <div className="bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all duration-300">
                <div className="text-center">
                  <div className="bg-blue-500 rounded-full w-20 h-20 flex items-center justify-center mx-auto mb-6">
                    <BiUser className="h-10 w-10 text-white" />
                  </div>
                  <h3 className="font-heading text-2xl font-semibold text-charcoal dark:text-white mb-2 transition-colors duration-300">
                    {t('home.creator_pha')}
                  </h3>
                  <p className="text-gray-600 dark:text-gray-300 mb-2 transition-colors duration-300">
                    {t('home.creator_pha_id')}
                  </p>
                  <p className="text-blue-500 font-medium mb-4">
                    {t('home.creator_pha_role')}
                  </p>
                </div>
              </div>
            </ScrollReveal>

            <ScrollReveal delay={200}>
              <div className="bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all duration-300">
                <div className="text-center">
                  <div className="bg-green-500 rounded-full w-20 h-20 flex items-center justify-center mx-auto mb-6">
                    <BiUser className="h-10 w-10 text-white" />
                  </div>
                  <h3 className="font-heading text-2xl font-semibold text-charcoal dark:text-white mb-2 transition-colors duration-300">
                    {t('home.creator_nam')}
                  </h3>
                  <p className="text-gray-600 dark:text-gray-300 mb-2 transition-colors duration-300">
                    {t('home.creator_nam_id')}
                  </p>
                  <p className="text-green-500 font-medium mb-4">
                    {t('home.creator_nam_role')}
                  </p>
                </div>
              </div>
            </ScrollReveal>
          </div>

          <ScrollReveal delay={300}>
            <div className="text-center mt-12">
              <div className="bg-gradient-to-r from-blue-500 to-green-500 rounded-2xl p-8 text-white">
                <BiHeart className="h-12 w-12 mx-auto mb-4" />
                <p className="text-xl font-medium">
                  {t('home.thesis_project')}
                </p>
              </div>
            </div>
          </ScrollReveal>
        </div>
      </section>
    </div>
    </PageTransition>
  );
};

export default AboutPage;
