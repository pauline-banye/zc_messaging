from unittest import mock

import pytest
from fastapi.testclient import TestClient
from main import app
from utils.db import DataStorage

client = TestClient(app)
create_room_url = "api/v1/org/6619ba4671a5f54782939d384/members/619ba4671a5f54782939d385/rooms"
get_room_members_url = "api/v1/org/6619ba4671a5f54782939d384//rooms/61dcf855eba8adb50ca13a24/members"

payload_group_dm = {
    "room_name": "test group dm",
    "room_type": "GROUP_DM",
    "room_members": {
        "61696f5ac4133ddaa309dcfe": {"closed": False, "role": "admin", "starred": False},
        "6169704bc4133ddaa309dd07": {"closed": False, "role": "admin", "starred": False},
        "619ba4671a5f54782939d385": {"closed": False, "role": "admin", "starred": False},
        "619baa5c1a5f54782939d386": {"closed": False, "role": "member", "starred": False}
    },
    "created_at": "2022-01-14 10:56:40.659309",
    "is_private": True,
    "is_archived": False
    }

fake_data_group_dm = {
    "room_name": "test group dm",
    "room_type": "GROUP_DM",
    "room_members": {
        "61696f5ac4133ddaa309dcfe": {"closed": False, "role": "admin", "starred": False},
        "6169704bc4133ddaa309dd07": {"closed": False, "role": "admin", "starred": False},
        "619ba4671a5f54782939d385": {"closed": False, "role": "admin", "starred": False},
        "619baa5c1a5f54782939d386": {"closed": False, "role": "member", "starred": False}
    },
    "created_at": "2022-01-11 03:18:02.364291",
    "description": None,
    "topic": None,
    "is_private": True,
    "is_archived": False,
    "id": "61dcf855eba8adb50ca13a24",
    "org_id": "619ba4671a5f54782939d384",
    "created_by": "619ba4671a5f54782939d385"
}

fake_org_members = {
    "61696f5ac4133ddaa309dcfe": {"closed": False, "role": "admin", "starred": False},
    "6169704bc4133ddaa309dd07": {"closed": False, "role": "admin", "starred": False},
    "619ba4671a5f54782939d385": {"closed": False, "role": "admin", "starred": False},
    "619baa5c1a5f54782939d386": {"closed": False, "role": "member", "starred": False}
}



@pytest.mark.asyncio
@mock.patch.object(DataStorage, "__init__", lambda x, y: None)
async def test_get_room_members_successful(mock_dataStorage_read):
    """Tests when room members are retrieved successfully
    Args:
        mock_dataStorage_read (AsyncMock): Asynchronous external api call
    """
    members = {
      "61696f5ac4133ddaa309dcfe": {"closed": False, "role": "admin", "starred": False},
      "6169704bc4133ddaa309dd07": {"closed": False, "role": "admin", "starred": False},
      "619ba4671a5f54782939d385": {"closed": False, "role": "admin", "starred": False},
      "619baa5c1a5f54782939d386": {"closed": False, "role": "member", "starred": False}
    }
    
    read_response = {
        "status": "success",
        "message": "Room members retrieved successfully",
        "data": members,
    }

    mock_dataStorage_read.return_value = fake_data_group_dm
    response = client.get(get_room_members_url)
    assert response.status_code == 200
    assert response.json() == read_response


@pytest.mark.asyncio
@mock.patch.object(DataStorage, "__init__", lambda x, y: None)
async def test_get_room_members_room_not_found(mock_dataStorage_read):
    """Tests when room is not found
    Args:
        mock_get_user_room (AsyncMock): Asynchronous external api call
    """
    mock_dataStorage_read.return_value = None
    read_response = {
        "detail": "Room not found",
    }

    response = client.get(get_room_members_url)
    assert response.status_code == 404
    assert response.json() == read_response


@pytest.mark.asyncio
@mock.patch.object(DataStorage, "__init__", lambda x, y: None)
async def test_get_room_members_invalid_url(mock_dataStorage_read):
    """Tests when room is not found
    Args:
        mock_dataStorage_read (AsyncMock): Asynchronous external api call
    """
    fake_url = "api/v1/org/939d384/rooms/0chfy68/members"
    mock_dataStorage_read.return_value = fake_data_group_dm

    response = client.get(fake_url)
    # assert get_room_members_url == fake_url
    assert response.status_code == 400


@pytest.mark.asyncio
@mock.patch.object(DataStorage, "__init__", lambda x, y: None)
async def test_get_members_reading_from_zc_core_returns_none(mock_dataStorage_read):
    """Get members reading from zc core returns none.
    Args:
        mock_dataStorage_read (AsyncMock): Asynchronous external api call
    """
    mock_dataStorage_read.return_value = None
    
    response = client.get(get_room_members_url)
    assert response.status_code == 404
    assert response.json() == {"detail": "Room not found"}


@pytest.mark.asyncio
@mock.patch.object(DataStorage, "__init__", lambda x, y: None)
# async def test_get_members_check_status_code(mock_get_user_room, mock_dataStorage_read):
async def test_get_members_check_status_code(mock_dataStorage_read):
    """Get members unsuccessful when getting from zc core fails.
    Args:
        mock_get_user_room (AsyncMock): Asynchronous external api call
        mock_dataStorage_read (AsyncMock): Asynchronous external api call
    """
    read_response = {
      "status_code": 424,
      "message": "Failed to retrieve room members"
      }
    
    # mock_get_user_room.return_value = fake_data_group_dm
    mock_dataStorage_read.return_value = read_response
    
    response = client.get(get_room_members_url)
    assert response.status_code == 404
    assert response.json() == {"detail": "Room not found"}
  
  
# @pytest.mark.asyncio
# @mock.patch.object(DataStorage, "__init__", lambda x, y: None)
# async def test_no_members_in_room(mock_get_user_room, mock_dataStorage_read):
#     """Get room members returns empty dict.

#     Args:
#         mock_get_room (AsyncMock): Asynchronous external api call
#         mock_dataStorage_read (AsyncMock): Asynchronous external api call
#     """

#     fake_data_group_dm["members"] = {}
#     read_response = {
#       "status_code": 424,
#       "message": "Failed to retrieve room members"}

#     mock_get_user_room.return_value = fake_data_group_dm["members"]
#     mock_dataStorage_read.return_value = read_response
                     
#     response = client.get(get_room_members_url)
#     assert response.status_code == 404
#     assert response.json() == {"detail": "Room not found"}
    
    