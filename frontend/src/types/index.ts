/**
 * Common type definitions for the app
 */

export interface HealthCheckResponse {
    status: string;
    timestamp?: string;
}

// Add more types as your app grows
export interface User {
    id: string;
    name: string;
    email: string;
}

export interface ApiError {
    message: string;
    code?: string;
    details?: any;
}
