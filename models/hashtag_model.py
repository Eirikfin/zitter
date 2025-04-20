from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base
from models.tweet_hashtag_model import tweet_hashtags

class Hashtag(Base):
    __tablename__ = "hashtags"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(255), index=True, unique=True)

    tweets = relationship("Tweet", secondary=tweet_hashtags, back_populates="hashtags")

