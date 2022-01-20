# from unittest import mock

# import pytest
# from fastapi.testclient import TestClient
# from main import app
# from utils.db import DataStorage

# client = TestClient(app)
# reaction_url = "api/v1/org/3467sd4671a5f5478df56u911/rooms/23dg67l0eba8adb50ca13a24/messages/61e6878165934b58b8e5d1e0/reaction"
# remove_reaction_url = "api/v1/org/3467sd4671a5f5478df56u911/rooms/23dg67l0eba8adb50ca13a24/messages/61e6878165934b58b8e5d1e0/reaction/remove"
# add_reaction_url = "api/v1/org/3467sd4671a5f5478df56u911/rooms/23dg67l0eba8adb50ca13a24/messages/61e6878165934b58b8e5d1e0/reaction/add"

# # reactions = [
# #         {
# #             "count": 2,
# #             "emoji": "lolz",
# #             "name": "lolz",
# #             "reactedUsersId": [
# #                 "61696f5ac4133ddaa309dcfe",
# #                 "619bab3b1a5f54782939d400"
# #             ]
# #         },
# #         {
# #             "count": 1,
# #             "emoji": "smile",
# #             "name": "smile",
# #             "reactedUsersId": [
# #                 "619bab3b1a5f54782939d400"
# #             ]
# #         },
# #     ]

# fake_room_data = {
#     "room_name": "General",
#     "room_type": "CHANNEL",
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
#         "619bab3b1a5f54782939d400": {
#             "closed": False,
#             "role": "member",
#             "starred": False,
#         },
#         "619ba4671a5f54782939d385": {
#             "closed": False,
#             "role": "member",
#             "starred": False,
#         },
#     },
#     "created_at": "2022-01-11 03:18:02.364291",
#     "description": None,
#     "topic": "General Information",
#     "is_private": False,
#     "is_archived": False,
#     "id": "23dg67l0eba8adb50ca13a24",
#     "org_id": "3467sd4671a5f5478df56u911",
#     "created_by": "619ba4671a5f54782939d385",
# }

# fake_message_data = {
#     "_id": "61e6878165934b58b8e5d1e0",
#     "created_at": "2022-01-18 09:05:32.479911",
#     "edited": False,
#     "emojis": [
#         {
#             "count": 2,
#             "emoji": "lol",
#             "name": "lol",
#             "reactedUsersId": [
#                 "61696f5ac4133ddaa309dcfe",
#                 "619bab3b1a5f54782939d400"
#             ]
#         },
#         {
#             "count": 1,
#             "emoji": "smile",
#             "name": "smile",
#             "reactedUsersId": [
#                 "619bab3b1a5f54782939d400"
#             ]
#         },
#     ],
#     "files": [],
#     "org_id": "619ba4671a5f54782939d384",
#     "richUiData": {
#       "blocks": [
#         {
#           "data": {},
#           "depth": 0,
#           "entityRanges": [],
#           "inlineStyleRanges": [],
#           "key": "random",
#           "text": "Helloooo",
#           "type": "unstyled"
#         }
#       ],
#       "entityMap": {}
#     },
#     "room_id": "61e6855e65934b58b8e5d1df",
#     "saved_by": [],
#     "sender_id": "619bab3b1a5f54782939d400",
#     "threads": [],
#     "timestamp": 0
#   }


# # {
# #   "status": "success",
# #   "message": "user's reaction removed",
# #   "data": {
# #     "count": 1,
# #     "emoji": "frown",
# #     "name": "frown",
# #     "reactedUsersId": [
# #       "619bab3b1a5f54782939d400"
# #     ]
# #   }
# # }

# # {
# #   "status": "success",
# #   "message": "reaction removed",
# #   "data": {
# #     "count": 0,
# #     "emoji": "frown",
# #     "name": "frown",
# #     "reactedUsersId": [
# #       "619bab3b1a5f54782939d400"
# #     ]
# #   }
# # }

# @pytest.mark.asyncio
# @mock.patch.object(DataStorage, "__init__", lambda x, y: None)
# async def test_add_reaction_when_reaction_does_not_exist_successful(
#     mock_dataStorage_read, mock_dataStorage_update, mock_centrifugo
# ):
#     """Add reaction to message
#     Args:
#         mock_dataStorage_read (AsyncMock): Asynchronous external api call
#         mock_dataStorage_update (AsyncMock): Asynchronous external api call
#         mock_centrifugo (AsyncMock): Asynchronous external api call
#     """
#     db = DataStorage("619ba4671a5f54782939d384")
#     db.plugin_id = "34453"
#     # fake_message_data["emojis"] = reactions

