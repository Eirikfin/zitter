from models import User
from schemas import LoginRequest
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
import bcrypt
import os 
from dotenv import load_dotenv
from middleware import generate_token

load_dotenv()

secret_key = os.getenv("SECRET_KEY")

def logInUser(db: Session, req: LoginRequest):
    #find the user in database using username:
    user = db.query(User).filter(User.username == req.username).first()
    #if no user was found:
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    #encode the inputted password and database password to bytes
    password_bytes = req.password.encode('utf-8')
    hashed_password_bytes = user.password.encode('utf-8')
    #compare passwords
    if not bcrypt.checkpw(password_bytes, hashed_password_bytes):
        raise HTTPException(status_code=401, detail="Wrong password")
    payload = {
        "id": user.id,
        "username": user.username
    }
    token = generate_token(payload, secret_key)
    
    #if match return success message
    return {"message": "Log In was successful!", "token": f"Bearer {token}"}