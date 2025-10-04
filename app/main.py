import logging

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from app.routes import auth, health_check, register, user
from app.config import SERVER_ADDRESS
from app.logs import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="HackYeah 2025 API",
    description="API for volunteer management system",
    version="1.0.0",
)

app.include_router(health_check.router)
app.include_router(auth.router)
app.include_router(register.router)
app.include_router(user.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(
        "main:app",  # Module path to FastAPI instance
        host=SERVER_ADDRESS,  # or "0.0.0.0" to be reachable externally
        port=8000,
        reload=True,  # Auto-reload on code changes (dev only)
    )
