from sqlalchemy.orm import Session
import pandas as pd
import os
from app.crud.user import create_organisation, OrganisationCreate
from app.crud.location import add_address, get_all_locations
from app.models.location import AddLocation, LocationData
from app.schemas.db_models import User
from app.schemas.enums import UserType, LocationType
from app.services.osm_maps import generate_map_with_locations
from app.db_handler.db_connection import SessionLocal


def add_data(session: Session):
    add_schools_as_organisations(session=session)
    add_events(session)

def add_events(session: Session):
    pass

def add_schools_as_organisations(session: Session):
    primary_schools_csv_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))),
        "data",
        "Szkoły podstawowe samorządowe w roku 2023-2024 - liczba uczniów (2025-10-04 23-03-03).csv",
    )

    df = pd.read_csv(primary_schools_csv_path)
    idx = 0
    for row in df.itertuples(index=True):
        idx += 1
        schoole_name = row._4
        address = f"{row.Ulica} {row._24}, {row.Miejscowość}"
        print(f"{schoole_name}: {address}")
        user_db = User(email=f"test{idx}@krakow.um.pl", password_hash="dummy@#$pass", user_type=UserType.ORGANISATION)
        session.add(user_db)
        session.commit()
        session.refresh(user_db)
        org = OrganisationCreate(
            org_name=schoole_name,
            contact_person=f"Smok Wawelski nr {idx}",
            description=schoole_name,
            phone_number="123456789",
            address=address,
            verified=True,
        )

        org = create_organisation(session, user_db, org_data=org)
        location_data = AddLocation(address=org.address, location_name=org.org_name)
        location = add_address(session=session, location_data=location_data)
        user_db.location_id = location.id
        session.commit()
        session.refresh(user_db)
        session.refresh(location)


session = SessionLocal()
add_schools_as_organisations(session)
locations = get_all_locations(session)
location_datas = []
for location in locations:
    location_datas.append(
        LocationData(
            name=location.name,
            latitude=location.latitude,
            longitude=location.longitude,
            category=LocationType.ORGANISATION,
        )
    )
generate_map_with_locations(location_datas)
