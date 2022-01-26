from unittest.mock import AsyncMock

import pytest


@pytest.fixture(name="mock_dataStorage_read")
def fixture_mock_dataStorage_read(mocker):
    """Patch for reading data from zc core.

    Args:
       mocker (Mock): For patching a third-party api call

    Returns:
       AsyncMock: An instance of the asyncmock class
    """
    core_read_mock = AsyncMock()
    mocker.patch("utils.db.DataStorage.read", side_effect=core_read_mock)
    return core_read_mock


@pytest.fixture(name="mock_dataStorage_write")
def fixture_mock_dataStorage_write(mocker):
    """Patch for writing to zc core.

    Args:
       mocker (Mock): For patching a third-party api call

    Returns:
        AsyncMock: An instance of the asyncmock class
    """
    async_mock_write = AsyncMock()
    mocker.patch("utils.db.DataStorage.write", side_effect=async_mock_write)
    return async_mock_write


@pytest.fixture(name="mock_get_room_members")
def fixture_mock_get_room_members(mocker):
    """Patch for getting room members.

    Args:
       mocker (Mock): For patching a third-party api call

    Returns:
       AsyncMock: An instance of the asyncmock class
    """
    mock_get_room_members = AsyncMock()
    mocker.patch("utils.room_utils.DataStorage.read", side_effect=mock_get_room_members)
    return mock_get_room_members


@pytest.fixture(name="mock_centrifugo")
def fixture_mock_centrifugo(mocker):
    """Patch for centrifugo external api call

    Args:
        mocker (Mock): For patching a third-party api call

    Returns:
        AsyncMock: An instance of the asyncmock class
    """
    async_mock_centrifugo = AsyncMock()
    mocker.patch(
        "utils.centrifugo.centrifugo_client.publish",
        side_effect=async_mock_centrifugo,
    )
    return async_mock_centrifugo


@pytest.fixture(name="mock_dataStorage_update")
def fixture_mock_dataStorage_update(mocker):
    """Patch for updating a document to zc core

    Args:
        mocker (Mock): For patching a third-party api call

    Returns:
        AsyncMock: An instance of the asyncmock class
    """
    zc_core_update_data = AsyncMock()
    mocker.patch("utils.db.DataStorage.update", side_effect=zc_core_update_data)
    return zc_core_update_data


@pytest.fixture(name="mock_dataStorage_delete")
def fixture_mock_dataStorage_delete(mocker):
    """Patch for deleting a document to zc core

    Args:
        mocker (Mock): For patching a third-party api call

    Returns:
        AsyncMock: An instance of the asyncmock class
    """
    zc_core_update_data = AsyncMock()
    mocker.patch("utils.db.DataStorage.delete", side_effect=zc_core_update_data)
    return zc_core_update_data


@pytest.fixture(name="mock_get_org_rooms")
def fixture_mock_get_org_rooms(mocker):
    """Patch for reading zc core.

    Args:
       mocker (Mock): For patching a third-party api call

    Returns:
       AsyncMock: An instance of the asyncmock class
    """
    zc_core_read_data = AsyncMock()
    mocker.patch("endpoints.rooms.DataStorage.read", side_effect=zc_core_read_data)
    return zc_core_read_data


@pytest.fixture(name="mock_get_all_members")
def fixture_mock_get_all_members(mocker):
    """Patch for reading zc core.

    Args:
       mocker (Mock): For patching a third-party api call

    Returns:
       AsyncMock: An instance of the asyncmock class
    """
    zc_core_read_data = AsyncMock()
    mocker.patch(
        "endpoints.rooms.DataStorage.get_all_members", side_effect=zc_core_read_data
    )
    return zc_core_read_data


@pytest.fixture(name="mock_get_org_members")
def fixture_mock_get_org_members(mocker):
    """Patch for reading zc core.

    Args:
       mocker (Mock): For patching a third-party api call

    Returns:
       AsyncMock: An instance of the asyncmock class
    """
    zc_core_read_data = AsyncMock()
    mocker.patch("endpoints.rooms.DataStorage.read", side_effect=zc_core_read_data)
    return zc_core_read_data


@pytest.fixture(name="mock_get_admin_members")
def fixture_mock_get_admin_members(mocker):
    """Patch for reading zc core.

    Args:
       mocker (Mock): For patching a third-party api call

    Returns:
       AsyncMock: An instance of the asyncmock class
    """
    zc_core_read_data = AsyncMock()
    mocker.patch("endpoints.rooms.DataStorage.read", side_effect=zc_core_read_data)
    return zc_core_read_data


