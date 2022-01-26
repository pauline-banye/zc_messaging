from unittest import mock

import pytest
from fastapi.testclient import TestClient
from main import app
from utils.db import DataStorage

client = TestClient(app)

remove_reaction_url = ("api/v1/org/3467sd4671a5f5478df56u911/rooms/23dg67l0eba8adb50ca13a24/"
    + "messages/61e6878165934b58b8e5d1e0/reaction/remove"
)    
add_reaction_url = ("api/v1/org/3467sd4671a5f5478df56u911/rooms/23dg67l0eba8adb50ca13a24/"
    + "messages/61e6878165934b58b8e5d1e0/reaction/add"    
)

fake_room_data = {
    "room_name": "General",
    "room_type": "CHANNEL",
    "room_members": {
        "61696f5ac4133ddaa309dcfe": {
            "closed": False,
            "role": "admin",
            "starred": False,
        },
        "6169704bc4133ddaa309dd07": {
            "closed": False,
            "role": "admin",
            "starred": False,
        },
        "619baa5c1a5f54782939d386": {
            "closed": False,
            "role": "member",
            "starred": False,
        },
        "619bab3b1a5f54782939d400": {
            "closed": False,
            "role": "member",
            "starred": False,
        },
        "619ba4671a5f54782939d385": {
            "closed": False,
            "role": "member",
            "starred": False,
        },
    },
    "created_at": "2022-01-11 03:18:02.364291",
    "description": None,
    "topic": "General Information",
    "is_private": False,
    "is_archived": False,
    "id": "23dg67l0eba8adb50ca13a24",
    "org_id": "3467sd4671a5f5478df56u911",
    "created_by": "619ba4671a5f54782939d385",
}
fake_message_data = {
    "_id": "61e6878165934b58b8e5d1e0",
    "created_at": "2022-01-18 09:05:32.479911",
    "edited": False,
    "emojis": [
        {
            "name": "smile",
            "count": 1,
            "emoji": "smile",
            "reactedUsersId": ["619bab3b1a5f54782939d400"]
        }
    ],
    "files": [],
    "org_id": "619ba4671a5f54782939d384",
    "richUiData": {
        "blocks": [
            {
                "data": {},
                "depth": 0,
                "entityRanges": [],
                "inlineStyleRanges": [],
                "key": "random",
                "text": "Helloooo",
                "type": "unstyled",
            }
        ],
        "entityMap": {},
    },
    "room_id": "61e6855e65934b58b8e5d1df",
    "saved_by": [],
    "sender_id": "619bab3b1a5f54782939d400",
    "threads": [],
    "timestamp": 0,
}
add_reaction_payload = {
    "name": "smile",
    "count": 1,
    "emoji": "smile",
    "reactedUsersId": ["619ba4671a5f54782939d385"],
}


# @pytest.mark.asyncio
# @mock.patch.object(DataStorage, "__init__", lambda x, y: None)
# async def test_add_member_to_reaction_when_reaction_already_exists(
#     mock_get_message, mock_get_room_members, mock_dataStorage_update, mock_centrifugo
#     # mock_dataStorage_read, mock_get_room_members, mock_dataStorage_update, mock_centrifugo
# ):
#     """Add member to reaction when reaction already exists.
#     Args:
#         mock_dataStorage_read (AsyncMock): Asynchronous external api call
#         mock_get_message (AsyncMock): Asynchronous external api call
#         mock_dataStorage_update (AsyncMock): Asynchronous external api call
#         mock_centrifugo (AsyncMock): Asynchronous external api call
#     """
#     db = DataStorage("619ba4671a5f54782939d384")
#     db.plugin_id = "34453"

#     update_response = {"status": 200, "message": "New reaction added successfully"}
#     centrifugo_response = {"status_code": 200}
#     success_response = {
#         "status": "success",
#         "message": "New reaction added successfully",
#         "data": {
#             "name": "smile",
#             "count": 2,
#             "emoji": "smile",
#             "reactedUsersId": [
#                 "619ba4671a5f54782939d385",
#                 "619bab3b1a5f54782939d400"
#             ]
#         },
#     }   
    
#     # fake_room_data["members"] = members
#     mock_get_room_members.return_value = fake_room_data
#     # mock_dataStorage_read.return_value = members
#     # mock_dataStorage_read.return_value = fake_message_data
#     mock_get_message.return_value = fake_message_data
#     # mock_dataStorage_read.return_value = members
#     mock_dataStorage_update.return_value = update_response
#     mock_centrifugo.return_value = centrifugo_response
    
#     response = client.put(url=add_reaction_url, json=add_reaction_payload)
    
#     assert response.status_code == 200
#     assert response.json() == success_response
    



# @pytest.mark.asyncio 
# @mock.patch.object(DataStorage, "__init__", lambda x, y: None)
# async def test_add_reaction_unsuccessful_when_room_not_found(mock_dataStorage_read):
#     """Add reaction unsuccessful when room not found.

#     Args:
#         mock_dataStorage_read (AsyncMock): Asynchronous external api call
#     """
#     db = DataStorage("619ba4671a5f54782939d384")
#     db.plugin_id = "34453"

