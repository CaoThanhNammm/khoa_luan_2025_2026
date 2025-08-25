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
  
  // State để theo dõi document_id từ database - 'so_tay_sinh_vien_2024' nghĩa là student handbook
  const [currentDocumentId, setCurrentDocumentId] = useState<string | null>(null);

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
      
      // Set currentDocumentId cho student handbook
      setCurrentDocumentId('so_tay_sinh_vien_2024'); // Student handbook có document_id = 'so_tay_sinh_vien_2024'
      console.log('Set currentDocumentId: so_tay_sinh_vien_2024 (student handbook - createNewConversation)');
      
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
      }],
      // Đánh dấu document info cho student handbook
      ...(documentId === 'so_tay_sinh_vien_2024' && {
        hasDocument: true,
        documentInfo: {
          documentId: null, // Student handbook có documentId là null
          filename: 'Sổ tay sinh viên 2024',
          fileSize: 0,
          sentencesCount: 0,
          uploadDate: new Date().toISOString(),
          status: 'processed'
        }
      })
    };
    
    // Render conversation tạm thời ngay lập tức
    setCurrentConversation(tempConversation);
    
    // Force a re-render by using React's state batching
    await new Promise(resolve => {
      // Use setTimeout to ensure the state update is processed
      setTimeout(resolve, 200);
    });
    
    try {
      // Sử dụng API /conversations cho student handbook
      const newConversation = documentId === 'so_tay_sinh_vien_2024' 
        ? await ChatService.startNewConversation(message)
        : await ChatService.startNewConversationWithDocument(message, documentId);
      
      // Set currentDocumentId dựa trên loại conversation
      if (documentId === 'so_tay_sinh_vien_2024') {
        setCurrentDocumentId('so_tay_sinh_vien_2024'); // Student handbook
        console.log('Set currentDocumentId: so_tay_sinh_vien_2024 (student handbook)');
      } else {
        setCurrentDocumentId(documentId); // Uploaded document
        console.log('Set currentDocumentId:', documentId);
      }
      
      // Mark the latest bot message for streaming effect
      const messagesWithStreaming = newConversation.messages.map((msg, index) => {
        if (msg.type === 'BOT' && index === newConversation.messages.length - 1) {
          return { ...msg, isLatest: true, isStreaming: true };
        }
        return { ...msg, isLatest: false, isStreaming: false };
      });

      const conversationWithStreaming = {
        ...newConversation,
        messages: messagesWithStreaming,
        // Đánh dấu là student handbook conversation nếu cần
        ...(documentId === 'so_tay_sinh_vien_2024' && {
          hasDocument: true,
          documentInfo: {
            documentId: null, // Student handbook có documentId là null
            filename: 'Sổ tay sinh viên 2024',
            fileSize: 0,
            sentencesCount: 0,
            uploadDate: new Date().toISOString(),
            status: 'processed'
          }
        })
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
      
      // Set currentDocumentId cho uploaded document
      setCurrentDocumentId(documentId);
      console.log('Set currentDocumentId:', documentId, '(uploaded document)');
      
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
      
      // Debug logging
      console.log('Debug switchToConversation:', {
        conversationId: id,
        hasDocument: conversation?.hasDocument,
        documentId: conversation?.documentInfo?.documentId,
        filename: conversation?.documentInfo?.filename
      });
      
      // Set currentDocumentId dựa trên thông tin từ database
      if (conversation?.hasDocument && conversation?.documentInfo) {
        setCurrentDocumentId(conversation.documentInfo.documentId);
        console.log('Set currentDocumentId:', conversation.documentInfo.documentId);
      } else {
        setCurrentDocumentId(undefined); // Không có document
        console.log('Set currentDocumentId: undefined (no document)');
      }
      
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
      
      // Sử dụng currentDocumentId để quyết định API nào sẽ gọi
      // 'so_tay_sinh_vien_2024' = student handbook -> gọi sendMessageStsv
      // other string = uploaded document -> gọi sendMessage  
      // undefined/null = no document -> gọi sendMessage
      const shouldUseStsv = currentDocumentId === 'so_tay_sinh_vien_2024';
      
      // Debug logging
      console.log('Debug sendMessage:', {
        currentDocumentId: currentDocumentId,
        shouldUseStsv: shouldUseStsv,
        conversationId: conversationId
      });
      
      // Send message to server với API phù hợp
      if (shouldUseStsv) {
        console.log('Calling sendMessageStsv (student handbook)');
        await ChatService.sendMessageStsv(conversationId, message);
      } else {
        console.log('Calling sendMessage (regular chat or uploaded document)');
        await ChatService.sendMessage(conversationId, message);
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

        // Update conversation with streaming effect
        const updatedConversationWithStreaming = {
          ...updatedConversation,
          messages: messagesWithStreaming
        };

        setCurrentConversation(updatedConversationWithStreaming);
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
    setCurrentDocumentId(undefined); // Reset document ID
    saveCurrentConversationId(null); // Clear saved conversation ID
    console.log('Cleared currentConversation and currentDocumentId');
  };
  // Load conversations when user changes
  useEffect(() => {
    if (user) {
      loadConversations();
    } else {
      setConversations([]);
      setCurrentConversation(null);
      setCurrentDocumentId(undefined); // Reset document ID when logout
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
