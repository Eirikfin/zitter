from models import User
from datetime import datetime, timezone
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
import bcrypt 



def createUser(db: Session, req):
    salt = bcrypt.gensalt(10)
    #has the request password, encode to bytes for hashing, decode to string for database 
    hashed_password = bcrypt.hashpw(req.password.encode("utf-8"), salt).decode("utf-8")

    newUser = User(
        username = req.username,
        email = req.email,
        password = hashed_password
    )
    
    try:
        db.add(newUser)
        db.commit()
        db.refresh(newUser)
        return {"message": "User created successfully", "user": {"id": newUser.id, "username": newUser.username}}
    except Exception as e:
        db.rollback()
        print(f"Error creating user: {str(e)}")  # Log the error for debugging
        raise HTTPException(status_code=400, detail=f"Error creating user: {str(e)}")


