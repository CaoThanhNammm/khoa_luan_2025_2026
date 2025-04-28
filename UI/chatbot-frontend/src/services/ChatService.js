import axios from "axios";
import AuthService from "./AuthService";

const API_URL = "/api/chat/";

class ChatService {
  getConversations() {
    return axios.get(API_URL + "conversations", {
      headers: AuthService.getAuthHeader()
    });
  }

  getConversation(id) {
    return axios.get(API_URL + "conversations/" + id, {
      headers: AuthService.getAuthHeader()
    });
  }

  startNewConversation(message) {
    return axios.post(
      API_URL + "conversations",
      { message },
      { headers: AuthService.getAuthHeader() }
    );
  }

  sendMessage(conversationId, message) {
    return axios.post(
      API_URL + `conversations/${conversationId}/messages`,
      { message },
      { headers: AuthService.getAuthHeader() }
    );
  }
  
  deleteConversation(id) {
    return axios.delete(API_URL + "conversations/" + id, {
      headers: AuthService.getAuthHeader()
    });
  }
}

const chatServiceInstance = new ChatService();
export default chatServiceInstance;