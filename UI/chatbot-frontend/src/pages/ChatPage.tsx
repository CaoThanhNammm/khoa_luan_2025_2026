import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useChat } from '../context/ChatContext';
import { useSettings } from '../context/SettingsContext';
// import { useTranslation } from '../utils/translations';
import { useNavigate } from 'react-router-dom';
import { ChatSidebar, ChatContainer, FileDropZone, WelcomeScreen } from '../components/chat';
import { FileUploadService } from '../services/FileUploadService';
import type { ChatSession, SidebarChatSession } from '../types/chat';
import PageTransition from '../components/PageTransition';

const ChatPage: React.FC = () => {
  const { user } = useAuth();
  const { showNotification } = useSettings();
  // const { t } = useTranslation(settings.language);
  const navigate = useNavigate();
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [isUploading, setIsUploading] = useState(false);
  const [showFileDropZone, setShowFileDropZone] = useState(false);
  
  const chatContext = useChat();

  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }
  }, [user, navigate]);

  // Hide file drop zone when a conversation is selected
  useEffect(() => {
    if (chatContext.currentConversation && showFileDropZone) {
      setShowFileDropZone(false);
    }
  }, [chatContext.currentConversation, showFileDropZone]);

  // Get messages from current conversation directly (no conversion needed)
  const messages = chatContext.currentConversation?.messages || [];

  const handleSendMessage = async (inputMessage: string) => {
    if (!inputMessage.trim()) return;

    try {
      if (chatContext.currentConversation) {
        // Check if this is a temporary conversation (with suggested questions)
        const isTemporaryConversation = chatContext.currentConversation.id.startsWith('temp_'); // Temporary IDs start with 'temp_'
        
        if (isTemporaryConversation) {
          // For temporary conversations, check if it has document info
          const hasDocument = chatContext.currentConversation.hasDocument;
          const documentId = chatContext.currentConversation.documentInfo?.documentId;
          
          if (hasDocument && documentId) {
            // Create conversation with document (for student handbook)
            await chatContext.createNewConversationWithDocument(inputMessage, documentId);
          } else {
            // Create regular conversation
            await chatContext.createNewConversation(inputMessage);
          }
        } else {
          // Send message to existing conversation
          await chatContext.sendMessage(chatContext.currentConversation.id, inputMessage);
        }
      } else {
        // Create new conversation
        await chatContext.createNewConversation(inputMessage);
      }
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };  const handleCreateNewSession = async (type: 'default' | 'upload') => {
    // Clear the current conversation to start fresh
    chatContext.clearError(); // Clear any existing errors
    chatContext.clearCurrentConversation(); // Clear the current conversation
    
    // If it's a default session, create a new conversation with suggested questions
    if (type === 'default') {
      try {
        // Hide file drop zone if it's currently showing
        setShowFileDropZone(false);
        // Create a new conversation with suggested questions (no initial message)
        await chatContext.createNewConversationWithSuggestedQuestions();
      } catch (error) {
        console.error('Error creating default session:', error);
      }
    } else {
      // For upload type, show file drop zone
      setShowFileDropZone(true);
    }
  };

  const handleSwitchToSession = async (conversationId: string) => {
    setShowFileDropZone(false); // Hide file drop zone when switching conversations
    await chatContext.switchToConversation(conversationId);
  };

  const handleDeleteSession = async (conversationId: string) => {
    await chatContext.deleteConversation(conversationId);
  };

  const handleFileUpload = async (file: File) => {
    // Prevent multiple simultaneous uploads
    if (isUploading) {
      showNotification('Upload already in progress. Please wait...', 'info');
      return;
    }

    // Validate file size (10MB = 10 * 1024 * 1024 bytes)
    const maxFileSize = 10 * 1024 * 1024;
    if (file.size > maxFileSize) {
      showNotification(
        `File size exceeds 10MB limit. Current size: ${(file.size / (1024 * 1024)).toFixed(2)}MB`,
        'error'
      );
      return;
    }

    setIsUploading(true);
    
    try {
      const response = await FileUploadService.uploadFile(file);
      
      // Check if upload was successful or is processing
      if (response && (response.document_id || response.filename || response.message)) {
        const filename = response.filename || file.name;
        const documentId = response.document_id || 'unknown';
        const fileSize = response.file_size || file.size;
        
        // Always show success message after upload completes
        showNotification(
          `File "${filename}" uploaded successfully!`,
          'success'
        );
        
        // Create empty conversation with uploaded document using document_id and full file info
        await chatContext.createEmptyConversationWithUploadedDocument(
          documentId, 
          filename, 
          fileSize,
          response.status,
          response.s3_key,
          response.s3_url
        );
        
        // Hide file drop zone after successful upload
        setShowFileDropZone(false);
      } else {
        throw new Error('Upload failed - no response data received');
      }
    } catch (error) {
      console.error('File upload failed:', error);
      let errorMessage = 'Unknown error occurred';
      
      if (error instanceof Error) {
        if (error.message.includes('timeout')) {
          errorMessage = 'Upload timeout - file processing took too long. Please try again with a smaller file.';
        } else if (error.message.includes('Network')) {
          errorMessage = 'Network error - please check your internet connection and try again.';
        } else {
          errorMessage = error.message;
        }
      }
      
      showNotification(
        `File upload failed: ${errorMessage}`,
        'error'
      );
    } finally {
      setIsUploading(false);
    }
  };

  const handleCancelFileUpload = () => {
    setShowFileDropZone(false);
  };

  if (!user) {
    return null; // Will redirect in useEffect
  }  // Convert conversations to SidebarChatSession format for sidebar
  const chatSessions: SidebarChatSession[] = chatContext.conversations.map((conv: ChatSession) => {
    // Safely parse the timestamp
    let timestamp = new Date();
    if (conv.createdAt) {
      const parsedDate = new Date(conv.createdAt);
      if (!isNaN(parsedDate.getTime())) {
        timestamp = parsedDate;
      }
    }
    
    return {
      id: conv.id.toString(),
      title: conv.title,
      lastMessage: conv.messages.length > 0 ? conv.messages[conv.messages.length - 1].content : 'No messages yet',
      timestamp: timestamp,
      hasDocument: conv.hasDocument || false,
      documentFilename: conv.documentInfo?.filename,
      documentType: conv.documentInfo?.documentId === 'so_tay_sinh_vien_2024' ? 'default' : 'upload'
    };
  });

  const currentSessionId = chatContext.currentConversation?.id.toString() || '';
  return (
    <PageTransition>
      <div className="chat-layout flex bg-gradient-to-br from-slate-50 via-purple-50/30 to-blue-50/40 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900 relative overflow-hidden transition-colors duration-500">
        {/* Enhanced decorative background elements */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-lavender/10 to-sky-blue/10 dark:from-indigo-500/10 dark:to-purple-500/10 rounded-full blur-3xl animate-float"></div>
          <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-gradient-to-tr from-sky-blue/10 to-lavender/10 dark:from-purple-500/10 dark:to-indigo-500/10 rounded-full blur-3xl animate-float" style={{ animationDelay: '1s' }}></div>
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-gradient-to-r from-purple-200/5 to-blue-200/5 dark:from-indigo-400/5 dark:to-purple-400/5 rounded-full blur-3xl animate-aurora"></div>
        </div>

      <ChatSidebar
        isSidebarOpen={isSidebarOpen}
        setIsSidebarOpen={setIsSidebarOpen}
        chatSessions={chatSessions}
        currentSessionId={currentSessionId}
        onCreateNewSession={handleCreateNewSession}
        onSwitchToSession={handleSwitchToSession}
        onDeleteSession={handleDeleteSession}
      />

      {/* Show FileDropZone, WelcomeScreen, or ChatContainer based on state */}
      {showFileDropZone ? (
        <FileDropZone
          onFileUpload={handleFileUpload}
          isUploading={isUploading}
          onCancel={handleCancelFileUpload}
        />
      ) : chatContext.currentConversation ? (
        <ChatContainer
          messages={messages}
          isTyping={chatContext.loading}
          isThinking={chatContext.isThinking}
          pendingMessage={chatContext.pendingMessage}
          onSendMessage={handleSendMessage}
          onFileUpload={handleFileUpload}
          isUploading={isUploading}
          conversationId={chatContext.currentConversation?.id}
          hasDocument={chatContext.currentConversation?.hasDocument || false}
          documentInfo={chatContext.currentConversation?.documentInfo}
          showSuggestedQuestions={messages.length === 0 && chatContext.currentConversation?.hasDocument}
        />
      ) : (
        <WelcomeScreen
          onCreateNewSession={handleCreateNewSession}
        />
      )}

      {/* File Upload Loading Overlay */}
      {isUploading && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center">
          <div className="bg-white dark:bg-slate-800 rounded-2xl p-8 shadow-2xl border border-gray-200 dark:border-slate-700 max-w-md w-full mx-4">
            <div className="text-center">
              <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-purple-600 mx-auto mb-6"></div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">
                Đang xử lý file...
              </h3>
              <p className="text-gray-600 dark:text-gray-400 text-sm mb-4">
                Đang upload và xử lý file PDF của bạn. Quá trình này có thể mất vài phút.
              </p>
              <div className="bg-gray-100 dark:bg-slate-700 rounded-lg p-3 mb-4">
                <div className="flex items-center justify-center space-x-2 text-sm text-gray-700 dark:text-gray-300">
                  <div className="w-2 h-2 bg-purple-600 rounded-full animate-pulse"></div>
                  <span>Vui lòng không đóng trang web</span>
                </div>
              </div>
              <div className="text-xs text-gray-500 dark:text-gray-400">
                Hệ thống đang phân tích nội dung và chuẩn bị cho việc chat
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Enhanced Error Display */}
      {chatContext.error && (
        <div className="fixed bottom-4 right-4 bg-gradient-to-r from-red-500 to-rose-500 dark:from-red-600 dark:to-rose-600 text-white px-6 py-3 rounded-xl shadow-lg dark:shadow-red-500/25 backdrop-blur-xl border border-red-400/20 animate-fade-in">
          {chatContext.error}
          <button 
            onClick={chatContext.clearError}
            className="ml-3 text-white/80 hover:text-white transition-colors rounded-lg p-1 hover:bg-white/10"
          >
            ×
          </button>
        </div>        )}
      </div>
    </PageTransition>
  );
};

export default ChatPage;
