
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from models.base import Base

class Log(Base):
    __tablename__ = "logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    method = Column(String(10) )
    url = Column(String(255))
    time = Column(String(100))

    def __repr__(self):
        return f"<Log(id={self.id}, method={self.method}, url={self.url}, time={self.time})>"