# @pytest.fixture(name="init_fake_room")
# def fixture_initialize_fake_room_data():
#     """A fixture that initialises a new fake room data for each test
#     Returns:
#         Dict: An room dictionary
#     """
#     room_data = {
#         "room_name": "General",
#         "room_type": "CHANNEL",
#         "room_members": {
#             "61696f5ac4133ddaa309dcfe": {
#                 "closed": False,
#                 "role": "admin",
#                 "starred": False,
#             },
#             "6169704bc4133ddaa309dd07": {
#                 "closed": False,
#                 "role": "admin",
#                 "starred": False,
#             },
#             "619baa5c1a5f54782939d386": {
#                 "closed": False,
#                 "role": "member",
#                 "starred": False,
#             },
#             "619baa5c1a5f54782930d386": {
#                 "closed": False,
#                 "role": "member",
#                 "starred": True,
#             },
#         },
#         "created_at": "2022-01-11 03:18:02.364291",
#         "description": None,
#         "topic": "General Information",
#         "is_private": False,
#         "is_archived": False,
#         "id": "23dg67l0eba8adb50ca13a24",
#         "org_id": "3467sd4671a5f5478df56u911",
#         "created_by": "619ba4671a5f54782939d385",
#     }
#     return room_data


@pytest.fixture(name="init_fake_room")
def fixture_initialize_fake_room_data():
    """A fixture that initialises a new fake room data for each test
    Returns:
        Dict: An room dictionary
    """
    return {
        "room_name": "General",
        "room_type": "CHANNEL",
        "room_members": {
            "61696f5ac4133ddaa309dcfe": {
                "closed": False,
                "role": "admin",
                "starred": False,
            },
            "6169704bc4133ddaa309dd07": {
                "closed": False,
                "role": "admin",
                "starred": False,
            },
            "619baa5c1a5f54782939d386": {
                "closed": False,
                "role": "member",
                "starred": False,
            },
            "619baa5c1a5f54782930d386": {
                "closed": False,
                "role": "member",
                "starred": True,
            },
        },
        "created_at": "2022-01-11 03:18:02.364291",
        "description": None,
        "topic": "General Information",
        "is_private": False,
        "is_archived": False,
        "id": "23dg67l0eba8adb50ca13a24",
        "org_id": "3467sd4671a5f5478df56u911",
        "created_by": "619ba4671a5f54782939d385",
    }


# @pytest.fixture(name="init_fake_message")
# def fixture_initialize_fake_message_data():
#     """A fixture that initialises a new fake message data for each test
#     Returns:
#         Dict: An message dictionary
#     """
#     return {
#     "_id": "61e6878165934b58b8e5d1e0",
#     "created_at": "2022-01-18 09:05:32.479911",
#     "edited": False,
#     "emojis": [
#         {
#             "count": 1,
#             "emoji": "smile",
#             "name": "smile",
#             "reactedUsersId": ["619bab3b1a5f54782939d400"],
#         },
#     ],
#     "files": [],
#     "org_id": "619ba4671a5f54782939d384",
#     "richUiData": {
#         "blocks": [
#             {
#                 "data": {},
#                 "depth": 0,
#                 "entityRanges": [],
#                 "inlineStyleRanges": [],
#                 "key": "random",
#                 "text": "Helloooo",
#                 "type": "unstyled",
#             }
#         ],
#         "entityMap": {},
#     },
#     "room_id": "61e6855e65934b58b8e5d1df",
#     "saved_by": [],
#     "sender_id": "619bab3b1a5f54782939d400",
#     "threads": [],
#     "timestamp": 0,
# }



# @pytest.fixture(name="mock_read")
# def fixture_mock_read(mocker):
#     """Patch for reading zc core.

#     Args:
#        mocker (Mock): For patching a third-party api call

#     Returns:
#        AsyncMock: An instance of the asyncmock class
#     """
#     # core_read_mock = AsyncMock()
#     # mocker.patch("utils.room_utils.DataStorage.read", side_effect=core_read_mock)
#     # return core_read_mock
#     zc_core_read_data = AsyncMock()
#     mocker.patch("endpoints.rooms.DataStorage.read", side_effect=zc_core_read_data)
#     return zc_core_read_data


