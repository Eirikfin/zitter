from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base

class Hashtag(Base):
    __tablename__ = "tweet_hashtags"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(255), index=True, unique=True)

    tweets = relationship("Tweet", secondary="tweet_hashtags", back_populates="hashtags")
