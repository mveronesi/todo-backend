import uuid
from typing import List
from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from database import TodoDB, get_db
from models import Todo, TodoBase, Token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import auth


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Todo not found"
            )
    return todo


@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: str, todo: TodoBase, db: Session = Depends(get_db)):
    db_todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
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
    todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Todo not found"
            )
    db.delete(todo)
    db.commit()
    return {"detail": "Todo deleted"}


@app.get("/todos/user/{user_id}", response_model=List[Todo])
def read_user_todos(user_id: uuid.UUID, db: Session = Depends(get_db)):
    todos = db.query(TodoDB).filter(TodoDB.user_id == user_id).all()
    if not todos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="No todos found for this user"
            )
    return todos


@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}