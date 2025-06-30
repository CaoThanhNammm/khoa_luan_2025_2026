import React from 'react';
import { motion } from 'framer-motion';

interface PageTransitionProps {
  children: React.ReactNode;
  className?: string;
  variant?: 'fade' | 'slide' | 'scale' | 'elegant';
}

const pageVariants = {
  fade: {
    initial: { opacity: 0 },
    in: { opacity: 1 },
    out: { opacity: 0 }
  },
  slide: {
    initial: { opacity: 0, x: 100 },
    in: { opacity: 1, x: 0 },
    out: { opacity: 0, x: -100 }
  },
  scale: {
    initial: { opacity: 0, scale: 0.8 },
    in: { opacity: 1, scale: 1 },
    out: { opacity: 0, scale: 1.1 }
  },
  elegant: {
    initial: {
      opacity: 0,
      y: 30,
      scale: 0.95,
      filter: 'blur(10px)'
    },
    in: {
      opacity: 1,
      y: 0,
      scale: 1,
      filter: 'blur(0px)'
    },
    out: {
      opacity: 0,
      y: -30,
      scale: 0.95,
      filter: 'blur(10px)'
    }
  }
};

const pageTransitions = {
  fade: {
    type: 'tween',
    ease: 'easeInOut',
    duration: 0.3
  },
  slide: {
    type: 'tween',
    ease: 'easeInOut',
    duration: 0.4
  },
  scale: {
    type: 'spring',
    damping: 25,
    stiffness: 120,
    duration: 0.5
  },
  elegant: {
    type: 'spring',
    damping: 30,
    stiffness: 100,
    mass: 0.8
  }
};

const PageTransition: React.FC<PageTransitionProps> = ({ 
  children, 
  className = '', 
  variant = 'elegant' 
}) => {
  return (
    <motion.div
      initial="initial"
      animate="in"
      exit="out"
      variants={pageVariants[variant]}
      transition={pageTransitions[variant]}
      className={`w-full h-full ${className}`}
      style={{ willChange: 'transform, opacity, filter' }}
    >
      {children}
    </motion.div>
  );
};

export default PageTransition;
