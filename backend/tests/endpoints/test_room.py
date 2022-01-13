# import pytest
# from fastapi.testclient import TestClient
# from main import app

# client = TestClient(app)

# create_channel_url = "api/v1/org/619ba4/members/we54kl/rooms"
# create_dm_url = "api/v1/org/619ba4/members/e21e10/rooms"


# test_payload_channel = {
#     "room_name": "test_channel",
#     "room_type": "CHANNEL",
#     "room_members": {
#         "we54kl": {
#         "role": "admin",
#         "starred": False,
#         "closed": False
#         }
#     },
#     "created_at": "2022-01-09 11:23:11.361217",
#     "description": "a test channel",
#     "topic": "testing",
#     "is_private": False,
#     "is_archived": False
#     }

# test_payload_dm = {
#     "room_name": "e21e10_dm",
#     "room_type": "DM",
#     "room_members": {
#         "e21e10": {
#         "role": "member",
#         "starred": False,
#         "closed": False
#         }
#     },
#     "created_at": "2022-01-09 11:23:11.361210",
#     "description": "personal message",
#     "topic": "test_dm",
#     "is_private": False,
#     "is_archived": False
#     }

# test_payload_group_dm = {
#   "room_name": "test group dm",
#   "room_type": "GROUP_DM",
#   "room_members": {
#     "61696f5ac4133ddaa309dcfe": {
#       "closed": False,
#       "role": "admin",
#       "starred": False
#     },
#     "6169704bc4133ddaa309dd07": {
#       "closed": False,
#       "role": "admin",
#       "starred": False
#     },
#     "619ba4671a5f54782939d385": {
#       "closed": False,
#       "role": "admin",
#       "starred": False
#     },
#     "619baa5c1a5f54782939d386": {
#       "closed": False,
#       "role": "member",
#       "starred": False
#     }
#   },
#   "is_private": False,
#   "is_archived": False
# }

# fake_data_channel = {
#     "_id": "c31a5f",
#     "created_at": "2022-01-09 11:23:11.361217",
#     "created_by": "we54kl",
#     "description": "a test channel",
#     "id": None,
#     "is_archived": False,
#     "is_private": False,
#     "org_id": "619ba4",
#     "room_members": {
#         "we54kl": {
#             "closed": False,
#             "role": "admin",
#             "starred": False
#             },
#     },
#     "room_name": "test_channel",
#     "room_type": "CHANNEL",
#     "topic": "testing"
# }

# # fake_data_group_dm = 

# fake_data_dm = {
#     "_id": "39fy78",
#     "created_at": "2022-01-09 11:23:11.361210",
#     "created_by": "e21e10",
#     "description": "personal message",
#     "id": None,
#     "is_archived": False,
#     "is_private": False,
#     "org_id": "619ba4",
#     "room_members": {
#         "e21e10": {"closed": False, "role": "member", "starred": False},
#     },
#     "room_name": "e21e10_dm",
#     "room_type": "DM",
#     "topic": "test_dm"
# }

# fake_org_members = {
#     "e21e10": {
#         "closed": False,
#         "role": "member", 
#         "starred": False
#         },
#     "we54kl": {
#         "role": "admin",
#         "starred": False,
#         "closed": False
#         }
#     }

# fake_admin_member = {
#     "we54kl": {
#         "role": "admin",
#         "starred": False,
#         "closed": False
#         }
#     }
  
# # fake_admin = {
# #     "we54kl": {
# #         "role": "admin",
# #         "starred": False,
# #         "closed": False
# #         }
# #     }
# # fake_admin_member = list(fake_admin)


# # channel tests
# # @pytest.mark.asyncio
# # async def test_create_channel_successful(mock_get_admin_members, mock_write, mock_centrifugo):
# #     """
# #     Create channel successful
    
# #     Args:
# #         mock_get_admin_members (AsyncMock): Asynchronous external api call
# #         mock_write (AsyncMock): Asynchronous external api call
# #         mock_centrifugo (AsyncMock): Asynchronous external api call
# #     """
# #     mock_get_admin_members.return_value = fake_admin_member
    
# #     success = {
# #         "status": "success",
# #         "message": "Room created",
# #         "data": fake_data_channel
# #         }
    
# #     mock_write.return_value = {
# #         "status": 201,
# #         "message": "success",
# #         "data": {
# #             "insert_count": 1,
# #             "object_id": "c31a5f"
# #             }
# #         }
# #     mock_centrifugo.return_value = {
# #         "status_code": 200
# #         }
    
# #     response = client.post(create_channel_url, json=test_payload_channel)
# #     assert response.status_code == 201
# #     # assert response.status_code == 422
# #     assert response.json() == success
        
    
# # @pytest.mark.asyncio
# # async def test_member_not_admin(mock_get_admin_members, mock_write):
# #     """
# #     Create Channel unsuccessful when member is not admin
    
# #     Args:
# #         mock_get_admin_members (AsyncMock): Asynchronous external api call
# #     """
# #     mock_get_admin_members.return_value = fake_admin_member
    
# #     test_payload_channel["room_members"] = {
# #         "e21e10": {
# #             "role": "member",
# #             "starred": False,
# #             "closed": False
# #             }
# #         }
    
# #     # test_payload_channel["room_members"]["role"] != "admin"
    
# #     # mock_write.return_value = {
# #     #     "status": 401
# #     #     # "message": "error",
# #     #     # "data": {
# #     #     #     "insert_count": 0,
# #     #     #     "object_id": None,
# #     #     #     }
# #     #     }
    
# #     mock_write.return_value = {
# #         "status": 401,
# #         "message": "error",
# #         "data": {
# #             "insert_count": 0,
# #             "object_id": None,
# #             }
# #         }
     
