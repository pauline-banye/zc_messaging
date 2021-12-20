from typing import Dict

from fastapi import APIRouter, BackgroundTasks, Body, HTTPException, status
from fastapi.responses import JSONResponse
from schema.response import ResponseModel
from schema.room import Role, Room, RoomMember, RoomRequest, RoomType
from utils.centrifugo import Events, centrifugo_client
from utils.db import DataStorage
from utils.room_utils import ROOM_COLLECTION, get_room, get_org_rooms
from utils.sidebar import sidebar

router = APIRouter()


@router.post(
    "/org/{org_id}/members/{member_id}/rooms",
    response_model=ResponseModel,
    status_code=status.HTTP_201_CREATED,
    responses={
        200: {"detail": {"room_id": "room_id"}},
        424: {"detail": "ZC Core Failed"},
    },
)
async def create_room(
    org_id: str, member_id: str, request: RoomRequest, background_tasks: BackgroundTasks
):
    """Creates a room between users.

    Registers a new document to the database collection.
    Returns the document id if the room is successfully created or already exist
    while publishing to the user sidebar in the background

    Args:
        org_id (str): A unique identifier of an organisation
        request: A pydantic schema that defines the room request parameters
        member_id: A unique identifier of the member creating the room

    Returns:
        HTTP_200_OK (room already exist): {room_id}
        HTTP_201_CREATED (new room created): {room_id}
    Raises
        HTTP_424_FAILED_DEPENDENCY: room creation unsuccessful
    """

    DB = DataStorage(org_id)
    room_obj = Room(**request.dict(), org_id=org_id, created_by=member_id)

    # check if creator is in room members
    if member_id not in room_obj.room_members.keys():
        room_obj.room_members[member_id] = {
            "role": Role.ADMIN,
            "starred": False,
            "closed": False,
        }

    response = await DB.write(ROOM_COLLECTION, data=room_obj.dict())
    if response and response.get("status_code", None) is None:
        room_id = {"room_id": response.get("data").get("object_id")}

        background_tasks.add_task(
            sidebar.publish,
            org_id,
            member_id,
            room_obj.room_type,
        )  # publish to centrifugo in the background

        room_obj.id = room_id["room_id"]  # adding the room id to the data
        return JSONResponse(
            content=ResponseModel.success(data=room_obj.dict(), message="room created"),
            status_code=status.HTTP_201_CREATED,
        )

    raise HTTPException(
        status_code=status.HTTP_424_FAILED_DEPENDENCY,
        detail="unable to create room",
    )


@router.put(
    "/org/{org_id}/rooms/{room_id}/members/{member_id}",
    status_code=status.HTTP_200_OK,
    responses={
        400: {"detail": "the max number for a Group_DM is 9"},
        401: {"detail": "member not an admin"},
        403: {"detail": "DM room or not found"},
        424: {"detail": "failed to add new members to room"},
    },
)
async def join_room(
    org_id: str,
    room_id: str,
    member_id: str,
    background_tasks: BackgroundTasks,
    new_members: Dict[str, RoomMember] = Body(...),
):
    """Adds a new member(s) to a room
    Args:
        data: a pydantic schema that defines the request params
        org_id (str): A unique identifier of an organisation
        room_id: A unique identifier of the room to be updated
        member_id: A unique identifier of the member initiating the request
        background_tasks: A parameter that allows tasks to be performed outside of the main function
        new_members: A dictionary of new members to be added to the room

    Returns:
        HTTP_200_OK: {
                        "status": 200,
                        "message": "success",
                        "data": {
                            "matched_documents": 1,
                            "modified_documents": 1
                        }
                    }
    Raises:
        HTTP_400_BAD_REQUEST: the max number for a Group_DM is 9
        HTTP_401_UNAUTHORIZED: member not in room or not an admin
        HTTP_403_FORBIDDEN: DM room or not found
        HTTP_424_FAILED_DEPENDENCY: failed to add new members to room
    """
    DB = DataStorage(org_id)  # initializes the datastorage class with the org id

    members = {
        k: v.dict() for k, v in new_members.items()
    }  # converts RoomMember to dict

    room = await get_room(org_id=org_id, room_id=room_id)

    if not room or room["room_type"].upper() == RoomType.DM:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="DM room cannot be joined or not found",
        )

    member = room.get("room_members").get(str(member_id))
    if member is None or member["role"].lower() != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="member not in room or not an admin",
        )

    if room["room_type"].upper() == RoomType.CHANNEL:
        room["room_members"].update(members)

    if room["room_type"].upper() == RoomType.GROUP_DM:
        room["room_members"].update(members)
        if len(room["room_members"].keys()) > 9:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="the max number for a Group_DM is 9",
            )

    update_members = {"room_members": room["room_members"]}
    update_response = await DB.update(
        ROOM_COLLECTION, document_id=room_id, data=update_members
    )  # updates the room data in the db collection

    background_tasks.add_task(
        centrifugo_client.publish,
        room=room_id,
        event=Events.ROOM_MEMBER_ADD,
        data=members,
    )  # publish to centrifugo in the background

    if update_response and update_response.get("status_code", None) is None:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=update_members,
        )
    raise HTTPException(
        status_code=status.HTTP_424_FAILED_DEPENDENCY,
        detail="failed to add new members to room",
    )
    

