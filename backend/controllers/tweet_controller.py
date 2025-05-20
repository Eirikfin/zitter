import re
import json
from sqlalchemy import func, or_, desc
from sqlalchemy.orm import joinedload
from models import Tweet, Hashtag, User
from config.db import SessionLocal
from schemas.tweet_schema import TweetCreate
from sqlalchemy.orm import Session
from middleware import decode_token
from dotenv import load_dotenv
import os
import redis.asyncio as aioredis
import asyncio
from fastapi import HTTPException
from cache.like_batcher import batch_like
from cache.like_batcher import like_buffer, db_access_counter

load_dotenv()

secret_key = os.getenv("SECRET_KEY")
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")

# Initialize Redis connection
redis = aioredis.from_url(redis_url, decode_responses=True)

# Utility to extract hashtags
def extract_hashtags(text: str):
    return set(re.findall(r"#(\w+)", text))  # Extract words after #

# Create a new tweet
def create_tweet(tweet_data: TweetCreate, token: str):
    db = SessionLocal()
    payload = decode_token(token, secret_key)
    user_id = payload["id"]
    try:
        new_tweet = Tweet(
            user_id=user_id,
            message=tweet_data.message,
        )

        db.add(new_tweet)
        db.flush()

        hashtags = extract_hashtags(tweet_data.message)

        for tag in hashtags:
            tag_text = tag.lower()

            hashtag = db.query(Hashtag).filter(func.lower(Hashtag.text) == tag_text).first()
            if not hashtag:
                hashtag = Hashtag(text=tag_text)
                db.add(hashtag)
                db.flush()

            new_tweet.hashtags.append(hashtag)

        db.commit()
        db.refresh(new_tweet)

        # Invalidate cache for tweets and hashtags
        asyncio.create_task(redis.delete("tweets"))
        asyncio.create_task(redis.delete("hashtags"))

        return new_tweet

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()




# Retrieve a tweet by ID
async def get_tweet_by_id(tweet_id: int):
    cache_key = f"tweet:{tweet_id}"
    cached_tweet = await redis.get(cache_key)

    if cached_tweet:
        return json.loads(cached_tweet)

    db = SessionLocal()
    try:
        tweet = (
            db.query(Tweet)
            .options(joinedload(Tweet.user))
            .filter(Tweet.id == tweet_id)
            .first()
        )

        if tweet:
            tweet_data = {
                "id": tweet.id,
                "message": tweet.message,
                "time_created": tweet.time_created.isoformat(),
                "username": tweet.user.username,
                "user_id": tweet.user.id,
            }
            await redis.set(cache_key, json.dumps(tweet_data), ex=3600)
            return tweet_data
        return None
    finally:
        db.close()
        increment_db_access()



# Get all tweets with pagination
async def get_tweets(db: Session, limit: int = 50, offset: int = 0):
    cache_key = f"tweets:{limit}:{offset}"
    cached_tweets = await redis.get(cache_key)
    
    print(cached_tweets)

    if cached_tweets:
        return json.loads(cached_tweets)

    tweets = db.query(Tweet).options(joinedload(Tweet.user)).order_by(desc(Tweet.id)).limit(limit).offset(offset).all()
    result = [
        {
            "id": tweet.id,
            "message": tweet.message,
            "time_created": tweet.time_created.isoformat(),
            "username": tweet.user.username
        }
        for tweet in tweets
    ]

   

    await redis.set(cache_key, json.dumps(result), ex=3600)
    return result


# Search tweets by message, username, or hashtag
async def search_tweets(search_query: str, db: Session, limit: int = 50, offset: int = 0):
    cache_key = f"search_tweets:{search_query}:{limit}:{offset}"
    cached_tweets = await redis.get(cache_key)

    if cached_tweets:
        return json.loads(cached_tweets)

    query = db.query(Tweet).join(User).outerjoin(Tweet.hashtags).options(
        joinedload(Tweet.user),
        joinedload(Tweet.hashtags)
    ).filter(
        or_(
            Tweet.message.like(f"%{search_query}%"),
            User.username.like(f"%{search_query}%"),
            Hashtag.text.like(f"%{search_query}%")
        )
    ).order_by(desc(Tweet.id)).limit(limit).offset(offset)

    tweets = query.all()

    result = [
        {
            "id": tweet.id,
            "message": tweet.message,
            "time_created": tweet.time_created.isoformat(),
            "username": tweet.user.username,
            "hashtags": [h.text for h in tweet.hashtags]
        }
        for tweet in tweets
    ]

    await redis.set(cache_key, json.dumps(result), ex=3600)  # Cache for 1 hour
    return result


# Get all hashtags with pagination
async def get_hashtags(db: Session, limit: int = 50, offset: int = 0):
    cache_key = f"hashtags:{limit}:{offset}"
    cached_hashtags = await redis.get(cache_key)

    if cached_hashtags:
        return json.loads(cached_hashtags)

    tags = db.query(Hashtag).order_by(Hashtag.text.asc()).limit(limit).offset(offset).all()
    result = [{"id": tag.id, "text": tag.text} for tag in tags]

    await redis.set(cache_key, json.dumps(result), ex=3600)  # Cache for 1 hour
    return result


async def like_tweet(db: Session, id: int):
    tweet = db.query(Tweet).filter(Tweet.id == id).first()

    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet was not found")

    batch_like(tweet.id)

    return {"message": "Tweet was liked!", "likes": tweet.likes}




async def get_total_likes(db: Session, tweet_id: int):
    tweet = db.query(Tweet).filter(Tweet.id == tweet_id).first()

    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")

    db_likes = tweet.likes
    db_access_counter["reads"] += 1

    # Likes still in the buffer (not yet flushed)
    buffered_likes = like_buffer[tweet_id]["likes"]

    return {
        "tweet_id": tweet_id,
        "likes_total": db_likes + buffered_likes,
        "likes_from_db": db_likes,
        "likes_from_buffer": buffered_likes
    }