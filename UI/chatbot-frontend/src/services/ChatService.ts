import axios from "./api";
import type { AxiosResponse } from "axios";
import type { ChatSession, Message } from "../types/chat";
import { adaptConversationToSession, adaptMessageToFrontend } from "../utils/apiAdapters";

const API_URL = "/api/chat/";

export interface ConversationResponse {
  id: string | number;
  title: string;
  createdAt: string;
  messages: MessageResponse[];
  hasDocument?: boolean;
  documentInfo?: {
    documentId: string;
    filename: string;
    fileSize: number;
    sentencesCount: number;
    uploadDate: string;
    status: string;
  };
}

export interface MessageRequest {
  message: string;
}

export interface MessageResponse {
  id: number;
  content: string;
  type: 'USER' | 'BOT';
  timestamp: string;
  conversationId: string | number;
}

class ChatService {
  async getConversations(): Promise<ChatSession[]> {
    const response = await axios.get<ConversationResponse[]>(API_URL + "conversations");
    return response.data.map(adaptConversationToSession);
  }

  async getConversation(id: string): Promise<ChatSession> {
    const response = await axios.get<ConversationResponse>(API_URL + "conversations/" + id);
    return adaptConversationToSession(response.data);
  }

  async startNewConversation(message: string): Promise<ChatSession> {
    const response = await axios.post<ConversationResponse>(
      API_URL + "conversations",
      { message }
    );
    return adaptConversationToSession(response.data);
  }

  async sendMessage(conversationId: string, message: string): Promise<Message> {
    const response = await axios.post<MessageResponse>(
      API_URL + `conversations/${conversationId}/messages`,
      { message }
    );
    return adaptMessageToFrontend(response.data);
  }

  async sendMessageStsv(conversationId: string, message: string): Promise<Message> {
    const response = await axios.post<MessageResponse>(
      API_URL + `conversations/${conversationId}/messages_stsv`,
      { message }
    );
    return adaptMessageToFrontend(response.data);
  }
  
  deleteConversation(id: string): Promise<AxiosResponse<{ message: string }>> {
    return axios.delete<{ message: string }>(API_URL + "conversations/" + id);
  }

  async startNewConversationWithDocument(message: string, documentId: string): Promise<ChatSession> {
    const response = await axios.post<ConversationResponse>(
      API_URL + "conversations/with-document",
      { message, document_id: documentId }
    );
    return adaptConversationToSession(response.data);
  }

  async createEmptyConversationWithDocument(documentId: string, filename: string, fileSize: number, status?: string, s3Key?: string, s3Url?: string): Promise<ChatSession> {
    const response = await axios.post<ConversationResponse>(
      API_URL + "conversations/empty-with-document",
      { 
        document_id: documentId, 
        filename: filename, 
        file_size: fileSize,
        title: `Cuộc trò chuyện với ${filename}`,
        status,
        s3_key: s3Key,
        s3_url: s3Url
      }
    );
    return adaptConversationToSession(response.data);
  }

  // Raw API methods for backward compatibility
  getConversationsRaw(): Promise<AxiosResponse<ConversationResponse[]>> {
    return axios.get<ConversationResponse[]>(API_URL + "conversations");
  }

  getConversationRaw(id: string): Promise<AxiosResponse<ConversationResponse>> {
    return axios.get<ConversationResponse>(API_URL + "conversations/" + id);
  }

  startNewConversationRaw(message: string): Promise<AxiosResponse<ConversationResponse>> {
    return axios.post<ConversationResponse>(
      API_URL + "conversations",
      { message }
    );
  }

  sendMessageRaw(conversationId: string, message: string): Promise<AxiosResponse<MessageResponse>> {
    return axios.post<MessageResponse>(
      API_URL + `conversations/${conversationId}/messages`,
      { message }
    );
  }

  sendMessageStsvRaw(conversationId: string, message: string): Promise<AxiosResponse<MessageResponse>> {
    return axios.post<MessageResponse>(
      API_URL + `conversations/${conversationId}/messages_stsv`,
      { message }
    );
  }
}

const chatServiceInstance = new ChatService();
export default chatServiceInstance;