@router.get(
    "/org/{org_id}/rooms",
    response_model=ResponseModel,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"detail": "failure to retrieve rooms"},
        424: {"detail": "failure to retrieve data"},
    },
)
async def get_all_rooms(org_id: str):
    """Get all rooms.

    Returns the list of rooms if the rooms are found in the database
    Raises HTTP_404_NOT_FOUND if the org_id is invalid or rooms are not found

    Args:
        org_id (str): A unique identifier of an organisation

    Returns:
        HTTP_200_OK (list of rooms in the org)
        {
            "_id": "61bc094b78fb01b18fac1425",
            "created_at": "2021-12-17 03:10:26.620752",
            "created_by": "619ba4671a5f54782939d385",
            "description": "string",
            "id": null,
            "is_archived": false,
            "is_private": false,
            "org_id": "619ba4671a5f54782939d384",
            "room_members": {
                "619ba4671a5f54782939d385": {
                "closed": false,
                "role": "admin",
                "starred": false
                }
            },
            "room_name": "testroom2",
            "room_type": "CHANNEL",
            "topic": "string"
        }

    Raises:
        HTTPException [404]: Failure to retrieve rooms
        HTTPException [424]: Failure to retrieve data
    """
    rooms = await get_org_rooms(org_id)

    try:
        if rooms:
            return JSONResponse(
                content=ResponseModel.success(
                    data=rooms, message="list of rooms in the org"
                ),
                status_code=status.HTTP_200_OK,
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Failure to retrieve rooms",
        )
    except HTTPException as error:
        raise HTTPException(
            data="Failure to retrieve data",
            status=status.HTTP_424_FAILED_DEPENDENCY,
        ) from error


@router.get(
    "/org/{org_id}/rooms/{room_id}",
    response_model=ResponseModel,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"detail": "room not found"},
        424: {"detail": "failure to retrieve data"},
    },
)
async def get_room_by_id(org_id: str, room_id: str):
    """Get room by id.

    Returns the room object if the room is found in the database
    Raises HTTP_404_NOT_FOUND if the room is not found

    Args:
        org_id (str): A unique identifier of an organisation
        room_id (str): A unique identifier of the room

    Returns:
        HTTP_200_OK (room found)
        {
            "_id": "61bc094b78fb01b18fac1425",
            "created_at": "2021-12-17 03:10:26.620752",
            "created_by": "619ba4671a5f54782939d385",
            "description": "string",
            "id": null,
            "is_archived": false,
            "is_private": false,
            "org_id": "619ba4671a5f54782939d384",
            "room_members": {
                "619ba4671a5f54782939d385": {
                "closed": false,
                "role": "admin",
                "starred": false
                }
            },
            "room_name": "testroom2",
            "room_type": "CHANNEL",
            "topic": "string"
        }

    Raises:
        HTTPException [404]: Room not found
        HTTPException [424]: Failure to retrieve data
    """
    room = await get_room(org_id, room_id)

    try:
        if room:
            return JSONResponse(
                content=ResponseModel.success(data=room, message="room found"),
                status_code=status.HTTP_200_OK,
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="room not found"
        )
    except HTTPException as error:
        raise HTTPException(
            data="Failure to retrieve data",
            status=status.HTTP_424_FAILED_DEPENDENCY,
        ) from error
        