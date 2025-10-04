from datetime import date

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette import status

from app.db_handler.db_connection import get_db
from app.schemas.db_models import User
from app.schemas.enums import UserType
from app.crud.user_crud import UserInfo, VolunteerInfo, add_user

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/register", response_class=HTMLResponse, tags=["auth"])
async def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "error": None})


@router.post("/register", response_class=HTMLResponse, tags=["auth"])
async def register(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    phone_number: str = Form(...),
    birth_date: str = Form(...),
    db: Session = Depends(get_db),
):
    # Basic required fields check (FastAPI Form(...) already enforces presence)
    # Validate unique email
    existing = db.query(User).filter(User.email == email).first()
    if existing is not None:
        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "error": "Użytkownik z takim adresem email już istnieje.",
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "phone_number": phone_number,
                "birth_date": birth_date,
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    # Parse birth date (YYYY-MM-DD)
    try:
        bd = date.fromisoformat(birth_date)
    except ValueError:
        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "error": "Nieprawidłowy format daty urodzenia (użyj RRRR-MM-DD).",
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "phone_number": phone_number,
                "birth_date": birth_date,
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    # For demo: store password as plain text in password_hash (aligns with current login logic)
    user_info = UserInfo(email=email, password_hash=password, user_type=UserType.VOLUNTEER)
    volunteer_info = VolunteerInfo(
        first_name=first_name,
        last_name=last_name,
        birth_date=bd,
        phone_number=phone_number,
    )

    try:
        _ = add_user(db, user_info, volunteer_info)
    except Exception:
        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "error": "Wystąpił błąd podczas tworzenia konta. Spróbuj ponownie.",
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "phone_number": phone_number,
                "birth_date": birth_date,
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    # Success: redirect to login page
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
