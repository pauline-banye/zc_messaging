from unittest import mock

import pytest
from fastapi.testclient import TestClient
from main import app
from utils.db import DataStorage

client = TestClient(app)

remove_reaction_url = "api/v1/org/619ba4/rooms/123456/messages/61e687/reaction/remove"
add_reaction_url = "api/v1/org/619ba4/rooms/123456/messages/61e687/reaction/add"

fake_core_room_data = {
    "_id": "619e28c31a5f54782939d59a",
    "created_at": "2021-11-24 11:23:11.361210",
    "created_by": "61696f",
    "description": "Section for general information",
    "id": None,
    "is_archived": False,
    "is_private": False,
    "org_id": "619baf",
    "room_members": {
        "61696f": {"closed": False, "role": "admin", "starred": False},
        "e21e10": {"closed": False, "role": "admin", "starred": False},
    },
    "room_name": "random",
    "room_type": "CHANNEL",
    "topic": "Information",
}
fake_zc_core_message_data = {
    "_id": "346556",
    "created_at": "2021-12-28 19:27:13.620083",
    "edited": False,
    "emojis": [],
    "files": [],
    "org_id": "1234",
    "richUiData": {
        "blocks": [
            {
                "data": {},
                "depth": 0,
                "entityRanges": [],
                "inlineStyleRanges": [],
                "key": "eljik",
                "text": "HI, I'm mark.. new here",
                "type": "unstyled",
            }
        ],
        "entityMap": {},
    },
    "room_id": "343235",
    "saved_by": [],
    "sender_id": "619ba4",
    "threads": [],
    "timestamp": 0,
}
reaction_payload = {
    "name": "smile",
    "count": 1,
    "emoji": "smile",
    "reactedUsersId": ["e21e10"],
}


# # PASSED
@pytest.mark.asyncio  # passed
@mock.patch.object(DataStorage, "__init__", lambda x, y: None)
async def test_add_reaction_when_no_reaction_exists(
    mock_dataStorage_read, mock_get_room, mock_dataStorage_update, mock_centrifugo
):
    """Add reaction to message when no reaction exists
    Args:
        mock_dataStorage_read (AsyncMock): Asynchronous external api call
        mock_get_room (AsyncMock): Asynchronous external api call
        mock_dataStorage_update (AsyncMock): Asynchronous external api call
        mock_centrifugo (AsyncMock): Asynchronous external api call
    """
    db = DataStorage("619ba4")
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
            "reactedUsersId": ["e21e10"],
        },
    }

    mock_dataStorage_read.return_value = fake_zc_core_message_data["emojis"]
    mock_get_room.return_value = fake_core_room_data
    mock_dataStorage_update.return_value = update_response
    mock_centrifugo.return_value = centrifugo_response

    response = client.put(url=add_reaction_url, json=reaction_payload)
    assert response.status_code == 200
    assert response.json() == success_response


@pytest.mark.asyncio  # passed
@mock.patch.object(DataStorage, "__init__", lambda x, y: None)
async def test_add_reaction_to_message_when_reactions_exist(
    mock_dataStorage_read, mock_get_room, mock_dataStorage_update, mock_centrifugo
):
    """Add reaction to message when reactions exist in the emoji array
    Args:
        mock_dataStorage_read (AsyncMock): Asynchronous external api call
        mock_get_room (AsyncMock): Asynchronous external api call
        mock_dataStorage_update (AsyncMock): Asynchronous external api call
        mock_centrifugo (AsyncMock): Asynchronous external api call
    """
    db = DataStorage("619ba4")
    db.plugin_id = "34453"

    fake_zc_core_message_data["emojis"] = [
        {
            "count": 1,
            "emoji": "smile",
            "name": "smile",
            "reactedUsersId": ["e21e10"],
        },
    ]
    new_reaction_payload = {
        "name": "frown",
        "count": 1,
        "emoji": "frown",
        "reactedUsersId": ["e21e10"],
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
            "reactedUsersId": ["e21e10"],
        },
    }

    mock_dataStorage_read.return_value = fake_zc_core_message_data["emojis"]
    mock_get_room.return_value = fake_core_room_data
    mock_dataStorage_update.return_value = update_response
    mock_centrifugo.return_value = centrifugo_response

    response = client.put(url=add_reaction_url, json=new_reaction_payload)
    assert response.status_code == 200
    assert response.json() == success_response


