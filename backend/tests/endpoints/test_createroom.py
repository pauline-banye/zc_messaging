# from unittest import mock

# import pytest
# from fastapi.testclient import TestClient
# from main import app
# from utils.db import DataStorage

# client = TestClient(app)
# create_room_url = "api/v1/org/3467sd4671a5f5478df56u911/members/619ba4671a5f54782939d385/rooms"

# create_room_payload = {
#     "room_name": "random",
#     "room_type": "CHANNEL",
#     "room_members": {},
#     "created_at": "2022-01-18 09:05:32.433020",
#     "description": "random discussions",
#     "topic": "random discussions",
#     "is_private": False,
#     "is_archived": False
# }
# create_room_success_response = {
#     "status": "success",
#     "message": "room created",
#     "data": {
#     "room_name": "random",
#     "room_type": "CHANNEL",
#     "room_members": {
#         "619bab3b1a5f54782939d400": {
#         "role": "admin",
#         "starred": False,
#         "closed": False
#         }
#     },
#     "created_at": "2022-01-18 09:05:32.433020",
#     "description": "random discussions",
#     "topic": "random discussions",
#     "is_private": False,
#     "is_archived": False,
#     "id": "61e6855e65934b58b8e5d1df",
#     "org_id": "619ba4671a5f54782939d384",
#     "created_by": "619bab3b1a5f54782939d400"
#     }
# }
# get_room_success_response = {
#     "status": "success",
#     "message": "room found",
#     "data": {
#     "_id": "61e6855e65934b58b8e5d1df",
#     "created_at": "2022-01-18 09:05:32.433020",
#     "created_by": "619bab3b1a5f54782939d400",
#     "description": "random discussions",
#     "id": None,
#     "is_archived": False,
#     "is_private": False,
#     "org_id": "619ba4671a5f54782939d384",
#     "room_members": {
#         "619bab3b1a5f54782939d400": {
#         "closed": False,
#         "role": "admin",
#         "starred": False
#         }
#     },
#     "room_name": "random",
#     "room_type": "CHANNEL",
#     "topic": "random discussions"
#     }
# }
# payload_room_data = {
#     "room_name": "test group dm",
#     "room_type": "GROUP_DM",
#     "room_members": {
#         "61696f5ac4133ddaa309dcfe": {"closed": False, "role": "admin", "starred": False},
#         "6169704bc4133ddaa309dd07": {"closed": False, "role": "admin", "starred": False},
#         "619baa5c1a5f54782939d386": {"closed": False, "role": "member", "starred": False}
#     },
#     "created_at": "2022-01-14 10:56:40.659309",
#     "is_private": True,
#     "is_archived": False
# }

# fake_room_data = {
#     "room_name": "test group dm",
#     "room_type": "GROUP_DM",
#     "room_members": {
#         "61696f5ac4133ddaa309dcfe": {
#             "closed": False,
#             "role": "admin",
#             "starred": False,
#         },
#         "6169704bc4133ddaa309dd07": {
#             "closed": False,
#             "role": "admin",
#             "starred": False,
#         },
#         "619baa5c1a5f54782939d386": {
#             "closed": False,
#             "role": "member",
#             "starred": False,
#         },
#         "619ba4671a5f54782939d385": {
#             "closed": False,
#             "role": "admin",
#             "starred": False,
#         },
#     },
#     "created_at": "2022-01-11 03:18:02.364291",
#     "description": None,
#     "topic": None,
#     "is_private": True,
#     "is_archived": False,
#     "id": "23dg67l0eba8adb50ca13a24",
#     "org_id": "3467sd4671a5f5478df56u911",
#     "created_by": "619ba4671a5f54782939d385",
# }

# fake_org_members = {
#     "61696f5ac4133ddaa309dcfe": {"closed": False, "role": "admin", "starred": False},
#     "6169704bc4133ddaa309dd07": {"closed": False, "role": "admin", "starred": False},
#     "619ba4671a5f54782939d385": {"closed": False, "role": "admin", "starred": False},
#     "619baa5c1a5f54782939d386": {"closed": False, "role": "member", "starred": False}
# }


# @pytest.mark.asyncio
# @mock.patch.object(DataStorage, "__init__", lambda x, y: None)
# async def test_create_room_successful(
#     mock_dataStorage_write, mock_centrifugo
# ):
#     """Send message successful
#     Args:
#         mock_dataStorage_read (AsyncMock): Asynchronous external api call
#         mock_dataStorage_write (AsyncMock): Asynchronous external api call
#         mock_centrifugo (AsyncMock): Asynchronous external api call
#     """
#     db = DataStorage("3467sd4671a5f5478df56u911")
#     db.plugin_id = "34453"
    
