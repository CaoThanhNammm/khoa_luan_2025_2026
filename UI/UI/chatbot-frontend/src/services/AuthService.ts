import axios from "./api";
import type { AxiosResponse } from "axios";

const API_URL = "/api/auth/";

export interface AuthResponse {
  token: string;
  type: string;
  id: number;
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
    
    return axios
      .post<AuthResponse>(API_URL + "login", { username, password })
      .then((response) => {
        console.log('Login response:', response);
        
        if (response.data && response.data.token) {
          // Create a properly structured user object before storing
          const userData = {
            id: response.data.id,
            username: response.data.username,
            email: response.data.email,
            token: response.data.token
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
    return axios.post<AuthResponse>(API_URL + "register", {
      username,
      email,
      password
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
