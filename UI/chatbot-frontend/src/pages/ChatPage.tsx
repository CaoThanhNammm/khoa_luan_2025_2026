import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useAuth } from '../context/AuthContext';
import { useChat } from '../context/ChatContext';
import { useNavigate, useParams, useLocation } from 'react-router-dom';
import { ChatSidebar, ChatContainer } from '../components/chat';
import type { ChatSession, SidebarChatSession } from '../types/chat';

const ChatPage: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const params = useParams();
  const location = useLocation();
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  
  const chatContext = useChat();
  const { 
    currentConversation, 
    conversations, 
    loading, 
    switchToConversation,
    clearError,
    clearCurrentConversation,
    sendMessage,
    createNewConversation,
    deleteConversation,
    error,
    isThinking,
    pendingMessage
  } = chatContext;

  // Get conversation ID from URL params if available
  const urlConversationId = params.conversationId ? parseInt(params.conversationId, 10) : null;

  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }
  }, [user, navigate]);  // State để theo dõi việc tạo session mới
  const [isCreatingNewSession, setIsCreatingNewSession] = useState(false);
  // State để theo dõi việc navigation
  const [isNavigating, setIsNavigating] = useState(false);
  // State để theo dõi conversation đang được load
  const [loadingConversationId, setLoadingConversationId] = useState<number | null>(null);  // Ref để track navigation timeout
  const navigationTimeoutRef = useRef<number | null>(null);
  // Ref để track switch conversation debounce
  const switchTimeoutRef = useRef<number | null>(null);
  // Handle URL synchronization with current conversation
  useEffect(() => {
    // Nếu đang tạo session mới, không làm gì cả
    if (isCreatingNewSession) {
      return;
    }

    // Avoid unnecessary calls if already loading
    if (loading) {
      return;
    }

    // If we have a URL conversation ID and it's different from current, switch to it
    if (urlConversationId && 
        currentConversation?.id !== urlConversationId && 
        conversations.length > 0 &&
        loadingConversationId !== urlConversationId) {
      
      const targetConversation = conversations.find(conv => conv.id === urlConversationId);
      if (targetConversation) {
        setLoadingConversationId(urlConversationId);
        switchToConversation(urlConversationId).finally(() => {
          setLoadingConversationId(null);
        });
      } else {
        // If conversation doesn't exist, navigate to base chat page
        navigate('/chat', { replace: true });
      }
    }    // Only update URL if we have a current conversation and URL doesn't reflect it
    // BUT don't do this if we're already on the base chat page (which means user wants to start fresh)
    else if (currentConversation && 
             !urlConversationId && 
             location.pathname === '/chat' &&
             !sessionStorage.getItem('newSessionIntent') &&
             !isNavigating) {
      // Clear any existing timeout
      if (navigationTimeoutRef.current) {
        clearTimeout(navigationTimeoutRef.current);
      }
      
      setIsNavigating(true);
      navigate(`/chat/${currentConversation.id}`, { replace: true });
      navigationTimeoutRef.current = setTimeout(() => setIsNavigating(false), 100);
    }
  }, [urlConversationId, currentConversation, conversations, loading, switchToConversation, navigate, location.pathname, isCreatingNewSession, loadingConversationId, isNavigating]);  // Cleanup timeout on unmount
  useEffect(() => {
    return () => {
      if (navigationTimeoutRef.current) {
        clearTimeout(navigationTimeoutRef.current);
      }
      if (switchTimeoutRef.current) {
        clearTimeout(switchTimeoutRef.current);
      }
    };  }, []);
  // Get messages from current conversation directly (no conversion needed)
  const messages = currentConversation?.messages || [];
  const currentSessionId = currentConversation?.id.toString() || '';

  // Convert conversations to SidebarChatSession format for sidebar
  const chatSessions: SidebarChatSession[] = conversations.map((conv: ChatSession) => ({
    id: conv.id.toString(),
    title: conv.title,
    lastMessage: conv.messages.length > 0 ? conv.messages[conv.messages.length - 1].content : 'No messages yet',
    timestamp: new Date(conv.createdAt)
  }));
  
  const handleSendMessage = async (inputMessage: string) => {
    if (!inputMessage.trim()) return;

    try {
      let conversationId: number | null = null;
        if (currentConversation) {
        // Send message to existing conversation
        conversationId = currentConversation.id;
        await sendMessage(conversationId, inputMessage);
      } else {
        // Create new conversation
        conversationId = await createNewConversation(inputMessage);
      }
      
      // Update URL to reflect current conversation
      if (conversationId && location.pathname === '/chat') {
        navigate(`/chat/${conversationId}`, { replace: true });
      }
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };  const handleCreateNewSession = useCallback(async () => {
    // Set flag để ngăn URL synchronization
    setIsCreatingNewSession(true);
    sessionStorage.setItem('newSessionIntent', 'true');
    
    // Clear the current conversation to start fresh
    clearError(); // Clear any existing errors
    clearCurrentConversation(); // Clear the current conversation
    
    // Navigate to base chat URL
    navigate('/chat', { replace: true });
    
    // Reset flag sau một khoảng thời gian ngắn
    setTimeout(() => {
      setIsCreatingNewSession(false);
      sessionStorage.removeItem('newSessionIntent');
    }, 100);
  }, [clearError, clearCurrentConversation, navigate]);  const handleSwitchToSession = useCallback(async (conversationId: string) => {
    const id = Number(conversationId);
    
    // Prevent duplicate switching
    if (currentConversation?.id === id || loadingConversationId === id) {
      return;
    }
    
    // Clear any existing switch timeout
    if (switchTimeoutRef.current) {
      clearTimeout(switchTimeoutRef.current);
    }
    
    setLoadingConversationId(id);
    setIsNavigating(true);
    
    try {
      await switchToConversation(id);
      // Update URL to reflect selected conversation
      navigate(`/chat/${id}`, { replace: true });
    } catch (error) {
      console.error('Error switching conversation:', error);
    } finally {
      setLoadingConversationId(null);
      switchTimeoutRef.current = setTimeout(() => setIsNavigating(false), 100);
    }
  }, [currentConversation?.id, loadingConversationId, switchToConversation, navigate]);
  const handleDeleteSession = async (conversationId: string) => {
    const id = Number(conversationId);
    await deleteConversation(id);
    
    // If we deleted the current conversation, navigate to base chat
    if (currentConversation?.id === id) {
      navigate('/chat', { replace: true });
    }  };

  // Keyboard shortcuts for navigation
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      // Ctrl+N for new conversation
      if (event.ctrlKey && event.key === 'n') {
        event.preventDefault();
        handleCreateNewSession();
      }
      
      // Ctrl+[ for previous conversation
      if (event.ctrlKey && event.key === '[') {
        event.preventDefault();
        const currentIndex = conversations.findIndex(conv => conv.id.toString() === currentSessionId);
        if (currentIndex > 0) {
          const prevConversation = conversations[currentIndex - 1];
          handleSwitchToSession(prevConversation.id.toString());
        }
      }
      
      // Ctrl+] for next conversation
      if (event.ctrlKey && event.key === ']') {
        event.preventDefault();
        const currentIndex = conversations.findIndex(conv => conv.id.toString() === currentSessionId);
        if (currentIndex < conversations.length - 1) {
          const nextConversation = conversations[currentIndex + 1];
          handleSwitchToSession(nextConversation.id.toString());
        }
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [conversations, currentSessionId, handleCreateNewSession, handleSwitchToSession]);
  if (!user) {
    return null; // Will redirect in useEffect
  }

  return (
      <div className="chat-layout flex bg-gradient-to-br from-slate-50 via-purple-50/30 to-blue-50/40 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900 relative overflow-hidden transition-colors duration-500">
        {/* Enhanced decorative background elements */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-lavender/10 to-sky-blue/10 dark:from-indigo-500/10 dark:to-purple-500/10 rounded-full blur-3xl animate-float"></div>
          <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-gradient-to-tr from-sky-blue/10 to-lavender/10 dark:from-purple-500/10 dark:to-indigo-500/10 rounded-full blur-3xl animate-float" style={{ animationDelay: '1s' }}></div>
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-gradient-to-r from-purple-200/5 to-blue-200/5 dark:from-indigo-400/5 dark:to-purple-400/5 rounded-full blur-3xl animate-aurora"></div>
        </div>      <ChatSidebar
        isSidebarOpen={isSidebarOpen}
        setIsSidebarOpen={setIsSidebarOpen}
        chatSessions={chatSessions}
        currentSessionId={currentSessionId}
        onCreateNewSession={handleCreateNewSession}
        onSwitchToSession={handleSwitchToSession}
        onDeleteSession={handleDeleteSession}
        loadingSessionId={loadingConversationId?.toString() || null}
      />      <ChatContainer
        messages={messages}
        isTyping={loading}
        isThinking={isThinking}
        pendingMessage={pendingMessage}
        onSendMessage={handleSendMessage}
        isLoadingConversation={loadingConversationId !== null}
        conversationId={currentConversation?.id.toString()}
      />

      {/* Enhanced Error Display */}
      {error && (
        <div className="fixed bottom-4 right-4 bg-gradient-to-r from-red-500 to-rose-500 dark:from-red-600 dark:to-rose-600 text-white px-6 py-3 rounded-xl shadow-lg dark:shadow-red-500/25 backdrop-blur-xl border border-red-400/20 animate-fade-in">
          {error}
          <button 
            onClick={clearError}
            className="ml-3 text-white/80 hover:text-white transition-colors rounded-lg p-1 hover:bg-white/10"
          >
            ×
          </button>
        </div>        )}
      </div>
  );
};

export default ChatPage;
