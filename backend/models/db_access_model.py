from sqlalchemy import Column, Integer
from models.base import Base

class Db_Accessed(Base):
    __tablename__ = "DbAccessedCount"
    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Integer, nullable=False, default=0)

    def __repr__(self):
        return f"<Db_accessed={self.amount}"