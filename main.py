from fastapi import FastAPI, Depends
from typing import Union
from sqlalchemy.orm import Session
from controllers.users_controller import createUser
from schemas import UserCreate
from config.db import SessionLocal

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

@app.get("/tweets/{tweet_id}")
def get_tweet(tweet_id: int, q: Union[str, None] = None):
    return{ "tweet_id": tweet_id, "q": q}