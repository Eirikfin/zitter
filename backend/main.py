from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
from controllers.users_controller import createUser, updateUser, deleteUser, getUser, getAllUsers, searchUser
from schemas import UserCreate, UserUpdate, LoginRequest
from controllers.log_controller import getLogs
from config.db import SessionLocal
from config.db import engine
from models.base import Base
from cache.like_batcher import lifespan

from schemas.tweet_schema import TweetResponse, TweetCreate
from controllers.tweet_controller import create_tweet, get_tweet_by_id, get_tweets, search_tweets, get_hashtags, redis
from controllers.login_controller import logInUser
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from middleware import log_requests
from controllers.tweet_controller import get_total_likes
from cache.like_batcher import batch_like

http_bearer = HTTPBearer()

Base.metadata.create_all(bind=engine)
app = FastAPI(lifespan=lifespan)

def get_token_from_header(authorization: str = Depends(http_bearer)):
    token = authorization.credentials
    return token

def get_db():
    db = SessionLocal()
    print(db)
    try:
        yield db
    finally:
        db.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://zitter-six.vercel.app",
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(log_requests)


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

@app.get("/users/search")
def search_users(query: str, db: Session = Depends(get_db)):
    return searchUser(db, query)

@app.get("/")
def read_root():
    return "Zitter API is live!"

@app.get("/tweets/all")
async def getTweets(limit: int = 50, offset: int = 0, db: Session = Depends(get_db)):
    return await get_tweets(db, limit=limit, offset=offset)

@app.get("/tweets/search")
async def search(query: str, db: Session = Depends(get_db)):
    return await search_tweets(query, db)

@app.get("/tweets/{tweet_id}", response_model=TweetResponse)
async def get_tweet(tweet_id: int):
    tweet = await get_tweet_by_id(tweet_id)
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found") 
    return tweet

@app.post("/tweets", response_model=TweetResponse)
async def post_tweet(tweet: TweetCreate, token: str = Depends(get_token_from_header)):
    created_tweet = await create_tweet(tweet, token)
    return created_tweet


@app.get("/logs")
def returnLogs():
    return getLogs()

@app.get("/likes/{tweet_id}")
async def get_likes_endpoint(tweet_id: int, db: Session = Depends(get_db)):
    return await get_total_likes(db, tweet_id)

@app.post("/likes/{tweet_id}")
async def like_tweet(tweet_id: int):
    batch_like(tweet_id)
    return {"message": f"Like registered for tweet {tweet_id}"}

