# from unittest import mock

# import pytest
# from fastapi.testclient import TestClient
# from main import app
# from utils.db import DataStorage

# client = TestClient(app)

# create_room_url = (
#     "api/v1/org/6619ba4671a5f54782939d384/members/619ba4671a5f54782939d385/rooms"
# )

# payload_room_data = {
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
#     },
#     "created_at": "2022-01-11 03:18:02.364291",
#     "is_private": False,
#     "is_archived": False,
# }

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

# fake_org_members = {
#     "61696f5ac4133ddaa309dcfe": {"closed": False, "role": "admin", "starred": False},
#     "6169704bc4133ddaa309dd07": {"closed": False, "role": "admin", "starred": False},
#     # "619ba4671a5f54782939d385": {"closed": False, "role": "admin", "starred": False},
#     "619baa5c1a5f54782939d386": {"closed": False, "role": "member", "starred": False},
# }
