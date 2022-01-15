import pytest
from fastapi.testclient import TestClient
from main import app

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



@pytest.mark.asyncio
async def test_create_room_successful(mock_get_org_rooms, mock_get_org_members, mock_dataStorage_write, mock_centrifugo):
    """Create room successful
    Args:
        mock_get_org_members (AsyncMock): Asynchronous external api call
        mock_dataStorage_write (AsyncMock): Asynchronous external api call
        mock_centrifugo (AsyncMock): Asynchronous external api call
    """
        
    success_response = {
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

    # write_response = {
    #     "status": 201,
    #     "message": "room created",
    #     "data": fake_data_group_dm
    # }
    
    write_response = {
        "status": 201,
        "message": "success",
        "data": {
            "insert_count": 1,
            "object_id": "61dcf855eba8adb50ca13a24",
            }
        }

    centrifugo_response = {"status_code": 200}

    Mock_get_org_rooms.return_value = fake_org_rooms
    mock_get_org_members.return_value = fake_org_members
    mock_dataStorage_write.return_value = write_response
    mock_centrifugo.return_value = centrifugo_response

    response = client.post(create_room_url, json=payload_group_dm)
    assert response.status_code == 201
    # assert response.json() == {"detail": "room created"}
    assert response == {
        "status": "success",
        "message": "Room created",
        "data": success_response
    }
    

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