@pytest.mark.asyncio  # passed
@mock.patch.object(DataStorage, "__init__", lambda x, y: None)
async def test_add_reaction_unsuccessful_when_updating_to_core_fails(
    mock_dataStorage_read, mock_get_room, mock_dataStorage_update
):
    """Add reaction unsuccessful when updating to core returns fails

    Args:
        mock_dataStorage_read (AsyncMock): Asynchronous external api call
        mock_get_room (AsyncMock): Asynchronous external api call
        mock_dataStorage_update (AsyncMock): Asynchronous external api call
    """
    db = DataStorage("619ba4")
    db.plugin_id = "34453"

    mock_dataStorage_read.return_value = fake_zc_core_message_data
    mock_get_room.return_value = fake_core_room_data
    mock_dataStorage_update.return_value = {
        "status_code": 422,
        "message": "unprocessible error",
    }

    response = client.put(url=add_reaction_url, json=reaction_payload)
    assert response.status_code == 424
    assert response.json() == {"detail": "Failed to add reaction"}


@pytest.mark.asyncio  # passed
@mock.patch.object(DataStorage, "__init__", lambda x, y: None)
async def test_add_reaction_when_message_not_found(mock_dataStorage_read):
    """Add reaction unsuccessful when message is not found
    Args:
        mock_dataStorage_read (AsyncMock): Asynchronous external api call
    """
    db = DataStorage("619ba4")
    db.plugin_id = "34453"

    read_response = None
    mock_dataStorage_read.return_value = read_response

    response = client.put(url=add_reaction_url, json=reaction_payload)
    assert response.status_code == 404
    assert response.json() == {"detail": "Message not found"}


@pytest.mark.asyncio
@mock.patch.object(DataStorage, "__init__", lambda x, y: None)
async def test_remove_reaction_when_no_reactions_exist(
    mock_dataStorage_read, mock_get_room, mock_dataStorage_update, mock_centrifugo
):
    """Remove reaction when reactions exist in the emoji array
    Args:
        mock_dataStorage_read (AsyncMock): Asynchronous external api call
        mock_get_room (AsyncMock): Asynchronous external api call
        mock_dataStorage_update (AsyncMock): Asynchronous external api call
        mock_centrifugo (AsyncMock): Asynchronous external api call
    """
    db = DataStorage("619ba4")
    db.plugin_id = "34453"

    update_response = {"status": 400}

    mock_dataStorage_read.return_value = fake_zc_core_message_data["emojis"]
    mock_get_room.return_value = fake_core_room_data
    mock_dataStorage_update.return_value = update_response

    response = client.put(url=remove_reaction_url, json=reaction_payload)
    assert response.status_code == 400
    assert response.json() == {"detail": "No reactions exist for this message"}


@pytest.mark.asyncio  # passed
@mock.patch.object(DataStorage, "__init__", lambda x, y: None)
async def test_add_reaction_with_invalid_room_member(
    mock_dataStorage_read, mock_dataStorage_update
):
    """Add reaction fails when sender is not a room member.
    Args:
        mock_dataStorage_read (AsyncMock): Asynchronous external api call
        mock_dataStorage_update (AsyncMock): Asynchronous external api call
    """
    db = DataStorage("619ba4")
    db.plugin_id = "34453"
    reaction_payload["reactedUsersId"] = ["v78290"]

    update_response = {"status": 401}

    mock_dataStorage_read.return_value = fake_core_room_data
    mock_dataStorage_read.return_value = fake_zc_core_message_data
    mock_dataStorage_update.return_value = update_response

    response = client.put(url=add_reaction_url, json=reaction_payload)
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid room member"}


@pytest.mark.asyncio  # passed
@mock.patch.object(DataStorage, "__init__", lambda x, y: None)
async def test_remove_reaction_when_message_not_found(mock_dataStorage_read):
    """Remove reaction unsuccessful when message is not found
    Args:
        mock_dataStorage_read (AsyncMock): Asynchronous external api call
    """
    db = DataStorage("619ba4")
    db.plugin_id = "34453"

    read_response = None
    mock_dataStorage_read.return_value = read_response

    response = client.put(url=remove_reaction_url, json=reaction_payload)
    assert response.status_code == 404
    assert response.json() == {"detail": "Message not found"}


