from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from .users_model import User  # Import User to avoid circular dependency


"""
Base = declarative_base()

class Tweet(Base):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Foreign key reference
    message = Column(String(255), nullable=False)
    hashtags = Column(String(255), nullable=True)  # No unique constraint
    time_created = Column(DateTime, default=func.now())

    # Relationship with User
    user = relationship("User", back_populates="tweets")

    def __repr__(self):
        return f"<Tweet(id={self.id}, user_id={self.user_id}, message={self.message})>"
"""