# #     response = client.post(create_channel_url, json=test_payload_channel)
# #     # assert response.status_code == 401
# #     # assert response.status_code == 422
# #     assert mock_write.status_code == 401
# #     assert response.json() == {"detail": "sender not authorized to create channel"}
    

# # @pytest.mark.asyncio
# # async def test_create_channel_failure(mock_get_admin_members, mock_write):
# #     """
# #     Create channel unsuccessful
    
# #     Args:
# #         mock_get_room (AsyncMock): Asynchronous external api call
# #         mock_write (AsyncMock): Asynchronous external api call
# #     """
# #     mock_get_admin_members.return_value = fake_admin_member
    
# #     mock_write.return_value = {
# #         "status": 400,
# #         "message": "error",
# #         "data": {
# #             "insert_count": 0,
# #             "object_id": None,
# #             }
# #         }
    
# #     response = client.post(create_channel_url, json=test_payload_channel)
# #     # assert response.status_code == 400
# #     # assert response.status_code == 422
# #     assert mock_write.status_code == 400
# #     assert response.json() == {
# #         "detail": "Failed to create channel"
# #         }


# # @pytest.mark.asyncio
# # async def test_failure_to_publish_new_channel_to_centrifugo(
# #     mock_get_admin_members, mock_write, mock_centrifugo
# #     ):
# #     """
# #     Create channel successful but failed to publish to centrifugo
    
# #     Args:
# #         mock_get_room (AsyncMock): Asynchronous external api call
# #         mock_write (AsyncMock): Asynchronous external api call
# #         mock_centrifugo (AsyncMock): Asynchronous external api call
# #     """
# #     mock_get_admin_members.return_value = fake_admin_member
    
# #     mock_write.return_value = {
# #         "status": 200,
# #         "message": "success",
# #         "data": {
# #             "insert_count": 1,
# #             "object_id": "c31a5f",
# #             }
# #         }
# #     centrifugo_response = {"status_code": 424}
    
# #     response = client.post(create_channel_url, json=test_payload_channel)
# #     assert response.status_code == 200
    
# #     mock_centrifugo.return_value = centrifugo_response
# #     assert centrifugo_response.status_code == 424
# #     assert mock_centrifugo.json() == {
# #         "detail": "Failed to publish to centrifugo"
# #     }


# # @pytest.mark.asyncio
# # async def test_create_channel_failure_to_get_admin_members(mock_get_admin_members):
# #     """
# #     Failure to retrieve admin member
    
# #     Args:
# #         mock_get_room (AsyncMock): Asynchronous external api call
# #     """
# #     mock_get_admin_members.return_value = None
    
# #     response = client.post(create_channel_url, json=test_payload_channel)
# #     # assert response.status_code == 424
# #     assert response.status_code == 422
# #     assert response.json() == {
# #         "detail": {"Failed to retrieve admin members": mock_get_admin_members.return_value}
# #         }
    

# # # DM tests
# # @pytest.mark.asyncio
# # async def test_create_dm_successful(mock_get_org_members, mock_write, mock_centrifugo):
# #     """
# #     Create DM successful
    
# #     Args:
# #         mock_get_org_members (AsyncMock): Asynchronous external api call
# #         mock_write (AsyncMock): Asynchronous external api call
# #         mock_centrifugo (AsyncMock): Asynchronous external api call
# #     """
# #     mock_get_org_members.return_value = fake_org_members
    
# #     mock_write.return_value = {
# #         "status": 200,
# #         "message": "success",
# #         "data": {
# #             "insert_count": 1,
# #             "object_id": "39fy78",
# #             }
# #         }
# #     mock_centrifugo.return_value = {
# #         "status_code": 200
# #         }
    
# #     response = client.post(create_dm_url, json=test_payload_dm)
# #     # assert response.status_code == 200
# #     # assert response.status_code == 400
# #     assert mock_write.status_code == 200
# #     assert response.json() == {
# #         "status": "success",
# #         "message": "Room created",
# #         "data": {
# #             "room_name": "e21e10_dm",
# #             "room_type": "DM",
# #             "room_members": {
# #                 "e21e10": {
# #                 "role": "member",
# #                 "starred": False,
# #                 "closed": False
# #                 }
# #             },
# #             "created_at": "2022-01-09 11:23:11.361210",
# #             "description": "personal message",
# #             "topic": "test_dm",
# #             "is_private": False,
# #             "is_archived": False,
# #             "id": "39fy78",
# #             "org_id": "619ba4",
# #             "created_by": "e21e10"
# #             }
# #         }


# # @pytest.mark.asyncio
# # async def test_create_dm_failure(mock_get_org_members, mock_write):
# #     """
# #     Create DM unsuccessful
    
# #     Args:
# #         mock_get_org_members (AsyncMock): Asynchronous external api call
# #         mock_write (AsyncMock): Asynchronous external api call
# #     """
# #     mock_get_org_members.return_value = fake_org_members
    
# #     mock_write.return_value = {
# #         "status": 400,
# #         "message": "error",
# #         "data": {
# #             "insert_count": 0,
# #             "object_id": None,
# #         }
# #     }
    
# #     response = client.post(create_dm_url, json=test_payload_dm)
# #     assert mock_write.status_code == 400
# #     assert response.json() == {
# #         "detail": {"Failed to create DM": mock_write.return_value}
        
# #         #  "detail': 'DM can only have 2 unique members"
# #     }
    
    
# # @pytest.mark.asyncio
# # async def test_failure_to_publish_new_dm_to_centrifugo(
# #     mock_get_org_members, mock_write, mock_centrifugo
# #     ):
# #     """
# #     Create DM successful but failed to publish to centrifugo
    