@pytest.mark.asyncio  # passed
@mock.patch.object(DataStorage, "__init__", lambda x, y: None)
async def test_remove_reaction_with_invalid_room_member(
    mock_dataStorage_read, mock_dataStorage_update
):
    """Remove reaction fails when sender is not a room member.
    Args:
        mock_dataStorage_read (AsyncMock): Asynchronous external api call
        mock_dataStorage_update (AsyncMock): Asynchronous external api call
    """
    db = DataStorage("619ba4")
    db.plugin_id = "34453"
    reaction_payload["reactedUsersId"] = ["v78290"]

    update_response = {"status": 401}

    mock_dataStorage_read.return_value = fake_core_room_data
    mock_dataStorage_read.return_value = fake_zc_core_message_data
    mock_dataStorage_update.return_value = update_response

    response = client.put(url=remove_reaction_url, json=reaction_payload)
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid room member"}


# FAILED
@pytest.mark.asyncio  # failed. asserting that response is {"detail": "Message not found"}
@mock.patch.object(DataStorage, "__init__", lambda x, y: None)
async def test_add_reaction_when_room_not_found(mock_dataStorage_read, mock_get_room):
    """Add reaction fails when room is not found
    Args:
        mock_dataStorage_read (AsyncMock): Asynchronous external api call
        mock_get_room (AsyncMock): Asynchronous external api call
    """
    db = DataStorage("619ba4")
    db.plugin_id = "34453"

    fake_core_room_data = {}

    mock_get_room.return_value = fake_core_room_data
    mock_dataStorage_read.return_value = fake_zc_core_message_data["emojis"]

    response = client.put(url=add_reaction_url, json=reaction_payload)
    assert response.status_code == 404
    assert response.json() == {"detail": "Room not found"}


@pytest.mark.asyncio  # failed. passed using fake reaction payload
@mock.patch.object(DataStorage, "__init__", lambda x, y: None)
async def test_add_member_reaction_to_message_when_reaction_already_exists(
    mock_dataStorage_read, mock_get_room, mock_dataStorage_update, mock_centrifugo
):
    """Add member reaction when the reaction already exists
    Args:
        mock_dataStorage_read (AsyncMock): Asynchronous external api call
        mock_get_room (AsyncMock): Asynchronous external api call
        mock_dataStorage_update (AsyncMock): Asynchronous external api call
        mock_centrifugo (AsyncMock): Asynchronous external api call
    """
    db = DataStorage("619ba4")
    db.plugin_id = "34453"

    # fake_reaction_payload = {
    #     "name": "smile",
    #     "count": 2,
    #     "emoji": "smile",
    #     "reactedUsersId": ["61696f", "e21e10"],
    # }

    update_response = {"status": 200, "message": "Reaction added successfully"}
    centrifugo_response = {"status_code": 200}
    success_response = {
        "status": "success",
        "message": "Reaction added successfully",
        "data": {
            "name": "smile",
            "count": 2,
            "emoji": "smile",
            "reactedUsersId": ["61696f", "e21e10"],
        },
    }

    mock_dataStorage_read.return_value = fake_zc_core_message_data["emojis"]
    mock_get_room.return_value = fake_core_room_data
    mock_dataStorage_update.return_value = update_response
    mock_centrifugo.return_value = centrifugo_response

    response = client.put(url=add_reaction_url, json=reaction_payload)
    # response = client.put(url=add_reaction_url, json=fake_reaction_payload)

    assert response.status_code == 200
    assert response.json() == success_response


@pytest.mark.asyncio  # failed. Asserting 200 instead of 409
@mock.patch.object(DataStorage, "__init__", lambda x, y: None)
async def test_add_reaction_to_message_with_duplicate_payload(
    mock_dataStorage_read, mock_get_room, mock_dataStorage_update
):
    """Add reaction to message with duplicate payload
    Args:
        mock_dataStorage_read (AsyncMock): Asynchronous external api call
        mock_get_room (AsyncMock): Asynchronous external api call
        mock_dataStorage_update (AsyncMock): Asynchronous external api call
        mock_centrifugo (AsyncMock): Asynchronous external api call
    """
    db = DataStorage("619ba4")
    db.plugin_id = "34453"

    core_message = [
        {
            "name": "smile",
            "count": 1,
            "emoji": "smile",
            "reactedUsersId": ["e21e10"],
        },
    ]

    update_response = {"status": 409}

    mock_dataStorage_read.return_value = core_message
    mock_get_room.return_value = fake_core_room_data
    mock_dataStorage_update.return_value = update_response

    response = client.put(url=add_reaction_url, json=reaction_payload)
    assert response.status_code == 409
    assert response.json() == {"detail": "Duplicate reaction"}


