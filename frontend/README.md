# HackYeah 2025 - React Native Frontend

React Native mobile application for HackYeah 2025 project.
This is a new [**React Native**](https://reactnative.dev) project, bootstrapped using [`@react-native-community/cli`](https://github.com/react-native-community/cli).

## Prerequisites

- Node.js (v18 or higher)
- npm or yarn
- Java Development Kit (JDK) 17 or higher
- Android Studio with Android SDK
- Android device or emulator

> **Note**: Make sure you have completed the [Set Up Your Environment](https://reactnative.dev/docs/set-up-your-environment) guide before proceeding.

## Setup Instructions

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Update `.env` with your configuration:

- `API_BASE_URL` - Backend API URL
  - For Android Emulator: `http://10.0.2.2:8000` (default)
  - For Physical Device: `http://<your-local-ip>:8000`
  - For Production: Your production API URL

### 3. Android Setup

1. **Install Android Studio**
   - Download from [developer.android.com](https://developer.android.com/studio)

2. **Install Android SDK**
   - Open Android Studio
   - Go to Settings → Appearance & Behavior → System Settings → Android SDK
   - Install SDK Platform 34 (or latest)
   - Install SDK Build-Tools

3. **Set Environment Variables**
   Add to your `~/.bashrc` or `~/.zshrc`:

   ```bash
   export ANDROID_HOME=$HOME/Android/Sdk
   export PATH=$PATH:$ANDROID_HOME/emulator
   export PATH=$PATH:$ANDROID_HOME/platform-tools
   ```

4. **Create Virtual Device (AVD)**
   - Open Android Studio
   - Tools → Device Manager
   - Create a new virtual device (Pixel 5 recommended)

## Running the App

### Step 1: Start Metro

First, you will need to run **Metro**, the JavaScript build tool for React Native.

To start the Metro dev server, run the following command from the root of your React Native project:

```sh
# Using npm
npm start

# OR using Yarn
yarn start
```

## Step 2: Build and run your app

With Metro running, open a new terminal window/pane from the root of your React Native project, and use one of the following commands to build and run your Android or iOS app:

### Android

```sh
# Using npm
npm run android

# OR using Yarn
yarn android
```

Make sure:

- You have an Android emulator running, OR
- An Android device connected via USB with USB debugging enabled

### iOS

> **Note**: iOS development requires macOS.

For iOS, remember to install CocoaPods dependencies (this only needs to be run on first clone or after updating native deps).

The first time you create a new project, run the Ruby bundler to install CocoaPods itself:

```sh
bundle install
```

Then, and every time you update your native dependencies, run:

```sh
bundle exec pod install
```

For more information, please visit [CocoaPods Getting Started guide](https://guides.cocoapods.org/using/getting-started.html).

```sh
# Using npm
npm run ios

# OR using Yarn
yarn ios
```

If everything is set up correctly, you should see your new app running in the Android Emulator, iOS Simulator, or your connected device.

This is one way to run your app — you can also build it directly from Android Studio or Xcode.

## Step 3: Modify your app

Now that you have successfully run the app, let's make changes!

Open `App.tsx` in your text editor of choice and make some changes. When you save, your app will automatically update and reflect these changes — this is powered by [Fast Refresh](https://reactnative.dev/docs/fast-refresh).

When you want to forcefully reload, for example to reset the state of your app, you can perform a full reload:

- **Android** google it.

## Congratulations! :tada:

You've successfully run and modified your React Native App. :partying_face:

### Now what?

- If you want to add this new React Native code to an existing application, check out the [Integration guide](https://reactnative.dev/docs/integration-with-existing-apps).
- If you're curious to learn more about React Native, check out the [docs](https://reactnative.dev/docs/getting-started).

## Troubleshooting

If you're having issues getting the above steps to work, see the [Troubleshooting](https://reactnative.dev/docs/troubleshooting) page.

## Common Issues

### Metro Bundler Issues

If you encounter caching issues:

```bash
npm start -- --reset-cache
```

### Build Errors

Clean the Android build:

```bash
cd android && ./gradlew clean
cd .. && npm run android
```

### Package Installation Issues

Remove and reinstall dependencies:

```bash
rm -rf node_modules package-lock.json
npm install
```

### Android Emulator Connection

If the app can't connect to the backend:

1. Make sure your backend is running at `http://localhost:8000`
2. For emulator, use `http://10.0.2.2:8000` in `.env`
3. For physical device, use your computer's local IP (e.g., `http://192.168.1.100:8000`)

## Backend Connection

The app is configured to connect to the FastAPI backend. Make sure the backend is running before starting the app:

```bash
# In the backend directory
cd ../backend
uv run uvicorn app.main:app --reload
```

The backend will be available at:

- API: `http://localhost:8000`
- Docs: `http://localhost:8000/docs`
- Health: `http://localhost:8000/health`

## Project Structure

```bash
frontend/
├── android/              # Android native code
├── ios/                 # iOS native code (if needed)
├── src/                 # Source code
│   ├── components/      # Reusable components (create as needed)
│   ├── screens/         # Screen components (create as needed)
│   ├── services/        # API services
│   │   └── api.ts       # API service for backend communication
│   ├── types/           # TypeScript types
│   │   ├── index.ts     # Common type definitions
│   │   └── env.d.ts     # Environment variable types
│   └── utils/           # Utility functions (create as needed)
├── App.tsx              # Main app component
├── .env                 # Environment variables (not in git)
├── .env.example         # Example environment variables
├── babel.config.js      # Babel configuration
├── package.json         # Dependencies
└── tsconfig.json        # TypeScript configuration
```

## Available Scripts

- `npm start` - Start Metro bundler
- `npm run android` - Run on Android
- `npm run ios` - Run on iOS (macOS only)
- `npm test` - Run tests
- `npm run lint` - Run linter

## Learn More

To learn more about React Native, take a look at the following resources:

- [React Native Website](https://reactnative.dev) - learn more about React Native.
- [Getting Started](https://reactnative.dev/docs/environment-setup) - an **overview** of React Native and how setup your environment.
- [Learn the Basics](https://reactnative.dev/docs/getting-started) - a **guided tour** of the React Native **basics**.
- [Blog](https://reactnative.dev/blog) - read the latest official React Native **Blog** posts.
- [`@facebook/react-native`](https://github.com/facebook/react-native) - the Open Source; GitHub **repository** for React Native.
