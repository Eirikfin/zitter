from models import User
from datetime import datetime, timezone
from schemas import UserUpdate
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
import bcrypt 


#creating a user:
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
    except Exception as err:
        db.rollback()
        print(f"Error creating user: {str(err)}")  # Log the error for debugging
        raise HTTPException(status_code=400, detail=f"Error creating user: {str(err)}")




def updateUser(db: Session, username: str, req: UserUpdate):
    
    try:
    # Fetch the user from the database
        user = db.query(User).filter(User.username == username).first()

    # If user doesn't exist, return an error message
        if not user:
            return {"message": "User not found"}

    # Update only the fields that are provided:
        for key, value in req.dict(exclude_unset=True).items():
            setattr(user, key, value)

        db.commit()
        db.refresh(user)

        return {"message": "User updated successfully", "user": user}
    except Exception as err:
        db.rollback()
        print(f"Error updating user: {str(err)}")  # Log the error for debugging
        raise HTTPException(status_code=400, detail=f"Error updating user: {str(err)}")



def deleteUser(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    