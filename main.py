from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import TodoDB, get_db
from models import Todo
import uuid
from typing import List


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/todos/", response_model=List[Todo])
def read_todos(db: Session = Depends(get_db)):
    todos = db.query(TodoDB).order_by(TodoDB.done, TodoDB.important.desc(), TodoDB.date).all()
    return todos if todos is not None else []


@app.post("/todos/", response_model=Todo)
def create_todo(todo: Todo, db: Session = Depends(get_db)):
    print("HERE")
    db_todo = TodoDB(**todo.model_dump())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


@app.get("/todos/{content}", response_model=List[Todo])
def read_todo(content: str, db: Session = Depends(get_db)):
    todos = db.query(TodoDB).filter(TodoDB.text.like(f"%{content}%")).all()
    return todos if todos is not None else []


@app.put("/todos/", response_model=Todo)
def update_todo(todo: Todo, db: Session = Depends(get_db)):
    db_todo = db.query(TodoDB).filter(TodoDB.id == todo.id).first()
    if db_todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Todo not found"
            )
    for key, value in todo.model_dump().items():
        setattr(db_todo, key, value)
    db.commit()
    return db_todo


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: str, db: Session = Depends(get_db)):
    todo_uuid = uuid.UUID(todo_id)
    todo = db.query(TodoDB).filter(TodoDB.id == todo_uuid).first()
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Todo not found"
            )
    db.delete(todo)
    db.commit()
    return {"detail": "Todo deleted"}
