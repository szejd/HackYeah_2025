from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette import status
from sqlalchemy.orm import Session

from app.db_handler.db_connection import get_db
from app.schemas.db_models import User

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/login", response_class=HTMLResponse, tags=["auth"])
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})


@router.post("/login", response_class=HTMLResponse, tags=["auth"])
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user: User | None = db.query(User).filter(User.email == email).first()

    error = None
    if user is None:
        error = "Nieprawidłowy email lub hasło."
    else:
        # For now, treat stored password_hash as plain text for demo purposes
        if user.password_hash != password:
            error = "Nieprawidłowy email lub hasło."

    if error:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": error, "email": email},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    # Auth success: set a simple cookie identifying the user.
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="auth_user_id", value=str(user.id), httponly=True, samesite="lax")
    return response


@router.post("/logout", tags=["auth"])
async def logout():
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("auth_user_id")
    return response
