import uuid
from datetime import date
from sqlalchemy import Column, Integer, String, Boolean, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean, Column, Integer, String, create_engine
from sqlalchemy import Date, UUID
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class UserDB(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


class TodoDB(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    text = Column(String, index=True)
    done = Column(Boolean, default=False)
    important = Column(Boolean, default=False)
    date = Column(Date, default=date.today)
    user_id = Column(UUID(as_uuid=True), default=uuid.uuid4)


engine = create_engine("sqlite:///./test.db")
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()