from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)


create_room_url = "api/v1/org/6619ba4671a5f54782939d384/members/619ba4671a5f54782939d385/rooms"

test_payload_channel = {
    "room_name": "testing_with_pauline",
    "room_type": "CHANNEL",
    "description": "testing",
    "topic": "testing",
    "room_members": {
        "619ba4671a5f54782939d385": {
        "role": "member",
        "starred": False,
        "closed": False
        }
    },
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
  "is_private": True,
  "is_archived": False
}

test_payload_dm = {
  "room_name": "test dm",
  "room_type": "DM",
  "room_members": {
    "61696f5ac4133ddaa309dcfe": {
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
  "is_private": True,
  "is_archived": False
}

fake_data_channel = {
        "room_name": "testing_with_pauline",
        "room_type": "CHANNEL",
        "room_members": {
        "619ba4671a5f54782939d385": {
            "role": "member",
            "starred": False,
            "closed": False
        }
        },
        "created_at": "2022-01-10 19:33:13.315281",
        "description": "testing",
        "topic": "testing",
        "is_private": False,
        "is_archived": False,
        "id": "61dc8b9eeba8adb50ca13a10",
        "org_id": "619ba4671a5f54782939d384",
        "created_by": "619ba4671a5f54782939d385"
        }

fake_data_dm = {
    "room_name": "test dm",
    "room_type": "DM",
    "room_members": {
      "61696f5ac4133ddaa309dcfe": {
        "role": "admin",
        "starred": False,
        "closed": False
      },
      "619ba4671a5f54782939d385": {
        "role": "member",
        "starred": False,
        "closed": False
      }
    },
    "created_at": "2022-01-11 03:33:03.746259",
    "description": None,
    "topic": None,
    "is_private": True,
    "is_archived": False,
    "id": "61dcfb65eba8adb50ca13a25",
    "org_id": "619ba4671a5f54782939d384",
    "created_by": "619ba4671a5f54782939d385"
  }

fake_data_group_dm = {
    "room_name": "test group dm",
    "room_type": "GROUP_DM",
    "room_members": {
      "61696f5ac4133ddaa309dcfe": {
        "role": "admin",
        "starred": False,
        "closed": False
      },
      "6169704bc4133ddaa309dd07": {
        "role": "admin",
        "starred": False,
        "closed": False
      },
      "619ba4671a5f54782939d385": {
        "role": "admin",
        "starred": False,
        "closed": False
      },
      "619baa5c1a5f54782939d386": {
        "role": "member",
        "starred": False,
        "closed": False
      }
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
}

fake_org_rooms = [
    {
        '_id': '61dc9051eba8adb50ca13a19', 
        'created_at': '2022-01-10 19:59:59.852748', 
        'created_by': '619ba4671a5f54782939d385', 
        'description': None, 
        'id': None, 
        'is_archived': False, 
        'is_private': False, 
        'org_id': '619ba4671a5f54782939d384', 
        'room_members': 
            {
                '619ba4671a5f54782939d385': 
                    {
                        'closed': False, 
                        'role': 'member', 
                        'starred': False
                    }
            }, 
        'room_name': 'channel test', 
        'room_type': 'CHANNEL', 
        'topic': None
    }, 
    {
        '_id': '619e2ebe1a5f54782939d59d',
        'created_at': '2021-11-24 11:23:11.361210',
        'created_by': '61696f5ac4133ddaa309dcfe',
        'description': None, 
        'id': None, 
        'is_archived': False,
        'is_private': True,
        'org_id': '619ba4671a5f54782939d384',
        'room_members': {
            '61696f5ac4133ddaa309dcfe': {
                'closed': False, 
                'role': 'admin', 
                'starred': False
                }, 
            '6169704bc4133ddaa309dd07': {
                'closed': False, 
                'role': 'admin', 
                'starred': False
                }
            }, 
        'room_name': None, 
        'room_type': 'DM', 
        'topic': None
    }
]

fake_all_members = [
    {
        "_id":"619bae071a5f54782939d58b",
        "bio":"",
        "deleted":False,
        "deleted_at":"0001-01-01T00:53:28+00:53",
        "display_name":"",
        "email":"mosesjoshua350@gmail.com",
        "files":"None",
        "first_name":"",
        "image_url":"",
        "joined_at":"2021-11-22T15:49:43.137+01:00",
        "language":"",
        "last_name":"",
        "org_id":"619ba4671a5f54782939d384",
        "phone":"",
        "presence":"true",
        "pronouns":"",
        "role":"member",
        "settings":{
            "accessibility":{
                "animation":False,
                "direct_message_announcement":{
                    "read_message":False,
                    "receive_sound":False,
                    "send_sound":False
                },
                "links":False,
                "press_empty_message_field":""
            },
            "advanced":{
                "excluded_channels":"None",
                "input_option":{
                    "dont_send_with_enter":False,
                    "format_messages":False
                },
                "other_option":{
                    "key_scroll_messages":False,
                    "send_survey":False,
                    "toggle_away_status":False,
                    "warn_against_files":False,
                    "warn_against_links":False
                },
                "press_enter_to":"",
                "search_option":{
                    "start_quick_switcher":False,
                    "start_slack_search":False
                }
            },
            "audio_and_video":{
                "enable_automatic_gain_control":False,
                "integrated_webcam":"",
                "microphone":"",
                "speaker":"",
                "when_joining_a_huddle":"None",
                "when_joining_a_zuri_chat_call":"None",
                "when_slack_is_in_the_background":"None"
            },
            "chat_settings":{
                "enter_is_send":False,
                "font_size":"",
                "media_visibility":False,
                "theme":"",
                "wallpaper":""
            },
            "languages_and_regions":{
                "language":"",
                "languages_zuri_should_spell_check":"None",
                "set_time_zone_automatically":False,
                "spell_check":False,
                "time_zone":""
            },
            "messages_and_media":{
                "additional_options":{
                    "clock":False,
                    "color_swatches":False,
                    "currently_typing":False
                },
                "bring_emails_into_zuri":"",
                "convert_emoticons_to_emoji":False,
                "custom":False,
                "emoji":"",
                "emoji_as_text":False,
                "frequently_used_emoji":False,
                "inline_media_and_links":{
                    "larger_than_2_mb":False,
                    "show_images_and_files_from_linked_websites":False,
                    "show_images_and_files_uploaded_to_zurichat":False,
                    "show_text_previews_of_linked_websites":False
                },
                "messages_one_click_reaction":"None",
                "names":"",
                "show_jumbomoji":False,
                "theme":""
            },
            "notifications":{
                "channel_hurdle_notification":False,
                "custom_notification_schedule":"None",
                "message_preview_in_each_notification":False,
                "mute_all_sounds":False,
                "notification_schedule":{
                    "day":"",
                    "from":"",
                    "to":""
                },
                "set_lounge_notifications_right":"",
                "set_message_notifications_right":""
            },
            "plugin_settings":"None",
            "sidebar":{
                "always_show_in_the_sidebar":"None",
                "list_private_channels_separately":False,
                "organize_external_conversations":False,
                "show_all_the_following":"",
                "show_conversations":"",
                "show_profile_picture_next_to_dm":False,
                "sidebar_sort":""
            },
            "themes":{
                "colors":"",
                "mode":""
            }
        },
        "socials":"None",
        "status":{
            "expiry_time":"",
            "status_history":"None",
            "tag":"",
            "text":""
        },
        "time_zone":"",
        "user_name":"mosesjoshua350"
    },
    
    {
        "_id":"61d9d9b35a3812d0a9d0b3fa",
        "bio":"",
        "deleted":False,
        "deleted_at":"0001-01-01T00:00:00Z",
        "display_name":"",
        "email":"aduragbemiife@gmail.com",
        "files":"None",
        "first_name":"",
        "image_url":"",
        "joined_at":"2022-01-08T19:36:35.684944659+01:00",
        "language":"",
        "last_name":"",
        "org_id":"619ba4671a5f54782939d384",
        "phone":"",
        "presence":"true",
        "pronouns":"",
        "role":"member",
        "settings":{
            "accessibility":{
                "animation":False,
                "direct_message_announcement":{
                    "read_message":False,
                    "receive_sound":False,
                    "send_sound":False
                },
                "links":False,
                "press_empty_message_field":""
            },
            "advanced":{
                "excluded_channels":"None",
                "input_option":{
                    "dont_send_with_enter":False,
                    "format_messages":False
                },
                "other_option":{
                    "key_scroll_messages":False,
                    "send_survey":False,
                    "toggle_away_status":False,
                    "warn_against_files":False,
                    "warn_against_links":False
                },
                "press_enter_to":"",
                "search_option":{
                    "start_quick_switcher":False,
                    "start_slack_search":False
                }
            },
            "audio_and_video":{
                "enable_automatic_gain_control":False,
                "integrated_webcam":"",
                "microphone":"",
                "speaker":"",
                "when_joining_a_huddle":"None",
                "when_joining_a_zuri_chat_call":"None",
                "when_slack_is_in_the_background":"None"
            },
            "chat_settings":{
                "enter_is_send":False,
                "font_size":"",
                "media_visibility":False,
                "theme":"",
                "wallpaper":""
            },
            "languages_and_regions":{
                "language":"",
                "languages_zuri_should_spell_check":"None",
                "set_time_zone_automatically":False,
                "spell_check":False,
                "time_zone":""
            },
            "messages_and_media":{
                "additional_options":{
                    "clock":False,
                    "color_swatches":False,
                    "currently_typing":False
                },
                "bring_emails_into_zuri":"",
                "convert_emoticons_to_emoji":False,
                "custom":False,
                "emoji":"",
                "emoji_as_text":False,
                "frequently_used_emoji":False,
                "inline_media_and_links":{
                    "larger_than_2_mb":False,
                    "show_images_and_files_from_linked_websites":False,
                    "show_images_and_files_uploaded_to_zurichat":False,
                    "show_text_previews_of_linked_websites":False
                },
                "messages_one_click_reaction":"None",
                "names":"",
                "show_jumbomoji":False,
                "theme":""
            },
            "notifications":{
                "channel_hurdle_notification":False,
                "custom_notification_schedule":"None",
                "message_preview_in_each_notification":False,
                "mute_all_sounds":False,
                "notification_schedule":{
                    "day":"",
                    "from":"",
                    "to":""
                },
                "set_lounge_notifications_right":"",
                "set_message_notifications_right":""
            },
            "plugin_settings":"None",
            "sidebar":{
                "always_show_in_the_sidebar":"None",
                "list_private_channels_separately":False,
                "organize_external_conversations":False,
                "show_all_the_following":"",
                "show_conversations":"",
                "show_profile_picture_next_to_dm":False,
                "sidebar_sort":""
            },
            "themes":{
                "colors":"",
                "mode":""
            }
        },
        "socials":"None",
        "status":{
            "expiry_time":"",
            "status_history":"None",
            "tag":"",
            "text":""
        },
        "time_zone":"",
        "user_name":"aduragbemiife"
    }
]




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



@pytest.mark.asyncio
async def test_channel_success_status_code(
    mock_get_all_members, mock_get_org_rooms, mock_write
    ):
    """
    Create channel successful status code
    
    Args:
        mock_get_room (AsyncMock): Asynchronous external api call
        mock_write (AsyncMock): Asynchronous external api call
    """
    
    mock_get_org_rooms.return_value = fake_org_rooms
    mock_get_all_members.return_value = fake_all_members
    
    
    mock_write.return_value = {
        "status": 201,
        "message": "success",
        "data": {
            "insert_count": 1,
            "object_id": "61dc8b9eeba8adb50ca13a10",
            }
        }
    
    response = client.post(create_room_url, json=test_payload_channel)
    assert response.status_code == 201
    assert response.json() == {
        "status": "success",
        "message": "room created",
        "data": fake_data_channel
    # "data": {
    #     "room_name": "testing_with_pauline",
    #     "room_type": "CHANNEL",
    #     "room_members": {
    #     "619ba4671a5f54782939d385": {
    #         "role": "member",
    #         "starred": False,
    #         "closed": False
    #     }
    #     },
    #     "created_at": "2022-01-10 19:33:13.315281",
    #     "description": "testing",
    #     "topic": "testing",
    #     "is_private": False,
    #     "is_archived": False,
    #     "id": "61dc8b9eeba8adb50ca13a10",
    #     "org_id": "619ba4671a5f54782939d384",
    #     "created_by": "619ba4671a5f54782939d385"
    #     }
    }


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