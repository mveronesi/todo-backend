from typing import List
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import Boolean, Column, Integer, String, create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Date, UUID
from datetime import date
from pydantic import BaseModel
import uuid

Base = declarative_base()

class TodoDB(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    text = Column(String, index=True)
    done = Column(Boolean, default=False)
    important = Column(Boolean, default=False)
    date = Column(Date, default=date.today)
    user_id = Column(UUID(as_uuid=True), default=uuid.uuid4)


class TodoBase(BaseModel):
    text: str
    done: bool
    important: bool
    date: date
    user_id: uuid.UUID


class Todo(TodoBase):
    id: int

    class Config:
        from_attributes = True


engine = create_engine("sqlite:///./test.db")
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/todos/", response_model=Todo)
def create_todo(todo: TodoBase, db: Session = Depends(get_db)):
    db_todo = TodoDB(**todo.model_dump())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


@app.get("/todos/{todo_id}", response_model=Todo)
def read_todo(todo_id: str, db: Session = Depends(get_db)):
    todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: str, todo: TodoBase, db: Session = Depends(get_db)):
    db_todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    for key, value in todo.model_dump().items():
        setattr(db_todo, key, value)
    db.commit()
    return db_todo


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: str, db: Session = Depends(get_db)):
    todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"detail": "Todo deleted"}


@app.get("/todos/user/{user_id}", response_model=List[Todo])
def read_user_todos(user_id: uuid.UUID, db: Session = Depends(get_db)):
    todos = db.query(TodoDB).filter(TodoDB.user_id == user_id).all()
    if not todos:
        raise HTTPException(status_code=404, detail="No todos found for this user")
    return todos