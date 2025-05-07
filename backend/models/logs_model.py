
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from models.base import Base

class User(Base):
    __tablename__ = "logs"
    
    id: Column(Integer, primary_key=True, autoincrement=True)
    method: Column(String(10) )
    url: Column(String(255))