#     add_reaction_payload = {
#         'name': 'lol',
#         'count': 1,
#         'emoji': 'lol',
#         'reactedUsersId': [
#             "619ba4671a5f54782939d385"
#             ]
#     }

#     update_response = {
#         "status" : 200,
#         "message" : "reaction added"
#     }
#     success_response = {
#         "status": "success",
#         "message": "reaction added",
#         "data": {
#             "name": "lol",
#             "count": 1,
#             "emoji": "lol",
#             "reactedUsersId": [
#             "619ba4671a5f54782939d385"
#             ]
#         }
#     }
#     centrifugo_response = {"status_code": 200}

#     mock_dataStorage_read.return_value = fake_message_data
#     mock_dataStorage_read.return_value = fake_room_data
#     mock_dataStorage_update.return_value = update_response
#     mock_centrifugo.return_value = centrifugo_response

#     response = client.put(url=reaction_url, json=add_reaction_payload)
#     assert response.status_code == 200
#     assert response.json() == success_response


# @pytest.mark.asyncio
# @mock.patch.object(DataStorage, "__init__", lambda x, y: None)
# async def test_add_reaction_when_reaction_exists_successful(
#     mock_dataStorage_read, mock_dataStorage_update, mock_centrifugo
# ):
#     """Add reaction to message
#     Args:
#         mock_dataStorage_read (AsyncMock): Asynchronous external api call
#         mock_dataStorage_update (AsyncMock): Asynchronous external api call
#         mock_centrifugo (AsyncMock): Asynchronous external api call
#     """
#     db = DataStorage("619ba4671a5f54782939d384")
#     db.plugin_id = "34453"
#     # fake_message_data["emojis"] = reactions

#     add_reaction_payload = {
#         'name': 'lol',
#         'count': 1,
#         'emoji': 'lol',
#         'reactedUsersId': [
#             "619ba4671a5f54782939d385"
#             ]
#     }

#     update_response = {
#         "status" : 200,
#         "message" : "reaction added"
#     }
#     # new_fake_message_data["emojis"] = fake_message_data["emojis"] + [add_reaction_payload]
#     reactions = fake_message_data["emojis"].append(add_reaction_payload)
    
#     success_response = {
#         "status": "success",
#         "message": "reaction added",
#         "data": reactions
#         # "data": new_fake_message_data["emojis"]
#         # "data": fake_message_data["emojis"][-1]
#         # "data": {
#         #     "name": "lol",
#         #     "count": 2,
#         #     "emoji": "lol",
#         #     "reactedUsersId": [
#         #     "619ba4671a5f54782939d385",
#         #     "619bab3b1a5f54782939d400"
#         #     ]
#         # }
#     }
#     centrifugo_response = {"status_code": 200}

#     mock_dataStorage_read.return_value = fake_message_data
#     mock_dataStorage_read.return_value = fake_room_data
#     mock_dataStorage_update.return_value = update_response
#     mock_centrifugo.return_value = centrifugo_response

#     response = client.put(url=reaction_url, json=add_reaction_payload)
#     assert response.status_code == 200
#     assert response.json() == success_response


# # @pytest.mark.asyncio
# # @mock.patch.object(DataStorage, "__init__", lambda x, y: None)
# # async def test_invalid_member_id(
# #     mock_dataStorage_read
# # ):
# #     """Remove reaction from message
# #     Args:
# #         mock_dataStorage_read (AsyncMock): Asynchronous external api call
# #         mock_dataStorage_update (AsyncMock): Asynchronous external api call
# #         mock_centrifugo (AsyncMock): Asynchronous external api call
# #     """
# #     db = DataStorage("619ba4671a5f54782939d384")
# #     db.plugin_id = "34453"

# #     members = {
# #         "61696f5ac4133ddaa309dcfe",
# #         "6169704bc4133ddaa309dd07",
# #         "619baa5c1a5f54782939d386",
# #         "619bab3b1a5f54782939d400",
# #         "619ba4671a5f54782939d385"
# #     }

# #     add_reaction_payload = {
# #         'name': 'lol',
# #         'count': 1,
# #         'emoji': 'lol',
# #         'reactedUsersId': [
# #             "619ba4671a585f547839d293"
# #             ]
# #     }
# #     add_reaction_payload["reactedUsersId"] = ["619ba4671a585f547839d293"]
# #     read_response = {"status_code": 401, "message": "Invalid room member"}