@pytest.mark.asyncio  # failed
@mock.patch.object(DataStorage, "__init__", lambda x, y: None)
async def test_remove_reaction_when_reactedUserid_is_more_than_one(
    mock_dataStorage_read, mock_get_room, mock_dataStorage_update, mock_centrifugo
):
    """Remove reaction when reactedUserid is more than one
    Args:
        mock_dataStorage_read (AsyncMock): Asynchronous external api call
        mock_get_room (AsyncMock): Asynchronous external api call
        mock_dataStorage_update (AsyncMock): Asynchronous external api call
        mock_centrifugo (AsyncMock): Asynchronous external api call
    """
    db = DataStorage("619ba4")
    db.plugin_id = "34453"

    fake_zc_core_message_data["emojis"] = [
        {
            "count": 2,
            "emoji": "smile",
            "name": "smile",
            "reactedUsersId": ["e21e10", "61696f"],
        },
    ]

    update_response = {"status": 200}
    centrifugo_response = {"status_code": 200}
    success_response = {
        "status": "success",
        "message": "Reaction removed successfully",
        "data": {
            "name": "smile",
            "count": 1,
            "emoji": "smile",
            "reactedUsersId": ["61696f"],
        },
    }

    mock_dataStorage_read.return_value = fake_zc_core_message_data["emojis"]
    mock_get_room.return_value = fake_core_room_data
    mock_dataStorage_update.return_value = update_response
    mock_centrifugo.return_value = centrifugo_response

    response = client.put(url=remove_reaction_url, json=reaction_payload)
    assert response.status_code == 200
    assert response.json() == success_response


@pytest.mark.asyncio  # failed
@mock.patch.object(DataStorage, "__init__", lambda x, y: None)
async def test_remove_reaction_unsuccessful_when_updating_to_core_fails(
    mock_dataStorage_read, mock_get_room, mock_dataStorage_update
):
    """Remove reaction unsuccessful when updating to core returns fails

    Args:
        mock_dataStorage_read (AsyncMock): Asynchronous external api call
        mock_get_room (AsyncMock): Asynchronous external api call
        mock_dataStorage_update (AsyncMock): Asynchronous external api call
    """
    db = DataStorage("619ba4")
    db.plugin_id = "34453"

    core_message = [
        {
            "name": "smile",
            "count": 1,
            "emoji": "smile",
            "reactedUsersId": ["e21e10"],
        }
    ]

    mock_dataStorage_read.return_value = core_message
    mock_get_room.return_value = fake_core_room_data
    mock_dataStorage_update.return_value = {
        "status_code": 422,
        "message": "unprocessible error",
    }

    response = client.put(url=remove_reaction_url, json=reaction_payload)
    assert response.status_code == 424
    assert response.json() == {"detail": "Failed to remove reaction"}


@pytest.mark.asyncio  # failed
@mock.patch.object(DataStorage, "__init__", lambda x, y: None)
async def test_remove_reaction_successful_when_reaction_count_is_one(
    mock_dataStorage_read, mock_get_room, mock_dataStorage_update
):
    """Remove reaction unsuccessful when reaction count is one

    Args:
        mock_dataStorage_read (AsyncMock): Asynchronous external api call
        mock_get_room (AsyncMock): Asynchronous external api call
        mock_dataStorage_update (AsyncMock): Asynchronous external api call
    """
    db = DataStorage("619ba4")
    db.plugin_id = "34453"

    core_message = [
        {
            "name": "smile",
            "count": 1,
            "emoji": "smile",
            "reactedUsersId": ["e21e10"],
        }
    ]

    mock_dataStorage_read.return_value = core_message
    mock_get_room.return_value = fake_core_room_data
    mock_dataStorage_update.return_value = {"status": 200}
    success_response = {
        "status": "success",
        "message": "Reaction removed successfully",
        "data": None,
    }

    response = client.put(url=remove_reaction_url, json=reaction_payload)
    assert response.status_code == 200
    assert response.json() == success_response
