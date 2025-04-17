from models.tweets_model import Tweet
from config.db import SessionLocal
from schemas.tweet_schema import TweetCreate
from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi import Depends, HTTPException, APIRouter


def create_tweet(tweet_data: TweetCreate): # tweet_data is the request body containing the tweet data and user ID
    db = SessionLocal() # Create a new session
    new_tweet = Tweet( # Create a new Tweet object
        user_id=tweet_data.user_id, # Get the user ID from the request body and assign it to the new tweet
        message=tweet_data.message, 
    )
    
    db.add(new_tweet) # Add the new tweet to the session
    db.commit() # Commit the session to save the new tweet to the database
    db.refresh(new_tweet) # reloads the values from the DB so that SQLAlchemy knows the auto-generated ID and timestamp from the DB
    
    db.close()
    return new_tweet # Return the newly created tweet object


# This function RETRIEVES a created tweet by its ID from the database.
def get_tweet_by_id(tweet_id: int): # Get the tweet ID from the request
    db = SessionLocal() # Create a new session
    tweet = db.query(Tweet).filter(Tweet.id == tweet_id).first() # Query the database for the tweet with the given ID
    db.close() # Close the session
    return tweet # Return the tweet object if found, otherwise return None

#Get all tweets:
def get_tweets(db: Session):
    tweets = db.query(Tweet).order_by(desc(Tweet.id)).all()
    result = [
        {
            "message": tweet.message,
            "time_created": tweet.time_created,
            "username": tweet.user.username
        } for tweet in tweets]
    
    return result


def searchTweets(db: Session, query: str):
    #query db for match with query matching message
    tweets = db.query(Tweet).filter(Tweet.message.ilike(f"%{query}%")).all()
    #if no result
    if not tweets:
         raise HTTPException(status_code=404, detail="no tweets were found")
    #what to return to user:
    result = [
    {   
        "id": tweet.id,
        "message": tweet.message,
        "time_created": tweet.time_created,
        "username": tweet.user.username
    } for tweet in tweets]

    return result