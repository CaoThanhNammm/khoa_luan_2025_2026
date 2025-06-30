import React, { useEffect, useState } from 'react';
import { BiCopy, BiCheck } from 'react-icons/bi';
import Prism from 'prismjs';

// Import CSS theme trước
import 'prismjs/themes/prism-tomorrow.css';

// Import các ngôn ngữ phổ biến
import 'prismjs/components/prism-javascript';
import 'prismjs/components/prism-typescript';
import 'prismjs/components/prism-java';
import 'prismjs/components/prism-python';
import 'prismjs/components/prism-css';
import 'prismjs/components/prism-markup';
import 'prismjs/components/prism-json';
import 'prismjs/components/prism-sql';
import 'prismjs/components/prism-bash';
import 'prismjs/components/prism-c';
import 'prismjs/components/prism-cpp';
import 'prismjs/components/prism-csharp';
import 'prismjs/components/prism-php';
import 'prismjs/components/prism-go';
import 'prismjs/components/prism-rust';

interface CodeBlockProps {
  code: string;
  language: string;
  blockIndex: number;
  copied: boolean;
  onCopy: (code: string, blockIndex: number) => void;
  isAutoDetected?: boolean;
}

const CodeBlock: React.FC<CodeBlockProps> = ({
  code,
  language,
  blockIndex,
  copied,
  onCopy,
  isAutoDetected = false
}) => {
  const [highlightedCode, setHighlightedCode] = useState('');

  useEffect(() => {
    // Normalize language name
    const normalizedLang = language.toLowerCase();
    const langMap: { [key: string]: string } = {
      'js': 'javascript',
      'ts': 'typescript',
      'py': 'python',
      'rb': 'ruby',
      'sh': 'bash',
      'shell': 'bash',
      'yml': 'yaml',
      'xml': 'markup',
      'html': 'markup'
    };

    const prismLang = langMap[normalizedLang] || normalizedLang;

    try {
      // Kiểm tra xem ngôn ngữ có được hỗ trợ không
      if (Prism.languages[prismLang]) {
        const highlighted = Prism.highlight(code, Prism.languages[prismLang], prismLang);
        setHighlightedCode(highlighted);
      } else {
        // Fallback to plain text if language not supported
        setHighlightedCode(code);
      }
    } catch (error) {
      console.warn('Prism highlighting failed:', error);
      setHighlightedCode(code);
    }
  }, [code, language]);
  return (
    <div className="my-4 w-full">
      <div className="bg-gray-900 dark:bg-gray-950 rounded-xl overflow-hidden border border-gray-200 dark:border-gray-700 relative group shadow-lg">
        {/* Language header with copy button */}
        <div className="bg-gray-800 dark:bg-gray-900 px-4 py-3 text-xs font-medium text-gray-300 dark:text-gray-400 border-b border-gray-700 flex justify-between items-center">
          <span className="capitalize font-semibold">
            {isAutoDetected ? 'Code (Auto-detected)' : (language || 'Code')}
          </span>
          <button
            onClick={() => onCopy(code, blockIndex)}
            className="opacity-70 hover:opacity-100 transition-all duration-200 p-1.5 rounded hover:bg-gray-700 text-gray-400 hover:text-gray-200 flex items-center gap-1"
            title="Copy code"
          >
            {copied ? <BiCheck className="h-3 w-3" /> : <BiCopy className="h-3 w-3" />}
            <span className="text-xs">Copy</span>
          </button>
        </div>
          {/* Code content */}
        <div className="relative">
          <div className="p-4 overflow-x-auto bg-gray-900 dark:bg-gray-950 max-h-96 overflow-y-auto custom-scrollbar">
            <pre className={`language-${language} !bg-transparent !p-0 !m-0`}>
              <code 
                className={`language-${language} !bg-transparent`}
                dangerouslySetInnerHTML={{ __html: highlightedCode }}
              />
            </pre>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CodeBlock;
