from sqlalchemy import Column, Integer, ForeignKey
from models.base import Base


class TweetHashtag(Base):
    __tablename__ = "hashtagstweets"
    id = Column(Integer, primary_key=True, index=True)
    tweet_id = Column(Integer, ForeignKey("tweets.id"), primary_key=True)
    hashtag_id = Column(Integer, ForeignKey("hashtags.id"), primary_key=True)
