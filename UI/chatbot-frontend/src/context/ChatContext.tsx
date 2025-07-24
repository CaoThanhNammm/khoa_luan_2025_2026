import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import type { ReactNode } from 'react';
import ChatService from '../services/ChatService';
import type { ChatSession, Message } from '../types/chat';
import { useAuth } from './AuthContext';
import { getErrorMessage } from '../utils/errorHandler';

interface ChatContextType {
  conversations: ChatSession[];
  currentConversation: ChatSession | null;
  loading: boolean;
  isThinking: boolean; // Thêm state cho thinking
  pendingMessage: Message | null; // Thêm state cho tin nhắn đang pending
  error: string | null;
  
  // Actions
  loadConversations: () => Promise<void>;
  createNewConversation: (message: string) => Promise<string | null>;
  createNewConversationWithDocument: (message: string, documentId: string) => Promise<string | null>;
  createNewConversationWithSuggestedQuestions: () => Promise<string | null>;
  createEmptyConversationWithUploadedDocument: (documentId: string, filename: string, fileSize: number, status?: string, s3Key?: string, s3Url?: string) => Promise<string | null>;
  switchToConversation: (id: string) => Promise<void>;
  deleteConversation: (id: string) => Promise<void>;
  sendMessage: (conversationId: string, message: string) => Promise<void>;
  clearCurrentConversation: () => void;
  clearError: () => void;
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

interface ChatProviderProps {
  children: ReactNode;
}

export const ChatProvider: React.FC<ChatProviderProps> = ({ children }) => {
  const { user } = useAuth();
  const [conversations, setConversations] = useState<ChatSession[]>([]);
  const [currentConversation, setCurrentConversation] = useState<ChatSession | null>(null);
  const [loading, setLoading] = useState(false);
  const [isThinking, setIsThinking] = useState(false); // Thêm state thinking
  const [pendingMessage, setPendingMessage] = useState<Message | null>(null); // Thêm state cho pending message
  const [error, setError] = useState<string | null>(null);

  // Save current conversation ID to localStorage
  const saveCurrentConversationId = useCallback((conversationId: string | null) => {
    if (user) {
      const key = `chatbot_current_conversation_${user.id}`;
      if (conversationId) {
        localStorage.setItem(key, conversationId);
      } else {
        localStorage.removeItem(key);
      }
    }
  }, [user]);

  // Get saved conversation ID from localStorage
  const getSavedConversationId = useCallback((): string | null => {
    if (user) {
      const key = `chatbot_current_conversation_${user.id}`;
      const saved = localStorage.getItem(key);
      return saved || null;
    }
    return null;
  }, [user]);
  // Load all conversations for the current user
  const loadConversations = useCallback(async () => {
    if (!user) return;
    
    setLoading(true);
    try {
      const conversations = await ChatService.getConversations();
      setConversations(conversations);
      
      // Try to restore the previously selected conversation
      const savedConversationId = getSavedConversationId();
      if (savedConversationId) {
        // Find the conversation in the loaded conversations
        const savedConversation = conversations.find(conv => conv.id === savedConversationId);
        if (savedConversation) {
          // Load the full conversation details
          try {
            const fullConversation = await ChatService.getConversation(savedConversationId);
            setCurrentConversation(fullConversation);
          } catch (err) {
            // If loading the specific conversation fails, just clear the saved ID
            console.warn('Failed to load saved conversation:', err);
            saveCurrentConversationId(null);
          }
        } else {
          // Conversation no longer exists, clear the saved ID
          saveCurrentConversationId(null);
        }
      }
      
      setError(null);
    } catch (err) {
      const errorMessage = getErrorMessage(err);
      setError(errorMessage);
      console.error('Error loading conversations:', err);
    } finally {
      setLoading(false);
    }
  }, [user, getSavedConversationId, saveCurrentConversationId]);  // Create a new conversation
  const createNewConversation = async (message: string): Promise<string | null> => {
    if (!user) return null;
    
    setLoading(true);
    setIsThinking(true);
    
    const tempId = `temp_${Date.now()}`;
    // Tạo conversation tạm thời với tin nhắn user
    const tempConversation = {
      id: tempId, // Temporary ID
      title: message.length > 50 ? message.substring(0, 50) + '...' : message,
      createdAt: new Date().toISOString(),
      messages: [{
        id: Date.now(),
        content: message,
        timestamp: new Date().toISOString(),
        type: 'USER' as const,
        conversationId: tempId, // Temporary conversation ID
        isLatest: false,
        isStreaming: false
      }]
    };
    
    // Render conversation tạm thời ngay lập tức
    setCurrentConversation(tempConversation);
    
    try {
      const newConversation = await ChatService.startNewConversation(message);
      
      // Mark the latest bot message for streaming effect
      const messagesWithStreaming = newConversation.messages.map((msg, index) => {
        if (msg.type === 'BOT' && index === newConversation.messages.length - 1) {
          return { ...msg, isLatest: true, isStreaming: true };
        }
        return { ...msg, isLatest: false, isStreaming: false };
      });

      const conversationWithStreaming = {
        ...newConversation,
        messages: messagesWithStreaming
      };
      
      setConversations(prev => [conversationWithStreaming, ...prev]);
      setCurrentConversation(conversationWithStreaming);
      saveCurrentConversationId(newConversation.id); // Save the new conversation ID
      setError(null);
      
      return newConversation.id;
    } catch (err) {
      const errorMessage = getErrorMessage(err);
      setError(errorMessage);
      console.error('Error creating conversation:', err);
      // Xóa conversation tạm thời nếu có lỗi
      setCurrentConversation(null);
      return null;
    } finally {
      setLoading(false);
      setIsThinking(false);
    }
  };

  // Create a new conversation with document (for student handbook)
  const createNewConversationWithDocument = async (message: string, documentId: string): Promise<string | null> => {
    if (!user) return null;
    
    setLoading(true);
    setIsThinking(true);
    
    const tempId = `temp_${Date.now()}`;
    // Tạo conversation tạm thời với tin nhắn user
    const tempConversation = {
      id: tempId, // Temporary ID
      title: message.length > 50 ? message.substring(0, 50) + '...' : message,
      createdAt: new Date().toISOString(),
      messages: [{
        id: Date.now(),
        content: message,
        timestamp: new Date().toISOString(),
        type: 'USER' as const,
        conversationId: tempId, // Temporary conversation ID
        isLatest: false,
        isStreaming: false
      }]
    };
    
    // Render conversation tạm thời ngay lập tức
    setCurrentConversation(tempConversation);
    
    try {
      const newConversation = await ChatService.startNewConversationWithDocument(message, documentId);
      
      // Mark the latest bot message for streaming effect
      const messagesWithStreaming = newConversation.messages.map((msg, index) => {
        if (msg.type === 'BOT' && index === newConversation.messages.length - 1) {
          return { ...msg, isLatest: true, isStreaming: true };
        }
        return { ...msg, isLatest: false, isStreaming: false };
      });

      const conversationWithStreaming = {
        ...newConversation,
        messages: messagesWithStreaming
      };
      
      setConversations(prev => [conversationWithStreaming, ...prev]);
      setCurrentConversation(conversationWithStreaming);
      saveCurrentConversationId(newConversation.id); // Save the new conversation ID
      setError(null);
      
      return newConversation.id;
    } catch (err) {
      const errorMessage = getErrorMessage(err);
      setError(errorMessage);
      console.error('Error creating conversation with document:', err);
      // Xóa conversation tạm thời nếu có lỗi
      setCurrentConversation(null);
      return null;
    } finally {
      setLoading(false);
      setIsThinking(false);
    }
  };

  // Create a new conversation with suggested questions (no initial message)
  const createNewConversationWithSuggestedQuestions = async (): Promise<string | null> => {
    if (!user) return null;
    
    // Create a temporary conversation with suggested questions display
    const tempConversation = {
      id: `temp_${Date.now()}`, // Temporary ID as string
      title: 'Cuộc trò chuyện mới',
      createdAt: new Date().toISOString(),
      messages: [], // No initial messages, will show suggested questions
      hasDocument: true,
      documentInfo: {
        documentId: 'so_tay_sinh_vien_2024',
        filename: 'Sổ tay sinh viên 2024',
        fileSize: 0,
        sentencesCount: 0,
        uploadDate: new Date().toISOString(),
        status: 'active'
      }
    };
    
    // Set the temporary conversation immediately to show suggested questions
    setCurrentConversation(tempConversation);
    setError(null);
    
    return tempConversation.id;
  };

  // Create an empty conversation with uploaded document and save to DB
  const createEmptyConversationWithUploadedDocument = async (documentId: string, filename: string, fileSize: number, status?: string, s3Key?: string, s3Url?: string): Promise<string | null> => {
    if (!user) return null;
    
    setLoading(true);
    
    try {
      // Create empty conversation in database with document info
      const newConversation = await ChatService.createEmptyConversationWithDocument(documentId, filename, fileSize, status, s3Key, s3Url);
      
      // Add to conversations list and set as current
      setConversations(prev => [newConversation, ...prev]);
      setCurrentConversation(newConversation);
      saveCurrentConversationId(newConversation.id); // Save the new conversation ID
      setError(null);
      
      return newConversation.id;
    } catch (err) {
      const errorMessage = getErrorMessage(err);
      setError(errorMessage);
      console.error('Error creating empty conversation with document:', err);
      return null;
    } finally {
      setLoading(false);
    }
  };

  // Switch to a specific conversation
  const switchToConversation = async (id: string) => {
    setLoading(true);
    try {
      const conversation = await ChatService.getConversation(id);
      setCurrentConversation(conversation);
      saveCurrentConversationId(id); // Save the current conversation ID
      setError(null);
    } catch (err) {
      const errorMessage = getErrorMessage(err);
      setError(errorMessage);
      console.error('Error loading conversation:', err);
    } finally {
      setLoading(false);
    }
  };
  // Delete a conversation
  const deleteConversation = async (id: string) => {
    try {
      await ChatService.deleteConversation(id);
      
      setConversations(prev => prev.filter(conv => conv.id !== id));
      
      if (currentConversation?.id === id) {
        setCurrentConversation(null);
        saveCurrentConversationId(null); // Clear saved conversation ID
      }
      
      setError(null);
    } catch (err) {
      const errorMessage = getErrorMessage(err);
      setError(errorMessage);
      console.error('Error deleting conversation:', err);
    }
  };  // Send a message in a conversation
  const sendMessage = async (conversationId: string, message: string) => {
    try {
      // Tạo pending message để hiển thị ngay lập tức
      const tempUserMessage = {
        id: Date.now(), // Temporary ID
        content: message,
        timestamp: new Date().toISOString(),
        type: 'USER' as const,
        conversationId: conversationId,
        isLatest: false,
        isStreaming: false
      };

      // Set pending message thay vì cập nhật currentConversation
      setPendingMessage(tempUserMessage);
      setIsThinking(true); // Bắt đầu thinking state
      
      // Kiểm tra xem conversation có phải là student handbook không
      const isStudentHandbook = currentConversation?.hasDocument && 
                               currentConversation?.documentInfo?.documentId === 'so_tay_sinh_vien_2024';
      
      // Send message to server với API phù hợp
      if (isStudentHandbook) {
        await ChatService.sendMessageStsv(conversationId, message);
      } else {
        const documentId = currentConversation?.hasDocument ? currentConversation?.documentInfo?.documentId : undefined;
        await ChatService.sendMessage(conversationId, message, documentId);
      }
      
      setIsThinking(false); // Kết thúc thinking state
      setPendingMessage(null); // Xóa pending message
      
      // Reload conversation để lấy dữ liệu mới nhất từ server
      if (currentConversation?.id === conversationId) {
        const updatedConversation = await ChatService.getConversation(conversationId);
        
        // Mark the latest bot message for streaming effect
        const messagesWithStreaming = updatedConversation.messages.map((msg, index) => {
          if (msg.type === 'BOT' && index === updatedConversation.messages.length - 1) {
            return { ...msg, isLatest: true, isStreaming: true };
          }
          return { ...msg, isLatest: false, isStreaming: false };
        });

        setCurrentConversation({
          ...updatedConversation,
          messages: messagesWithStreaming
        });
      }
      
      setError(null);
    } catch (err) {
      setIsThinking(false); // Đảm bảo tắt thinking state khi có lỗi
      setPendingMessage(null); // Xóa pending message khi có lỗi
      const errorMessage = getErrorMessage(err);
      setError(errorMessage);
      console.error('Error sending message:', err);
    }
  };
  const clearError = () => {
    setError(null);
  };
  const clearCurrentConversation = () => {
    setCurrentConversation(null);
    saveCurrentConversationId(null); // Clear saved conversation ID
  };
  // Load conversations when user changes
  useEffect(() => {
    if (user) {
      loadConversations();
    } else {
      setConversations([]);
      setCurrentConversation(null);
      // Clear any saved conversation data when user logs out
      Object.keys(localStorage).forEach(key => {
        if (key.startsWith('chatbot_current_conversation_')) {
          localStorage.removeItem(key);
        }
      });
    }
  }, [user, loadConversations]);  const value: ChatContextType = {
    conversations,
    currentConversation,
    loading,
    isThinking,
    pendingMessage,
    error,
    loadConversations,
    createNewConversation,
    createNewConversationWithDocument,
    createNewConversationWithSuggestedQuestions,
    createEmptyConversationWithUploadedDocument,
    switchToConversation,
    deleteConversation,
    sendMessage,
    clearCurrentConversation,
    clearError
  };

  return (
    <ChatContext.Provider value={value}>
      {children}
    </ChatContext.Provider>
  );
};

export const useChat = (): ChatContextType => {
  const context = useContext(ChatContext);
  if (context === undefined) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
};
