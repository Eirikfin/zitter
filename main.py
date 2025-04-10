from fastapi import FastAPI, Depends
from typing import Union
from sqlalchemy.orm import Session
from controllers.users_controller import createUser, updateUser, deleteUser, getUser, getAllUsers
from schemas import UserCreate, UserUpdate, LoginRequest
from models import User
from config.db import SessionLocal
from schemas.tweet_schema import TweetResponse, TweetCreate
from controllers.tweet_controller import create_tweet, get_tweet_by_id, get_tweets
from controllers.login_controller import logInUser
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#Cors config:
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


#log in:
@app.post("/login")
def login_user(req: LoginRequest, db: Session = Depends(get_db)):
    return logInUser(db, req)

#creating a new user:
@app.post("/users")
def register_user( req: UserCreate, db: Session = Depends(get_db)):
    return createUser(db, req)
#updating a user:
@app.patch("/users/{username}")
def update_user(username: str, req: UserUpdate,  db: Session = Depends(get_db)):
    return updateUser(db, username, req)
#delete a user:
@app.delete("/user/{username}")
def delete_user(username: str, db: Session = Depends(get_db)):
    return deleteUser(db, username)
#get a user:
@app.get("/user/{username}")
def get_user(username: str, db: Session = Depends(get_db)):
    return getUser(db, username)
#get all users:
@app.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    return getAllUsers(db)


@app.get("/")
def read_root():
    return "Zitter API is live!"

@app.get("/tweets/all")
def getTweets(db: Session = Depends(get_db)):
    return get_tweets(db)

@app.get("/tweets/{tweet_id}", response_model=TweetResponse)
def get_tweet(tweet_id: int):
    tweet = get_tweet_by_id(tweet_id)
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found") 
    return tweet



@app.post("/tweets", response_model=TweetCreate)
def post_tweet(tweet: TweetCreate):
    return create_tweet(tweet)