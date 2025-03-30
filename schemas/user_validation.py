from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr  # ✅ Ensures valid email format
    password: str  # ✅ Can add length validation later
