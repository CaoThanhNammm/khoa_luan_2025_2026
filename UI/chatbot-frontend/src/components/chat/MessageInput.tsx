import React, { useState, useRef } from 'react';
import { BiPaperPlane, BiPaperclip } from 'react-icons/bi';
import { useSettings } from '../../context/SettingsContext';
import { useTranslation } from '../../utils/translations';

interface MessageInputProps {
  onSendMessage: (message: string) => void;
  onFileUpload?: (file: File) => Promise<void>;
  isTyping: boolean;
  isUploading?: boolean;
  conversationId?: number;
}

const MessageInput: React.FC<MessageInputProps> = ({ 
  onSendMessage, 
  onFileUpload, 
  isTyping, 
  isUploading = false}) => {
  const [inputMessage, setInputMessage] = useState('');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { settings, showNotification } = useSettings();
  const { t } = useTranslation(settings.language);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputMessage.trim() || isTyping || isUploading) return;
    
    onSendMessage(inputMessage);
    setInputMessage('');
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e as React.FormEvent);
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file && file.type === 'application/pdf') {
      // Check file size (max 10MB)
      const maxSize = 10 * 1024 * 1024; // 10MB in bytes
      if (file.size > maxSize) {
        showNotification('File size must be less than 10MB', 'error');
        if (fileInputRef.current) {
          fileInputRef.current.value = '';
        }
        return;
      }
      setSelectedFile(file);
    } else if (file) {
      showNotification('Please select a PDF file', 'error');
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  const handleFileUpload = async () => {
    if (!selectedFile || !onFileUpload || isUploading) return;
    
    try {
      await onFileUpload(selectedFile);
      setSelectedFile(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    } catch (error) {
      console.error('File upload failed:', error);
    }
  };

  const handleRemoveFile = () => {
    setSelectedFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handlePaperclipClick = () => {
    if (!isUploading && !isTyping) {
      fileInputRef.current?.click();
    }
  };

  return (
    <div className="border-t border-white/20 dark:border-gray-700/20 bg-white/90 dark:bg-gray-800/90 backdrop-blur-xl px-6 py-4 shadow-xl shadow-gray-100/50 dark:shadow-gray-900/50 transition-colors duration-300">
      {/* File Upload Input (Hidden) */}
      <input
        ref={fileInputRef}
        type="file"
        accept=".pdf"
        onChange={handleFileSelect}
        className="hidden"
        disabled={isUploading || isTyping}
      />

      {/* Selected File Preview */}
      {selectedFile && (
        <div className="mb-3 flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-xl border border-gray-200/50 dark:border-gray-600/50">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-red-100 dark:bg-red-900/30 rounded-lg">
              <svg className="w-4 h-4 text-red-600 dark:text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <div>
              <p className="text-sm font-medium text-gray-700 dark:text-gray-300">
                {selectedFile.name}
              </p>
              <p className="text-xs text-gray-500 dark:text-gray-400">
                {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
              </p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <button
              onClick={handleFileUpload}
              disabled={isUploading || isTyping}
              className={`
                px-3 py-1.5 text-xs font-medium rounded-lg transition-all duration-200
                ${isUploading
                  ? 'bg-gray-300 dark:bg-gray-600 text-gray-500 cursor-not-allowed'
                  : 'bg-blue-500 hover:bg-blue-600 text-white shadow-md hover:shadow-lg'
                }
              `}
            >
              {isUploading ? (
                <div className="flex items-center space-x-1">
                  <svg className="w-3 h-3 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                  <span>Uploading...</span>
                </div>
              ) : (
                'Upload'
              )}
            </button>
            
            <button
              onClick={handleRemoveFile}
              disabled={isUploading || isTyping}
              className="p-1.5 text-gray-400 hover:text-red-500 transition-colors duration-200 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-600"
            >
              <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      )}

      <form onSubmit={handleSubmit} className="flex space-x-4 items-end">
        <div className="flex-1 relative group">
          {/* Paperclip Icon */}
          {onFileUpload && (
            <button
              type="button"
              onClick={handlePaperclipClick}
              disabled={isTyping || isUploading}
              className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300 transition-colors duration-200 disabled:opacity-40 disabled:cursor-not-allowed z-10"
              title={isUploading ? "Uploading..." : "Upload PDF file"}
            >
              {isUploading ? (
                <svg className="h-5 w-5 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
              ) : (
                <BiPaperclip className="h-5 w-5" />
              )}
            </button>
          )}
          
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={t('chat.placeholder')}
            className={`w-full py-4 pr-14 border-2 border-gray-200/80 dark:border-gray-600/80 rounded-2xl focus:outline-none focus:ring-4 focus:ring-lavender/30 dark:focus:ring-indigo-500/30 focus:border-lavender dark:focus:border-indigo-500 transition-all duration-300 bg-white/90 dark:bg-gray-700/90 backdrop-blur-sm shadow-lg shadow-gray-100/50 dark:shadow-gray-900/50 font-medium placeholder-gray-500 dark:placeholder-gray-400 text-charcoal dark:text-white group-hover:shadow-xl ${
              onFileUpload ? 'pl-12' : 'pl-5'
            }`}
            disabled={isTyping || isUploading}
            maxLength={1000}
          />
          <div className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400 dark:text-gray-500">
            <div className="text-xs font-semibold bg-gray-100 dark:bg-gray-600 px-2 py-1 rounded-lg">
              {inputMessage.length}/1000
            </div>
          </div>
        </div>
        <button
          type="submit"
          disabled={!inputMessage.trim() || isTyping || isUploading}
          className="h-14 w-14 bg-gradient-to-br from-charcoal via-gray-800 to-slate-900 dark:from-indigo-600 dark:via-indigo-700 dark:to-indigo-800 text-white rounded-2xl disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center shadow-lg shadow-charcoal/20 dark:shadow-indigo-500/20 hover:shadow-xl hover:shadow-charcoal/30 dark:hover:shadow-indigo-500/30 transition-all duration-300 transform hover:scale-110 disabled:hover:scale-100 active:scale-95"
        >
          <BiPaperPlane className="h-6 w-6 transform transition-transform group-hover:translate-x-0.5 group-hover:-translate-y-0.5" />
        </button>
      </form>
      <div className="text-xs text-gray-500 dark:text-gray-400 mt-3 text-center font-medium flex items-center justify-center space-x-4 transition-colors duration-300">
        <span className="flex items-center space-x-1">
          <kbd className="px-2 py-1 bg-gray-100 dark:bg-gray-600 rounded text-xs font-semibold">Enter</kbd>
          <span>{t('chat.enter_to_send')}</span>
        </span>
        <span className="text-gray-300 dark:text-gray-600">•</span>
        <span className="flex items-center space-x-1">
          <kbd className="px-2 py-1 bg-gray-100 dark:bg-gray-600 rounded text-xs font-semibold">Shift</kbd>
          <span>+</span>
          <kbd className="px-2 py-1 bg-gray-100 dark:bg-gray-600 rounded text-xs font-semibold">Enter</kbd>
          <span>{t('chat.shift_enter')}</span>
        </span>
      </div>
    </div>
  );
};

export default MessageInput;