# #     Args:
# #         mock_get_org_members (AsyncMock): Asynchronous external api call
# #         mock_write (AsyncMock): Asynchronous external api call
# #         mock_centrifugo (AsyncMock): Asynchronous external api call
# #     """
# #     mock_get_org_members.return_value = fake_org_members
    
# #     mock_write.return_value = {
# #         "status": 200,
# #         "message": "success",
# #         "data": {
# #             "insert_count": 1,
# #             "object_id": "39fy78",
# #             }
# #         }
# #     centrifugo_response = {"status_code": 424}
    
# #     response = client.post(create_channel_url, json=test_payload_channel)
# #     # assert response.status_code == 200
# #     # assert response.status_code == 422
# #     assert mock_write.status_code == 200
# #     assert response.json() == {
# #         "status": "success",
# #         "message": "Room created",
# #         "data": {
# #             "room_name": "e21e10_dm",
# #             "room_type": "DM",
# #             "room_members": {
# #                 "e21e10": {
# #                 "role": "member",
# #                 "starred": False,
# #                 "closed": False
# #                 }
# #             },
# #             "created_at": "2022-01-09 11:23:11.361210",
# #             "description": "personal message",
# #             "topic": "test_dm",
# #             "is_private": False,
# #             "is_archived": False,
# #             "id": "39fy78",
# #             "org_id": "619ba4",
# #             "created_by": "e21e10"
# #             }
# #         }
    
# #     mock_centrifugo.return_value = centrifugo_response
# #     assert mock_centrifugo.status_code == 424
# #     assert mock_centrifugo.json() == {
# #         "detail": {"Failed to publish to centrifugo": centrifugo_response}
# #     }


# # @pytest.mark.asyncio
# # async def test_duplicate_dm_name(mock_get_org_members, mock_write):
# #     """
# #     Create DM unsuccessful when name already exists
    
# #     Args:
# #         mock_get_org_members (AsyncMock): Asynchronous external api call
# #         mock_write (AsyncMock): Asynchronous external api call
# #     """
# #     mock_get_org_members.return_value = fake_org_members
    
# #     test_payload_dm["room_name"] = "e21e10_dm"
    
# #     mock_write.return_value = {
# #         "status": 400,
# #         "message": "error",
# #         "data": {
# #             "insert_count": 0,
# #             "object_id": None,
# #             }
# #         }
    
# #     response = client.post(create_dm_url, json=test_payload_dm)
# #     assert response.status_code == 400
# #     assert response.json() == {"detail": "DM name already exists"}
    
 
# # @pytest.mark.asyncio
# # async def test_duplicate_channel_name(mock_get_org_members, mock_write):
# #      """
# #      Create channel unsuccessful when name already exists
     
# #      Args:
# #          mock_get_org_members (AsyncMock): Asynchronous external api call
# #          mock_write (AsyncMock): Asynchronous external api call
# #      """
# #      mock_get_org_members.return_value = fake_org_members
     
# #      test_payload_channel["room_name"] = "test_channel"
     
# #      mock_write.return_value = {
# #          "status": 400,
# #          "message": "error",
# #          "data": {
# #              "insert_count": 0,
# #              "object_id": None,
# #              }
# #          }
     
# #      response = client.post(create_channel_url, json=test_payload_channel)
# #      assert response.status_code == 400
# #      assert response.json() == {"detail": "Channel name already exists"}   
    

# # @pytest.mark.asyncio
# # async def test_create_dm_with_invalid_members(mock_get_org_members, mock_write):
# #     """
# #     Create DM with invalid members
    
# #     Args:
# #         mock_get_org_members (AsyncMock): Asynchronous external api call
# #         mock_write (AsyncMock): Asynchronous external api call
# #     """
# #     mock_get_org_members.return_value = fake_org_members
        
# #     test_payload_dm["room_members"] = {
# #         "e21e10": {
# #             "role": "member",
# #             "starred": False,
# #             "closed": False
# #             },
# #         "bkbu87": {
# #             "role": "member",
# #             "starred": False,
# #             "closed": False
# #             }
# #         }
    
# #     mock_write.return_value = {
# #         "status": 400,
# #         "message": "error",
# #         "data": {
# #             "insert_count": 0,
# #             "object_id": None,
# #         }
# #     }
    
# #     response = client.post(create_dm_url, json=test_payload_dm)
# #     # assert response.status_code == 400
# #     assert response.status_code == 422
# #     assert response.json() == {
# #         # "detail": {"Failed to create DM": mock_write.json()}
# #         "detail": "Invalid members"
# #     }



# # @pytest.mark.asyncio
# # async def test_create_dm_check_status_code(mock_get_org_members, mock_write):
# #     """
# #     Create DM unsuccessful when writing to zc core return a response with status_code.
# #     Args:
# #         mock_get_org_members (AsyncMock): Asynchronous external api call
# #         mock_write (AsyncMock): Asynchronous external api call
# #     """

# #     write_response = {"status_code": 422, "message": "unprocessible error"}
# #     mock_get_org_members.return_value = fake_org_members
# #     mock_write.return_value = write_response
# #     response = client.post(create_dm_url, json=test_payload_dm)
# #     assert response.status_code == 424
# #     assert response.json() == {"detail": {"Room not created": write_response}}


# # @pytest.mark.asyncio
# # async def test_channel_name_is_correct(mock_write):
# #     """
# #     Create channel with incorrect name
    
# #     Args:
# #         mock_write (AsyncMock): Asynchronous external api call
# #     """
# #     test_payload_channel["room_name"] = "test_channel"
    
