/**
 * API Service
 * Handles all communication with the FastAPI backend
 */

import {API_BASE_URL as ENV_API_URL} from '@env';

const API_BASE_URL = ENV_API_URL || 'http://10.0.2.2:8000';

interface ApiResponse<T> {
  data?: T;
  error?: string;
  status: number;
}

class ApiService {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  /**
   * Generic GET request
   */
  async get<T>(endpoint: string): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      const data = await response.json();

      return {
        data,
        status: response.status,
      };
    } catch (error) {
      console.error('API GET Error:', error);
      return {
        error: error instanceof Error ? error.message : 'Unknown error',
        status: 500,
      };
    }
  }

  /**
   * Generic POST request
   */
  async post<T, R>(endpoint: string, body: T): Promise<ApiResponse<R>> {
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      });

      const data = await response.json();

      return {
        data,
        status: response.status,
      };
    } catch (error) {
      console.error('API POST Error:', error);
      return {
        error: error instanceof Error ? error.message : 'Unknown error',
        status: 500,
      };
    }
  }

  /**
   * Health check endpoint
   */
  async healthCheck(): Promise<ApiResponse<{status: string}>> {
    return this.get('/health');
  }
}

export const apiService = new ApiService();
export default ApiService;
