import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# get_room_members_url = "api/v1/org/619ba46/rooms/61dcf85/members"
# create_room_url = "api/v1/org/619ba46/member_id/61696f5/rooms"

# payload_group_dm = {
#   "room_name": "test group dm",
#   "room_type": "GROUP_DM",
#   "room_members": {
#         "61696f5": {"role": "admin", "starred": False, "closed": False},
#         "6169704": {"role": "admin", "starred": False, "closed": False},
#         "619ba46": {"role": "admin", "starred": False, "closed": False},
#         "619baa5": {"role": "member", "starred": False, "closed": False},
#     },
#   "is_private": True,
#   "is_archived": False
# }

# fake_org_members = {
#     "61696f5": {"role": "admin", "starred": False, "closed": False},
#     "6169704": {"role": "admin", "starred": False, "closed": False},
#     "619ba46": {"role": "admin", "starred": False, "closed": False},
#     "619baa5": {"role": "member", "starred": False, "closed": False},
# }

# fake_data_group_dm = {
#     "room_name": "test group dm",
#     "room_type": "GROUP_DM",
#     "room_members": {
#         "61696f5": {"role": "admin", "starred": False, "closed": False},
#         "6169704": {"role": "admin", "starred": False, "closed": False},
#         "619ba46": {"role": "admin", "starred": False, "closed": False},
#         "619baa5": {"role": "member", "starred": False, "closed": False},
#     },
#     "created_at": "2022-01-11 03:18:02.364291",
#     "description": None,
#     "topic": None,
#     "is_private": True,
#     "is_archived": False,
#     "id": "61dcf85",
#     "org_id": "619ba46",
#     "created_by": "61696f5",
# }


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
async def test_get_room_members_successful(mock_get_user_room):
    """Tests when room members are retrieved successfully
    Args:
        mock_get_user_room (AsyncMock): Asynchronous external api call
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

    mock_get_user_room.return_value = fake_data_group_dm
    response = client.get(get_room_members_url)
    assert response.status_code == 200
    assert response.json() == read_response


@pytest.mark.asyncio
async def test_get_room_members_room_not_found(mock_get_user_room):
    """Tests when room is not found
    Args:
        mock_get_user_room (AsyncMock): Asynchronous external api call
    """
    mock_get_user_room.return_value = None
    read_response = {
        "detail": "Room not found",
    }

    response = client.get(get_room_members_url)
    assert response.status_code == 404
    assert response.json() == read_response


# @pytest.mark.asyncio
# async def test_get_room_members_invalid_url(mock_get_user_room):
#     """Tests when room is not found
#     Args:
#         mock_get_user_room (AsyncMock): Asynchronous external api call
#     """
#     fake_url = "api/v1/org/939d384/rooms/0chfy68/members"
#     mock_get_user_room.return_value = fake_data_group_dm

#     response = client.get(fake_url)
#     # assert get_room_members_url == fake_url
#     assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_members_reading_from_zc_core_returns_none(mock_get_user_room):
    """Get members reading from zc core returns none.
    Args:
        mock_get_user_room (AsyncMock): Asynchronous external api call
    """
    mock_get_user_room.return_value = None
    
    response = client.get(get_room_members_url)
    assert response.status_code == 404
    assert response.json() == {"detail": "Room not found"}


@pytest.mark.asyncio
async def test_get_members_check_status_code(mock_get_user_room, mock_dataStorage_read):
    """Get members unsuccessful when getting from zc core fails.
    Args:
        mock_get_user_room (AsyncMock): Asynchronous external api call
        mock_dataStorage_read (AsyncMock): Asynchronous external api call
    """
    read_response = {
      "status_code": 424,
      "message": "Failed to retrieve room members"
      }
    
    mock_get_user_room.return_value = fake_data_group_dm
    mock_dataStorage_read.return_value = read_response
    
    response = client.get(get_room_members_url)
    assert response.status_code == 404
    assert response.json() == {"detail": "Room not found"}
  
  
