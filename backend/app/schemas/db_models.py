from backend.app.schemas.enums import UserType

from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy.orm import relationship
import datetime
from sqlalchemy import (
    Integer, String, Enum, DateTime, Text, ForeignKey, func, Boolean, Date
)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    verified: Mapped[bool] = mapped_column(Boolean)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    user_type: Mapped[UserType] = mapped_column(Enum, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), onupdate=func.now())

    # Relationships to subclasses
    volunteer = relationship("Volunteer", uselist=False, back_populates="user")
    organisation = relationship("Organisation", uselist=False, back_populates="user")
    coordinator = relationship("Coordinator", uselist=False, back_populates="user")


class Volunteer(Base):
    __tablename__ = 'volunteer'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    birth_date: Mapped[datetime.date] = mapped_column(Date)
    phone_number: Mapped[int] = mapped_column(String(20))
    availability: Mapped[int] = mapped_column(Text)

    user = relationship("User", back_populates="volunteer")


class Organisation(Base):
    __tablename__ = 'organisation'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), primary_key=True)
    org_name: Mapped[int] = mapped_column(String(255))
    contact_person: Mapped[int] = mapped_column(String(100))
    description: Mapped[int] = mapped_column(Text)
    phone_number: Mapped[int] = mapped_column(String(20))
    address: Mapped[int] = mapped_column(Text)

    user = relationship("User", back_populates="organisation")


class Coordinator(Base):
    __tablename__ = 'coordinator'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), primary_key=True)
    first_name: Mapped[int] = mapped_column(String(100))
    last_name: Mapped[int] = mapped_column(String(100))
    phone_number: Mapped[int] = mapped_column(String(20))

    user = relationship("User", back_populates="coordinator")


class Skill(Base):
    __tablename__ = 'skill'

    id: Mapped[int] = mapped_column(primary_key=True)
    skill_name: Mapped[str] = mapped_column(Text)