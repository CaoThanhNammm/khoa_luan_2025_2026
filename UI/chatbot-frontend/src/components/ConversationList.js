import React, { useState, useEffect, useCallback } from 'react';
import { Alert, Button, Spinner } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import ChatService from '../services/ChatService';

const ConversationList = ({ currentUser, darkMode }) => {
  const [conversations, setConversations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { t } = useTranslation();
  
  const navigate = useNavigate();

  const loadConversations = useCallback(() => {
    ChatService.getConversations()
      .then(response => {
        setConversations(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error("Error loading conversations:", error);
        setError(t('load_failed'));
        setLoading(false);
      });
  }, [t]);

  useEffect(() => {
    loadConversations();
  }, [loadConversations]);

  const viewConversation = (id) => {
    navigate('/chat', { state: { conversationId: id } });
  };

  const deleteConversation = (id, e) => {
    e.stopPropagation();
    
    if (window.confirm(t('delete_confirm'))) {
      ChatService.deleteConversation(id)
        .then(() => {
          setConversations(conversations.filter(c => c.id !== id));
        })
        .catch(error => {
          console.error("Error deleting conversation:", error);
          setError(t('delete_failed'));
        });
    }
  };

  // Group conversations by date
  const groupByDate = (conversations) => {
    const groups = {};
    
    conversations.forEach(conversation => {
      const date = new Date(conversation.createdAt).toDateString();
      if (!groups[date]) {
        groups[date] = [];
      }
      groups[date].push(conversation);
    });
    
    return Object.entries(groups).map(([date, convs]) => ({
      date,
      conversations: convs
    }));
  };

  const conversationGroups = groupByDate(conversations);

  return (
    <div className={`container py-4 ${darkMode ? 'dark-mode' : ''}`}>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2 className="mb-0">
          <i className="bi bi-clock-history me-2 text-primary"></i>
          {t('conversation_history')}
        </h2>
      </div>
      
      {error && (
        <Alert variant="danger" className="error-feedback" onClose={() => setError('')} dismissible>
          <i className="bi bi-exclamation-circle me-2"></i>
          {error}
        </Alert>
      )}
      
      {loading ? (
        <div className="text-center my-5">
          <Spinner animation="border" variant="primary" />
          <p className="mt-3">{t('loading_conversations')}</p>
        </div>
      ) : (
        <div>
          {conversations.length === 0 ? (
            <div className={`text-center my-5 py-5 rounded ${darkMode ? 'bg-dark' : 'bg-light'}`}>
              <i className="bi bi-chat-square-text mb-3" style={{ fontSize: '3rem', color: darkMode ? '#6c757d' : '#adb5bd' }}></i>
              <h4>{t('no_conversations')}</h4>
              <p className="text-muted mb-4">{t('start_message')}</p>
              <Button 
                variant="primary"
                onClick={() => navigate('/chat')}
                className="px-4 py-2"
              >
                <i className="bi bi-chat-text me-2"></i>
                {t('start_conversation')}
              </Button>
            </div>
          ) : (
            <div>
              {conversationGroups.map(group => (
                <div key={group.date} className="mb-4">
                  <h6 className="text-uppercase text-muted mb-3 fw-bold small">
                    {new Date(group.date).toLocaleDateString(undefined, {
                      weekday: 'long',
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric'
                    })}
                  </h6>
                  <div className="list-group">
                    {group.conversations.map(conversation => (
                      <div 
                        key={conversation.id}
                        className={`list-group-item list-group-item-action d-flex align-items-center p-3 rounded mb-2 border-0 shadow-sm ${darkMode ? 'bg-dark text-white' : ''}`}
                        onClick={() => viewConversation(conversation.id)}
                        style={{ cursor: 'pointer', transition: 'transform 0.15s ease-in-out, box-shadow 0.15s ease-in-out' }}
                        onMouseOver={(e) => {
                          e.currentTarget.style.transform = 'translateY(-2px)';
                          e.currentTarget.style.boxShadow = '0 4px 8px rgba(0,0,0,0.1)';
                        }}
                        onMouseOut={(e) => {
                          e.currentTarget.style.transform = 'translateY(0)';
                          e.currentTarget.style.boxShadow = '0 1px 3px rgba(0,0,0,0.08)';
                        }}
                      >
                        <div className="d-flex align-items-center flex-grow-1">
                          <div className="conversation-icon me-3 text-primary">
                            <i className="bi bi-chat-left-text" style={{ fontSize: '1.5rem' }}></i>
                          </div>
                          <div className="flex-grow-1">
                            <h5 className="mb-1">{conversation.title}</h5>
                            <div className="d-flex align-items-center text-muted small">
                              <i className="bi bi-chat-dots me-1"></i>
                              <span>{conversation.messages.length} {t('messages')}</span>
                              <span className="mx-2">•</span>
                              <i className="bi bi-clock me-1"></i>
                              <span>{new Date(conversation.createdAt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                            </div>
                          </div>
                        </div>
                        <div className="ms-3 d-flex">
                          <Button
                            variant="outline-primary"
                            size="sm"
                            className="me-2"
                            onClick={(e) => {
                              e.stopPropagation();
                              viewConversation(conversation.id);
                            }}
                          >
                            <i className="bi bi-eye"></i>
                          </Button>
                          <Button
                            variant="outline-danger"
                            size="sm"
                            onClick={(e) => deleteConversation(conversation.id, e)}
                          >
                            <i className="bi bi-trash"></i>
                          </Button>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ConversationList;