# #     mock_write.return_value = {
# #         "status": 200,
# #         "message": "success",
# #         "data": {
# #             "insert_count": 1,
# #             "object_id": "39fy78",
# #         }
# #     }
# #     response = client.post(create_channel_url, json=test_payload_channel)
# #     # assert response.status_code == 200
# #     # assert response.json() == {
# #     #     "status": "success",
# #     #     "message": "Room created",
# #     #     "data": fake_data_channel
# #     #     }
# #     # assert response.json()["data"]["room_name"] == "test_channel"
# #     assert response.json() == {
# #         "status": "success",
# #         "message": "Room created",
# #         "data": {
# #             "_id": "c31a5f",
# #             "created_at": "2022-01-09 11:23:11.361217",
# #             "created_by": "we54kl",
# #             "description": "a test channel",
# #             "id": None,
# #             "is_archived": False,
# #             "is_private": False,
# #             "org_id": "619ba4",
# #             "room_members": {
# #                 "we54kl": {
# #                     "closed": False,
# #                     "role": "admin",
# #                     "starred": False
# #                     },
# #             },
# #             "room_name": "test_channel",
# #             "room_type": "CHANNEL",
# #             "topic": "testing"
# #             }
# #         }          

    
# @pytest.mark.asyncio
# async def test_channel_success_status_code(
#     mock_get_admin_members, mock_write
#     ):
#     """
#     Create channel successful status code
    
#     Args:
#         mock_get_room (AsyncMock): Asynchronous external api call
#         mock_write (AsyncMock): Asynchronous external api call
#     """
#     mock_get_admin_members.return_value = fake_admin_member
    
#     mock_write.return_value = {
#         "status": 201,
#         "message": "success",
#         "data": {
#             "insert_count": 1,
#             "object_id": "c31a5f",
#             }
#         }
    
#     response = client.post(create_channel_url, json=test_payload_channel)
#     assert response.status_code != 400
#     # assert response.status_code == 201


# @pytest.mark.asyncio
# async def test_dm_success_status_code(
#     mock_get_org_members, mock_write
#     ):
#     """
#     Create channel successful status code
    
#     Args:
#         mock_get_room (AsyncMock): Asynchronous external api call
#         mock_write (AsyncMock): Asynchronous external api call
#     """
#     mock_get_org_members.return_value = fake_org_members
    
#     mock_write.return_value = {
#         "status": 201,
#         "message": "success",
#         "data": {
#             "insert_count": 1,
#             "object_id": "c31a5f",
#             }
#         }
    
#     response = client.post(create_channel_url, json=test_payload_dm)
#     # assert response.status_code != 400
#     assert response.status_code != 201


# @pytest.mark.asyncio
# async def test_channel_url_is_invalid(
#     mock_get_admin_members, mock_write
#     ):
#     """
#     Create channel url is valid
    
#     Args:
#         mock_get_room (AsyncMock): Asynchronous external api call
#         mock_write (AsyncMock): Asynchronous external api call
#     """
#     mock_get_admin_members.return_value = fake_admin_member
#     mock_write.data = test_payload_channel
#     invalid_channel_url = "api/v1/org/klitm8/members/we54kl/rooms"
    
#     response = client.post(invalid_channel_url, json=test_payload_channel)
    
#     assert create_channel_url != invalid_channel_url
#     assert response.status_code == 422


# @pytest.mark.asyncio
# async def test_member_not_in_org(mock_get_org_members, mock_write):
#     """
#     Create DM unsuccessful when member is not in the organization
    
#     Args:
#         mock_get_org_members (AsyncMock): Asynchronous external api call
#     """
#     mock_get_org_members.return_value = fake_org_members
    
#     test_payload_dm["room_members"] = {
#         "bkbu87": {
#             "role": "member",
#             "starred": False,
#             "closed": False
#             }
#         }
    
#     mock_write.return_value = {
#         "status": 400,
#         "message": "error",
#         "data": {
#             "insert_count": 0,
#             "object_id": None,
#             }
#         }
     
#     response = client.post(create_dm_url, json=test_payload_dm)
#     assert response.status_code == 400
#     assert response.json() == {'detail': 'DM can only have 2 unique members'}#{"detail": "sender not a member of the organization"}
    

# @pytest.mark.asyncio
# async def test_dm_url_is_invalid(mock_get_org_members, mock_write):
#     """
#     Create DM with invalid url
    
#     Args:
#     mock_get_org_members (AsyncMock): Asynchronous external api call
#     mock_write (AsyncMock): Asynchronous external api call
    
#     """
#     mock_get_org_members.return_value = fake_org_members
#     mock_write.data = test_payload_dm
#     invalid_dm_url = "api/v1/org/fgyw35/members/yii93/rooms"
    
#     response = client.post(invalid_dm_url, json=test_payload_dm)
    
#     assert create_channel_url != invalid_dm_url
#     assert response.status_code == 400


import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

create_channel_url = "api/v1/org/619ba4/members/we54kl/rooms"
create_dm_url = "api/v1/org/619ba4/members/e21e10/rooms"


test_payload_channel = {
    "room_name": "test_channel",
    "room_type": "CHANNEL",
    "room_members": {
        "we54kl": {
        "role": "admin",
        "starred": False,
        "closed": False
        }
    },
    "created_at": "2022-01-09 11:23:11.361217",
    "description": "a test channel",
    "topic": "testing",
    "is_private": False,
    "is_archived": False
    }

test_payload_dm = {
    "room_name": "e21e10_dm",
    "room_type": "DM",
    "room_members": {
        "e21e10": {
        "role": "member",
        "starred": False,
        "closed": False
        }
    },
    "created_at": "2022-01-09 11:23:11.361210",
    "description": "personal message",
    "topic": "test_dm",
    "is_private": False,
    "is_archived": False
    }

