from __future__ import annotations
from typing import TYPE_CHECKING
from pydantic import BaseModel
from app.schemas.db_models import Location, Volunteer, Organisation, Coordinator
from app.schemas.enums import LocationType, UserType

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class LocationData(BaseModel):
    name: str
    latitude: float
    longitude: float
    category: LocationType


def add_location(session: Session, location_data: LocationData) -> int:
    if location_data.latitude > 90 or location_data.latitude < -90:
        raise ValueError(
            f"Bledne wspolrzedne - szerokosc geograficzna poza skala: dostarczona wartosc to {location_data.latitude}"
        )
    if location_data.longitude > 180 or location_data.longitude < -180:
        raise ValueError(
            f"Bledne wspolrzedne - dlugosc geograficzna poza skala: dostarczona wartosc to {location_data.longitude}"
        )
    new_location = Location(
        name=location_data.name,
        latitude=location_data.latitude,
        longitude=location_data.longitude,
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
    db_location: Location = session.get_one(Location, location_id)
    if len(db_location.events) > 0:
        location_type = LocationType.EVENT
    else:
        if db_location.users[0].user_type == UserType.VOLUNTEER:
            location_type = LocationType.VOLUNTEER
        elif db_location.users[0].user_type == UserType.ORGANISATION:
            location_type = LocationType.ORGANISATION
        else:
            raise ValueError("Nie mozna wydedukowac rodzaju lokalizacji")
    return LocationData(
        name=db_location.name, latitude=db_location.latitude, longitude=db_location.longitude, category=location_type
    )