@pytest.mark.asyncio
async def test_no_members_in_room(mock_get_user_room, mock_dataStorage_read):
    """Get room members returns empty dict.

    Args:
        mock_get_room (AsyncMock): Asynchronous external api call
        mock_dataStorage_read (AsyncMock): Asynchronous external api call
    """

    fake_data_group_dm["members"] = {}
    read_response = {
      "status_code": 424,
      "message": "Failed to retrieve room members"}

    mock_get_user_room.return_value = fake_data_group_dm["members"]
    mock_dataStorage_read.return_value = read_response
                     
    response = client.get(get_room_members_url)
    assert response.status_code == 404
    assert response.json() == {"detail": "Room not found"}
    
    
    

# @pytest.mark.asyncio
# async def test_send_message_successful(mock_get_org_members, mock_dataStorage_write, mock_centrifugo):
#     """Send message successful
#     Args:
#         mock_get_org_members (AsyncMock): Asynchronous external api call
#         mock_dataStorage_write (AsyncMock): Asynchronous external api call
#         mock_centrifugo (AsyncMock): Asynchronous external api call
#     """
        
#     success_response = {
#             "room_name": "test group dm",
#             "room_type": "GROUP_DM",
#             "room_members": {
#                 "61696f5ac4133ddaa309dcfe": {
#                     "role": "admin",
#                     "starred": False,
#                     "closed": False
#                 },
#                 "6169704bc4133ddaa309dd07": {
#                     "role": "admin",
#                     "starred": False,
#                     "closed": False
#                 },
#                 "619ba4671a5f54782939d385": {
#                     "role": "admin",
#                     "starred": False,
#                     "closed": False
#                 },
#                 "619baa5c1a5f54782939d386": {
#                     "role": "member",
#                     "starred": False,
#                     "closed": False
#                 }
#             },
#             "created_at": "2022-01-11 03:18:02.364291",
#             "description": None,
#             "topic": None,
#             "is_private": True,
#             "is_archived": False,
#             "id": "61dcf855eba8adb50ca13a24",
#             "org_id": "619ba4671a5f54782939d384",
#             "created_by": "619ba4671a5f54782939d385"
#         }  

#     # write_response = {
#     #     "status": 201,
#     #     "message": "room created",
#     #     "data": fake_data_group_dm
#     # }
    
#     write_response = {
#         "status": 201,
#         "message": "success",
#         "data": {
#             "insert_count": 1,
#             "object_id": "61dcf855eba8adb50ca13a24",
#             }
#         }

#     centrifugo_response = {"status_code": 200}

#     mock_get_org_members.return_value = fake_org_members
#     mock_dataStorage_write.return_value = write_response
#     mock_centrifugo.return_value = centrifugo_response

#     response = client.post(create_room_url, json=payload_group_dm)
#     assert response.status_code == 201
#     # assert response.json() == {"detail": "room created"}
#     assert response == {
#         "status": "success",
#         "message": "Room created",
#         "data": success_response
#     }
    

# status_code_response = 200
# already_exists_response = {
#   "detail": {
#     "message": "room already exists",
#     "room_id": "61dcf855eba8adb50ca13a24"
#   }
# }

# status_code_response = 400
# no_topic_response = {
#   "detail": "DM or Group DM should not have a topic"
# }

# status_code_response = 400
# no_description_response = {
#   "detail": "DM or Group DM should not have a description"
# }


# {
# "room_name": "newest test group dm",
#   "room_type": "GROUP_DM",
#   "room_members": {
#     "61696f5ac4133ddaa309dcfe": {
#       "closed": false,
#       "role": "admin",
#       "starred": false
#     },
#     "6169704bc4133ddaa309dd07": {
#       "closed": false,
#       "role": "admin",
#       "starred": false
#     },
#     "619ba4671a5f54782939d385": {
#       "closed": false,
#       "role": "admin",
#       "starred": false
#     },
#     "619baa5c1a5f54782939d386": {
#       "closed": false,
#       "role": "member",
#       "starred": false
#   }},
#   "created_at": "2022-01-14 10:56:40.659309",
#   "is_private": false,
#   "is_archived": false
# }
