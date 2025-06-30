import React from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import { AnimatePresence } from 'framer-motion';
import Navbar from './Navbar';

const Layout: React.FC = () => {
  const location = useLocation();

  return (
    <div className="min-h-screen bg-off-white dark:bg-gray-900 transition-colors duration-300">
      <Navbar />
      <main className="flex-1 relative overflow-hidden">
        <AnimatePresence mode="wait" initial={false}>
          <div key={location.pathname}>
            <Outlet />
          </div>
        </AnimatePresence>
      </main>
    </div>
  );
};

export default Layout;
