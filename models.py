from pydantic import BaseModel
import uuid
from datetime import date

class Todo(BaseModel):
    id: uuid.UUID
    text: str
    done: bool
    important: bool
    date: date

    class Config:
        from_attributes = True  
