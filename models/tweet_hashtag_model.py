from sqlalchemy import Table, Column, Integer, ForeignKey
from models.base import Base

TweetHashtag = Table(
    "tweet_hashtags",
    Base.metadata,
    Column("tweet_id", Integer, ForeignKey("tweets.id"), primary_key=True),
    Column("hashtag_id", Integer, ForeignKey("hashtags.id"), primary_key=True)
)
