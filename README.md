# HackYeah 2025

A full-stack application with FastAPI backend and React Native mobile frontend.

## Project Structure

```
HackYeah_2025/
├── backend/          # FastAPI backend
│   ├── app/         # Application code
│   ├── tests/       # Backend tests
│   └── pyproject.toml
├── frontend/        # React Native mobile app
│   ├── android/     # Android native code
│   ├── src/         # App source code
│   └── package.json
└── README.md
```

## Quick Start

### Backend (FastAPI)

1. **Navigate to backend directory:**

   ```bash
   cd backend
   ```

2. **Install dependencies:**

   ```bash
   uv sync
   ```

3. **Run the server:**

   ```bash
   uv run fastapi run
   ```

   The API will be available at `http://localhost:8000`

   - API Documentation: `http://localhost:8000/docs`
   - Health Check: `http://localhost:8000/health`

### Frontend (React Native)

1. **Navigate to frontend directory:**

   ```bash
   cd frontend
   ```

2. **Install dependencies:**

   ```bash
   npm install
   ```

3. **Set up environment:**

   ```bash
   cp .env.example .env
   ```

4. **Start Metro bundler:**

   ```bash
   npm start
   ```

5. **Run on Android (in a new terminal):**

   ```bash
   npm run android
   ```

## Development Workflow

1. **Start Backend:**

   ```bash
   cd backend && uv run uvicorn app.main:app --reload
   ```

2. **Start Frontend:**

   ```bash
   cd frontend && npm start
   ```

3. **Run Android App:**

   ```bash
   cd frontend && npm run android
   ```

## Prerequisites

### Backend

- Python 3.11+
- uv package manager

### Frontend

- Node.js 18+
- npm or yarn
- Java JDK 17+
- Android Studio with Android SDK
- Android Emulator or physical device

## Environment Variables

### Backend

Configure in `backend/.env` (if needed)

### Frontend

Configure in `frontend/.env`:

- `API_BASE_URL` - Backend API URL (default: `http://10.0.2.2:8000` for Android emulator)

## Testing

### Backend Tests

```bash
cd backend
uv run pytest
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Documentation

- Backend: See [backend/README.md](backend/README.md)
- Frontend: See [frontend/README.md](frontend/README.md)

## Tech Stack

- **Backend:** FastAPI, Python 3.13, uvicorn
- **Frontend:** React Native, TypeScript, React 18
- **Build Tools:** uv (backend), npm (frontend)

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request
