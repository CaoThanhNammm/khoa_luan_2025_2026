import React from 'react';
import { useTypewriter } from '../../hooks/useTypewriter';

interface TypewriterTextProps {
  text: string;
  speed?: number;
  startDelay?: number;
  enabled?: boolean;
  className?: string;
}

const TypewriterText: React.FC<TypewriterTextProps> = ({
  text,
  speed = 30,
  startDelay = 0,
  enabled = true,
  className = ''
}) => {
  console.log('TypewriterText props:', { text: text.substring(0, 50) + '...', enabled, speed });
  
  const { displayedText, isTyping } = useTypewriter({
    text,
    speed,
    startDelay,
    enabled
  });

  console.log('TypewriterText state:', { 
    displayedText: displayedText.substring(0, 50) + '...', 
    isTyping,
    originalLength: text.length,
    displayedLength: displayedText.length
  });  // Hàm format message với typewriter effect
  const formatMessage = (content: string) => {
    // Thêm cursor vào cuối text nếu đang typing
    const contentWithCursor = isTyping && enabled ? content + '|' : content;
      // Detect if we're currently typing inside a code block
    const incompleteCodeMatch = contentWithCursor.match(/```[^`]*$/);
    
    // If we have an incomplete code block at the end, we're typing inside it
    const isTypingInCodeBlock = incompleteCodeMatch && isTyping;
    
    if (isTypingInCodeBlock) {
      // Split into parts: before code block, incomplete code block
      const beforeCode = contentWithCursor.substring(0, contentWithCursor.lastIndexOf('```'));
      const codePartWithOpening = contentWithCursor.substring(contentWithCursor.lastIndexOf('```'));
      const codeContent = codePartWithOpening.slice(3); // Remove opening ```
      const lines = codeContent.split('\n');
      const language = lines[0]?.trim() || '';
      const code = lines.slice(1).join('\n');
      
      return (
        <div className="space-y-3">
          {/* Render content before code block */}
          {beforeCode && formatCompleteContent(beforeCode)}
          
          {/* Render incomplete code block with frame */}
          <div className="relative bg-gray-900 rounded-lg overflow-hidden my-4">
            <div className="flex items-center justify-between px-4 py-2 bg-gray-800 border-b border-gray-700">
              <span className="text-gray-300 text-sm font-medium">
                {language || 'Code'}
              </span>
            </div>
            <pre className="p-4 overflow-x-auto">
              <code className="text-green-400 text-sm font-mono whitespace-pre">
                {code}
              </code>
            </pre>
          </div>
        </div>
      );
    }
    
    // Normal processing for complete content
    return formatCompleteContent(contentWithCursor);
  };

  const formatCompleteContent = (content: string) => {
    // Split content into blocks (text vs code blocks)
    const blocks = content.split(/(```[\s\S]*?```)/g);
    
    return (
      <div className="space-y-3">
        {blocks.map((block, blockIdx) => {
          // Handle code blocks
          if (block.startsWith('```') && block.endsWith('```')) {
            const codeContent = block.slice(3, -3);
            const lines = codeContent.split('\n');
            const language = lines[0]?.trim() || '';
            const code = lines.slice(1).join('\n');

            return (
              <div key={blockIdx} className="relative bg-gray-900 rounded-lg overflow-hidden my-4">
                <div className="flex items-center justify-between px-4 py-2 bg-gray-800 border-b border-gray-700">
                  <span className="text-gray-300 text-sm font-medium">
                    {language || 'Code'}
                  </span>
                </div>
                <pre className="p-4 overflow-x-auto">
                  <code className="text-green-400 text-sm font-mono">
                    {code}
                  </code>
                </pre>
              </div>
            );
          }

          // Handle regular text blocks
          if (block.trim()) {
            return formatTextBlock(block, blockIdx);
          }

          return null;
        })}
      </div>
    );
  };

  const formatTextBlock = (content: string, blockIdx: number) => {
    // Split text into lines for processing
    const lines = content.split('\n');
    
    return (
      <div key={blockIdx} className="space-y-2">
        {lines.map((line, lineIdx) => (
          <p key={lineIdx} className="text-gray-800 dark:text-gray-200 leading-relaxed">
            {formatInlineText(line)}
          </p>
        ))}
      </div>
    );
  };

  const formatInlineText = (text: string) => {
    // Handle both bold text, inline code, and cursor
    const parts = text.split(/(\*\*[^*]+\*\*|`[^`]+`|\|)/g);
    return (
      <>
        {parts.map((part, idx) => {
          if (part.startsWith('**') && part.endsWith('**')) {
            return (
              <span key={idx} className="chat-text-bold">
                {part.slice(2, -2)}
              </span>
            );
          }
          if (part.startsWith('`') && part.endsWith('`')) {
            return (
              <code key={idx} className="px-1.5 py-0.5 mx-0.5 bg-gray-100 dark:bg-gray-800 text-black dark:text-black rounded text-sm font-mono border border-gray-200 dark:border-gray-700">
                {part.slice(1, -1)}
              </code>
            );
          }
          // Handle cursor
          if (part === '|') {
            return (
              <span key={idx} className="inline-block w-0.5 h-4 bg-blue-500 animate-pulse ml-0.5" 
                    style={{ animation: 'blink 1s infinite' }} />
            );
          }
          return <span key={idx}>{part}</span>;
        })}
      </>
    );
  };  return (
    <div className={className}>
      <style>{`
        @keyframes blink {
          0%, 50% { opacity: 1; }
          51%, 100% { opacity: 0; }
        }
      `}</style>
      {formatMessage(displayedText)}
    </div>
  );
};

export default TypewriterText;
