import { API_CONFIG } from './api';

export interface ContactMessage {
  name: string;
  email: string;
  subject: string;
  message: string;
}

export interface ContactResponse {
  success: boolean;
  message: string;
  messageId?: number;
  submittedAt?: string;
  error?: string;
}

export interface ContactMessageDetails extends ContactMessage {
  id: number;
  createdAt: string;
  isRead: boolean;
  adminReply?: string;
  repliedAt?: string;
}

export interface ContactMessagePage {
  content: ContactMessageDetails[];
  totalElements: number;
  totalPages: number;
  size: number;
  number: number;
  first: boolean;
  last: boolean;
}

class ContactService {
  /**
   * Submit a contact message
   */  async submitContactMessage(contactData: ContactMessage): Promise<ContactResponse> {
    try {
      const response = await fetch(`${API_CONFIG.BASE_URL}/api/contact/submit`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(contactData),
      });      // Check if response has content before trying to parse JSON
      const contentType = response.headers.get('content-type');
      let data: ContactResponse = { success: false, message: "Unknown error" };
      
      if (contentType && contentType.includes('application/json')) {
        try {
          const text = await response.text();
          if (text && text.trim()) {
            data = JSON.parse(text);
          }
        } catch (parseError) {
          console.error('Error parsing JSON response:', parseError);
        }
      }

      if (!response.ok) {
        throw new Error(data.message || `HTTP ${response.status}: ${response.statusText}`);
      }

      return data;
    } catch (error) {
      console.error('Error submitting contact message:', error);
      throw error;
    }
  }

  /**
   * Get all contact messages (Admin only)
   */  async getAllMessages(page: number = 0, size: number = 10): Promise<ContactMessagePage> {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_CONFIG.BASE_URL}/api/contact/admin/messages?page=${page}&size=${size}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch contact messages');
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching contact messages:', error);
      throw error;
    }
  }

  /**
   * Get unread contact messages (Admin only)
   */  async getUnreadMessages(page: number = 0, size: number = 10): Promise<ContactMessagePage> {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_CONFIG.BASE_URL}/api/contact/admin/unread?page=${page}&size=${size}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch unread messages');
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching unread messages:', error);
      throw error;
    }
  }

  /**
   * Get unread message count (Admin only)
   */  async getUnreadCount(): Promise<number> {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_CONFIG.BASE_URL}/api/contact/admin/unread-count`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch unread count');
      }

      const data = await response.json();
      return data.unreadCount;
    } catch (error) {
      console.error('Error fetching unread count:', error);
      throw error;
    }
  }

  /**
   * Mark message as read (Admin only)
   */  async markAsRead(messageId: number): Promise<ContactResponse> {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_CONFIG.BASE_URL}/api/contact/admin/messages/${messageId}/read`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || 'Failed to mark message as read');
      }

      return data;
    } catch (error) {
      console.error('Error marking message as read:', error);
      throw error;
    }
  }

  /**
   * Reply to a contact message (Admin only)
   */  async replyToMessage(messageId: number, adminReply: string): Promise<ContactResponse> {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_CONFIG.BASE_URL}/api/contact/admin/messages/${messageId}/reply`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ adminReply }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || 'Failed to send reply');
      }

      return data;
    } catch (error) {
      console.error('Error sending reply:', error);
      throw error;
    }
  }

  /**
   * Search messages (Admin only)
   */  async searchMessages(keyword: string, page: number = 0, size: number = 10): Promise<ContactMessagePage> {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_CONFIG.BASE_URL}/api/contact/admin/search?keyword=${encodeURIComponent(keyword)}&page=${page}&size=${size}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('Failed to search messages');
      }

      return await response.json();
    } catch (error) {
      console.error('Error searching messages:', error);
      throw error;
    }
  }

  /**
   * Get messages by email (Admin only)
   */  async getMessagesByEmail(email: string): Promise<ContactMessageDetails[]> {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_CONFIG.BASE_URL}/api/contact/admin/by-email?email=${encodeURIComponent(email)}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch messages by email');
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching messages by email:', error);
      throw error;
    }
  }
}

export default new ContactService();