# #     mock_dataStorage_read.return_value == members
# #     mock_dataStorage_read.return_value == read_response
# #     response = client.put(url=add_reaction_url)
# #     # response = client.put(url=add_reaction_url, json=add_reaction_payload)
# #     assert response.status_code == 422
# #     assert response.json() == {"detail": "Invalid room member" }









# # @pytest.mark.asyncio
# # @mock.patch.object(DataStorage, "__init__", lambda x, y: None)
# # async def test_remove_reaction_no_reaction_exists(
# #     mock_dataStorage_read, mock_dataStorage_update, mock_centrifugo
# # ):
# #     """Remove reaction from message
# #     Args:
# #         mock_dataStorage_read (AsyncMock): Asynchronous external api call
# #         mock_dataStorage_update (AsyncMock): Asynchronous external api call
# #         mock_centrifugo (AsyncMock): Asynchronous external api call
# #     """
# #     db = DataStorage("619ba4671a5f54782939d384")
# #     db.plugin_id = "34453"
# #     fake_message_data["emojis"] = []

# #     remove_reaction_payload = {
# #         'name': 'lol',
# #         'count': 1,
# #         'emoji': 'lol',
# #         'reactedUsersId': [
# #             "619ba4671a5f54782939d385"
# #             ]
# #     }

# #     update_response = {
# #         "status" : 404,
# #         "message" : "No reactions found"
# #     }
# #     centrifugo_response = {"status_code": 200}

# #     mock_dataStorage_read.return_value = fake_message_data
# #     mock_dataStorage_read.return_value = fake_room_data
# #     mock_dataStorage_update.return_value = update_response
# #     mock_centrifugo.return_value = centrifugo_response

# #     response = client.put(url=remove_reaction_url, json=remove_reaction_payload)
# #     assert response.status_code == 404


# # @pytest.mark.asyncio
# # @mock.patch.object(DataStorage, "__init__", lambda x, y: None)
# # async def test_remove_reaction_when_user_has_not_reacted_with_emoji(
# #     mock_dataStorage_read, mock_dataStorage_update, mock_centrifugo
# # ):
# #     """Remove reaction from message
# #     Args:
# #         mock_dataStorage_read (AsyncMock): Asynchronous external api call
# #         mock_dataStorage_update (AsyncMock): Asynchronous external api call
# #         mock_centrifugo (AsyncMock): Asynchronous external api call
# #     """
# #     db = DataStorage("619ba4671a5f54782939d384")
# #     db.plugin_id = "34453"
# #     fake_message_data["emojis"] == [
# #         {
# #             "count": 1,
# #             "emoji": "smile",
# #             "name": "smile",
# #             "reactedUsersId": [
# #                 "619bab3b1a5f54782939d400"
# #             ]
# #         },
# #     ]

# #     remove_reaction_payload = {
# #         "count": 1,
# #         "emoji": "smile",
# #         "name": "smile",
# #         'reactedUsersId': [
# #             "619ba4671a5f54782939d385"
# #             ]
# #     }

# #     remove_reaction_payload["reactedUsersId"] = ["619ba4671a5f54782939d385"]
# #     read_response = {
# #         "status_code" : 409,
# #         "message" : "Member hasn't reacted with this emoji"
# #     }
# #     # success_response = {
# #     #     "status": "success",
# #     #     "message": "reaction removed",
# #     #     "data": {
# #     #         "name": "smile",
# #     #         "count": 0,
# #     #         "emoji": "smile",
# #     #         "reactedUsersId": []
# #     #     }
# #     # }
# #     # centrifugo_response = {"status_code": 200}

# #     mock_dataStorage_read.return_value = fake_message_data
# #     mock_dataStorage_read.return_value == read_response
# #     # mock_dataStorage_read.return_value = fake_room_data
# #     # mock_dataStorage_update.return_value == update_response
# #     # mock_centrifugo.return_value = centrifugo_response

# #     # response = client.put(url=remove_reaction_url, json=remove_reaction_payload)
# #     response = client.put(url=remove_reaction_url)
# #     assert response.status_code == 422
# #     assert response.json() == {"detail": "Member hasn't reacted with this emoji"}





