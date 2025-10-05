from geopy.geocoders import Nominatim
from app.schemas.db_models import Location, User
from app.schemas.enums import LocationType, UserType
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.location import AddLocation

def address_to_coordinates(address: str) -> tuple[float, float]:
    geolocator = Nominatim(user_agent="osm_address_locator")
    location = geolocator.geocode(address)
    if location:
        # print(f"Address: {address}")
        # print(f"Latitude: {location.latitude}, Longitude: {location.longitude}")
        return (location.latitude, location.longitude)
    else:
        raise ValueError("Address not found.")

def add_address(session: Session, location_data: AddLocation) -> Location:
    latitude, longitude = address_to_coordinates(location_data.address)
    location = Location(name=location_data.location_name,
                        latitude=latitude,
                        longitude=longitude)

    try:
        session.add(location)
        session.commit()
        session.refresh(location)
    except Exception as e:
        session.rollback()
        raise e
    return location

def get_all_locations(session: Session) -> list[Location]:
    locations = session.execute(select(Location)).scalars().all()
    return locations

def get_locations_for_location_type(session: Session, location_type: LocationType) -> list[Location]:
    if location_type == LocationType.EVENT:
        stmt = select(Location).where(Location.events.any())
        locations = session.execute(stmt).scalars().all()
    elif location_type == LocationType.ORGANISATION:
        stmt = select(Location).where(
            Location.users.any(User.user_type == UserType.ORGANISATION)
        )
        locations = session.execute(stmt).scalars().all()
    return locations
