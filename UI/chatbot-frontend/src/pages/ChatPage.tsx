import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useChat } from '../context/ChatContext';
import { useSettings } from '../context/SettingsContext';
import { useTranslation } from '../utils/translations';
import { useNavigate } from 'react-router-dom';
import { ChatSidebar, ChatContainer, FileDropZone } from '../components/chat';
import { FileUploadService } from '../services/FileUploadService';
import type { ChatSession, SidebarChatSession } from '../types/chat';
import PageTransition from '../components/PageTransition';

const ChatPage: React.FC = () => {
  const { user } = useAuth();
  const { settings, showNotification } = useSettings();
  const { t } = useTranslation(settings.language);
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
        // Send message to existing conversation
        await chatContext.sendMessage(chatContext.currentConversation.id, inputMessage);
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
    
    // If it's a default session, create a new conversation with default document
    if (type === 'default') {
      try {
        // Hide file drop zone if it's currently showing
        setShowFileDropZone(false);
        // Create a new conversation with the default document
        const defaultMessage = "Xin chào, tôi muốn tìm hiểu về thông tin trong sổ tay sinh viên.";
        await chatContext.createNewConversationWithDocument(defaultMessage, 'so-tay-sinh-vien-2024');
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
    await chatContext.switchToConversation(Number(conversationId));
  };

  const handleDeleteSession = async (conversationId: string) => {
    await chatContext.deleteConversation(Number(conversationId));
  };

  const handleFileUpload = async (file: File) => {
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
      // Get current conversation ID if available
      const conversationId = chatContext.currentConversation?.id;
      console.log('Uploading file with conversation ID:', conversationId);
      
      const response = await FileUploadService.uploadFile(file, conversationId);
      
      // Check if upload was successful or is processing
      if (response && (response.document_id || response.filename || response.message)) {
        const filename = response.filename || file.name;
        const documentId = response.document_id || 'unknown';
        const status = response.status || 'success';
        
        if (status === 'processing') {
          showNotification(
            `File "${filename}" uploaded and is being processed. You can start chatting while processing continues in the background.`,
            'info'
          );
        } else {
          showNotification(
            `File "${filename}" uploaded successfully! Document ID: ${documentId}${conversationId ? ` linked to conversation ${conversationId}` : ''}`,
            'success'
          );
        }
        
        // Create appropriate message based on processing status
        const chatMessage = status === 'processing' 
          ? `I've uploaded a PDF file: ${filename}. The file is currently being processed. Please help me analyze this document once processing is complete.`
          : `I've uploaded a PDF file: ${filename}. Please help me analyze this document.`;
        
        // If no current conversation, create a new one with the uploaded file info
        if (!chatContext.currentConversation) {
          await chatContext.createNewConversation(chatMessage);
        } else {
          // If there's a current conversation, send a message about the uploaded file
          await chatContext.sendMessage(chatContext.currentConversation.id, chatMessage);
        }
        
        // Reload conversations to get updated document information
        await chatContext.loadConversations();
        
        // Hide file drop zone after successful upload
        setShowFileDropZone(false);
      } else {
        throw new Error('Upload failed - no response data received');
      }
    } catch (error) {
      console.error('File upload failed:', error);
      showNotification(
        `File upload failed: ${error instanceof Error ? error.message : 'Unknown error'}`,
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
  const chatSessions: SidebarChatSession[] = chatContext.conversations.map((conv: ChatSession) => ({
    id: conv.id.toString(),
    title: conv.title,
    lastMessage: conv.messages.length > 0 ? conv.messages[conv.messages.length - 1].content : 'No messages yet',
    timestamp: new Date(conv.createdAt),
    hasDocument: conv.hasDocument || false,
    documentFilename: conv.documentInfo?.filename,
    documentType: conv.documentInfo?.documentId === 'so-tay-sinh-vien-2024' ? 'default' : 'upload'
  }));

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

      {/* Show FileDropZone or ChatContainer based on state */}
      {showFileDropZone ? (
        <FileDropZone
          onFileUpload={handleFileUpload}
          isUploading={isUploading}
          onCancel={handleCancelFileUpload}
        />
      ) : (
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
        />
      )}

      {/* File Upload Loading Overlay */}
      {isUploading && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center">
          <div className="bg-white dark:bg-slate-800 rounded-2xl p-8 shadow-2xl border border-gray-200 dark:border-slate-700 max-w-sm w-full mx-4">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto mb-4"></div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                {t('chat.processing_file')}
              </h3>
              <p className="text-gray-600 dark:text-gray-400 text-sm">
                {t('chat.processing_description')}
              </p>
              <div className="mt-4 text-xs text-gray-500 dark:text-gray-400">
                {t('chat.do_not_close')}
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
