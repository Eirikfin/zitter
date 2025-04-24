# models/tweet_hashtag_model.py
from sqlalchemy import Table, Column, Integer, ForeignKey
from models.base import Base

tweet_hashtags = Table(
    "tweet_hashtags",
    Base.metadata,
    Column("tweet_id", Integer, ForeignKey("tweets.id")),
    Column("hashtag_id", Integer, ForeignKey("hashtags.id")),
)
