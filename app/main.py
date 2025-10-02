from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from app.routes import health_check
from app.services.world_time import get_world_times

app = FastAPI()

app.include_router(health_check.router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = get_world_times()
    return templates.TemplateResponse("index.html", {"request": request, "world_times": data})


if __name__ == "__main__":
    uvicorn.run(
        app,  # Module path to FastAPI instance
        host="0.0.0.0",  # or "0.0.0.0" to be reachable externally
        port=8000,
        reload=True,  # Auto-reload on code changes (dev only)
    )
