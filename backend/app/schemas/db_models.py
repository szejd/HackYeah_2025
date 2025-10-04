from backend.app.schemas.enums import UserType
from backend.app.utils.time_utils import get_poland_time_now

from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy.orm import relationship
import datetime
from sqlalchemy import Integer, String, Enum, DateTime, Text, ForeignKey, Boolean, Date, Table, Column


class Base(DeclarativeBase):
    pass


# Many-to-many association tables
user_chat_association = Table(
    "user_chat_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("chat_id", Integer, ForeignKey("chat.id")),
)

user_domain_association = Table(
    "user_domain_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("domain_id", Integer, ForeignKey("domain.id")),
)

volunteer_skill_association = Table(
    "volunteer_skill_association",
    Base.metadata,
    Column("volunteer_id", Integer, ForeignKey("volunteer.id")),
    Column("skill_id", Integer, ForeignKey("skill.id")),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    user_type: Mapped[UserType] = mapped_column(Enum, nullable=False)
    location_id: Mapped[int] = mapped_column(ForeignKey("location.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=get_poland_time_now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=get_poland_time_now(), onupdate=get_poland_time_now()
    )

    location: Mapped["Location"] = relationship("Location", back_populates="users")
    chats: Mapped[list["Chat"]] = relationship("Chat", secondary=user_chat_association, back_populates="users")
    domains: Mapped[list["Domain"]] = relationship("Domain", secondary=user_domain_association, back_populates="users")
    time_logs: Mapped[list["TimeLog"]] = relationship("TimeLog", back_populates="user")

    volunteer = relationship("Volunteer", uselist=False, back_populates="user", cascade="delete, delete-orphan")
    organisation = relationship("Organisation", uselist=False, back_populates="user", cascade="delete, delete-orphan")
    coordinator = relationship("Coordinator", uselist=False, back_populates="user", cascade="delete, delete-orphan")


class Volunteer(Base):
    __tablename__ = "volunteer"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    birth_date: Mapped[datetime.date] = mapped_column(Date)
    phone_number: Mapped[str] = mapped_column(String(20))

    user = relationship("User", back_populates="volunteer")
    skills: Mapped[list["Skill"]] = relationship(
        "Skill", secondary=volunteer_skill_association, back_populates="volunteers"
    )
    domains: Mapped[list["Domain"]] = relationship("Domain", back_populates="volunteer")
    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="volunteer")
    certificates: Mapped[list["Certificate"]] = relationship("Certificate", back_populates="volunteer")


class Organisation(Base):
    __tablename__ = "organisation"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    org_name: Mapped[str] = mapped_column(String(255))
    contact_person: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text)
    phone_number: Mapped[str] = mapped_column(String(20))
    address: Mapped[str] = mapped_column(Text)
    verified: Mapped[bool] = mapped_column(Boolean)

    user = relationship("User", back_populates="organisation")
    domains: Mapped[list["Domain"]] = relationship("Domain", back_populates="organisation")
    events: Mapped[list["Event"]] = relationship("Event", back_populates="organisation")


class Coordinator(Base):
    __tablename__ = "coordinator"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    school: Mapped[str] = mapped_column(String(500))
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    phone_number: Mapped[str] = mapped_column(String(20))
    verified: Mapped[bool] = mapped_column(Boolean)

    user = relationship("User", back_populates="coordinator")


class Skill(Base):
    __tablename__ = "skill"

    id: Mapped[int] = mapped_column(primary_key=True)
    skill_name: Mapped[str] = mapped_column(Text)

    volunteers: Mapped[list["Volunteer"]] = relationship(
        "Volunteer", secondary=volunteer_skill_association, back_populates="skills"
    )
    requirements: Mapped[list["Requirement"]] = relationship("Requirement", back_populates="skill")


class Domain(Base):
    __tablename__ = "domain"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text)

    users: Mapped[list["User"]] = relationship("User", secondary=user_domain_association, back_populates="domains")


class Location(Base):
    __tablename__ = "location"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    latitude: Mapped[float]
    longitude: Mapped[float]

    users: Mapped[list["User"]] = relationship("User", back_populates="location")
    events: Mapped[list["Event"]] = relationship("Event", back_populates="location")


