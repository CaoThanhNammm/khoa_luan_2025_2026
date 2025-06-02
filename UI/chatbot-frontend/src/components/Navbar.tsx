import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { BiLogOut, BiChat, BiHome, BiUser } from 'react-icons/bi';

const Navbar: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="bg-white shadow-sm border-b border-gray-100 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <BiChat className="h-8 w-8 text-charcoal" />
            <span className="font-heading text-xl font-semibold text-charcoal">
              NLU ChatBot
            </span>
          </Link>

          {/* Navigation Links */}
          <div className="flex items-center space-x-6">
            {user ? (
              <>
                <Link
                  to="/"
                  className="flex items-center space-x-1 text-charcoal hover:text-lavender transition-colors"
                >
                  <BiHome className="h-5 w-5" />
                  <span>Home</span>
                </Link>                <Link
                  to="/chat"
                  className="flex items-center space-x-1 text-charcoal hover:text-lavender transition-colors"
                >
                  <BiChat className="h-5 w-5" />
                  <span>Chat</span>
                </Link>
                <Link
                  to="/profile"
                  className="flex items-center space-x-1 text-charcoal hover:text-lavender transition-colors"
                >
                  <BiUser className="h-5 w-5" />
                  <span>Profile</span>
                </Link>                <div className="flex items-center space-x-4">
                  <div className="flex items-center space-x-2">
                    <span className="text-sm font-medium text-charcoal">
                      {user.name}
                    </span>
                  </div>
                  <button
                    onClick={handleLogout}
                    className="flex items-center space-x-1 text-charcoal hover:text-red-600 transition-colors"
                  >
                    <BiLogOut className="h-5 w-5" />
                    <span>Logout</span>
                  </button>
                </div>
              </>
            ) : (
              <>
                <Link
                  to="/login"
                  className="text-charcoal hover:text-lavender transition-colors font-medium"
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  className="btn-primary"
                >
                  Sign Up
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