test_payload_group_dm = {
  "room_name": "test group dm",
  "room_type": "GROUP_DM",
  "room_members": {
    "61696f5ac4133ddaa309dcfe": {
      "closed": False,
      "role": "admin",
      "starred": False
    },
    "6169704bc4133ddaa309dd07": {
      "closed": False,
      "role": "admin",
      "starred": False
    },
    "619ba4671a5f54782939d385": {
      "closed": False,
      "role": "admin",
      "starred": False
    },
    "619baa5c1a5f54782939d386": {
      "closed": False,
      "role": "member",
      "starred": False
    }
  },
  "is_private": False,
  "is_archived": False
}

fake_data_channel = {
    "_id": "c31a5f",
    "created_at": "2022-01-09 11:23:11.361217",
    "created_by": "we54kl",
    "description": "a test channel",
    "id": None,
    "is_archived": False,
    "is_private": False,
    "org_id": "619ba4",
    "room_members": {
        "we54kl": {
            "closed": False,
            "role": "admin",
            "starred": False
            },
    },
    "room_name": "test_channel",
    "room_type": "CHANNEL",
    "topic": "testing"
}

# fake_data_group_dm = 

fake_data_dm = {
    "_id": "39fy78",
    "created_at": "2022-01-09 11:23:11.361210",
    "created_by": "e21e10",
    "description": "personal message",
    "id": None,
    "is_archived": False,
    "is_private": False,
    "org_id": "619ba4",
    "room_members": {
        "e21e10": {"closed": False, "role": "member", "starred": False},
    },
    "room_name": "e21e10_dm",
    "room_type": "DM",
    "topic": "test_dm"
}

fake_org_members = {
    "e21e10": {
        "closed": False,
        "role": "member", 
        "starred": False
        },
    "we54kl": {
        "role": "admin",
        "starred": False,
        "closed": False
        }
    }

fake_admin_member = {
    "we54kl": {
        "role": "admin",
        "starred": False,
        "closed": False
        }
    }
  
# fake_admin = {
#     "we54kl": {
#         "role": "admin",
#         "starred": False,
#         "closed": False
#         }
#     }
# fake_admin_member = list(fake_admin)


# channel tests
# @pytest.mark.asyncio
# async def test_create_channel_successful(mock_get_admin_members, mock_write, mock_centrifugo):
#     """
#     Create channel successful
    
#     Args:
#         mock_get_admin_members (AsyncMock): Asynchronous external api call
#         mock_write (AsyncMock): Asynchronous external api call
#         mock_centrifugo (AsyncMock): Asynchronous external api call
#     """
#     mock_get_admin_members.return_value = fake_admin_member
    
#     success = {
#         "status": "success",
#         "message": "Room created",
#         "data": fake_data_channel
#         }
    
#     mock_write.return_value = {
#         "status": 201,
#         "message": "success",
#         "data": {
#             "insert_count": 1,
#             "object_id": "c31a5f"
#             }
#         }
#     mock_centrifugo.return_value = {
#         "status_code": 200
#         }
    
#     response = client.post(create_channel_url, json=test_payload_channel)
#     assert response.status_code == 201
#     # assert response.status_code == 422
#     assert response.json() == success
        
    
# @pytest.mark.asyncio
# async def test_member_not_admin(mock_get_admin_members, mock_write):
#     """
#     Create Channel unsuccessful when member is not admin
    
#     Args:
#         mock_get_admin_members (AsyncMock): Asynchronous external api call
#     """
#     mock_get_admin_members.return_value = fake_admin_member
    
#     test_payload_channel["room_members"] = {
#         "e21e10": {
#             "role": "member",
#             "starred": False,
#             "closed": False
#             }
#         }
    
#     # test_payload_channel["room_members"]["role"] != "admin"
    
#     # mock_write.return_value = {
#     #     "status": 401
#     #     # "message": "error",
#     #     # "data": {
#     #     #     "insert_count": 0,
#     #     #     "object_id": None,
#     #     #     }
#     #     }
    
#     mock_write.return_value = {
#         "status": 401,
#         "message": "error",
#         "data": {
#             "insert_count": 0,
#             "object_id": None,
#             }
#         }
     
#     response = client.post(create_channel_url, json=test_payload_channel)
#     # assert response.status_code == 401
#     # assert response.status_code == 422
#     assert mock_write.status_code == 401
#     assert response.json() == {"detail": "sender not authorized to create channel"}
    

# @pytest.mark.asyncio
# async def test_create_channel_failure(mock_get_admin_members, mock_write):
#     """
#     Create channel unsuccessful
    
#     Args:
#         mock_get_room (AsyncMock): Asynchronous external api call
#         mock_write (AsyncMock): Asynchronous external api call
#     """
#     mock_get_admin_members.return_value = fake_admin_member
    
#     mock_write.return_value = {
#         "status": 400,
#         "message": "error",
#         "data": {
#             "insert_count": 0,
#             "object_id": None,
#             }
#         }
    
#     response = client.post(create_channel_url, json=test_payload_channel)
#     # assert response.status_code == 400
#     # assert response.status_code == 422
#     assert mock_write.status_code == 400
#     assert response.json() == {
#         "detail": "Failed to create channel"
#         }


# @pytest.mark.asyncio
# async def test_failure_to_publish_new_channel_to_centrifugo(
#     mock_get_admin_members, mock_write, mock_centrifugo
#     ):
#     """
#     Create channel successful but failed to publish to centrifugo
    
#     Args:
#         mock_get_room (AsyncMock): Asynchronous external api call
#         mock_write (AsyncMock): Asynchronous external api call
#         mock_centrifugo (AsyncMock): Asynchronous external api call
#     """
#     mock_get_admin_members.return_value = fake_admin_member
    
