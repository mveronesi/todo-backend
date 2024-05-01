from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from database import TodoDB, get_db
from models import Todo
import uuid


app = FastAPI()


@app.post("/todos/", response_model=Todo)
def create_todo(todo: Todo, db: Session = Depends(get_db)):
    db_todo = TodoDB(**todo.model_dump())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


@app.get("/todos/{todo_id}", response_model=Todo)
def read_todo(todo_id: str, db: Session = Depends(get_db)):
    todo_uuid = uuid.UUID(todo_id)
    todo = db.query(TodoDB).filter(TodoDB.id == todo_uuid).first()
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Todo not found"
            )
    return todo


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
