from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from models.users_model import User
from models.base import Base


class Tweet(Base):
    __tablename__ = "tweets"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(String(255), nullable=False)
    time_created = Column(DateTime, default=func.now())
    
    # Relationship to User
    user = relationship("User", back_populates="tweets")
    
    def __repr__(self):
        return f"<Tweet(id={self.id}, user_id={self.user_id}, message={self.message})>"

