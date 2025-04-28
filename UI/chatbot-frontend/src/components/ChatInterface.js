import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Alert, Spinner, Badge, Button, Tooltip, OverlayTrigger } from 'react-bootstrap';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import ChatService from '../services/ChatService';

const ChatInterface = ({ currentUser, darkMode }) => {
  const [conversations, setConversations] = useState([]);
  const [currentConversation, setCurrentConversation] = useState(null);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [sendingMessage, setSendingMessage] = useState(false);
  const [error, setError] = useState('');
  const [isMobileView, setIsMobileView] = useState(window.innerWidth < 768);
  const [showSidebar, setShowSidebar] = useState(true);
  const { t } = useTranslation();
  const navigate = useNavigate();

  const messagesEndRef = useRef(null);
  const messageInputRef = useRef(null);
  const chatMessagesRef = useRef(null);

  // Handle responsive layout
  useEffect(() => {
    const handleResize = () => {
      const mobile = window.innerWidth < 768;
      setIsMobileView(mobile);
      if (mobile) {
        setShowSidebar(false);
      } else {
        setShowSidebar(true);
      }
    };

    window.addEventListener('resize', handleResize);
    handleResize();
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const loadConversations = useCallback(() => {
    setLoading(true);
    ChatService.getConversations()
      .then(response => {
        setConversations(response.data);
        setLoading(false);

        // Load the most recent conversation if available
        if (response.data.length > 0 && !currentConversation) {
          setCurrentConversation(response.data[0]);
        }
      })
      .catch(error => {
        console.error("Error loading conversations:", error);
        setError(t('load_failed'));
        setLoading(false);
      });
  }, [t]); // Removed currentConversation from dependency array

  useEffect(() => {
    loadConversations();
  }, [loadConversations]);

  useEffect(() => {
    scrollToBottom();
  }, [currentConversation, sendingMessage]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleNewConversation = () => {
    setCurrentConversation(null);
    setMessage('');
    setTimeout(() => {
      messageInputRef.current?.focus();
    }, 100);

    // If on mobile, hide sidebar automatically when creating new chat
    if (isMobileView) {
      setShowSidebar(false);
    }
  };

  const selectConversation = (conversation) => {
    setCurrentConversation(conversation);

    // If on mobile, hide sidebar automatically when selecting a conversation
    if (isMobileView) {
      setShowSidebar(false);
    }
  };

  const deleteConversation = (e, conversationId) => {
    e.stopPropagation();
    if (window.confirm(t('delete_confirm'))) {
      ChatService.deleteConversation(conversationId)
        .then(() => {
          setConversations(conversations.filter(c => c.id !== conversationId));
          if (currentConversation && currentConversation.id === conversationId) {
            setCurrentConversation(null);
          }
        })
        .catch(error => {
          console.error("Error deleting conversation:", error);
          setError(t('delete_failed'));
        });
    }
  };

  const sendMessage = (e) => {
    e.preventDefault();

    if (!message.trim()) return;

    setSendingMessage(true);
    const currentMessage = message; // Store the current message
    setMessage(''); // Clear the input field immediately after submission

    if (!currentConversation) {
      // Starting a new conversation
      ChatService.startNewConversation(currentMessage)
        .then(response => {
          setCurrentConversation(response.data);
          setConversations([response.data, ...conversations]);
          setSendingMessage(false);
          messageInputRef.current?.focus();
        })
        .catch(error => {
          console.error("Error starting conversation:", error);
          setError(t('error_start_conversation'));
          setSendingMessage(false);
        });
    } else {
      // Send a message in existing conversation
      // First add the user message to the UI for immediate feedback
      const userMessage = {
        id: Date.now(), // temporary ID
        content: currentMessage,
        type: 'USER',
        timestamp: new Date().toISOString(),
        conversationId: currentConversation.id
      };

      const updatedConversation = {
        ...currentConversation,
        messages: [...currentConversation.messages, userMessage]
      };

      setCurrentConversation(updatedConversation);

      // Send the message to the server
      ChatService.sendMessage(currentConversation.id, currentMessage)
        .then(response => {
          // Add the bot response
          const updatedMessages = [...updatedConversation.messages, response.data];
          const finalConversation = {
            ...updatedConversation,
            messages: updatedMessages
          };

          setCurrentConversation(finalConversation);

          // Update the conversation in the list
          const updatedConversations = conversations.map(conv =>
            conv.id === currentConversation.id ? finalConversation : conv
          );

          setConversations(updatedConversations);
          setSendingMessage(false);
          messageInputRef.current?.focus();
        })
        .catch(error => {
          console.error("Error sending message:", error);
          setError(t('error_send_message'));
          setSendingMessage(false);
        });
    }
  };

  const formatTimestamp = (timestamp) => {
    if (!timestamp) return '';

    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  // Format the date for conversation list
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);

    if (date.toDateString() === today.toDateString()) {
      return t('today');
    } else if (date.toDateString() === yesterday.toDateString()) {
      return t('yesterday');
    } else {
      return date.toLocaleDateString(
        t('i18n.language') === 'vi' ? 'vi-VN' : 'en-US',
        { month: 'short', day: 'numeric' }
      );
    }
  };

  // Truncate conversation title to a specific length
  const truncateTitle = (title, maxLength = 28) => {
    if (title && title.length > maxLength) {
      return title.substring(0, maxLength) + '...';
    }
    return title || t('new_chat');
  };

  const getMessageCount = (conversation) => {
    return conversation.messages ? conversation.messages.length : 0;
  };

  // Render typing indicator animation
  const renderTypingIndicator = () => (
    <div className="typing-indicator">
      <span></span>
      <span></span>
      <span></span>
    </div>
  );

  return (
    <div className={`chat-container ${darkMode ? 'dark-mode' : ''}`}>
      {/* Mobile toggle button */}
      {isMobileView && (
        <button
          className={`sidebar-toggle ${showSidebar ? 'active' : ''}`}
          onClick={() => setShowSidebar(!showSidebar)}
          aria-label="Toggle sidebar"
        >
          <i className={`bi ${showSidebar ? 'bi-x-lg' : 'bi-list'}`}></i>
        </button>
      )}

      {/* Sidebar with conversation list */}
      <div className={`sidebar ${showSidebar ? 'active' : ''} ${darkMode ? 'dark' : ''}`}>
        <div className="sidebar-header">
          <button
            className="new-chat-button"
            onClick={handleNewConversation}
          >
            <i className="bi bi-plus-lg me-2"></i> {t('new_chat')}
          </button>

          {isMobileView && (
            <button
              className="btn-close sidebar-close"
              onClick={() => setShowSidebar(false)}
              aria-label="Close sidebar"
            ></button>
          )}
        </div>

        <h6 className="sidebar-title">
          <i className="bi bi-clock-history me-2"></i>
          {t('conversation_history')}
        </h6>

        {loading ? (
          <div className="text-center p-4">
            <Spinner animation="border" size="sm" className="me-2" />
            <span>{t('loading_conversations')}</span>
          </div>
        ) : (
          <ul className="conversation-list">
            {conversations.length === 0 ? (
              <li className="empty-state">
                <div className="empty-icon">
                  <i className="bi bi-chat-square-text"></i>
                </div>
                <p>{t('no_conversations')}</p>
              </li>
            ) : (
              conversations.map(conv => (
                <li
                  key={conv.id}
                  className={`conversation-item ${currentConversation && currentConversation.id === conv.id ? 'active' : ''}`}
                  onClick={() => selectConversation(conv)}
                >
                  <div className="conversation-content">
                    <div className="conversation-icon">
                      <i className="bi bi-chat-left-text"></i>
                    </div>
                    <div className="conversation-details">
                      <div className="conversation-title">{truncateTitle(conv.title)}</div>
                      <div className="conversation-meta">
                        <span className="conversation-count">
                          <i className="bi bi-chat-dots me-1"></i>
                          {getMessageCount(conv)}
                        </span>
                        <span className="conversation-date">
                          <i className="bi bi-calendar me-1"></i>
                          {formatDate(conv.createdAt)}
                        </span>
                      </div>
                    </div>
                    <OverlayTrigger
                      placement="top"
                      overlay={<Tooltip>{t('delete_conversation')}</Tooltip>}
                    >
                      <button
                        className="conversation-delete"
                        onClick={(e) => deleteConversation(e, conv.id)}
                        aria-label={t('delete_conversation')}
                      >
                        <i className="bi bi-trash"></i>
                      </button>
                    </OverlayTrigger>
                  </div>
                </li>
              ))
            )}
          </ul>
        )}

        {/* Navigation buttons on mobile */}
        {isMobileView && (
          <div className="sidebar-footer">
            <button
              className="sidebar-nav-button"
              onClick={() => navigate('/conversations')}
            >
              <i className="bi bi-clock-history me-2"></i>
              {t('history')}
            </button>
            <button
              className="sidebar-nav-button"
              onClick={() => navigate('/settings')}
            >
              <i className="bi bi-gear me-2"></i>
              {t('settings')}
            </button>
          </div>
        )}
      </div>

      {/* Main chat area */}
      <div className={`chat-main ${darkMode ? 'dark' : ''}`}>
        {currentConversation && (
          <div className="chat-header">
            <h2 className="chat-title">
              <i className={`bi bi-chat-dots me-2 ${darkMode ? 'text-info' : 'text-primary'}`}></i>
              {truncateTitle(currentConversation.title, 40)}
            </h2>
            <div className="chat-actions">
              <Badge bg={darkMode ? "info" : "primary"} className="message-count">
                <i className="bi bi-chat-fill me-1"></i>
                {getMessageCount(currentConversation)} {t('messages')}
              </Badge>
              <Button
                variant={darkMode ? "outline-danger" : "outline-danger"}
                size="sm"
                onClick={(e) => deleteConversation(e, currentConversation.id)}
                className="ms-2"
              >
                <i className="bi bi-trash me-1"></i>
                {t('delete_conversation')}
              </Button>
            </div>
          </div>
        )}

        <div className={`chat-messages ${darkMode ? 'dark' : ''}`} ref={chatMessagesRef}>
          {error && (
            <Alert variant="danger" onClose={() => setError('')} dismissible className="error-alert">
              <i className="bi bi-exclamation-circle me-2"></i>
              {error}
            </Alert>
          )}

          {!currentConversation && !sendingMessage && (
            <div className="welcome-message">
              <div className="welcome-icon">
                <i className="bi bi-chat-square-text"></i>
              </div>
              <h3>{t('how_help_today')}</h3>
              <p>{t('start_message')}</p>

              {/* Quick prompt suggestions */}
              <div className="prompt-suggestions">
                <button className="prompt-suggestion" onClick={() => setMessage("Nói về học vụ Nông Lâm")}>
                  Nói về học vụ Nông Lâm
                </button>
                <button className="prompt-suggestion" onClick={() => setMessage("Nói về học phí")}>
                  Nói về học phí
                </button>
                <button className="prompt-suggestion" onClick={() => setMessage("Nói về truyền thống của trường")}>
                  Nói về truyền thống của trường
                </button>
              </div>
            </div>
          )}

          {currentConversation && currentConversation.messages.map((msg, index) => (
            <div
              key={msg.id}
              className={`message ${msg.type === 'USER' ? 'user' : 'bot'} ${darkMode ? 'dark' : ''}`}
            >
              <div className="message-avatar">
                {msg.type === 'USER' ? (
                  <div className="avatar user-avatar">
                    <i className="bi bi-person-fill"></i>
                  </div>
                ) : (
                  <div className="avatar bot-avatar">
                    <i className="bi bi-robot"></i>
                  </div>
                )}
              </div>
              <div className={`message-bubble ${msg.type === 'USER' ? 'user-bubble' : 'bot-bubble'} ${darkMode ? 'dark' : ''}`}>
                <div className="message-content">{msg.content}</div>
                <span className="message-time">
                  {formatTimestamp(msg.timestamp)}
                </span>
              </div>
            </div>
          ))}

          {sendingMessage && (
            <div className={`message bot ${darkMode ? 'dark' : ''}`}>
              <div className="message-avatar">
                <div className="avatar bot-avatar">
                  <i className="bi bi-robot"></i>
                </div>
              </div>
              <div className="message-bubble">
                {renderTypingIndicator()}
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Message input */}
        <div className={`message-input-container ${darkMode ? 'dark' : ''}`}>
          <form onSubmit={sendMessage} className={`message-form ${darkMode ? 'dark' : ''}`}>
            <input
              type="text"
              className={`message-input ${darkMode ? 'dark' : ''}`}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder={t('type_message')}
              disabled={sendingMessage}
              ref={messageInputRef}
            />
            <button
              type="submit"
              className={`send-button ${!message.trim() || sendingMessage ? 'disabled' : ''}`}
              disabled={!message.trim() || sendingMessage}
            >
              {sendingMessage ? (
                <Spinner animation="border" size="sm" role="status" />
              ) : (
                <i className="bi bi-send-fill"></i>
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;