class Event(Base):
    __tablename__ = "event"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    signup_start: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    signup_end: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    location_id: Mapped[int] = mapped_column(ForeignKey("location.id"))
    organisation_id: Mapped[int] = mapped_column(ForeignKey("organisation.id"))

    location: Mapped["Location"] = relationship("Location", back_populates="events")
    organisation: Mapped["Organisation"] = relationship("Organisation", back_populates="events")
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="event")
    registrations: Mapped[list["Registration"]] = relationship("Registration", back_populates="event")
    certificates: Mapped[list["Certificate"]] = relationship("TimeLog", back_populates="event")


class Task(Base):
    __tablename__ = "task"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    estimation_minutes: Mapped[int] = mapped_column(Integer)
    organisation_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    event_id: Mapped[int | None] = mapped_column(ForeignKey("event.id"))

    event: Mapped[Event | None] = relationship("Event", back_populates="tasks")
    organisation: Mapped[Organisation | None] = relationship("Organisation", back_populates="tasks")
    time_logs: Mapped[list["TimeLog"]] = relationship("TimeLog", back_populates="task")
    requirements: Mapped[list["Requirement"]] = relationship("Requirement", back_populates="task")


class Requirement(Base):
    __tablename__ = "requirement"
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(Text)
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id"))
    skill_id: Mapped[int] = mapped_column(ForeignKey("skill.id"))

    task: Mapped["Task"] = relationship("Task", back_populates="requirements")
    skill: Mapped["Skill"] = relationship("Skill", back_populates="requirements")


class Chat(Base):
    __tablename__ = "chat"
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=get_poland_time_now())

    users: Mapped[list["User"]] = relationship("User", secondary=user_chat_association, back_populates="chats")
    messages: Mapped[list["Message"]] = relationship("Message", back_populates="chat")


class Message(Base):
    __tablename__ = "message"
    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chat.id"))
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    content: Mapped[str] = mapped_column(Text, nullable=False)
    sent_at: Mapped[datetime] = mapped_column(DateTime, default=get_poland_time_now())

    chat: Mapped["Chat"] = relationship("Chat", back_populates="messages")
    sender: Mapped["User"] = relationship("User")


class Registration(Base):
    __tablename__ = "registration"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    event_id: Mapped[int] = mapped_column(ForeignKey("event.id"))
    registered_at: Mapped[datetime] = mapped_column(DateTime, default=get_poland_time_now())
    status: Mapped[str] = mapped_column(String(50))

    user: Mapped["User"] = relationship("User")
    event: Mapped["Event"] = relationship("Event", back_populates="registrations")


class Review(Base):
    __tablename__ = "review"
    id: Mapped[int] = mapped_column(primary_key=True)
    volunteer_id: Mapped[int] = mapped_column(ForeignKey("volunteer.id"))
    rating: Mapped[int] = mapped_column(Integer)
    comment: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=get_poland_time_now())

    volunteer: Mapped[Volunteer] = relationship("Volunteer", back_populates="reviews")


class Certificate(Base):
    __tablename__ = "certificate"
    id: Mapped[int] = mapped_column(primary_key=True)
    volunteer_id: Mapped[int] = mapped_column(ForeignKey("volunteer.id"))
    template_id: Mapped[int] = mapped_column(ForeignKey("certificate_template.id"))
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    issued_at: Mapped[datetime] = mapped_column(DateTime, default=get_poland_time_now())

    volunteer: Mapped["Volunteer"] = relationship("Volunteer", back_populates="certificates")
    template: Mapped["CertificateTemplate"] = relationship("CertificateTemplate", back_populates="certificates")
    event: Mapped["Event"] = relationship("Event", back_populates="certificates")


class CertificateTemplate(Base):
    __tablename__ = "certificate_template"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text)

    certificates: Mapped[list["Certificate"]] = relationship("Certificate", back_populates="template")
    event: Mapped["Event"] = relationship("Event", back_populates="time_logs")


class TimeLog(Base):
    __tablename__ = "timelog"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id"))
    minutes: Mapped[int] = mapped_column(Integer)
    logged_at: Mapped[datetime] = mapped_column(DateTime, default=get_poland_time_now())

    user: Mapped["User"] = relationship("User", back_populates="time_logs")
    task: Mapped["Task"] = relationship("Task", back_populates="time_logs")
