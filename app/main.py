from app.routes import health_check
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.services.world_time import get_world_times

app = FastAPI()

app.include_router(health_check.router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = get_world_times()
    return templates.TemplateResponse(
        "index.html", {"request": request, "world_times": data}
    )


@app.get("/greet")
def greet(name: str = "World"):
    return {"message": f"Hello, {name}!"}