# @pytest.fixture(name="mock_get_user_room")
# def fixture_mock_get_user_room(mocker):
#     """Patch for reading zc core.
#     Args:
#        mocker (Mock): For patching a third-party api call
#     Returns:
#        AsyncMock: An instance of the asyncmock class
#     """
#     zc_core_read_data = AsyncMock()
#     mocker.patch("endpoints.rooms.DataStorage.read", side_effect=zc_core_read_data)
#     return zc_core_read_data


# @pytest.fixture(name="mock_write")
# def fixture_mock_write(mocker):
#     """Patch for writing to zc core.
#     Args:
#        mocker (Mock): For patching a third-party api call
#     Returns:
#         AsyncMock: An instance of the asyncmock class
#     """
#     async_mock_write = AsyncMock()
#     mocker.patch("endpoints.messages.DataStorage.write", side_effect=async_mock_write)
#     return async_mock_write


# @pytest.fixture(name="room_mock_write")
# def fixture_room_mock_write(mocker):
#     """Patch for writing to zc core.
#     Args:
#        mocker (Mock): For patching a third-party api call
#     Returns:
#         AsyncMock: An instance of the asyncmock class
#     """
#     async_mock_write = AsyncMock()
#     mocker.patch("endpoints.rooms.DataStorage.write", side_effect=async_mock_write)
#     return async_mock_write


# @pytest.fixture(name="mock_centrifugo")
# def fixture_mock_centrifugo(mocker):
#     """Patch for centrifugo external api call
#     Args:
#         mocker (Mock): For patching a third-party api call
#     Returns:
#         AsyncMock: An instance of the asyncmock class
#     """
#     async_mock_centrifugo = AsyncMock()
#     mocker.patch(
#         "endpoints.messages.centrifugo_client.publish",
#         side_effect=async_mock_centrifugo,
#     )
#     return async_mock_centrifugo


# @pytest.fixture(name="mock_get_message")
# def fixture_mock_get_message(mocker):
#     """Patch for reading zc core for retrieving a single message
#     Args:
#         mocker (Mock): For patching a third-party api call
#     Returns:
#         AsyncMock: An instance of the asyncmock class
#     """
#     zc_core_read_data = AsyncMock()
#     mocker.patch("endpoints.messages.DataStorage.read", side_effect=zc_core_read_data)
#     return zc_core_read_data


# @pytest.fixture(name="mock_update_message")
# def fixture_mock_update_message(mocker):
#     """Patch for updating a document to zc core
#     Args:
#         mocker (Mock): For patching a third-party api call
#     Returns:
#         AsyncMock: An instance of the asyncmock class
#     """
#     zc_core_update_data = AsyncMock()
#     mocker.patch(
#         "endpoints.messages.DataStorage.update", side_effect=zc_core_update_data
#     )
#     return zc_core_update_data


# from mykie88
# @pytest.fixture(name="mock_get_user_room")
# def fixture_mock_get_user_room(mocker):
#     """Patch for reading zc core.
#     Args:
#        mocker (Mock): For patching a third-party api call
#     Returns:
#        AsyncMock: An instance of the asyncmock class
#     """
#     core_read_mock = AsyncMock()
#     mocker.patch("utils.room_utils.DataStorage.read", side_effect=core_read_mock)
#     return core_read_mock



# @pytest.fixture(name="mock_get_room_members")
# def fixture_mock_get_room_members(mocker):
#     """Patch for getting room members.

#     Args:
#        mocker (Mock): For patching a third-party api call

#     Returns:
#        AsyncMock: An instance of the asyncmock class
#     """
#     mock_get_room_members = AsyncMock()
#     mocker.patch("utils.room_utils.DataStorage.read", side_effect=mock_get_room_members)
#     return mock_get_room_members


@pytest.fixture(name="mock_get_message")
def fixture_mock_get_message(mocker):
    """Patch for reading data from zc core.

    Args:
       mocker (Mock): For patching a third-party api call

    Returns:
       AsyncMock: An instance of the asyncmock class
    """
    core_read_mock = AsyncMock()
    # mocker.patch("utils.message_utils.DataStorage.read", side_effect=core_read_mock)
    mocker.patch("endpoints.messages.DataStorage.read", side_effect=core_read_mock)
    return core_read_mock 