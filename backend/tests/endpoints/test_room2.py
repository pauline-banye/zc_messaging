from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)


create_room_url = "api/v1/org/6619ba4671a5f54782939d384/members/619ba4671a5f54782939d385/rooms"
get_room_members_url = "api/v1/org/619ba4671a5f54782939d384/rooms/61dcf855eba8adb50ca13a24/members"
join_room_test_url = "api/v1/org/619org/rooms/619Chrm1/members/619mem1"


test_join_room_payload = {"619mem3": {"role": "member", "starred": False, "closed": False}}

fake_core_room_data = {
    "_id": "619Chrm1",
    "is_private": False,
    "room_members": {
        "619mem1": {"closed": False, "role": "admin", "starred": False},
        "619mem2": {"closed": False, "role": "member", "starred": False},
    },
    "room_type": "CHANNEL",
}



test_create_channel_payload = {
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

# payload_group_dm = {
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
#   "is_private": True,
#   "is_archived": False
# }

# payload_dm = {
#   "room_name": "test dm",
#   "room_type": "DM",
#   "room_members": {
#     "61696f5ac4133ddaa309dcfe": {
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
#   "is_private": True,
#   "is_archived": False
# }


# fake_data_channel = {
#         "room_name": "testing_with_pauline",
#         "room_type": "CHANNEL",
#         "room_members": {
#         "619ba4671a5f54782939d385": {
#             "role": "member",
#             "starred": False,
#             "closed": False
#             }
#         },
#         "created_at": "2022-01-10 19:33:13.315281",
#         "description": "testing",
#         "topic": "testing",
#         "is_private": False,
#         "is_archived": False,
#         "id": "61dc8b9eeba8adb50ca13a10",
#         "org_id": "619ba4671a5f54782939d384",
#         "created_by": "619ba4671a5f54782939d385"
#         }

# fake_data_dm = {
#     "room_name": "test dm",
#     "room_type": "DM",
#     "room_members": {
#       "61696f5ac4133ddaa309dcfe": {
#         "role": "admin",
#         "starred": False,
#         "closed": False
#       },
#       "619ba4671a5f54782939d385": {
#         "role": "member",
#         "starred": False,
#         "closed": False
#       }
#     },
#     "created_at": "2022-01-11 03:33:03.746259",
#     "description": None,
#     "topic": None,
#     "is_private": True,
#     "is_archived": False,
#     "id": "61dcfb65eba8adb50ca13a25",
#     "org_id": "619ba4671a5f54782939d384",
#     "created_by": "619ba4671a5f54782939d385"
#   }

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

# fake_org_members = {
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
# }

# fake_org_rooms = [
#     {
#         '_id': '61dc9051eba8adb50ca13a19', 
#         'created_at': '2022-01-10 19:59:59.852748', 
#         'created_by': '619ba4671a5f54782939d385', 
#         'description': None, 
#         'id': None, 
#         'is_archived': False, 
#         'is_private': False, 
#         'org_id': '619ba4671a5f54782939d384', 
#         'room_members': 
#             {
#                 '619ba4671a5f54782939d385': 
#                     {
#                         'closed': False, 
#                         'role': 'member', 
#                         'starred': False
#                     }
#             }, 
#         'room_name': 'channel test', 
#         'room_type': 'CHANNEL', 
#         'topic': None
#     }, 
#     {
#         '_id': '619e2ebe1a5f54782939d59d',
#         'created_at': '2021-11-24 11:23:11.361210',
#         'created_by': '61696f5ac4133ddaa309dcfe',
#         'description': None, 
#         'id': None, 
#         'is_archived': False,
#         'is_private': True,
#         'org_id': '619ba4671a5f54782939d384',
#         'room_members': {
#             '61696f5ac4133ddaa309dcfe': {
#                 'closed': False, 
#                 'role': 'admin', 
#                 'starred': False
#                 }, 
#             '6169704bc4133ddaa309dd07': {
#                 'closed': False, 
#                 'role': 'admin', 
#                 'starred': False
#                 }
#             }, 
#         'room_name': None, 
#         'room_type': 'DM', 
#         'topic': None
#     }
# ]

# fake_all_members = [
#     {
#         "_id":"619bae071a5f54782939d58b",
#         "bio":"",
#         "deleted":False,
#         "deleted_at":"0001-01-01T00:53:28+00:53",
#         "display_name":"",
#         "email":"mosesjoshua350@gmail.com",
#         "files":"None",
#         "first_name":"",
#         "image_url":"",
#         "joined_at":"2021-11-22T15:49:43.137+01:00",
#         "language":"",
#         "last_name":"",
#         "org_id":"619ba4671a5f54782939d384",
#         "phone":"",
#         "presence":"true",
#         "pronouns":"",
#         "role":"member",
#         "settings":{
#             "accessibility":{
#                 "animation":False,
#                 "direct_message_announcement":{
#                     "read_message":False,
#                     "receive_sound":False,
#                     "send_sound":False
#                 },
#                 "links":False,
#                 "press_empty_message_field":""
#             },
#             "advanced":{
#                 "excluded_channels":"None",
#                 "input_option":{
#                     "dont_send_with_enter":False,
#                     "format_messages":False
#                 },
#                 "other_option":{
#                     "key_scroll_messages":False,
#                     "send_survey":False,
#                     "toggle_away_status":False,
#                     "warn_against_files":False,
#                     "warn_against_links":False
#                 },
#                 "press_enter_to":"",
#                 "search_option":{
#                     "start_quick_switcher":False,
#                     "start_slack_search":False
#                 }
#             },
#             "audio_and_video":{
#                 "enable_automatic_gain_control":False,
#                 "integrated_webcam":"",
#                 "microphone":"",
#                 "speaker":"",
#                 "when_joining_a_huddle":"None",
#                 "when_joining_a_zuri_chat_call":"None",
#                 "when_slack_is_in_the_background":"None"
#             },
#             "chat_settings":{
#                 "enter_is_send":False,
#                 "font_size":"",
#                 "media_visibility":False,
#                 "theme":"",
#                 "wallpaper":""
#             },
#             "languages_and_regions":{
#                 "language":"",
#                 "languages_zuri_should_spell_check":"None",
#                 "set_time_zone_automatically":False,
#                 "spell_check":False,
#                 "time_zone":""
#             },
#             "messages_and_media":{
#                 "additional_options":{
#                     "clock":False,
#                     "color_swatches":False,
#                     "currently_typing":False
#                 },
#                 "bring_emails_into_zuri":"",
#                 "convert_emoticons_to_emoji":False,
#                 "custom":False,
#                 "emoji":"",
#                 "emoji_as_text":False,
#                 "frequently_used_emoji":False,
#                 "inline_media_and_links":{
#                     "larger_than_2_mb":False,
#                     "show_images_and_files_from_linked_websites":False,
#                     "show_images_and_files_uploaded_to_zurichat":False,
#                     "show_text_previews_of_linked_websites":False
#                 },
#                 "messages_one_click_reaction":"None",
#                 "names":"",
#                 "show_jumbomoji":False,
#                 "theme":""
#             },
#             "notifications":{
#                 "channel_hurdle_notification":False,
#                 "custom_notification_schedule":"None",
#                 "message_preview_in_each_notification":False,
#                 "mute_all_sounds":False,
#                 "notification_schedule":{
#                     "day":"",
#                     "from":"",
#                     "to":""
#                 },
#                 "set_lounge_notifications_right":"",
#                 "set_message_notifications_right":""
#             },
#             "plugin_settings":"None",
#             "sidebar":{
#                 "always_show_in_the_sidebar":"None",
#                 "list_private_channels_separately":False,
#                 "organize_external_conversations":False,
#                 "show_all_the_following":"",
#                 "show_conversations":"",
#                 "show_profile_picture_next_to_dm":False,
#                 "sidebar_sort":""
#             },
#             "themes":{
#                 "colors":"",
#                 "mode":""
#             }
#         },
#         "socials":"None",
#         "status":{
#             "expiry_time":"",
#             "status_history":"None",
#             "tag":"",
#             "text":""
#         },
#         "time_zone":"",
#         "user_name":"mosesjoshua350"
#     },
    
#     {
#         "_id":"61d9d9b35a3812d0a9d0b3fa",
#         "bio":"",
#         "deleted":False,
#         "deleted_at":"0001-01-01T00:00:00Z",
#         "display_name":"",
#         "email":"aduragbemiife@gmail.com",
#         "files":"None",
#         "first_name":"",
#         "image_url":"",
#         "joined_at":"2022-01-08T19:36:35.684944659+01:00",
#         "language":"",
#         "last_name":"",
#         "org_id":"619ba4671a5f54782939d384",
#         "phone":"",
#         "presence":"true",
#         "pronouns":"",
#         "role":"member",
#         "settings":{
#             "accessibility":{
#                 "animation":False,
#                 "direct_message_announcement":{
#                     "read_message":False,
#                     "receive_sound":False,
#                     "send_sound":False
#                 },
#                 "links":False,
#                 "press_empty_message_field":""
#             },
#             "advanced":{
#                 "excluded_channels":"None",
#                 "input_option":{
#                     "dont_send_with_enter":False,
#                     "format_messages":False
#                 },
#                 "other_option":{
#                     "key_scroll_messages":False,
#                     "send_survey":False,
#                     "toggle_away_status":False,
#                     "warn_against_files":False,
#                     "warn_against_links":False
#                 },
#                 "press_enter_to":"",
#                 "search_option":{
#                     "start_quick_switcher":False,
#                     "start_slack_search":False
#                 }
#             },
#             "audio_and_video":{
#                 "enable_automatic_gain_control":False,
#                 "integrated_webcam":"",
#                 "microphone":"",
#                 "speaker":"",
#                 "when_joining_a_huddle":"None",
#                 "when_joining_a_zuri_chat_call":"None",
#                 "when_slack_is_in_the_background":"None"
#             },
#             "chat_settings":{
#                 "enter_is_send":False,
#                 "font_size":"",
#                 "media_visibility":False,
#                 "theme":"",
#                 "wallpaper":""
#             },
#             "languages_and_regions":{
#                 "language":"",
#                 "languages_zuri_should_spell_check":"None",
#                 "set_time_zone_automatically":False,
#                 "spell_check":False,
#                 "time_zone":""
#             },
#             "messages_and_media":{
#                 "additional_options":{
#                     "clock":False,
#                     "color_swatches":False,
#                     "currently_typing":False
#                 },
#                 "bring_emails_into_zuri":"",
#                 "convert_emoticons_to_emoji":False,
#                 "custom":False,
#                 "emoji":"",
#                 "emoji_as_text":False,
#                 "frequently_used_emoji":False,
#                 "inline_media_and_links":{
#                     "larger_than_2_mb":False,
#                     "show_images_and_files_from_linked_websites":False,
#                     "show_images_and_files_uploaded_to_zurichat":False,
#                     "show_text_previews_of_linked_websites":False
#                 },
#                 "messages_one_click_reaction":"None",
#                 "names":"",
#                 "show_jumbomoji":False,
#                 "theme":""
#             },
#             "notifications":{
#                 "channel_hurdle_notification":False,
#                 "custom_notification_schedule":"None",
#                 "message_preview_in_each_notification":False,
#                 "mute_all_sounds":False,
#                 "notification_schedule":{
#                     "day":"",
#                     "from":"",
#                     "to":""
#                 },
#                 "set_lounge_notifications_right":"",
#                 "set_message_notifications_right":""
#             },
#             "plugin_settings":"None",
#             "sidebar":{
#                 "always_show_in_the_sidebar":"None",
#                 "list_private_channels_separately":False,
#                 "organize_external_conversations":False,
#                 "show_all_the_following":"",
#                 "show_conversations":"",
#                 "show_profile_picture_next_to_dm":False,
#                 "sidebar_sort":""
#             },
#             "themes":{
#                 "colors":"",
#                 "mode":""
#             }
#         },
#         "socials":"None",
#         "status":{
#             "expiry_time":"",
#             "status_history":"None",
#             "tag":"",
#             "text":""
#         },
#         "time_zone":"",
#         "user_name":"aduragbemiife"
#     }
# ]



@pytest.mark.asyncio
async def test_get_room_members(
    mock_get_user_room, mock_read
):
    """Retrieve room members in the room
    
    Args:
        mock_get_user_room (AsyncMock): Asynchronous external api call
        mock_read (AsyncMock): Asynchronous external api call
    
    """
    
    success = {
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
    
    room = fake_data_group_dm
    members = room["room_members"]
    
    read_response = {
        "status": 200,
        "message": "All room members retrieved successfully",
        "data": members
    }
    
    mock_get_user_room.return_value = room
    mock_read.return_value = read_response
    
    response = client.get(get_room_members_url)
    assert response.status_code == 200
    assert response.json() == success
        

@pytest.mark.asyncio
async def test_join_room_success(mock_get_user_room, mock_update, mock_centrifugo):
    """Tests when a member successfully joins a room
    Args:
        mock_get_user_room (AsyncMock): Asynchronous external api call
        mock_update (AsyncMock): Asynchronous external api call
        mock_centrifugo (AsyncMock): Asynchronous external api call
    """
    success_response = {
        "room_members": {
            "619mem1": {"closed": False, "role": "admin", "starred": False},
            "619mem2": {"closed": False, "role": "member", "starred": False},
            "619mem3": {"closed": False, "role": "member", "starred": False},
        }
    }

    update_response = {
        "status": 200,
        "message": "success",
        "data": {"matched_documents": 1, "modified_documents": 1},
    }

    centrifugo_response = {"status_code": 200}

    mock_get_user_room.return_value = fake_core_room_data
    mock_update.return_value = update_response
    mock_centrifugo.return_value = centrifugo_response

    response = client.put(url=join_room_test_url, json=test_join_room_payload)
    assert response.status_code == 200
    assert response.json() == success_response


# @pytest.mark.asyncio
# async def test_join_private_room(mock_get_user_room, mock_update, mock_centrifugo):
#     """Tests when a member is successfully added to a private room
#     Args:
#         mock_get_user_room (AsyncMock): Asynchronous external api call
#         mock_update (AsyncMock): Asynchronous external api call
#         mock_centrifugo (AsyncMock): Asynchronous external api call
#     """
#     fake_core_room_data["is_private"] = True
#     success_response = {
#         "room_members": {
#             "619mem1": {"closed": False, "role": "admin", "starred": False},
#             "619mem2": {"closed": False, "role": "member", "starred": False},
#             "619mem3": {"closed": False, "role": "member", "starred": False},
#         }
#     }

#     update_response = {
#         "status": 200,
#         "message": "success",
#         "data": {"matched_documents": 1, "modified_documents": 1},
#     }

#     centrifugo_response = {"status_code": 200}

#     mock_get_user_room.return_value = fake_core_room_data
#     mock_update.return_value = update_response
#     mock_centrifugo.return_value = centrifugo_response

#     response = client.put(url=join_room_test_url, json=test_join_room_payload)
#     assert response.status_code == 200
#     assert response.json() == success_response


# @pytest.mark.asyncio
# async def test_cannot_join_DMroom(mock_get_user_room):
#     """Tests when a member is successfully stopped from joining a DM room
#     Args:
#         mock_get_user_room (AsyncMock): Asynchronous external api call
#     """
#     fake_core_room_data["room_type"] = "DM"
#     mock_get_user_room.return_value = fake_core_room_data

#     response = client.put(url=join_room_test_url, json=test_join_room_payload)
#     assert response.status_code == 403
#     assert response.json() == {"detail": "DM room cannot be joined or not found"}


# @pytest.mark.asyncio
# async def test_max_number_for_groupDM(mock_get_user_room):
#     """Tests maximum member entries for a group DM
#     Args:
#         mock_get_user_room (AsyncMock): Asynchronous external api call
#     """
#     fake_core_room_data["room_type"] = "GROUP_DM"
#     mock_get_user_room.return_value = fake_core_room_data
#     payload = {
#         "619mem3": {"role": "member", "starred": False, "closed": False},
#         "619mem4": {"role": "member", "starred": False, "closed": False},
#         "619mem5": {"role": "member", "starred": False, "closed": False},
#         "619mem6": {"role": "member", "starred": False, "closed": False},
#         "619mem7": {"role": "member", "starred": False, "closed": False},
#         "619mem8": {"role": "member", "starred": False, "closed": False},
#         "619mem9": {"role": "member", "starred": False, "closed": False},
#         "619mem10": {"role": "member", "starred": False, "closed": False},
#         "619mem11": {"role": "member", "starred": False, "closed": False},
#     }
#     test_join_room_payload.update(payload)
#     response = client.put(url=join_room_test_url, json=test_join_room_payload)
#     assert response.status_code == 400
#     assert response.json() == {"detail": "the max number for a Group_DM is 9"}
    