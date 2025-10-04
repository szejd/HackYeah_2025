from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from app.routes import health_check
from app.settings import SERVER_ADDRESS
from app.db_connection import SessionLocal

app = FastAPI()

app.include_router(health_check.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="static")


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


@app.get("/greet")
def greet(name: str = "World"):
    return {"message": f"Hello, {name}!"}


# Usage example: opening a session
if __name__ == "__main__":
    # Create a new session
    session = SessionLocal()
    try:
        pass
    finally:
        session.close()
