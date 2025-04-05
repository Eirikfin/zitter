from fastapi import FastAPI, Depends
from typing import Union
from sqlalchemy.orm import Session
from controllers.users_controller import createUser
from schemas import UserCreate
from config.db import SessionLocal
from schemas.tweet_schema import TweetResponse, TweetCreate
from controllers.tweet_controller import create_tweet, get_tweet_by_id
from fastapi import HTTPException

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#creating a new user:
@app.post("/users")
def register_user(req: UserCreate, db: Session = Depends(get_db)):
    return createUser(db, req)


@app.get("/")
def read_root():
    return "Zitter API is live!"

@app.get("/tweets/{tweet_id}", response_model=TweetResponse)
def get_tweet(tweet_id: int):
    tweet = get_tweet_by_id(tweet_id)
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found") 
    return tweet

@app.post("/tweets", response_model=TweetCreate)
def post_tweet(tweet: TweetCreate):
    return create_tweet(tweet)