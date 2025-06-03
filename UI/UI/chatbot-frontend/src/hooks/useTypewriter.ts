import { useState, useEffect, useRef } from 'react';

interface TypewriterOptions {
  text: string;
  speed?: number;
  startDelay?: number;
  enabled?: boolean;
}

export const useTypewriter = ({ 
  text, 
  speed = 30, 
  startDelay = 0, 
  enabled = true 
}: TypewriterOptions) => {
  const [displayedText, setDisplayedText] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const indexRef = useRef(0);
  const timeoutRef = useRef<number | null>(null);

  useEffect(() => {
    console.log('useTypewriter effect triggered:', { 
      text: text.substring(0, 50) + '...', 
      enabled, 
      speed,
      textLength: text.length 
    });
    
    if (!enabled) {
      console.log('Typewriter disabled, showing full text immediately');
      setDisplayedText(text);
      setIsTyping(false);
      return;
    }

    // Reset when text changes
    console.log('Starting typewriter effect...');
    setDisplayedText('');
    setIsTyping(true);
    indexRef.current = 0;

    // Clear any existing timeout
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }

    const startTyping = () => {
      const typeNextChar = () => {
        if (indexRef.current < text.length) {
          const newText = text.slice(0, indexRef.current + 1);
          console.log(`Typing character ${indexRef.current + 1}/${text.length}: "${newText.slice(-1)}"`);
          setDisplayedText(newText);
          indexRef.current++;
          timeoutRef.current = window.setTimeout(typeNextChar, speed);
        } else {
          console.log('Typewriter finished');
          setIsTyping(false);
        }
      };

      timeoutRef.current = window.setTimeout(typeNextChar, startDelay);
    };

    startTyping();

    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, [text, speed, startDelay, enabled]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, []);

  return { displayedText, isTyping };
};
