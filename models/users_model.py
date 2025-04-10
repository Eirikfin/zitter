from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from models.base import Base



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    time_created = Column(DateTime, default=func.now())
    
    tweets = relationship("Tweet", back_populates="user")


    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"
