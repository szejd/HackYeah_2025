from backend.app.schemas.enums import UserType

from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy.orm import relationship
import datetime
from sqlalchemy import (
    Integer, String, Enum, DateTime, Text, ForeignKey, Boolean, Date
)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    user_type: Mapped[UserType] = mapped_column(Enum, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.datetime.now(),
                                                 onupdate=datetime.datetime.now())

    # Relationships to subclasses
    volunteer = relationship("Volunteer", uselist=False, back_populates="user", cascade="delete-orphan")
    organisation = relationship("Organisation", uselist=False, back_populates="user", cascade="delete-orphan")
    coordinator = relationship("Coordinator", uselist=False, back_populates="user", cascade="delete-orphan")


class Volunteer(Base):
    __tablename__ = 'volunteer'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    birth_date: Mapped[datetime.date] = mapped_column(Date)
    phone_number: Mapped[str] = mapped_column(String(20))

    user = relationship("User", back_populates="volunteer")
    skills = relationship("Skill", back_populates="volunteer")


class Organisation(Base):
    __tablename__ = 'organisation'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    org_name: Mapped[str] = mapped_column(String(255))
    contact_person: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text)
    phone_number: Mapped[str] = mapped_column(String(20))
    address: Mapped[str] = mapped_column(Text)
    verified: Mapped[bool] = mapped_column(Boolean)

    user = relationship("User", back_populates="organisation")


class Coordinator(Base):
    __tablename__ = 'coordinator'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    school: Mapped[str] = mapped_column(String(500))
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    phone_number: Mapped[str] = mapped_column(String(20))
    verified: Mapped[bool] = mapped_column(Boolean)

    user = relationship("User", back_populates="coordinator")


class Skill(Base):
    __tablename__ = 'skill'

    id: Mapped[int] = mapped_column(primary_key=True)
    skill_name: Mapped[str] = mapped_column(Text)

    volunteer = relationship("Volunteer", back_populates="skills")
