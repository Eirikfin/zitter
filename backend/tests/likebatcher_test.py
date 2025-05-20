import pytest
import time
from unittest.mock import MagicMock, patch
import sys
import os

#setting root directory to the backend directory
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))

from cache import batch_like, like_buffer, flush_likes_to_db




def test_batch_like_triggers_flush_when_10_likes():
    tweet_id = 123
    like_buffer[tweet_id]["likes"] = 9
    like_buffer[tweet_id]["last_update"] = 0  # Far in the past
    
    with patch("cache.like_batcher.flush_likes_to_db") as mock_flush:
        batch_like(tweet_id)

    assert like_buffer[tweet_id]["likes"] == 10
    mock_flush.assert_called_once_with(tweet_id)



def test_batch_like_triggers_flush_on_timeout():
    tweet_id = 456
    like_buffer[tweet_id]["likes"] = 1
    like_buffer[tweet_id]["last_update"] = time.time() - 61  # force timeout

    with patch("cache.like_batcher.flush_likes_to_db") as mock_flush:
        batch_like(tweet_id)

    mock_flush.assert_called_once_with(tweet_id)



def test_flush_likes_to_db_success():
    tweet_id = 1
    like_buffer[tweet_id]["likes"] = 5
    mock_tweet = MagicMock()
    mock_tweet.likes = 10

    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = mock_tweet

    with patch("cache.like_batcher.SessionLocal", return_value=mock_db), \
         patch("cache.like_batcher.increment_db_access") as mock_increment:

        flush_likes_to_db(tweet_id)

    assert mock_tweet.likes == 15
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(mock_tweet)
    mock_increment.assert_called_once()
    assert like_buffer[tweet_id]["likes"] == 0

def test_flush_likes_to_db_tweet_not_found():
    tweet_id = 999
    like_buffer[tweet_id]["likes"] = 3

    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None

    with patch("cache.like_batcher.SessionLocal", return_value=mock_db):
        flush_likes_to_db(tweet_id)

    # Should not raise or crash; just print error
    mock_db.commit.assert_not_called()

def test_flush_likes_to_db_zero_buffer():
    tweet_id = 42
    like_buffer[tweet_id]["likes"] = 0

    with patch("cache.like_batcher.SessionLocal") as mock_session:
        flush_likes_to_db(tweet_id)

    mock_session.assert_called_once()
    # No DB action should occur
    mock_session.return_value.commit.assert_not_called()
