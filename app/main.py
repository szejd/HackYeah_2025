import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from app.routes import user, health_check, navigation, event
from app.logs import setup_logging
from app.config import SERVER_ADDRESS
from app.db_handler.db_connection import init_db, engine

setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize database
    logger.info("Initializing database...")
    init_db(engine)
    logger.info("Database initialized successfully")
    yield
    # Shutdown: cleanup if needed
    logger.info("Shutting down...")


app = FastAPI(
    title="HackYeah 2025 API",
    description="API for volunteer management system",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(health_check.router)
app.include_router(user.router)
app.include_router(navigation.router)
app.include_router(event.router)


app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(
        "main:app",  # Module path to FastAPI instance
        host=SERVER_ADDRESS,
        port=8000,
        reload=True,  # Auto-reload on code changes (dev only)
    )
