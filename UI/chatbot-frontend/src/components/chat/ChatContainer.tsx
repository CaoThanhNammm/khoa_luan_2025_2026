import React from 'react';
import ChatHeader from './ChatHeader';
import ChatMessages from './ChatMessages';
import MessageInput from './MessageInput';
import SuggestedQuestions from './SuggestedQuestions';
import type { Message, DocumentInfo } from '../../types/chat';

interface ChatContainerProps {
  messages: Message[];
  isTyping: boolean;
  isThinking?: boolean;
  pendingMessage?: Message | null;
  onSendMessage: (message: string) => void;
  onFileUpload?: (file: File) => Promise<void>;
  isUploading?: boolean;
  conversationId?: string;
  hasDocument?: boolean;
  documentInfo?: DocumentInfo;
  showSuggestedQuestions?: boolean;
}

const ChatContainer: React.FC<ChatContainerProps> = ({
  messages,
  isTyping,
  isThinking = false,
  pendingMessage = null,
  onSendMessage,
  onFileUpload,
  isUploading = false,
  conversationId,
  hasDocument = false,
  documentInfo,
  showSuggestedQuestions = false
}) => {
  // Ẩn file upload nếu đang chat với sổ tay sinh viên (tài liệu mặc định)
  const isDefaultDocument = documentInfo?.documentId === 'so-tay-sinh-vien-2024';
  const shouldShowFileUpload = onFileUpload && !isDefaultDocument;

  return (
    <div className="flex-1 flex flex-col h-full bg-gradient-to-br from-slate-50 via-purple-50/30 to-blue-50/40 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900 transition-colors duration-500 relative overflow-hidden">
      {/* Enhanced decorative background elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-lavender/10 to-sky-blue/10 dark:from-indigo-500/10 dark:to-purple-500/10 rounded-full blur-3xl animate-float"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-gradient-to-tr from-sky-blue/10 to-lavender/10 dark:from-purple-500/10 dark:to-indigo-500/10 rounded-full blur-3xl animate-float" style={{ animationDelay: '1s' }}></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-gradient-to-r from-purple-200/5 to-blue-200/5 dark:from-indigo-400/5 dark:to-purple-400/5 rounded-full blur-3xl animate-aurora"></div>
      </div>
      
      <ChatHeader 
        isTyping={isTyping || isThinking} 
        hasDocument={hasDocument}
        documentInfo={documentInfo}
      />
      <div className="flex-1 flex flex-col min-h-0 bg-white/90 dark:bg-slate-800/90 backdrop-blur-xl shadow-xl shadow-gray-100/50 dark:shadow-slate-900/50 border border-gray-200/60 dark:border-slate-700/60 rounded-2xl mx-4 mb-4 transition-all duration-300 relative z-10 overflow-hidden">
        {showSuggestedQuestions && messages.length === 0 ? (
          <>
            <div className="flex-1 min-h-0">
              <SuggestedQuestions 
                onQuestionClick={onSendMessage} 
                documentId={documentInfo?.documentId}
                filename={documentInfo?.filename}
              />
            </div>
            <div className="flex-shrink-0">
              <MessageInput 
                onSendMessage={onSendMessage} 
                onFileUpload={shouldShowFileUpload ? onFileUpload : undefined}
                isTyping={isTyping || isThinking}
                isUploading={isUploading}
                conversationId={conversationId}
              />
            </div>
          </>
        ) : (
          <>
            <div className="flex-1 min-h-0">
              <ChatMessages messages={messages} isTyping={isTyping} isThinking={isThinking} pendingMessage={pendingMessage} />
            </div>
            <div className="flex-shrink-0">
              <MessageInput 
                onSendMessage={onSendMessage} 
                onFileUpload={shouldShowFileUpload ? onFileUpload : undefined}
                isTyping={isTyping || isThinking}
                isUploading={isUploading}
                conversationId={conversationId}
              />
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default ChatContainer;
