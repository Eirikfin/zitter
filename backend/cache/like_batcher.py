import time
from config.db import SessionLocal
from models import Tweet
from collections import defaultdict
import threading
from contextlib import asynccontextmanager
from fastapi import FastAPI


# like buffer stores temporary like data in memory before flushing it to the database.
like_buffer = defaultdict(lambda: {"likes": 0, "last_update": time.time()}) 

# db_access_counter tracks the number of reads and writest to the database.
# Used later for API log reporting (/logs)
db_access_counter = {"reads": 0, "writes": 0}


def batch_like(tweet_id: int):
    now = time.time() #current time in seconds
    buffer = like_buffer[tweet_id] #get or create entry for this tweet
    
    buffer["likes"] += 1 #increase like count in memory
    
    # Flush triggers:
    #1. if the tweet has 10 or more buffered likes 
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
        # loops through all tweets currently being tracked in the buffer
        for tweet_id, buffer in like_buffer.items():
            # if there are pending likes and it has been more than 60s since last db write:
            if buffer["likes"] > 0 and (now - buffer["last_update"]) >= 60:
                print(f"[AUTO FLUSH] Flushing tweet {tweet_id} due to timeout.")
                flush_likes_to_db(tweet_id)
                buffer["last_update"] = now
        time.sleep(10)  # Checks every 10 seconds
        
       
        # we use FastAPI lifespan event to start our flush_old_likes function when the app starts 
        #and keep it running continuously so the likes dont get "stuck" with no new likes after 60s
@asynccontextmanager
async def lifespan(app: FastAPI):
    # launches the flush function in a separate background thread
    threading.Thread(target=flush_old_likes, daemon=True).start() 
    yield

# ensure it the background thread begins at startup
app = FastAPI(lifespan=lifespan)
