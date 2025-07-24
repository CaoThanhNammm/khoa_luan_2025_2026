import axios from "./api";
import type { AxiosResponse } from "axios";

const API_URL = "/api/auth/";

export interface AuthResponse {
  access_token?: string;
  token?: string;
  token_type?: string;
  type?: string;
  id: number;
  user_id?: number;
  username: string;
  email: string;
}

export interface User {
  id: number;
  username: string;
  email: string;
  token: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export interface ForgotPasswordRequest {
  email: string;
}

export interface ResetPasswordRequest {
  token: string;
  newPassword: string;
}

class AuthService {
  login(username: string, password: string): Promise<AxiosResponse<AuthResponse>> {
    console.log('Attempting login with username:', username);
    
    // FastAPI OAuth2 login requires form data format
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);
    
    return axios
      .post<AuthResponse>(API_URL + "login", formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      })
      .then((response) => {
        console.log('Login response:', response);
        
        // Handle both token and access_token formats for compatibility
        const token = response.data.access_token || response.data.token;
        const userId = response.data.user_id || response.data.id;
        
        if (response.data && token) {
          // Create a properly structured user object before storing
          const userData = {
            id: userId,
            username: response.data.username,
            email: response.data.email,
            token: token
          };
          localStorage.setItem("user", JSON.stringify(userData));
          console.log('User data saved to localStorage');
        } else {
          console.warn('Login response missing token or data');
        }
        return response;
      })
      .catch(error => {
        console.error('Login error details:', error.response?.data || error.message);
        console.error('Login error status:', error.response?.status);
        console.error('Login error headers:', error.response?.headers);
        
        // Log the full error response for debugging
        if (error.response) {
          console.error('Full error response:', {
            status: error.response.status,
            statusText: error.response.statusText,
            data: error.response.data,
            headers: error.response.headers
          });
        }
        
        throw error;
      });
  }

  register(username: string, email: string, password: string): Promise<AxiosResponse<AuthResponse>> {
    console.log('Attempting registration with username:', username, 'email:', email);
    
    return axios.post<AuthResponse>(API_URL + "register", {
      username,
      email,
      password
    }, {
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      }
    }).then((response) => {
      console.log('Registration response:', response);
      return response;
    }).catch(error => {
      console.error('Registration error details:', error.response?.data || error.message);
      console.error('Registration error status:', error.response?.status);
      console.error('Registration error headers:', error.response?.headers);
      
      // Log the full error response for debugging
      if (error.response) {
        console.error('Full registration error response:', {
          status: error.response.status,
          statusText: error.response.statusText,
          data: error.response.data,
          headers: error.response.headers
        });
      }
      
      throw error;
    });
  }

  forgotPassword(email: string): Promise<AxiosResponse<{ message: string }>> {
    return axios.post<{ message: string }>(API_URL + "forgot-password", { email });
  }

  resetPassword(token: string, password: string): Promise<AxiosResponse<{ message: string }>> {
    return axios.post<{ message: string }>(API_URL + "reset-password", {
      token: token,
      newPassword: password
    });
  }

  logout(): void {
    localStorage.removeItem("user");
  }

  getCurrentUser(): User | null {
    const userStr = localStorage.getItem("user");
    if (userStr) return JSON.parse(userStr);
    return null;
  }

  getAuthHeader(): { Authorization: string } | Record<string, never> {
    const user = this.getCurrentUser();
    if (user && user.token) {
      return { Authorization: 'Bearer ' + user.token };
    } else {
      return {};
    }
  }
}

const authServiceInstance = new AuthService();
export default authServiceInstance;
