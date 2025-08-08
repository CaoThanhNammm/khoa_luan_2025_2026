import React, { useState, memo } from 'react';
import { BiBot, BiUser, BiCopy, BiCheck } from 'react-icons/bi';
import type { Message } from '../../types/chat';
import TypewriterText from './TypewriterText';
import CodeBlock from './CodeBlock';

interface MessageItemProps {
  message: Message;
  index: number;
}

const                                                               MessageItem: React.FC<MessageItemProps> = memo(({ message, index }) => {
  const [copied, setCopied] = useState(false);
  const [codeCopied, setCodeCopied] = useState<{ [key: number]: boolean }>({});

  const formatTime = (timestamp: string): string => {
    return new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(message.content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy text: ', err);
    }
  };

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

  // Check if message contains code blocks
const formatMessage = (content: string) => {
    // Split content into blocks (text vs code blocks)
    const blocks = content.split(/(```[\s\S]*?```)/g);
    
    return (
      <div className="space-y-3">
        {blocks.map((block, blockIdx) => {
          // Handle code blocks
          if (block.startsWith('```') && block.endsWith('```')) {
            const codeContent = block.slice(3, -3);
            const lines = codeContent.split('\n');
            
            // Extract language from first line if present
            let language = '';
            let codeLines = lines;
            if (lines[0] && !lines[0].includes(' ') && lines[0].trim().length < 20) {
              language = lines[0].trim();
              codeLines = lines.slice(1);            }

            return (
              <CodeBlock
                key={blockIdx}
                code={codeLines.join('\n')}
                language={language}
                blockIndex={blockIdx}
                copied={codeCopied[blockIdx] || false}
                onCopy={copyCodeToClipboard}
              />
            );
          }
          
          // Handle regular text blocks
          return (
            <div key={blockIdx}>
              {formatTextBlock(block)}
            </div>
          );
        })}
      </div>
    );
  };

  const formatTextBlock = (content: string) => {
    const lines = content.split('\n');
    
    return (
      <div className="space-y-2">
        {lines.map((line, idx) => {
          const trimmedLine = line.trim();
          
          // Handle bullet points (single * followed by space)
          // Match patterns like "* Text" but not "**bold**"
          const isBulletPoint = trimmedLine.match(/^\*\s/) && !trimmedLine.match(/^\*\*/);
          if (isBulletPoint) {
            const bulletText = trimmedLine.substring(1).trim();
            return (
              <div key={idx} className="bullet-point">
                <span className="bullet-marker">•</span>
                <span className="bullet-content">{formatInlineText(bulletText)}</span>
              </div>
            );
          }
          
          // Handle numbered lists
          const numberedMatch = trimmedLine.match(/^(\d+)\.\s*(.+)/);
          if (numberedMatch) {
            return (
              <div key={idx} className="bullet-point">
                <span className="bullet-marker">{numberedMatch[1]}.</span>
                <span className="bullet-content">{formatInlineText(numberedMatch[2])}</span>
              </div>
            );
          }          // Handle standalone bold text lines
          if (trimmedLine.startsWith('**') && trimmedLine.endsWith('**') && trimmedLine.length > 4) {
            const boldText = trimmedLine.slice(2, -2);
            return (
              <div key={idx} className="chat-text-bold my-3 text-base">
                {boldText}
              </div>
            );
          }
          
          // Handle regular text with inline formatting
          if (trimmedLine) {
            return (
              <div key={idx} className="my-2 leading-relaxed">
                {formatInlineText(trimmedLine)}
              </div>
            );
          }
          
          // Handle empty lines
          return <div key={idx} className="h-2"></div>;
        })}
      </div>
    );
  };
  const formatInlineText = (text: string) => {
    // Handle both bold text and inline code
    const parts = text.split(/(\*\*[^*]+\*\*|`[^`]+`)/g);
    return (
      <>        {parts.map((part, idx) => {
          if (part.startsWith('**') && part.endsWith('**')) {
            return (
              <span key={idx} className="chat-text-bold">
                {part.slice(2, -2)}
              </span>
            );
          }          if (part.startsWith('`') && part.endsWith('`')) {
            return (
              <code key={idx} className="px-1.5 py-0.5 mx-0.5 bg-gray-100 dark:bg-gray-800 text-black dark:text-black rounded text-sm font-mono border border-gray-200 dark:border-gray-700">
                {part.slice(1, -1)}
              </code>
            );
          }
          return <span key={idx}>{part}</span>;
        })}
      </>
    );
  };

  const isUser = message.type === 'USER';

  return (
    <div
      className={`flex items-start space-x-4 opacity-0 animate-fade-in group ${
        isUser ? 'flex-row-reverse space-x-reverse' : ''
      }`}
      style={{ animationDelay: `${index * 0.1}s` }}
    >      <div className={`h-10 w-10 rounded-2xl flex items-center justify-center flex-shrink-0 shadow-lg ${
        isUser 
          ? 'bg-gradient-to-br from-charcoal via-gray-800 to-slate-900 shadow-charcoal/20 dark:from-blue-600 dark:via-blue-700 dark:to-blue-800'
          : 'bg-gradient-to-br from-lavender via-purple-200 to-sky-blue shadow-lavender/20 dark:from-slate-600 dark:via-slate-700 dark:to-slate-800'
      }`}>
        {isUser ? (
          <BiUser className="h-5 w-5 text-white" />
        ) : (
          <BiBot className="h-5 w-5 text-charcoal dark:text-white" />
        )}
      </div>
      
      <div className={`flex flex-col max-w-xs lg:max-w-2xl xl:max-w-3xl ${isUser ? 'items-end' : 'items-start'}`}>        <div className={`relative px-5 py-4 rounded-2xl shadow-lg ${
          isUser 
            ? 'bg-gradient-to-br from-charcoal via-gray-800 to-slate-900 text-white shadow-charcoal/20 dark:from-blue-600 dark:via-blue-700 dark:to-blue-800'
            : 'bg-white/95 backdrop-blur-sm text-charcoal border border-white/50 shadow-gray-100/80 dark:bg-slate-800/90 dark:text-gray-100 dark:border-slate-700/50'
        }`}>          <div className="text-sm chat-text text-crisp">
            {!isUser && (message.isStreaming || message.isLatest) ? (
              <TypewriterText 
                text={message.content}
                speed={30}
                enabled={message.isStreaming !== false}
              />
            ) : (
              formatMessage(message.content)
            )}
          </div>
            {/* Copy button - only show for bot messages */}
          {!isUser && (
            <button
              onClick={copyToClipboard}
              className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200 p-1.5 rounded-lg bg-gray-100/80 dark:bg-slate-700/80"
              title="Copy message"
            >
              {copied ? (
                <BiCheck className="h-4 w-4 text-green-500" />
              ) : (
                <BiCopy className="h-4 w-4 text-gray-500 dark:text-gray-400" />
              )}
            </button>
          )}
          
          {/* Enhanced message tail */}
          <div className={`absolute top-4 w-3 h-3 transform rotate-45 ${
            isUser
              ? 'bg-gradient-to-br from-charcoal to-gray-800 -right-1.5 dark:from-blue-600 dark:to-blue-800'
              : 'bg-white/95 border-l border-b border-white/50 -left-1.5 dark:bg-slate-800/90 dark:border-slate-700/50'
          }`}></div>
        </div>
          <span className="text-xs text-gray-500 dark:text-gray-400 mt-2 px-2 chat-timestamp opacity-70">
          {formatTime(message.timestamp)}
        </span>
      </div>    </div>
  );
});

export default MessageItem;
