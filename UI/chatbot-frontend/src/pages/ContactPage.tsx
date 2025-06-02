import React, { useState } from 'react';
import { useSettings } from '../context/SettingsContext';
import { useTranslation } from '../utils/translations';
import { 
  BiEnvelope, 
  BiPhone, 
  BiMapPin, 
  BiTime, 
  BiSend, 
  BiUser, 
  BiMessage,
  BiSupport,
  BiQuestionMark,
  BiHeart
} from 'react-icons/bi';

const ContactPage: React.FC = () => {
  const { settings } = useSettings();
  const { t } = useTranslation(settings.language);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    // Simulate form submission
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Reset form
    setFormData({ name: '', email: '', subject: '', message: '' });
    setIsSubmitting(false);
    
    // In a real app, you would send this to your backend
    alert(t('contact.message_sent'));
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-off-white via-beige to-lavender/20 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 py-20 px-4 transition-colors duration-300">
        <div className="max-w-6xl mx-auto text-center">
          <div className="mb-8">
            <BiEnvelope className="h-20 w-20 text-charcoal dark:text-white mx-auto mb-6 transition-colors duration-300" />
          </div>
          <div>
            <h1 className="font-heading text-5xl sm:text-6xl lg:text-7xl font-bold text-charcoal dark:text-white mb-6 transition-colors duration-300">
              {t('contact.title')}
            </h1>
            <p className="text-xl sm:text-2xl text-gray-600 dark:text-gray-300 max-w-4xl mx-auto leading-relaxed transition-colors duration-300">
              {t('contact.subtitle')}
            </p>
          </div>
        </div>
      </section>

      {/* Contact Information Section */}
      <section className="py-20 px-4 bg-white dark:bg-gray-800 transition-colors duration-300">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="font-heading text-4xl font-bold text-charcoal dark:text-white mb-6 transition-colors duration-300">
              {t('contact.get_in_touch')}
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto leading-relaxed transition-colors duration-300">
              {t('contact.get_in_touch_desc')}
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
            <div className="text-center p-6 rounded-2xl bg-beige/50 dark:bg-gray-700/50 hover:bg-beige dark:hover:bg-gray-700 transition-colors">
              <BiEnvelope className="h-12 w-12 text-blue-500 mx-auto mb-4" />
              <h3 className="font-heading text-xl font-semibold text-charcoal dark:text-white mb-3 transition-colors duration-300">
                {t('contact.email')}
              </h3>
              <p className="text-gray-600 dark:text-gray-300 transition-colors duration-300">
                support@nluai.com
              </p>
            </div>

            <div className="text-center p-6 rounded-2xl bg-lavender/30 dark:bg-indigo-900/30 hover:bg-lavender/50 dark:hover:bg-indigo-900/50 transition-colors">
              <BiPhone className="h-12 w-12 text-green-500 mx-auto mb-4" />
              <h3 className="font-heading text-xl font-semibold text-charcoal dark:text-white mb-3 transition-colors duration-300">
                {t('contact.phone')}
              </h3>
              <p className="text-gray-600 dark:text-gray-300 transition-colors duration-300">
                +1 (555) 123-4567
              </p>
            </div>

            <div className="text-center p-6 rounded-2xl bg-sky-blue/30 dark:bg-blue-900/30 hover:bg-sky-blue/50 dark:hover:bg-blue-900/50 transition-colors">
              <BiMapPin className="h-12 w-12 text-red-500 mx-auto mb-4" />
              <h3 className="font-heading text-xl font-semibold text-charcoal dark:text-white mb-3 transition-colors duration-300">
                {t('contact.office')}
              </h3>
              <p className="text-gray-600 dark:text-gray-300 transition-colors duration-300">
                San Francisco, CA
              </p>
            </div>

            <div className="text-center p-6 rounded-2xl bg-beige/50 dark:bg-gray-700/50 hover:bg-beige dark:hover:bg-gray-700 transition-colors">
              <BiTime className="h-12 w-12 text-purple-500 mx-auto mb-4" />
              <h3 className="font-heading text-xl font-semibold text-charcoal dark:text-white mb-3 transition-colors duration-300">
                {t('contact.hours')}
              </h3>
              <p className="text-gray-600 dark:text-gray-300 transition-colors duration-300">
                24/7 {t('contact.support')}
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Contact Form Section */}
      <section className="py-20 px-4 bg-beige/30 dark:bg-gray-900 transition-colors duration-300">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="font-heading text-4xl font-bold text-charcoal dark:text-white mb-6 transition-colors duration-300">
              {t('contact.send_message')}
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto leading-relaxed transition-colors duration-300">
              {t('contact.send_message_desc')}
            </p>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-3xl shadow-lg p-8 transition-colors duration-300">
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-charcoal dark:text-white mb-2 transition-colors duration-300">
                    <BiUser className="h-4 w-4 inline mr-2" />
                    {t('contact.name')}
                  </label>
                  <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    required
                    className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-lavender dark:focus:ring-indigo-500 focus:border-transparent bg-white dark:bg-gray-700 text-charcoal dark:text-white transition-colors duration-300"
                    placeholder={t('contact.name_placeholder')}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-charcoal dark:text-white mb-2 transition-colors duration-300">
                    <BiEnvelope className="h-4 w-4 inline mr-2" />
                    {t('contact.email')}
                  </label>
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                    className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-lavender dark:focus:ring-indigo-500 focus:border-transparent bg-white dark:bg-gray-700 text-charcoal dark:text-white transition-colors duration-300"
                    placeholder={t('contact.email_placeholder')}
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-charcoal dark:text-white mb-2 transition-colors duration-300">
                  <BiQuestionMark className="h-4 w-4 inline mr-2" />
                  {t('contact.subject')}
                </label>
                <select
                  name="subject"
                  value={formData.subject}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-lavender dark:focus:ring-indigo-500 focus:border-transparent bg-white dark:bg-gray-700 text-charcoal dark:text-white transition-colors duration-300"
                >
                  <option value="">{t('contact.select_subject')}</option>
                  <option value="general">{t('contact.general_inquiry')}</option>
                  <option value="support">{t('contact.technical_support')}</option>
                  <option value="feedback">{t('contact.feedback')}</option>
                  <option value="partnership">{t('contact.partnership')}</option>
                  <option value="other">{t('contact.other')}</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-charcoal dark:text-white mb-2 transition-colors duration-300">
                  <BiMessage className="h-4 w-4 inline mr-2" />
                  {t('contact.message')}
                </label>
                <textarea
                  name="message"
                  value={formData.message}
                  onChange={handleChange}
                  required
                  rows={6}
                  className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-lavender dark:focus:ring-indigo-500 focus:border-transparent bg-white dark:bg-gray-700 text-charcoal dark:text-white transition-colors duration-300 resize-vertical"
                  placeholder={t('contact.message_placeholder')}
                />
              </div>

              <div className="text-center">
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="btn-primary inline-flex items-center px-8 py-4 text-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isSubmitting ? (
                    <>
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-3"></div>
                      {t('contact.sending')}
                    </>
                  ) : (
                    <>
                      <BiSend className="h-5 w-5 mr-3" />
                      {t('contact.send_message')}
                    </>
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="py-20 px-4 bg-gradient-to-r from-charcoal to-gray-800 dark:from-gray-800 dark:to-gray-900 transition-colors duration-300">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="font-heading text-4xl font-bold text-white mb-6">
              {t('contact.faq')}
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto leading-relaxed">
              {t('contact.faq_desc')}
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6">
              <div className="flex items-start gap-4">
                <div className="bg-blue-500 rounded-full w-12 h-12 flex items-center justify-center flex-shrink-0">
                  <BiSupport className="h-6 w-6 text-white" />
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-white mb-3">
                    {t('contact.faq_response_time')}
                  </h3>
                  <p className="text-gray-300 leading-relaxed">
                    {t('contact.faq_response_time_answer')}
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6">
              <div className="flex items-start gap-4">
                <div className="bg-green-500 rounded-full w-12 h-12 flex items-center justify-center flex-shrink-0">
                  <BiQuestionMark className="h-6 w-6 text-white" />
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-white mb-3">
                    {t('contact.faq_support_hours')}
                  </h3>
                  <p className="text-gray-300 leading-relaxed">
                    {t('contact.faq_support_hours_answer')}
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6">
              <div className="flex items-start gap-4">
                <div className="bg-purple-500 rounded-full w-12 h-12 flex items-center justify-center flex-shrink-0">
                  <BiEnvelope className="h-6 w-6 text-white" />
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-white mb-3">
                    {t('contact.faq_best_contact')}
                  </h3>
                  <p className="text-gray-300 leading-relaxed">
                    {t('contact.faq_best_contact_answer')}
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6">
              <div className="flex items-start gap-4">
                <div className="bg-orange-500 rounded-full w-12 h-12 flex items-center justify-center flex-shrink-0">
                  <BiHeart className="h-6 w-6 text-white" />
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-white mb-3">
                    {t('contact.faq_feedback')}
                  </h3>
                  <p className="text-gray-300 leading-relaxed">
                    {t('contact.faq_feedback_answer')}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default ContactPage;
