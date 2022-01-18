# from unittest import mock

# import pytest
# from fastapi.testclient import TestClient
# from main import app
# from utils.db import DataStorage

# client = TestClient(app)
# reaction_url = "api/v1/org/619ba4/rooms/343235/messages/346556/reaction"

# reaction_payload = {
#         "name": "lol",
#         "count": 1,
#         "emoji": "lol",
#         "reactedUsersId": ["619ba4671a5f54782939d385"]
#     }

# fake_room_data = {
#     "_id": "343235",
#     "created_at": "2021-11-24 11:23:11.361210",
#     "created_by": "6169704bc4133ddaa309dd07",
#     "description": "Section for general information",
#     "id": None,
#     "is_archived": False,
#     "is_private": False,
#     "org_id": "619baf",
#     "room_members": {
#         "6169704bc4133ddaa309dd07": {"closed": False, "role": "admin", "starred": False},
#         "619ba4671a5f54782939d385": {"closed": False, "role": "admin", "starred": False},
#     },
#     "room_name": "random",
#     "room_type": "CHANNEL",
#     "topic": "Information",
# }


# fake_message_data = {
#     "_id": "346556",
#     "created_at": "2021-12-28 19:27:13.620083",
#     "edited": False,
#     "emojis": [],
#     "files": [],
#     "org_id": "1234",
#     "richUiData": {
#         "blocks": [
#             {
#                 "data": {},
#                 "depth": 0,
#                 "entityRanges": [],
#                 "inlineStyleRanges": [],
#                 "key": "eljik",
#                 "text": "HI, I'm mark.. new here",
#                 "type": "unstyled",
#             }
#         ],
#         "entityMap": {},
#     },
#     "room_id": "343235",
#     "saved_by": [],
#     "sender_id": "619ba4671a5f54782939d385",
#     "threads": [],
#     "timestamp": 0,
# }

# fake_room_members = {
#     #"61696f5ac4133ddaa309dcfe": {"closed": False, "role": "admin", "starred": False},
#     "6169704bc4133ddaa309dd07": {"closed": False, "role": "admin", "starred": False},
#     "619ba4671a5f54782939d385": {"closed": False, "role": "admin", "starred": False},
#     #"619baa5c1a5f54782939d386": {"closed": False, "role": "member", "starred": False}
# }

# @pytest.mark.asyncio
# @mock.patch.object(DataStorage, "__init__", lambda x, y: None)
# async def test_add_reaction_successful(
#     mock_get_room_members, mock_dataStorage_read, mock_dataStorage_update, mock_centrifugo
# ):
#     """Add reaction to message
#     Args:
#         mock_get_room_members (AsyncMock): Asynchronous external api call
#         mock_dataStorage_read (AsyncMock): Asynchronous external api call
#         mock_dataStorage_update (AsyncMock): Asynchronous external api call
#         mock_centrifugo (AsyncMock): Asynchronous external api call
#     """
#     db = DataStorage("619ba4")
#     db.plugin_id = "34453"
    
    
#     # members = list(fake_room_data["room_members"])
#     # members = list(fake_room_members.keys())
#     # members = list(fake_room_members)
#     # reaction_payload["reactedUsersId"] in members
    
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
#     reaction_payload["reactedUsersId"] = success_response["data"]["reactedUsersId"]    
#     centrifugo_response = {"status_code": 200}

#     mock_dataStorage_read.return_value = fake_message_data
#     # mock_dataStorage_read.return_value = fake_room_members
#     # mock_get_room_members.return_value = fake_room_members
#     mock_get_room_members.return_value = fake_room_data["room_members"]
#     # mock_dataStorage_read.return_value = fake_room_data["room_members"]
#     mock_dataStorage_update.return_value = update_response
#     mock_centrifugo.return_value = centrifugo_response

#     response = client.put(url=reaction_url, json=reaction_payload)
#     assert response.status_code == 424
#     # success_response["data"]["reactedUsersId"] = response.json()["data"]["reactedUsersId"]
#     assert response.json() == success_response