#     mock_write.return_value = {
#         "status": 200,
#         "message": "success",
#         "data": {
#             "insert_count": 1,
#             "object_id": "c31a5f",
#             }
#         }
#     centrifugo_response = {"status_code": 424}
    
#     response = client.post(create_channel_url, json=test_payload_channel)
#     assert response.status_code == 200
    
#     mock_centrifugo.return_value = centrifugo_response
#     assert centrifugo_response.status_code == 424
#     assert mock_centrifugo.json() == {
#         "detail": "Failed to publish to centrifugo"
#     }


# @pytest.mark.asyncio
# async def test_create_channel_failure_to_get_admin_members(mock_get_admin_members):
#     """
#     Failure to retrieve admin member
    
#     Args:
#         mock_get_room (AsyncMock): Asynchronous external api call
#     """
#     mock_get_admin_members.return_value = None
    
#     response = client.post(create_channel_url, json=test_payload_channel)
#     # assert response.status_code == 424
#     assert response.status_code == 422
#     assert response.json() == {
#         "detail": {"Failed to retrieve admin members": mock_get_admin_members.return_value}
#         }
    

# # DM tests
# @pytest.mark.asyncio
# async def test_create_dm_successful(mock_get_org_members, mock_write, mock_centrifugo):
#     """
#     Create DM successful
    
#     Args:
#         mock_get_org_members (AsyncMock): Asynchronous external api call
#         mock_write (AsyncMock): Asynchronous external api call
#         mock_centrifugo (AsyncMock): Asynchronous external api call
#     """
#     mock_get_org_members.return_value = fake_org_members
    
#     mock_write.return_value = {
#         "status": 200,
#         "message": "success",
#         "data": {
#             "insert_count": 1,
#             "object_id": "39fy78",
#             }
#         }
#     mock_centrifugo.return_value = {
#         "status_code": 200
#         }
    
#     response = client.post(create_dm_url, json=test_payload_dm)
#     # assert response.status_code == 200
#     # assert response.status_code == 400
#     assert mock_write.status_code == 200
#     assert response.json() == {
#         "status": "success",
#         "message": "Room created",
#         "data": {
#             "room_name": "e21e10_dm",
#             "room_type": "DM",
#             "room_members": {
#                 "e21e10": {
#                 "role": "member",
#                 "starred": False,
#                 "closed": False
#                 }
#             },
#             "created_at": "2022-01-09 11:23:11.361210",
#             "description": "personal message",
#             "topic": "test_dm",
#             "is_private": False,
#             "is_archived": False,
#             "id": "39fy78",
#             "org_id": "619ba4",
#             "created_by": "e21e10"
#             }
#         }


# @pytest.mark.asyncio
# async def test_create_dm_failure(mock_get_org_members, mock_write):
#     """
#     Create DM unsuccessful
    
#     Args:
#         mock_get_org_members (AsyncMock): Asynchronous external api call
#         mock_write (AsyncMock): Asynchronous external api call
#     """
#     mock_get_org_members.return_value = fake_org_members
    
#     mock_write.return_value = {
#         "status": 400,
#         "message": "error",
#         "data": {
#             "insert_count": 0,
#             "object_id": None,
#         }
#     }
    
#     response = client.post(create_dm_url, json=test_payload_dm)
#     assert mock_write.status_code == 400
#     assert response.json() == {
#         "detail": {"Failed to create DM": mock_write.return_value}
        
#         #  "detail': 'DM can only have 2 unique members"
#     }
    
    
# @pytest.mark.asyncio
# async def test_failure_to_publish_new_dm_to_centrifugo(
#     mock_get_org_members, mock_write, mock_centrifugo
#     ):
#     """
#     Create DM successful but failed to publish to centrifugo
    
#     Args:
#         mock_get_org_members (AsyncMock): Asynchronous external api call
#         mock_write (AsyncMock): Asynchronous external api call
#         mock_centrifugo (AsyncMock): Asynchronous external api call
#     """
#     mock_get_org_members.return_value = fake_org_members
    
#     mock_write.return_value = {
#         "status": 200,
#         "message": "success",
#         "data": {
#             "insert_count": 1,
#             "object_id": "39fy78",
#             }
#         }
#     centrifugo_response = {"status_code": 424}
    
#     response = client.post(create_channel_url, json=test_payload_channel)
#     # assert response.status_code == 200
#     # assert response.status_code == 422
#     assert mock_write.status_code == 200
#     assert response.json() == {
#         "status": "success",
#         "message": "Room created",
#         "data": {
#             "room_name": "e21e10_dm",
#             "room_type": "DM",
#             "room_members": {
#                 "e21e10": {
#                 "role": "member",
#                 "starred": False,
#                 "closed": False
#                 }
#             },
#             "created_at": "2022-01-09 11:23:11.361210",
#             "description": "personal message",
#             "topic": "test_dm",
#             "is_private": False,
#             "is_archived": False,
#             "id": "39fy78",
#             "org_id": "619ba4",
#             "created_by": "e21e10"
#             }
#         }
    
#     mock_centrifugo.return_value = centrifugo_response
#     assert mock_centrifugo.status_code == 424
#     assert mock_centrifugo.json() == {
#         "detail": {"Failed to publish to centrifugo": centrifugo_response}
#     }


# @pytest.mark.asyncio
# async def test_duplicate_dm_name(mock_get_org_members, mock_write):
#     """
#     Create DM unsuccessful when name already exists
    
#     Args:
#         mock_get_org_members (AsyncMock): Asynchronous external api call
#         mock_write (AsyncMock): Asynchronous external api call
#     """
#     mock_get_org_members.return_value = fake_org_members
    
