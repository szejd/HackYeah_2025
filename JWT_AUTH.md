# JWT Authentication Guide

This application now uses JWT (JSON Web Tokens) for authentication.

## How It Works

1. **Register a new user** using one of the registration endpoints
2. **Login** with email and password to receive a JWT token
3. **Use the token** in subsequent requests to protected endpoints

## Endpoints

### Public Endpoints (No Authentication Required)

- `POST /users/register/volunteer` - Register as a volunteer
- `POST /users/register/organisation` - Register as an organisation
- `POST /users/register/coordinator` - Register as a coordinator
- `POST /users/login` - Login and receive JWT token

### Protected Endpoints (Require JWT Token)

- `GET /users/me` - Get current authenticated user info
- `GET /users/me/profile` - Get current user's complete profile
- And any other endpoint that uses `CurrentUser` dependency

## Usage Examples

### 1. Register a New User

```bash
curl -X POST http://localhost:8000/users/register/volunteer \
  -H "Content-Type: application/json" \
  -d '{
    "user": {
      "email": "volunteer@example.com",
      "password": "password",
      "user_type": "volunteer"
    },
    "volunteer": {
      "first_name": "John",
      "last_name": "Doe",
      "birth_date": "1990-01-01",
      "phone_number": "+48123456789"
    }
  }'
```

### 2. Login to Get JWT Token

```bash
curl -X POST http://localhost:8000/users/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "volunteer@example.com",
    "password": "securepassword123"
  }'
```

Response:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "volunteer@example.com",
    "user_type": "volunteer",
    "created_at": "2025-10-04T12:00:00",
    "updated_at": "2025-10-04T12:00:00"
  }
}
```

### 3. Access Protected Endpoints

Use the token in the `Authorization` header:

```bash
curl -X GET http://localhost:8000/users/me \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

```bash
curl -X GET http://localhost:8000/users/me/profile \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## Frontend Integration

### JavaScript/Fetch Example

```javascript
// 1. Login
const loginResponse = await fetch('http://localhost:8000/users/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password123'
  })
});

const { access_token } = await loginResponse.json();

// 2. Store token (e.g., in localStorage)
localStorage.setItem('token', access_token);

// 3. Use token in protected requests
const profileResponse = await fetch('http://localhost:8000/users/me/profile', {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('token')}`
  }
});

const profile = await profileResponse.json();
```

## Configuration

### Environment Variables

Add these to your `.env` file:

```env
# JWT Configuration
JWT_SECRET_KEY=your-very-secret-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**IMPORTANT**: Change `JWT_SECRET_KEY` to a strong, random secret in production!

## Security Features

### Password Hashing

- Passwords are hashed using **bcrypt** (industry standard)
- Original passwords are never stored in the database
- Only password hashes are stored

### JWT Tokens

- Tokens are signed with HS256 algorithm
- Tokens expire after 30 minutes (configurable)
- Tokens contain: user ID, email, and user type

## Testing with Swagger UI

1. Start the server: `uv run fastapi run`
2. Open <http://localhost:8000/docs>
3. Click "Authorize" button at the top
4. Login to get a token
5. Enter the token in the format: `Bearer <your-token>`
6. Try protected endpoints

## Token Expiration

Tokens expire after 30 minutes by default. When a token expires:

- The API will return a 401 Unauthorized error
- The frontend should redirect to login page
- User needs to login again to get a fresh token

### Handling Expired Tokens

```javascript
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
```

## Adding Authentication to Your Endpoints

To protect any endpoint, add the `CurrentUser` dependency:

```python
from app.routes.user import CurrentUser

@router.get("/protected-endpoint")
async def protected_endpoint(current_user: CurrentUser):
    """This endpoint requires authentication."""
    return {
        "message": f"Hello {current_user.email}",
        "user_id": current_user.id
    }
```

# Frontend Logout Implementation Guide

This guide explains how to implement logout functionality on the frontend to work with the JWT-based authentication API.

## Overview

Since the backend uses JWT tokens for authentication (stateless), the logout process primarily happens on the client side by discarding the token. The `/users/logout` endpoint validates the token before confirming logout.

---

## 1. Store the JWT Token

When the user logs in, store the token securely:

```javascript
// After successful login response
const loginResponse = await fetch('/users/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
});

const data = await loginResponse.json();

// Store the token (choose one approach):
localStorage.setItem('access_token', data.access_token);  // Option 1: localStorage
sessionStorage.setItem('access_token', data.access_token); // Option 2: sessionStorage
// Or use cookies with httpOnly flag for better security
```

**Storage Options:**

- `localStorage`: Persists across browser sessions (survives closing/reopening browser)
- `sessionStorage`: Only persists for the current browser session
- `httpOnly cookies`: Most secure, but requires backend cookie handling

---

## 2. Include Token in Authenticated Requests

For all protected endpoints, include the token in the Authorization header:

```javascript
const token = localStorage.getItem('access_token');

