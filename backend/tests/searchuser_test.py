import sys
import os
import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException

#setting root directory to the backend directory
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))

from models import User
from middleware import increment_db_access
from controllers import searchUser



def test_search_user_success():
    # mock user instance
    mock_user = MagicMock(spec=User)
    mock_user.id = 1
    mock_user.username = "testuser"
    mock_user.time_created = "2024-01-01"

    # mock DB session
    mock_db = MagicMock()
    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.all.return_value = [mock_user]

    # patch the increment function
    with patch("controllers.users_controller.increment_db_access") as mock_increment:
        result = searchUser(mock_db, "test")
    
    assert result == [{
        "id": 1,
        "username": "testuser",
        "joined": "2024-01-01"
    }]
    mock_increment.assert_called_once()


def test_search_user_not_found():
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.all.return_value = []

    with pytest.raises(HTTPException) as exc_info:
        searchUser(mock_db, "nonexistent")

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "no users was found"