#     # mock_dataStorage_read.return_value = fake_message_data["emojis"]
#     mock_dataStorage_read.return_value = None #{"members": {}}

#     response = client.put(url=add_reaction_url, json=add_reaction_payload)
#     assert response.status_code == 404
#     # assert response.json() == {"detail": "Failed to retrieve room members"}
#     assert response.json() == {"detail": "Room not found"}

#PASSED
@pytest.mark.asyncio 
@mock.patch.object(DataStorage, "__init__", lambda x, y: None)
async def test_add_reaction_unsuccessful_when_message_not_found(mock_dataStorage_read):
    """Add reaction unsuccessful when message is not found
    Args:
        mock_dataStorage_read (AsyncMock): Asynchronous external api call
    """
    db = DataStorage("619ba4671a5f54782939d384")
    db.plugin_id = "34453"

    read_response = None
    mock_dataStorage_read.return_value = read_response

    response = client.put(url=add_reaction_url, json=add_reaction_payload)
    assert response.status_code == 404
    assert response.json() == {"detail": "Message not found"}


@pytest.mark.asyncio 
@mock.patch.object(DataStorage, "__init__", lambda x, y: None)
async def test_add_reaction_with_invalid_room_member(mock_dataStorage_read, mock_dataStorage_update):
    """Add reaction fails when sender is not a room member.
    Args:
        mock_dataStorage_read (AsyncMock): Asynchronous external api call
        mock_dataStorage_update (AsyncMock): Asynchronous external api call
    """
    db = DataStorage("619ba4671a5f54782939d384")
    db.plugin_id = "34453"
    add_reaction_payload["reactedUsersId"] = ["9d406191a5f54bab3b782930"]

    update_response = {"status": 401}

    mock_dataStorage_read.return_value = fake_message_data["emojis"]
    mock_dataStorage_read.return_value = fake_room_data
    mock_dataStorage_update.return_value = update_response

    response = client.put(url=add_reaction_url, json=add_reaction_payload)
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid room member"}


@pytest.mark.asyncio 
@mock.patch.object(DataStorage, "__init__", lambda x, y: None)
async def test_add_reaction_when_no_reaction_exists(
    mock_dataStorage_read, mock_dataStorage_update, mock_centrifugo
):
    """Add reaction to message
    Args:
        mock_dataStorage_read (AsyncMock): Asynchronous external api call
        mock_dataStorage_update (AsyncMock): Asynchronous external api call
        mock_centrifugo (AsyncMock): Asynchronous external api call
    """
    db = DataStorage("619ba4671a5f54782939d384")
    db.plugin_id = "34453"
    
    update_response = {"status": 200}
    centrifugo_response = {"status_code": 200}
    success_response = {
        "status": "success",
        "message": "Reaction added successfully",
        "data": {
            "name": "smile",
            "count": 1,
            "emoji": "smile",
            "reactedUsersId": ["619ba4671a5f54782939d385"],
        },
    }

    mock_dataStorage_read.return_value = fake_message_data["emojis"]
    mock_dataStorage_read.return_value = fake_room_data
    mock_dataStorage_update.return_value = update_response
    mock_centrifugo.return_value = centrifugo_response

    response = client.put(url=add_reaction_url, json=add_reaction_payload)
    assert response.status_code == 200
    assert response.json() == success_response


@pytest.mark.asyncio
@mock.patch.object(DataStorage, "__init__", lambda x, y: None)
async def test_add_reaction_to_message_when_reactions_exist(
    mock_dataStorage_read, mock_dataStorage_update, mock_centrifugo
):
    """Add reaction to message when reactions exist
    Args:
        mock_dataStorage_read (AsyncMock): Asynchronous external api call
        mock_dataStorage_update (AsyncMock): Asynchronous external api call
        mock_centrifugo (AsyncMock): Asynchronous external api call
    """
    db = DataStorage("619ba4671a5f54782939d384")
    db.plugin_id = "34453"
    fake_message_data["emojis"] = [
        {
            "count": 1,
            "emoji": "smile",
            "name": "smile",
            "reactedUsersId": ["619bab3b1a5f54782939d400"],
        },
    ]
    new_reaction_payload = {
        "name": "frown",
        "count": 1,
        "emoji": "frown",
        "reactedUsersId": ["619ba4671a5f54782939d385"],
    }
    
    update_response = {"status": 200}
    centrifugo_response = {"status_code": 200}
    success_response = {
        "status": "success",
        "message": "Reaction added successfully",
        "data": {
            "name": "frown",
            "count": 1,
            "emoji": "frown",
            "reactedUsersId": ["619ba4671a5f54782939d385"],
        },
    }
    
    mock_dataStorage_read.return_value = fake_message_data["emojis"]
    mock_dataStorage_read.return_value = fake_room_data
    mock_dataStorage_update.return_value = update_response
    mock_centrifugo.return_value = centrifugo_response
    
    response = client.put(url=add_reaction_url, json=new_reaction_payload)
    assert response.status_code == 200
    assert response.json() == success_response
  
