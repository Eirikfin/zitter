import time
from middleware import increment_db_access
from config.db import SessionLocal
from models import Tweet
from collections import defaultdict # defaultdict is a dictionary subclass that calls a factory function to supply missing values
import threading
from contextlib import asynccontextmanager
from fastapi import FastAPI

# like_buffer is a dictionary to store the number of likes and the last update time for each tweet
# like buffer stores temporary like data in memory before flushing it to the database.
# Key = tweet_id
# Value = dictionary with
# -"like": number of new (unwritten) likes
# - "last update" last time this tweet's like were written to the DB
like_buffer = defaultdict(lambda: {"likes": 0, "last_update": time.time()}) 

# db_access_counter tracks the number of reads and writest to the database.
# Used later for API log reporting (/logs)
db_access_counter = {"reads": 0, "writes": 0} # db_access_counter is a dictionary to store the number of reads and writes to the database


def batch_like(tweet_id: int):
    now = time.time() #current time in seconds
    buffer = like_buffer[tweet_id] #get or create entry for this tweet
    
    buffer["likes"] += 1 #increase like count in memory
    
    # Flush triggers:
    # 1. if the tweet has 10 or more buffered likes 
    #2. or its been more than 60 seconds sinvr last DB write (for low-liked tweets)
    
    if buffer["likes"] >= 10 or (now - buffer["last_update"]) >= 60:
        flush_likes_to_db(tweet_id)
        buffer["last_update"] = now




def flush_likes_to_db(tweet_id: int):
    db = SessionLocal() # start a new DB session
    try:
        buffered_likes = like_buffer[tweet_id]["likes"] # get how many likes are waiting
        
        # if there are no new likes, dont touch the DB
        if buffered_likes == 0:
            return
        
        #fetch the tweet from the DB
        tweet = db.query(Tweet).filter(Tweet.id == tweet_id).first()
        
        # if the tweet exists, apply the batched likes
        if tweet:
            tweet.likes += buffered_likes # add buffered like to the current value in DB
            db.commit() # save changes
            db.refresh(tweet) # refresh the tweet object with latest db state
            increment_db_access() #log that we did a DB write (for /logs)
            
            print(f"[DB WRITE] tweet {tweet_id} upadate with +{buffered_likes} likes") 
            
            like_buffer[tweet_id]["likes"] = 0 #reset the buffer for this tweet
        else:
            print(f"[ERROR] Tweet {tweet_id} not found. Likes not flushed.")
            
    except Exception as e:
        print(f"[ERROR] Could not update tweet {tweet_id} updated with +{buffered_likes} likes")
        db.rollback()
    finally:
        db.close()




def flush_old_likes():
    while True:
        now = time.time()
        for tweet_id, buffer in like_buffer.items():
            if buffer["likes"] > 0 and (now - buffer["last_update"]) >= 60:
                print(f"[AUTO FLUSH] Flushing tweet {tweet_id} due to timeout.")
                flush_likes_to_db(tweet_id)
                buffer["last_update"] = now
        time.sleep(10)  # Checks every 10 seconds
        
@asynccontextmanager
async def lifespan(app: FastAPI):
    threading.Thread(target=flush_old_likes, daemon=True).start()
    yield

app = FastAPI(lifespan=lifespan)
