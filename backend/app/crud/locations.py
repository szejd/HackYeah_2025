from __future__ import annotations
from typing import TYPE_CHECKING
from pydantic import BaseModel
from app.schemas.db_models import Location, Volunteer, Organisation, Coordinator

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class LocationData(BaseModel):
    name: str
    latitude: float
    longitude: float


def add_location(session: Session, location_data: LocationData) -> int:
    if location_data.latitude > 90 or location_data.latitude < -90:
        raise ValueError(f"Bledne wspolrzedne - szerokosc geograficzna poza skala: dostarczona wartosc to {location_data.latitude}")
    if location_data.longitude > 180 or location_data.longitude < -180:
        raise ValueError(f"Bledne wspolrzedne - dlugosc geograficzna poza skala: dostarczona wartosc to {location_data.longitude}")
    new_location = Location(
        name=location_data.name,
        latitude=location_data.latitude,
        longitude=location_data.longitude
    )
    try:
        session.add(new_location)
        session.commit()
        session.refresh(new_location)
        return new_location.id
    except Exception as e:
        session.rollback()
        raise e


def get_location(session: Session, location_id: int) -> LocationData:
    db_location = session.get_one(Location, location_id)
    return LocationData(name=db_location.name, latitude=db_location.latitude, longitude=db_location.longitude)