#     test_payload_dm["room_name"] = "e21e10_dm"
    
#     mock_write.return_value = {
#         "status": 400,
#         "message": "error",
#         "data": {
#             "insert_count": 0,
#             "object_id": None,
#             }
#         }
    
#     response = client.post(create_dm_url, json=test_payload_dm)
#     assert response.status_code == 400
#     assert response.json() == {"detail": "DM name already exists"}
    
 
# @pytest.mark.asyncio
# async def test_duplicate_channel_name(mock_get_org_members, mock_write):
#      """
#      Create channel unsuccessful when name already exists
     
#      Args:
#          mock_get_org_members (AsyncMock): Asynchronous external api call
#          mock_write (AsyncMock): Asynchronous external api call
#      """
#      mock_get_org_members.return_value = fake_org_members
     
#      test_payload_channel["room_name"] = "test_channel"
     
#      mock_write.return_value = {
#          "status": 400,
#          "message": "error",
#          "data": {
#              "insert_count": 0,
#              "object_id": None,
#              }
#          }
     
#      response = client.post(create_channel_url, json=test_payload_channel)
#      assert response.status_code == 400
#      assert response.json() == {"detail": "Channel name already exists"}   
    

# @pytest.mark.asyncio
# async def test_create_dm_with_invalid_members(mock_get_org_members, mock_write):
#     """
#     Create DM with invalid members
    
#     Args:
#         mock_get_org_members (AsyncMock): Asynchronous external api call
#         mock_write (AsyncMock): Asynchronous external api call
#     """
#     mock_get_org_members.return_value = fake_org_members
        
#     test_payload_dm["room_members"] = {
#         "e21e10": {
#             "role": "member",
#             "starred": False,
#             "closed": False
#             },
#         "bkbu87": {
#             "role": "member",
#             "starred": False,
#             "closed": False
#             }
#         }
    
#     mock_write.return_value = {
#         "status": 400,
#         "message": "error",
#         "data": {
#             "insert_count": 0,
#             "object_id": None,
#         }
#     }
    
#     response = client.post(create_dm_url, json=test_payload_dm)
#     # assert response.status_code == 400
#     assert response.status_code == 422
#     assert response.json() == {
#         # "detail": {"Failed to create DM": mock_write.json()}
#         "detail": "Invalid members"
#     }



# @pytest.mark.asyncio
# async def test_create_dm_check_status_code(mock_get_org_members, mock_write):
#     """
#     Create DM unsuccessful when writing to zc core return a response with status_code.
#     Args:
#         mock_get_org_members (AsyncMock): Asynchronous external api call
#         mock_write (AsyncMock): Asynchronous external api call
#     """

#     write_response = {"status_code": 422, "message": "unprocessible error"}
#     mock_get_org_members.return_value = fake_org_members
#     mock_write.return_value = write_response
#     response = client.post(create_dm_url, json=test_payload_dm)
#     assert response.status_code == 424
#     assert response.json() == {"detail": {"Room not created": write_response}}


# @pytest.mark.asyncio
# async def test_channel_name_is_correct(mock_write):
#     """
#     Create channel with incorrect name
    
#     Args:
#         mock_write (AsyncMock): Asynchronous external api call
#     """
#     test_payload_channel["room_name"] = "test_channel"
    
#     mock_write.return_value = {
#         "status": 200,
#         "message": "success",
#         "data": {
#             "insert_count": 1,
#             "object_id": "39fy78",
#         }
#     }
#     response = client.post(create_channel_url, json=test_payload_channel)
#     # assert response.status_code == 200
#     # assert response.json() == {
#     #     "status": "success",
#     #     "message": "Room created",
#     #     "data": fake_data_channel
#     #     }
#     # assert response.json()["data"]["room_name"] == "test_channel"
#     assert response.json() == {
#         "status": "success",
#         "message": "Room created",
#         "data": {
#             "_id": "c31a5f",
#             "created_at": "2022-01-09 11:23:11.361217",
#             "created_by": "we54kl",
#             "description": "a test channel",
#             "id": None,
#             "is_archived": False,
#             "is_private": False,
#             "org_id": "619ba4",
#             "room_members": {
#                 "we54kl": {
#                     "closed": False,
#                     "role": "admin",
#                     "starred": False
#                     },
#             },
#             "room_name": "test_channel",
#             "room_type": "CHANNEL",
#             "topic": "testing"
#             }
#         }          

    
    
    
    
# @pytest.mark.asyncio
# async def test_channel_success_status_code(
#     mock_get_admin_members, mock_write
#     ):
#     """
#     Create channel successful status code
    
#     Args:
#         mock_get_room (AsyncMock): Asynchronous external api call
#         mock_write (AsyncMock): Asynchronous external api call
#     """
#     mock_get_admin_members.return_value = fake_admin_member
    
#     mock_write.return_value = {
#         "status": 201,
#         "message": "success",
#         "data": {
#             "insert_count": 1,
#             "object_id": "c31a5f",
#             }
#         }
    
#     response = client.post(create_channel_url, json=test_payload_channel)
#     assert response.status_code != 400
#     # assert response.status_code == 201


# @pytest.mark.asyncio
# async def test_dm_success_status_code(
#     mock_get_org_members, mock_write
#     ):
#     """
#     Create channel successful status code
    
#     Args:
#         mock_get_room (AsyncMock): Asynchronous external api call
#         mock_write (AsyncMock): Asynchronous external api call
#     """
#     mock_get_org_members.return_value = fake_org_members
    
#     mock_write.return_value = {
#         "status": 201,
#         "message": "success",
#         "data": {
#             "insert_count": 1,
#             "object_id": "c31a5f",
#             }
#         }
    