# # @pytest.mark.asyncio
# # @mock.patch.object(DataStorage, "__init__", lambda x, y: None)
# # async def test_remove_reaction_when_only_one_exists_successful(
# #     mock_dataStorage_read, mock_dataStorage_update, mock_centrifugo
# # ):
# #     """Remove reaction from message
# #     Args:
# #         mock_dataStorage_read (AsyncMock): Asynchronous external api call
# #         mock_dataStorage_update (AsyncMock): Asynchronous external api call
# #         mock_centrifugo (AsyncMock): Asynchronous external api call
# #     """
# #     db = DataStorage("619ba4671a5f54782939d384")
# #     db.plugin_id = "34453"
# #     fake_message_data["emojis"] == [
# #         {
# #             "count": 1,
# #             "emoji": "smile",
# #             "name": "smile",
# #             "reactedUsersId": [
# #                 "619bab3b1a5f54782939d400"
# #             ]
# #         },
# #     ]

# #     remove_reaction_payload = {
# #         "count": 1,
# #         "emoji": "smile",
# #         "name": "smile",
# #         "reactedUsersId": [
# #             "619bab3b1a5f54782939d400"
# #         ]
# #     }
# #     # fake_message_data["emojis"] == []
# #     fake_message_data["emojis"] == []
# #     update_response = {
# #         "status" : 200,
# #         "message" : "reaction removed"
# #     }
# #     success_response = {
# #         "status": "success",
# #         "message": "reaction removed",
# #         "data": {
# #             "name": "smile",
# #             "count": 0,
# #             "emoji": "smile",
# #             "reactedUsersId": []
# #         }
# #     }
# #     centrifugo_response = {"status_code": 200}

# #     mock_dataStorage_read.return_value = fake_message_data["emojis"]
# #     # mock_dataStorage_read.return_value = fake_message_data
# #     # mock_dataStorage_read.return_value == reactions
# #     mock_dataStorage_read.return_value = fake_room_data
# #     mock_dataStorage_update.return_value == update_response
# #     mock_centrifugo.return_value = centrifugo_response

# #     response = client.put(url=remove_reaction_url, json=remove_reaction_payload)
# #     assert response.status_code == 404
# #     assert response.json() == success_response


# # @pytest.mark.asyncio
# # @mock.patch.object(DataStorage, "__init__", lambda x, y: None)
# # async def test_add_reaction_when_reaction_already_exists_successful(
# #     mock_dataStorage_read, mock_dataStorage_update, mock_centrifugo
# # ):
# #     """Add reaction to message
# #     Args:
# #         mock_dataStorage_read (AsyncMock): Asynchronous external api call
# #         mock_dataStorage_update (AsyncMock): Asynchronous external api call
# #         mock_centrifugo (AsyncMock): Asynchronous external api call
# #     """
# #     db = DataStorage("619ba4671a5f54782939d384")
# #     db.plugin_id = "34453"
# #     fake_message_data["emojis"] = reactions

# #     add_reaction_payload = {
# #         "count": 1,
# #         "emoji": "smile",
# #         "name": "smile",
# #         "reactedUsersId": [
# #             "6169704bc4133ddaa309dd07"
# #         ]
# #     }

# #     reactions == reactions.append(add_reaction_payload)
# #     update_response = {
# #         "status" : 200,
# #         "message" : "reaction added",
# #         "data": {
# #             "name": "smile",
# #             "count": 2,
# #             "emoji": "smile",
# #             "reactedUsersId": [
# #             "619bab3b1a5f54782939d400",
# #             "6169704bc4133ddaa309dd07"
# #             ]
# #         }
# #     }
# #     # success_response = {
# #     #     "status": "success",
# #     #     "message": "reaction added",
# #     #     "data": {
# #     #         "name": "smile",
# #     #         "count": 1,
# #     #         "emoji": "smile",
# #     #         "reactedUsersId": [
# #     #         "6169704bc4133ddaa309dd07"
# #     #         ]
# #     #     }
# #     # }
# #     centrifugo_response = {"status_code": 200}

# #     # mock_dataStorage_read.return_value = fake_message_data["emojis"]
# #     mock_dataStorage_read.return_value = reactions
# #     mock_dataStorage_read.return_value = fake_room_data
# #     mock_dataStorage_update.return_value == update_response
# #     mock_centrifugo.return_value = centrifugo_response

# #     response = client.put(url=reaction_url, json=add_reaction_payload)
# #     assert response.status_code == 200
# #     # assert response.json() == success_response
