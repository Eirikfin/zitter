from models import User, Tweet
from datetime import datetime, timezone
from schemas import UserUpdate
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy import desc
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



#update a user:
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

        user_data = {
            "username": user.username,
            "email": user.email,
            "joined": user.time_created
        }

        return {"message": "User updated successfully", "user": user_data}
    except Exception as err:
        db.rollback()
        print(f"Error updating user: {str(err)}")  # Log the error for debugging
        raise HTTPException(status_code=400, detail=f"Error updating user: {str(err)}")


#delete a user:
def deleteUser(db: Session, username: str):
    try:
        #search db for username
        user = db.query(User).filter(User.username == username).first()

        #if no user is found:
        if not user:
            return {"message": "User not found"}

        #remove user from data base and commit
        db.delete(user)
        db.commit()
        
        return {"message": "User has been deleted."}


    except Exception as err:
        db.rollback()
        print(f"Error deleting user: {str(err)}")  # Log the error for debugging
        raise HTTPException(status_code=400, detail=f"Error deleting user: {str(err)}")
    

def getUser(db: Session, username: str):
    try:
        user = db.query(User).filter(User.username == username).first()

        if not user:
           raise HTTPException(status_code=404, detail="No user was found")

        # Get tweets sorted by time_created in descending order directly in the query
        tweets = db.query(Tweet).filter(Tweet.user_id == user.id).order_by(desc(Tweet.time_created)).all()

        result = {
            "id": user.id,
            "username": user.username,
            "joined": user.time_created,
            "tweets": [
                {
                    "id": tweet.id,
                    "message": tweet.message,
                    "time_created": tweet.time_created
                } for tweet in tweets
            ]
        }

        return result
    except Exception as err:
        print(f"Error getting user: {str(err)}")
        raise HTTPException(status_code=500, detail=f"Error getting user: {str(err)}")

        
    

#get all users:

def getAllUsers(db: Session):
    users = db.query(User).all()

    result = [
        {"id": user.id, "username": user.username, "joined": user.time_created}
        for user in users
    ]

    return result


#search for users:
def searchUser(db: Session, query: str):
    users = db.query(User).filter(User.username.ilike(f"%{query}%")).all()
    if not users:
        raise HTTPException(status_code=404, detail="no users was found")
    result = [
        {"id": user.id, "username": user.username, "joined": user.time_created}
        for user in users
    ]

    return result