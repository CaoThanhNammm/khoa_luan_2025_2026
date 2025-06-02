import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { BiChat, BiRocket, BiShield, BiBot } from 'react-icons/bi';

const HomePage: React.FC = () => {
  const { user } = useAuth();

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-off-white via-beige to-lavender/20 py-20 px-4">
        <div className="max-w-6xl mx-auto text-center">
          <div className="mb-8">
            <BiChat className="h-20 w-20 text-charcoal mx-auto mb-6" />
            <h1 className="font-heading text-5xl sm:text-6xl lg:text-7xl font-bold text-charcoal mb-6">
              NLU ChatBot
            </h1>
            <p className="text-xl sm:text-2xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
              Experience the future of conversational AI with our advanced Natural Language Understanding chatbot.
            </p>
          </div>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center max-w-md mx-auto">
            {user ? (
              <Link to="/chat" className="btn-primary w-full sm:w-auto text-lg px-8 py-4">
                Continue Chatting
              </Link>
            ) : (
              <>
                <Link to="/chat" className="btn-primary w-full sm:w-auto text-lg px-8 py-4">
                  Start Chat
                </Link>
                <Link to="/register" className="btn-secondary w-full sm:w-auto text-lg px-8 py-4">
                  Create Account
                </Link>
              </>
            )}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 bg-white">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="font-heading text-4xl font-bold text-charcoal mb-4">
              Why Choose NLU ChatBot?
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Built with cutting-edge technology to provide you with the most natural and helpful AI conversations.
            </p>
          </div>          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center p-8 rounded-2xl bg-beige/50 hover:bg-beige transition-colors">
              <BiBot className="h-12 w-12 text-charcoal mx-auto mb-4" />
              <h3 className="font-heading text-2xl font-semibold text-charcoal mb-3">
                Lightning Fast
              </h3>
              <p className="text-gray-600 leading-relaxed">
                Get instant responses powered by advanced natural language processing algorithms.
              </p>
            </div>

            <div className="text-center p-8 rounded-2xl bg-lavender/30 hover:bg-lavender/50 transition-colors">
              <BiShield className="h-12 w-12 text-charcoal mx-auto mb-4" />
              <h3 className="font-heading text-2xl font-semibold text-charcoal mb-3">
                Secure & Private
              </h3>
              <p className="text-gray-600 leading-relaxed">
                Your conversations are protected with enterprise-grade security and privacy measures.
              </p>
            </div>

            <div className="text-center p-8 rounded-2xl bg-sky-blue/30 hover:bg-sky-blue/50 transition-colors">
              <BiRocket className="h-12 w-12 text-charcoal mx-auto mb-4" />
              <h3 className="font-heading text-2xl font-semibold text-charcoal mb-3">
                Always Learning
              </h3>
              <p className="text-gray-600 leading-relaxed">
                Our AI continuously improves to provide more accurate and helpful responses.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 bg-gradient-to-r from-charcoal to-gray-800">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="font-heading text-4xl font-bold text-white mb-6">
            Ready to Start Conversations?
          </h2>
          <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
            Join thousands of users who are already experiencing the power of natural language understanding.
          </p>
          {!user && (
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center max-w-md mx-auto">
              <Link to="/register" className="bg-white text-charcoal px-8 py-4 rounded-lg font-medium hover:bg-gray-100 transition-colors w-full sm:w-auto">
                Get Started Free
              </Link>
              <Link to="/login" className="border border-white text-white px-8 py-4 rounded-lg font-medium hover:bg-white hover:text-charcoal transition-colors w-full sm:w-auto">
                Sign In
              </Link>
            </div>
          )}
        </div>
      </section>
    </div>
  );
};

export default HomePage;
