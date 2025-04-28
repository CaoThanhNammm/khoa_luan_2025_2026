import axios from "axios";
import AuthService from "./AuthService";

const API_URL = "/api/users/";

class UserService {
  getUserProfile() {
    return axios.get(API_URL + "profile", { 
      headers: AuthService.getAuthHeader() 
    });
  }

  updateProfile(userData) {
    return axios.put(API_URL + "profile", userData, {
      headers: AuthService.getAuthHeader()
    }).then(response => {
      // Update the stored user data if necessary
      const currentUser = AuthService.getCurrentUser();
      if (currentUser) {
        // Only update username and email, not the token
        currentUser.username = userData.username;
        currentUser.email = userData.email;
        localStorage.setItem("user", JSON.stringify(currentUser));
      }
      return response.data;
    });
  }

  updatePassword(passwordData) {
    return axios.put(API_URL + "password", passwordData, {
      headers: AuthService.getAuthHeader()
    });
  }

  updateSettings(settingsData) {
    return axios.put(API_URL + "settings", settingsData, {
      headers: AuthService.getAuthHeader()
    });
  }
}

const userServiceInstance = new UserService();
export default userServiceInstance;