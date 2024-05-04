from datetime import date
from sqlalchemy import Column, String, Boolean, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean, Column, String, create_engine
from sqlalchemy import Date, UUID
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class TodoDB(Base):
    __tablename__ = "todos"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    text = Column(String, index=True)
    done = Column(Boolean, default=False)
    important = Column(Boolean, default=False)
    date = Column(Date, default=date.today)


engine = create_engine("sqlite:///./test.db")
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()