const response = await fetch('/users/me', {
    method: 'GET',
    headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    }
});
```

---

## 3. Implement Logout Function

Create a logout function that:

1. Calls the backend logout endpoint (optional but recommended)
2. Removes the token from storage
3. Redirects to login page

```javascript
async function logout() {
    const token = localStorage.getItem('access_token');
    
    try {
        // Optional: Call the backend logout endpoint to validate token
        await fetch('/users/logout', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
    } catch (error) {
        console.error('Logout error:', error);
    } finally {
        // Always clear the token, even if the API call fails
        localStorage.removeItem('access_token');
        // Clear any other user-related data
        localStorage.removeItem('user_data');
        
        // Redirect to login page
        window.location.href = '/login';
    }
}
```

---

## 4. Handle Token Expiration

Implement automatic logout when token expires or becomes invalid:

```javascript
async function makeAuthenticatedRequest(url, options = {}) {
    const token = localStorage.getItem('access_token');
    
    const response = await fetch(url, {
        ...options,
        headers: {
            ...options.headers,
            'Authorization': `Bearer ${token}`
        }
    });
    
    // If token expired or invalid, logout automatically
    if (response.status === 401) {
        localStorage.removeItem('access_token');
        window.location.href = '/login';
        throw new Error('Session expired. Please login again.');
    }
    
    return response;
}

// Use this wrapper for all authenticated requests
makeAuthenticatedRequest('/users/me/profile')
    .then(res => res.json())
    .then(data => console.log(data))
    .catch(err => console.error(err));
```

---

## 5. Add Logout Button to UI

### HTML Example

```html
<button id="logoutBtn" onclick="logout()">Logout</button>
```

### Or with Event Listener

```html
<button id="logoutBtn">Logout</button>

<script>
document.getElementById('logoutBtn').addEventListener('click', logout);
</script>
```

---

## 6. Optional: Check Token Expiration

For better UX, check if the token is expired before making requests:

```javascript
/**
 * Decode JWT and check if it's expired
 * @param {string} token - JWT token
 * @returns {boolean} - true if expired, false otherwise
 */
function isTokenExpired(token) {
    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        const exp = payload.exp * 1000; // Convert to milliseconds
        return Date.now() >= exp;
    } catch (e) {
        return true; // If we can't decode, treat as expired
    }
}

// Check before each request
const token = localStorage.getItem('access_token');
if (!token || isTokenExpired(token)) {
    logout();
}
```

---

## 7. Complete Example: Auth Utility Module

Here's a complete example combining all the concepts:

```javascript
// auth.js - Authentication utility module

class AuthService {
    constructor() {
        this.TOKEN_KEY = 'access_token';
        this.USER_KEY = 'user_data';
    }

    /**
     * Store authentication token and user data
     */
    setAuth(token, user) {
        localStorage.setItem(this.TOKEN_KEY, token);
        localStorage.setItem(this.USER_KEY, JSON.stringify(user));
    }

    /**
     * Get stored authentication token
     */
    getToken() {
        return localStorage.getItem(this.TOKEN_KEY);
    }

    /**
     * Get stored user data
     */
    getUser() {
        const user = localStorage.getItem(this.USER_KEY);
        return user ? JSON.parse(user) : null;
    }

    /**
     * Check if user is authenticated
     */
    isAuthenticated() {
        const token = this.getToken();
        if (!token) return false;
        return !this.isTokenExpired(token);
    }

    /**
     * Check if token is expired
     */
    isTokenExpired(token) {
        try {
            const payload = JSON.parse(atob(token.split('.')[1]));
            const exp = payload.exp * 1000;
            return Date.now() >= exp;
        } catch (e) {
            return true;
        }
    }

    /**
     * Login user
     */
    async login(email, password) {
        const response = await fetch('/users/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        if (!response.ok) {
            throw new Error('Login failed');
        }

        const data = await response.json();
        this.setAuth(data.access_token, data.user);
        return data;
    }

    /**
     * Logout user
     */
    async logout() {
        const token = this.getToken();
        
        try {
            // Call backend logout endpoint
            await fetch('/users/logout', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });
        } catch (error) {
            console.error('Logout error:', error);
        } finally {
            // Always clear local data
            localStorage.removeItem(this.TOKEN_KEY);
            localStorage.removeItem(this.USER_KEY);
            window.location.href = '/login';
        }
    }

    /**
     * Make authenticated API request
     */
    async request(url, options = {}) {
        const token = this.getToken();
        
        if (!token || this.isTokenExpired(token)) {
            await this.logout();
            throw new Error('Session expired');
        }

        const response = await fetch(url, {
            ...options,
            headers: {
                ...options.headers,
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.status === 401) {
            await this.logout();
            throw new Error('Unauthorized');
        }

        return response;
    }
}

// Create singleton instance
const authService = new AuthService();
export default authService;
```

### Usage Example

```javascript
import authService from './auth.js';

// Login
async function handleLogin(email, password) {
    try {
        const data = await authService.login(email, password);
        console.log('Logged in:', data.user);
        window.location.href = '/dashboard';
    } catch (error) {
        console.error('Login failed:', error);
        alert('Login failed. Please check your credentials.');
    }
}

// Logout
async function handleLogout() {
    await authService.logout();
}

// Make authenticated request
async function fetchUserProfile() {
    try {
        const response = await authService.request('/users/me/profile');
        const profile = await response.json();
        console.log('Profile:', profile);
    } catch (error) {
        console.error('Failed to fetch profile:', error);
    }
}

// Check if authenticated
if (!authService.isAuthenticated()) {
    window.location.href = '/login';
}
```
