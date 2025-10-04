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