# # @pytest.mark.asyncio
# # @mock.patch.object(DataStorage, "__init__", lambda x, y: None)
# # async def test_update_message_successful(
# #     mock_dataStorage_read, mock_dataStorage_update, mock_centrifugo
# # ):
# #     """Update message successful.
# #     Args:
# #         mock_dataStorage_read (AsyncMock): Asynchronous external api call
# #         mock_dataStorage_update (AsyncMock): Asynchronous external api call
# #         mock_centrifugo (AsyncMock): Asynchronous external api call
# #     """
# #     db = DataStorage("619ba4")
# #     db.plugin_id = "34453"
# #     mock_dataStorage_read.return_value = fake_zc_core_message_data
# #     mock_dataStorage_update.return_value = {
# #         "status": 200,
# #         "message": "success",
# #         "data": {"matched_documents": 1, "modified_documents": 1},
# #     }
# #     mock_centrifugo.return_value = {"status_code": 200}
# #     response = client.put(update_message_test_url, json=update_message_test_payload)
# #     assert response.status_code == 200
# #     assert response.json() == {
# #         "status": "success",
# #         "message": "Message edited",
# #         "data": {
# #             "_id": "346556",
# #             "created_at": "2021-12-28 19:27:13.620083",
# #             "edited": True,
# #             "emojis": [],
# #             "files": [],
# #             "org_id": "1234",
# #             "richUiData": {
# #                 "blocks": [
# #                     {
# #                         "data": {},
# #                         "depth": 0,
# #                         "entityRanges": [],
# #                         "inlineStyleRanges": [],
# #                         "key": "eljik",
# #                         "text": "HI,  mark",
# #                         "type": "unstyled",
# #                     }
# #                 ],
# #                 "entityMap": {},
# #             },
# #             "room_id": "343235",
# #             "saved_by": [],
# #             "sender_id": "619ba4",
# #             "threads": [],
# #             "timestamp": 0,
# #         },
# #     }








# # @pytest.mark.asyncio
# # @mock.patch.object(DataStorage, "__init__", lambda x, y: None)
# # async def test_send_message_successful(
# #     mock_dataStorage_read, mock_dataStorage_write, mock_centrifugo
# # ):
# #     """Send message successful
# #     Args:
# #         mock_get_room (AsyncMock): Asynchronous external api call
# #         mock_dataStorage_write (AsyncMock): Asynchronous external api call
# #         mock_centrifugo (AsyncMock): Asynchronous external api call
# #     """
# #     db = DataStorage("619ba4")
# #     db.plugin_id = "34453"
# #     success_response = {
# #         "status": "success",
# #         "message": "new message sent",
# #         "data": {
# #             "sender_id": "e21e10",
# #             "emojis": [],
# #             "richUiData": {
# #                 "blocks": [
# #                     {
# #                         "key": "eljik",
# #                         "text": "HI, I'm mark.. new here",
# #                         "type": "unstyled",
# #                         "depth": 0,
# #                         "inlineStyleRanges": [],
# #                         "entityRanges": [],
# #                         "data": {},
# #                     }
# #                 ],
# #                 "entityMap": {},
# #             },
# #             "files": [],
# #             "saved_by": [],
# #             "timestamp": 0,
# #             "created_at": "",
# #             "room_id": "123456",
# #             "org_id": "619ba4",
# #             "message_id": "a1a1a1",
# #             "edited": False,
# #             "threads": [],
# #         },
# #     }

# #     write_response = {
# #         "status": 200,
# #         "message": "success",
# #         "data": {"insert_count": 1, "object_id": "a1a1a1"},
# #     }

# #     centrifugo_response = {"status_code": 200}

# #     mock_dataStorage_read.return_value = fake_core_room_data
# #     mock_dataStorage_write.return_value = write_response
# #     mock_centrifugo.return_value = centrifugo_response

# #     response = client.post(send_message_test_url, json=send_message_test_payload)
# #     assert response.status_code == 201
# #     success_response["data"]["created_at"] = response.json()["data"]["created_at"]
# #     assert response.json() == success_response
