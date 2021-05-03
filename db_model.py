 
from sqlalchemy import (
    create_engine,
    Column,
    ForeignKey,
    Integer,
    String,
    TIMESTAMP,
    Boolean,
    Enum,
    ARRAY,
    JSON,
    FLOAT
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

user = os.environ.get("POSTGRES_USER")
password = os.environ.get("POSTGRES_PASSWORD")
host = os.environ.get("POSTGRES_HOST")
db = os.environ.get("POSTGRES_DB")

engine = create_engine("postgresql://" + user + ":" + password + "@" + host + "/" + db)
print('connected to sql')

class Event(Base):
    __tablename__ = "event"

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organization.id"))
    location_id = Column(Integer, ForeignKey("location.id"), nullable=True)
    description = Column(String)
    name = Column(String)
    cover_image_url = Column(String, nullable=True)
    cover_image_hash = Column(String, nullable=True)
    poster_image_url = Column(String, nullable=True)
    poster_image_hash = Column(String, nullable=True)
    profile_image_url = Column(String, nullable=True)
    profile_image_hash = Column(String, nullable=True)
    attendee_limit = Column(Integer)
    contact = Column(String, nullable=True)
    registration_due_date = Column(TIMESTAMP, nullable=True)

class UserEvent(Base):
    __tablename__ = "user_event"

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    event_id = Column(Integer, ForeignKey("event.id"))
    rating = Column(Integer, nullable=True)
    ticket = Column(String, nullable=True)
    status = Column(
        Enum("PENDING", "APPROVED", "REJECTED", "ATTENDED", name="status_enum", create_type=False)
    )
    is_internal = Column(Boolean)


class EventRecommendation(Base):
    __tablename__ = "event_recommendation"
    
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
    
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("event.id"))
    event_vector = Column(ARRAY(FLOAT))
    score = Column(JSON)

class EventDuration(Base):
    __tablename__ = "event_duration"

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("event.id"))
    start = Column(TIMESTAMP)
    finish = Column(TIMESTAMP)


Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
