# React Native Frontend Setup - Quick Start Guide

## ✅ What Has Been Set Up

Your React Native Android app is now ready! Here's what was configured:

### 1. Project Structure
- ✅ React Native 0.81.4 initialized
- ✅ TypeScript support enabled
- ✅ Environment variable support configured
- ✅ API service for backend communication
- ✅ Type definitions for TypeScript

### 2. Configuration Files
- ✅ `.env` - Environment variables (API_BASE_URL configured for Android emulator)
- ✅ `.env.example` - Template for environment variables
- ✅ `babel.config.js` - Configured with react-native-dotenv
- ✅ `.gitignore` - Updated to exclude .env files

### 3. Source Code
- ✅ `src/services/api.ts` - API service for FastAPI backend
- ✅ `src/types/index.ts` - Common type definitions
- ✅ `src/types/env.d.ts` - Environment variable types
- ✅ `App.example.tsx` - Example app with backend health check

### 4. Dependencies Installed
- ✅ All React Native dependencies
- ✅ react-native-dotenv for environment variables

## 🚀 Next Steps

### 1. Test the Setup (Recommended)

Replace the default App.tsx with the example:

```bash
cd /home/maokx/PythonProjects/HackYeah_2025/frontend
cp App.example.tsx App.tsx
```

This example app will:
- Show a health check connection to your FastAPI backend
- Display helpful debugging information
- Demonstrate how to use the API service

### 2. Start the Backend

In a separate terminal:

```bash
cd /home/maokx/PythonProjects/HackYeah_2025/backend
uv run uvicorn app.main:app --reload
```

### 3. Start the React Native App

Terminal 1 - Start Metro:
```bash
cd /home/maokx/PythonProjects/HackYeah_2025/frontend
npm start
```

Terminal 2 - Run on Android:
```bash
cd /home/maokx/PythonProjects/HackYeah_2025/frontend
npm run android
```

## 📱 Android Emulator Setup

If you don't have an Android emulator yet:

1. **Install Android Studio**
   - Download from https://developer.android.com/studio

2. **Open Android Studio**
   - Go to: Tools → Device Manager
   - Click "Create Device"
   - Select: Pixel 5 or similar
   - Download and select: Android 14 (API 34) or latest
   - Click "Finish"

3. **Set Environment Variables**
   
   Add to `~/.bashrc` or `~/.zshrc`:
   ```bash
   export ANDROID_HOME=$HOME/Android/Sdk
   export PATH=$PATH:$ANDROID_HOME/emulator
   export PATH=$PATH:$ANDROID_HOME/platform-tools
   ```

   Then reload:
   ```bash
   source ~/.bashrc  # or source ~/.zshrc
   ```

4. **Start the Emulator**
   ```bash
   # List available devices
   emulator -list-avds
   
   # Start an emulator
   emulator -avd <device_name>
   ```

## 🔧 Configuration

### Environment Variables (.env)

The `.env` file contains:

```bash
API_BASE_URL=http://10.0.2.2:8000  # For Android emulator
API_TIMEOUT=30000
NODE_ENV=development
```

**Important Network Notes:**
- **Android Emulator**: Use `http://10.0.2.2:8000` (already configured)
- **Physical Android Device**: Use your computer's local IP (e.g., `http://192.168.1.100:8000`)
- **Production**: Update to your production API URL

To find your local IP:
```bash
# Linux/Mac
ip addr show | grep inet
# or
ifconfig | grep inet
```

## 📁 Project Structure

```
frontend/
├── android/              # Android native code
├── src/
│   ├── services/
│   │   └── api.ts       # API service for backend communication
│   └── types/
│       ├── index.ts     # Type definitions
│       └── env.d.ts     # Environment variable types
├── App.tsx              # Main app component
├── App.example.tsx      # Example app with backend connection
├── .env                 # Environment variables (not in git)
├── .env.example         # Environment template
├── babel.config.js      # Babel config with dotenv support
└── package.json         # Dependencies
```

## 🛠️ Using the API Service

The API service is ready to use in your components:

```typescript
import {apiService} from './src/services/api';

// Health check
const response = await apiService.healthCheck();

// GET request
const data = await apiService.get('/your-endpoint');

// POST request
const result = await apiService.post('/your-endpoint', {
  key: 'value'
});
```

## 📝 Development Workflow

1. **Start Backend** (Terminal 1):
   ```bash
   cd backend && uv run uvicorn app.main:app --reload
   ```

2. **Start Metro** (Terminal 2):
   ```bash
   cd frontend && npm start
   ```

3. **Run Android** (Terminal 3):
   ```bash
   cd frontend && npm run android
   ```

4. **Make Changes**:
   - Edit files in `frontend/src/`
   - App will auto-reload with Fast Refresh
   - Press 'r' in Metro terminal to manually reload

## 🐛 Troubleshooting

### Can't connect to backend?

1. Check backend is running: `http://localhost:8000/health`
2. Verify `.env` has correct `API_BASE_URL`
3. For emulator: Must use `http://10.0.2.2:8000`
4. For device: Must use local IP (not localhost)

### Build errors?

```bash
cd android && ./gradlew clean
cd .. && npm run android
```

### Metro cache issues?

```bash
npm start -- --reset-cache
```

### Package issues?

```bash
rm -rf node_modules package-lock.json
npm install
```

## 📚 Resources

- [React Native Docs](https://reactnative.dev/docs/getting-started)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [TypeScript Docs](https://www.typescriptlang.org/docs/)
- [Android Studio Guide](https://developer.android.com/studio/intro)

## ✨ You're Ready!

Your React Native app is fully configured and ready for development. The example app demonstrates backend connectivity and provides a starting point for your HackYeah 2025 project!

Happy coding! 🚀