#     response = client.post(create_channel_url, json=test_payload_dm)
#     # assert response.status_code != 400
#     assert response.status_code != 201


# @pytest.mark.asyncio
# async def test_channel_url_is_invalid(
#     mock_get_admin_members, mock_write
#     ):
#     """
#     Create channel url is valid
    
#     Args:
#         mock_get_room (AsyncMock): Asynchronous external api call
#         mock_write (AsyncMock): Asynchronous external api call
#     """
#     mock_get_admin_members.return_value = fake_admin_member
#     mock_write.data = test_payload_channel
#     invalid_channel_url = "api/v1/org/klitm8/members/we54kl/rooms"
    
#     response = client.post(invalid_channel_url, json=test_payload_channel)
    
#     assert create_channel_url != invalid_channel_url
#     assert response.status_code == 422


# @pytest.mark.asyncio
# async def test_member_not_in_org(mock_get_org_members, mock_write):
#     """
#     Create DM unsuccessful when member is not in the organization
    
#     Args:
#         mock_get_org_members (AsyncMock): Asynchronous external api call
#     """
#     mock_get_org_members.return_value = fake_org_members
    
#     test_payload_dm["room_members"] = {
#         "bkbu87": {
#             "role": "member",
#             "starred": False,
#             "closed": False
#             }
#         }
    
#     mock_write.return_value = {
#         "status": 400,
#         "message": "error",
#         "data": {
#             "insert_count": 0,
#             "object_id": None,
#             }
#         }
     
#     response = client.post(create_dm_url, json=test_payload_dm)
#     assert response.status_code == 400
#     assert response.json() == {'detail': 'DM can only have 2 unique members'}#{"detail": "sender not a member of the organization"}
    

# @pytest.mark.asyncio
# async def test_dm_url_is_invalid(mock_get_org_members, mock_write):
#     """
#     Create DM with invalid url
    
#     Args:
#     mock_get_org_members (AsyncMock): Asynchronous external api call
#     mock_write (AsyncMock): Asynchronous external api call
    
#     """
#     mock_get_org_members.return_value = fake_org_members
#     mock_write.data = test_payload_dm
#     invalid_dm_url = "api/v1/org/fgyw35/members/yii93/rooms"
    
#     response = client.post(invalid_dm_url, json=test_payload_dm)
    
#     assert create_channel_url != invalid_dm_url
#     assert response.status_code == 400


# fake_room_members_url = "api/v1/org/619ba4671a5f54782939d384/rooms/619e28c31a5f54782939d59a/members"

# fake_room_data = {
#     '_id': '619e28c31a5f54782939d59a', 
#     'created_at': '2021-11-24 11:23:11.361210', 
#     'created_by': '61696f5ac4133ddaa309dcfe', 
#     'description': 'Section for general information', 
#     'id': None, 
#     'is_archived': False, 
#     'is_private': False, 
#     'org_id': '619ba4671a5f54782939d384', 
#     "room_members": {
#         '61696f5ac4133ddaa309dcfe': {
#             'closed': False,
#             'role': 'admin',
#             'starred': False
#             }, 
#         '6169704bc4133ddaa309dd07': {
#             'closed': False,
#             'role': 'admin',
#             'starred': False
#             }, 
#         '619ba4671a5f54782939d385': {
#             'closed': False, 
#             'role': 'admin', 
#             'starred': False
#             }, 
#         '619baa5c1a5f54782939d386': {
#             'closed': False, 
#             'role': 'member', 
#             'starred': False
#             }
#         }, 
#     'room_name': 'random',
#     'room_type': 'CHANNEL',
#     'topic': 'Information'
#     }

# fake_room_members = {
#     '61696f5ac4133ddaa309dcfe': {
#         'closed': False,
#         'role': 'admin',
#         'starred': False
#         }, 
#     '6169704bc4133ddaa309dd07': {
#         'closed': False, 
#         'role': 'admin', 
#         'starred': False
#         }, 
#     '619ba4671a5f54782939d385': {
#         'closed': False, 
#         'role': 'admin',
#         'starred': False
#         }, 
#     '619baa5c1a5f54782939d386': {
#         'closed': False,
#         'role': 'member',
#         'starred': False
#         }
#     }

# fake_member_filter =  {
#     '619baa5c1a5f54782939d386': {
#         'closed': False,
#         'role': 'member',
#         'starred': False
#         }
#     }

# success = {
#     "status": "success",
#     "message": "Room members retrieved successfully",
#     "data": {
#     '61696f5ac4133ddaa309dcfe': {
#         'closed': False,
#         'role': 'admin',
#         'starred': False
#         }, 
#     '6169704bc4133ddaa309dd07': {
#         'closed': False, 
#         'role': 'admin', 
#         'starred': False
#         }, 
#     '619ba4671a5f54782939d385': {
#         'closed': False, 
#         'role': 'admin',
#         'starred': False
#         }, 
#     '619baa5c1a5f54782939d386': {
#         'closed': False,
#         'role': 'member',
#         'starred': False
#         }
#     }
# }

# @pytest.mark.asyncio
# async def test_get_room_members_sucessful(mock_get_user_room, mock_read):
#     """Get room members successful
    
#     Args:
#         mock_get_room (AsyncMock): Asynchronous external api call
#         mock_read (AsyncMock): Asynchronous external api call
#     """
#     mock_get_user_room.return_value = fake_room_data
#     fake_room_members = fake_room_data["room_members"]
    
#     mock_read.return_value = {
#         'status': 'success',
#         'message': 'Room members retrieved successfully',
#         'data': fake_room_members
#     }
    
#     response = await client.get(fake_room_members_url)
#     assert response.status_code == 200
#     assert response.json() == success
    



