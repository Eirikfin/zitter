from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Tweet schema for creating a new tweet
class TweetCreate(BaseModel):
    user_id: int
    message: str
    
# Tweet schema for the response
class TweetResponse(BaseModel):
    id: int
    user_id: int
    message: str
    time_created: datetime
    
    class config:
        orm_mode = True # This allows Pydantic to read data as dictionaries from ORM models
