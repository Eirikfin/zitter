import re
from sqlalchemy import func, or_, desc
from sqlalchemy.orm import joinedload
from models import Tweet, Hashtag, User
from config.db import SessionLocal
from schemas.tweet_schema import TweetCreate
from sqlalchemy.orm import Session


# Utility to extract hashtags
def extract_hashtags(text: str):
    return set(re.findall(r"#(\w+)", text))  # Extract words after #

# Create a new tweet
def create_tweet(tweet_data: TweetCreate):
    db = SessionLocal()
    try:
        new_tweet = Tweet(
            user_id=tweet_data.user_id,
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
        return new_tweet

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


# Retrieve a tweet by ID
def get_tweet_by_id(tweet_id: int):
    db = SessionLocal()
    tweet = db.query(Tweet).filter(Tweet.id == tweet_id).first()
    db.close()
    return tweet


# Get all tweets with pagination
def get_tweets(db: Session, limit: int = 50, offset: int = 0):
    tweets = db.query(Tweet).options(joinedload(Tweet.user)).order_by(desc(Tweet.id)).limit(limit).offset(offset).all()
    result = [
        {
            "id": tweet.id,
            "message": tweet.message,
            "time_created": tweet.time_created,
            "username": tweet.user.username
        }
        for tweet in tweets
    ]
    return result


# Search tweets by message, username, or hashtag
def search_tweets(search_query: str, db: Session, limit: int = 50, offset: int = 0):
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
            "time_created": tweet.time_created,
            "username": tweet.user.username,
            "hashtags": [h.text for h in tweet.hashtags]
        }
        for tweet in tweets
    ]
    return result


# Get all hashtags with pagination
def get_hashtags(db: Session, limit: int = 50, offset: int = 0):
    tags = db.query(Hashtag).order_by(Hashtag.text.asc()).limit(limit).offset(offset).all()
    return [{"id": tag.id, "text": tag.text} for tag in tags]
