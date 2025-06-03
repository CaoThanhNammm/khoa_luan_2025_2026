import React, { useState } from 'react';
import { useTypewriter } from '../../hooks/useTypewriter';
import CodeBlock from './CodeBlock';

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
  const [codeCopied, setCodeCopied] = useState<{ [key: number]: boolean }>({});
  
  console.log('TypewriterText props:', { text: text.substring(0, 50) + '...', enabled, speed });
    const { displayedText, isTyping } = useTypewriter({
    text,
    speed,
    startDelay,
    enabled
  });

  // Copy code to clipboard function
  const copyCodeToClipboard = async (code: string, blockIndex: number) => {
    try {
      await navigator.clipboard.writeText(code);
      setCodeCopied(prev => ({ ...prev, [blockIndex]: true }));
      setTimeout(() => {
        setCodeCopied(prev => ({ ...prev, [blockIndex]: false }));
      }, 2000);
    } catch (err) {
      console.error('Failed to copy code: ', err);
    }
  };

  console.log('TypewriterText state:', { 
    displayedText: displayedText.substring(0, 50) + '...', 
    isTyping,
    originalLength: text.length,
    displayedLength: displayedText.length
  });  // Hàm format message với typewriter effect
  const formatMessage = (content: string) => {
    // Thêm cursor vào cuối text nếu đang typing
    const contentWithCursor = isTyping && enabled ? content + '|' : content;
    
    // Enhanced detection for incomplete code blocks
    const patterns = [
      /```[^`]*$/,           // Standard incomplete: ```java
      /```\w*\n[\s\S]*$/,    // With language and content: ```java\ncode...
      /```\s*\n[\s\S]*$/     // With whitespace: ```\ncode...
    ];
    
    let incompleteCodeMatch = null;
    for (const pattern of patterns) {
      incompleteCodeMatch = contentWithCursor.match(pattern);
      if (incompleteCodeMatch) break;
    }
    
    // If we have an incomplete code block at the end, we're typing inside it
    const isTypingInCodeBlock = incompleteCodeMatch && isTyping;
    
    console.log('formatMessage analysis:', {
      isTyping,
      hasIncompleteCode: !!incompleteCodeMatch,
      isTypingInCodeBlock,
      contentLength: content.length,
      lastChars: content.slice(-20)
    });
    
    if (isTypingInCodeBlock) {
      // Split into parts: before code block, incomplete code block
      const beforeCode = contentWithCursor.substring(0, contentWithCursor.lastIndexOf('```'));
      const codePartWithOpening = contentWithCursor.substring(contentWithCursor.lastIndexOf('```'));
      const codeContent = codePartWithOpening.slice(3); // Remove opening ```
      const lines = codeContent.split('\n');
      const language = lines[0]?.trim() || '';
      const code = lines.slice(1).join('\n');
      
      console.log('Rendering incomplete code block:', { language, codeLength: code.length });
        return (
        <div className="space-y-3">
          {/* Render content before code block */}
          {beforeCode && formatCompleteContent(beforeCode)}
          {/* Render incomplete code block using CodeBlock component */}
          <CodeBlock
            code={code}
            language={language}
            blockIndex={-1}
            copied={codeCopied[-1] || false}
            onCopy={copyCodeToClipboard}
          />
        </div>
      );
    }
    
    // Normal processing for complete content
    return formatCompleteContent(contentWithCursor);
  };
  const formatCompleteContent = (content: string) => {
    console.log('formatCompleteContent input:', content.substring(0, 100) + '...');
    
    // Improved regex to handle code blocks more robustly
    // This will match ```...``` blocks, including those with various whitespace patterns
    const codeBlockRegex = /(```[\s\S]*?```)/g;
    const blocks = content.split(codeBlockRegex);
    
    console.log('Split blocks:', blocks.map(b => ({ 
      type: b.startsWith('```') ? 'code' : 'text', 
      content: b.substring(0, 50) + '...' 
    })));
    
    return (
      <div className="space-y-3">
        {blocks.map((block, blockIdx) => {
          // Skip empty blocks
          if (!block.trim()) {
            return null;
          }
          
          // More robust code block detection
          const isCodeBlock = block.match(/^```[\s\S]*```$/);
          
          if (isCodeBlock) {
            console.log('Processing code block:', block.substring(0, 100) + '...');
            
            // Extract code content more carefully
            let codeContent = block.slice(3, -3); // Remove opening and closing ```
            
            // Handle edge case where there might be extra whitespace
            codeContent = codeContent.replace(/^\n/, '').replace(/\n$/, '');
            
            const lines = codeContent.split('\n');
            const firstLine = lines[0] || '';
            
            // Language detection - handle various formats
            let language = '';
            let code = codeContent;
            
            // Check if first line looks like a language identifier
            if (firstLine.trim().length < 20 && !firstLine.includes(' ') && !firstLine.includes('{')) {
              language = firstLine.trim();
              code = lines.slice(1).join('\n');
            }
              console.log('Detected language:', language, 'Code length:', code.length);
            
            return (
              <CodeBlock
                key={blockIdx}
                code={code}
                language={language}
                blockIndex={blockIdx}
                copied={codeCopied[blockIdx] || false}
                onCopy={copyCodeToClipboard}
              />
            );
          }

          // Handle regular text blocks
          return formatTextBlock(block, blockIdx);
        })}
      </div>
    );
  };  const formatTextBlock = (content: string, blockIdx: number) => {
    // More strict fallback detection - only for blocks that are clearly code
    const hasMultipleCodePatterns = [
      content.match(/^\s*(import\s+|from\s+.*import)/m),      // import statements
      content.match(/^\s*(public|private|protected)\s+(class|static|void)/m), // Java/C# modifiers
      content.match(/^\s*(function\s+\w+\s*\(|const\s+\w+\s*=\s*\()/m), // JS functions
      content.match(/^\s*(def\s+\w+\s*\(|class\s+\w+.*:)/m), // Python functions/classes
      content.match(/^\s*#include\s*<.*>/m),                  // C/C++ includes
      content.match(/\w+\s*\([^)]*\)\s*{[\s\S]*}/),          // Function with body
      content.match(/^\s*(for|while|if)\s*\([^)]*\)\s*{/m)   // Control structures
    ].filter(Boolean);    // Only treat as code if:
    // 1. Has multiple code patterns (not just mentioning keywords)
    // 2. Has multiple lines 
    // 3. Doesn't look like natural language (low ratio of articles/prepositions)
    const textLines = content.split('\n');
    const hasMultipleLines = textLines.length > 2;
    
    // Check if it looks like natural language vs code
    const naturalLanguageWords = /\b(the|a|an|and|or|but|in|on|at|to|for|of|with|by|from|about|into|through|during|before|after|above|below|up|down|out|off|over|under|again|further|then|once|when|where|why|how|all|any|both|each|few|more|most|other|some|such|no|nor|not|only|own|same|so|than|too|very|can|will|just|should|now)\b/gi;
    const naturalLanguageMatches = content.match(naturalLanguageWords) || [];
    const totalWords = content.split(/\s+/).length;
    const naturalLanguageRatio = naturalLanguageMatches.length / totalWords;
    
    const isLikelyCode = (
      hasMultipleCodePatterns.length >= 2 && 
      hasMultipleLines && 
      naturalLanguageRatio < 0.3 // Less than 30% natural language words
    );
      if (isLikelyCode) {
      console.log('Fallback: Detected code-like content in text block:', {
        patterns: hasMultipleCodePatterns.length,
        lines: textLines.length,
        naturalRatio: naturalLanguageRatio,
        content: content.substring(0, 100)
      });
      
      // Use CodeBlock component for auto-detected code
      return (
        <CodeBlock
          key={blockIdx}
          code={content.trim()}
          language="" // Auto-detected code, no specific language
          blockIndex={blockIdx}
          copied={codeCopied[blockIdx] || false}
          onCopy={copyCodeToClipboard}
          isAutoDetected={true}
        />
      );
    }
    // Split text into lines for normal processing
    const lines = textLines;
    
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
