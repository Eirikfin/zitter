from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str  

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None