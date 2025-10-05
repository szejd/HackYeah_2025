from datetime import datetime, date
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db_handler.db_connection import get_db
from app.schemas.db_models import Event

router = APIRouter(prefix="/events", tags=["events"])


def _to_iso_date(dt: datetime | date) -> str:
    if isinstance(dt, datetime):
        return dt.date().isoformat()
    return dt.isoformat()


@router.get("/upcoming")
def get_upcoming_events(db: Session = Depends(get_db)) -> List[dict]:
    today = datetime.now()
    q = (
        db.query(Event)
        .filter(Event.start_date >= today)
        .order_by(Event.start_date.asc())
        .limit(500)
    )

    events = []
    for ev in q.all():
        events.append(
            {
                "id": ev.id,
                "name": ev.name,
                "description": ev.description,
                "start_date": ev.start_date.isoformat(),
                "end_date": ev.end_date.isoformat(),
            }
        )
    return events