#     success_response = {
#         "status": "success",
#         "message": "room created",
#         "data": {
#             "room_name": "test group dm",
#             "room_type": "GROUP_DM",
#             "room_members": {
#                 "61696f5ac4133ddaa309dcfe": {
#                     "closed": False,
#                     "role": "admin",
#                     "starred": False,
#                 },
#                 "6169704bc4133ddaa309dd07": {
#                     "closed": False,
#                     "role": "admin",
#                     "starred": False,
#                 },
#                 "619baa5c1a5f54782939d386": {
#                     "closed": False,
#                     "role": "member",
#                     "starred": False,
#                 },
#                 "619ba4671a5f54782939d385": {
#                     "closed": False,
#                     "role": "admin",
#                     "starred": False,
#                 },
#             },
#             "created_at": "2022-01-11 03:18:02.364291",
#             "description": None,
#             "topic": None,
#             "is_private": True,
#             "is_archived": False,
#             "id": "23dg67l0eba8adb50ca13a24",
#             "org_id": "3467sd4671a5f5478df56u911",
#             "created_by": "619ba4671a5f54782939d385",
#         }
#     }

#     write_response = {
#         "status": 201,
#         "message": "success",
#         "data": {"insert_count": 1, "object_id": "23dg67l0eba8adb50ca13a24"},
#     }

#     centrifugo_response = {"status_code": 200}

#     mock_dataStorage_write.return_value = write_response
#     mock_centrifugo.return_value = centrifugo_response

#     response = client.post(url=create_room_url, json=payload_room_data)
#     assert response.status_code == 201
#     success_response["data"]["created_by"] = response.json()["data"]["created_by"]
#     assert response.json() == success_response






# @pytest.mark.asyncio
# @mock.patch.object(DataStorage, "__init__", lambda x, y: None)
# async def test_get_room_members_successful(mock_dataStorage_read):
#     """Tests when room members are retrieved successfully
#     Args:
#         mock_dataStorage_read (AsyncMock): Asynchronous external api call
#     """
#     db = DataStorage("3467sd4671a5f5478df56u911")
#     db.plugin_id = "34453"

#     members = {
#         "61696f5ac4133ddaa309dcfe": {
#             "closed": False,
#             "role": "admin",
#             "starred": False,
#         },
#         "6169704bc4133ddaa309dd07": {
#             "closed": False,
#             "role": "admin",
#             "starred": False,
#         },
#         "619baa5c1a5f54782939d386": {
#             "closed": False,
#             "role": "member",
#             "starred": False,
#         },
#     }

#     read_response = {
#         "status": "success",
#         "message": "Room members retrieved successfully",
#         "data": members,
#     }

#     mock_dataStorage_read.return_value = fake_room_data

#     response = client.get(url=get_room_members_url)
#     assert response.status_code == 200
#     assert response.json() == read_response


# @pytest.mark.asyncio
# @mock.patch.object(DataStorage, "__init__", lambda x, y: None)
# async def test_get_members_room_not_found(mock_dataStorage_read):
#     """Tests when room is not found
#     Args:
#         mock_get_user_room (AsyncMock): Asynchronous external api call
#     """
#     db = DataStorage("3467sd4671a5f5478df56u911")
#     db.plugin_id = "34453"

#     mock_dataStorage_read.return_value = None
#     read_response = {
#         "detail": "Room not found",
#     }

#     response = client.get(url=get_room_members_url)
#     assert response.status_code == 404
#     assert response.json() == read_response


# @pytest.mark.asyncio
# @mock.patch.object(DataStorage, "__init__", lambda x, y: None)
# async def test_get_members_unsuccessful(mock_dataStorage_read):
#     """Get room members unsuccessful

#     Args:
#         mock_dataStorage_read (AsyncMock): Asynchronous external api call
#     """
#     db = DataStorage("3467sd4671a5f5478df56u911")
#     db.plugin_id = "34453"

#     fake_room_data["members"] = {}
#     read_response = {"status_code": 424, "message": "Failure to retrieve room members"}

#     mock_dataStorage_read.return_value == read_response

#     response = client.get(url=get_room_members_url)
#     assert response.status_code == 424
#     assert response.json() == {"detail": "Failure to retrieve room members"}
