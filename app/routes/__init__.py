"""API routes for the application."""

from app.routes.health_check import router as health_router
from app.routes.user import router as user_router

__all__ = ["health_router", "user_router"]
