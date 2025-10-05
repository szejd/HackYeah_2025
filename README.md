# HackYeah 2025 - Digital Volunteer Center

A volunteer management platform built for HackYeah 2025 challenge. This system enables organizations to manage volunteer events, track participation, and coordinate volunteer activities efficiently.

## 📋 Prerequisites

- Python 3.13 or higher
- PostgreSQL 18 (for production)
- Docker & Docker Compose (optional, for containerized deployment)

## 🛠️ Tech Stack

- **Backend Framework**: FastAPI
- **Database**: SQLAlchemy with PostgreSQL support
- **Authentication**: JWT (PyJWT + bcrypt)
- **Templating**: Jinja2
- **Maps**: Folium, Geopy
- **Package Management**: uv

## 📦 Installation

### Local Development Setup

1. **Install uv** (Python package manager)

   Follow the [official installation guide](https://docs.astral.sh/uv/getting-started/installation/):

2. **Install Python 3.13** (if not already installed)

   ```bash
   uv python install 3.13
   ```

3. **Clone the repository**

   ```bash
   git clone https://github.com/szejd/HackYeah_2025.git
   cd HackYeah_2025
   ```

4. **Create and activate virtual environment**

   ```bash
   uv venv
   source .venv/bin/activate  # On Linux/macOS
   # or
   .\.venv\Scripts\activate.bat  # On Windows
   ```

5. **Install dependencies**

   ```bash
   uv sync --dev
   ```

6. **Set up environment variables**

   Create a `.env` file in the root directory. See `.env.example`.

### Docker Deployment

1. **Build and run with Docker Compose**

   ```bash
   docker compose up --build
   ```

2. **Access the application**
   - API: <http://localhost:8000>
   - API Documentation: <http://localhost:8000/docs>

## 🚀 Usage

### Running the Application

**Development Mode** (with auto-reload):

```bash
uv run fastapi dev
```

**Production Mode**:

```bash
uv run fastapi run
```

## 🧪 Testing

### Run All Tests

```bash
uv run pytest tests/ -v
```

## 🔍 Code Quality

### Linting & Formatting

Check code with Ruff:

```bash
uv run ruff check app/ tests/
```

Auto-fix issues:

```bash
uv run ruff check --fix app/ tests/
```

### Type Checking (Optional)

Using dmypy daemon for faster type checking:

```bash
# Start the daemon
uv run dmypy start

# Check files
uv run dmypy check -- app/ tests/

# Stop the daemon when done
uv run dmypy stop
```

## 📁 Project Structure

```bash
HackYeah_2025/
├── app/
│   ├── crud/           # Database CRUD operations
│   ├── db_handler/     # Database connection and utilities
│   ├── models/         # SQLAlchemy models
│   ├── routes/         # API endpoints
│   ├── schemas/        # Pydantic schemas and enums
│   ├── services/       # Business logic (OSM maps, etc.)
│   ├── static/         # Static files (CSS, JS, assets)
│   ├── templates/      # Jinja2 HTML templates
│   ├── utils/          # Utility functions (auth, time, etc.)
│   ├── config.py       # Configuration management
│   ├── logs.py         # Logging setup
│   └── main.py         # FastAPI application entry point
├── tests/              # Test suite
├── data/               # Data files
├── docker-compose.yml  # Docker composition
├── Dockerfile          # Docker image definition
├── pyproject.toml      # Project metadata and dependencies
└── README.md           # This file
```

## 🔐 Authentication

The application uses JWT (JSON Web Tokens) for authentication. Here's a quick example:

1. **Register a user**:

   ```bash
   curl -X POST "http://localhost:8000/users/register/volunteer" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "volunteer@example.com",
       "password": "SecurePass123",
       "first_name": "John",
       "last_name": "Doe"
     }'
   ```

2. **Login to get token**:

   ```bash
   curl -X POST "http://localhost:8000/users/login" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "volunteer@example.com",
       "password": "SecurePass123"
     }'
   ```

3. **Use token for authenticated requests**:

   ```bash
   curl -X GET "http://localhost:8000/users/me" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
   ```

## 📦 Adding Dependencies

To add a new package:

```bash
uv add package-name
```

For development dependencies:

```bash
uv add --dev package-name
```

## 👥 Team

Built with ❤️ for HackYeah 2025 ✨ŁapkiDevs✨
