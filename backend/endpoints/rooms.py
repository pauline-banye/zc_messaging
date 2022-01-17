from http.client import responses
import json
from typing import Dict, Optional

from fastapi import (APIRouter, BackgroundTasks, Body, HTTPException, Query,
                     Request, status)
from fastapi.responses import JSONResponse
from schema.response import ResponseModel
from schema.room import Role, Room, RoomMember, RoomRequest, RoomType
from utils.centrifugo import Events, centrifugo_client
from utils.db import DataStorage
from utils.room_utils import (ROOM_COLLECTION, get_org_rooms, get_room,
                              get_room_members, remove_room_member)
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
    print("room object",room_obj)

    # check if creator is in room members
    if member_id not in room_obj.room_members.keys():
        room_obj.room_members[member_id] = {
            "role": Role.ADMIN,
            "starred": False,
            "closed": False,
        }

    response = await DB.write(ROOM_COLLECTION, data=room_obj.dict())
    print("response", response)
    
    if response and response.get("status_code", None) is None:
        room_id = {"room_id": response.get("data").get("object_id")}
        print("room_id", room_id)

        background_tasks.add_task(
            sidebar.publish,
            org_id,
            member_id,
            room_obj.room_type,
        )  # publish to centrifugo in the background

        room_obj.id = room_id["room_id"]  # adding the room id to the data
        print("room object dict" , room_obj.dict())
        return JSONResponse(
            content=ResponseModel.success(
                data=room_obj.dict(), message="room created"),
            status_code=status.HTTP_201_CREATED,
        )
    print("response", response)
    raise HTTPException(
        status_code=status.HTTP_424_FAILED_DEPENDENCY,
        detail="unable to create room",
    )


@router.patch(
    "/org/{org_id}/rooms/{room_id}/members/{member_id}",
    response_model=ResponseModel,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"detail": "room or member not found"},
        424: {"detail": "member removal unsuccessful"},
    },
)
async def remove_member(
    org_id: str, room_id: str, member_id: str, admin_id: Optional[str] = None
):
    """Removes a member from a room either when removed by an admin or member leaves the room.

    Fetches the room which the member is removed from from the database collection
    Pops the member being removed from the room's members dict
    Updates the database collection with the new room
    Returns the room dict if member was removed successfully

    Args:
        org_id (str): A unique identifier of an organisation
        member_id (str): A unique identifier of the member being removed from the room
        room_id (str): A unique identifier of the room a member is being removed from
        admin_id (str): A unique identifier of the member removing another member

    Returns:
        HTTP_200_OK (member removed from room): {room}
    Raises
        HTTP_404_NOT_FOUND: room or member not found
        HTTP_403_FORBIDDEN: not authorized to remove room  member
        HTTP_424_FAILED_DEPENDENCY: member removal unsuccessful
    """
    room_data = await get_room(org_id, room_id)
    if not room_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="room does not exist",
        )
    if room_data["room_type"] != RoomType.CHANNEL:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="cannot remove member from DM rooms",
        )

    if member_id not in room_data["room_members"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not a member of the room",
        )

    if admin_id not in room_data["room_members"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="admin id specified not a member of the room",
        )

    admin_data = room_data["room_members"].get(
        admin_id
    )  # member will be none if no admin is supplied

    if admin_data is not None and admin_data.get("role") != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="must be an admin to remove member",
        )

    try:
        result = await remove_room_member(
            org_id=org_id, room_data=room_data, member_id=member_id
        )

    except ValueError as value_error:
        raise HTTPException(
            detail=value_error, status_code=status.HTTP_404_NOT_FOUND
        ) from value_error

    except ConnectionError as connect_error:
        raise HTTPException(
            detail=json.dumps(str(connect_error)),
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
        ) from connect_error
    else:
        return JSONResponse(
            content=ResponseModel.success(
                data=result, message="user removed from room successfully"
            ),
            status_code=status.HTTP_200_OK,
        )


@router.put(
    "/org/{org_id}/rooms/{room_id}/members/{member_id}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseModel,
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
                "room_members": {
                    "619123member1": {"closed": False, "role": "admin", "starred": False},
                    "619123member2": {"closed": False, "role": "admin", "starred": False},
                    "619123member3": {"closed": False, "role": "admin", "starred": False}
                }
            }
    Raises:
        HTTP_400_BAD_REQUEST: the max number for a Group_DM is 9
        HTTP_401_UNAUTHORIZED: member not in room or not an admin
        HTTP_403_FORBIDDEN: room not found || DM room cannot be joined
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
            detail="room not found" if not room else "DM room cannot be joined",
        )

    member = room.get("room_members").get(str(member_id))

    if room["room_type"].upper() == RoomType.CHANNEL:
        if room["is_private"] is True and (
            member is None or member["role"].lower() != Role.ADMIN
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="only admins can add new members",
            )
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
            content=ResponseModel.success(
                data=update_members, message="member(s) successfully added"
            ),
        )
    raise HTTPException(
        status_code=status.HTTP_424_FAILED_DEPENDENCY,
        detail="failed to add new members to room",
    )


@router.put(
    "/org/{org_id}/rooms/{room_id}",
    response_model=ResponseModel,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"detail": "member not in room"},
        403: {"detail": "cannot close a channel room"},
        404: {"detail": "room not found"},
        424: {"detail": "unable to close conversation"},
    },
)
async def close_conversation(
    org_id: str,
    room_id: str,
    member_id: str,
    background_tasks: BackgroundTasks,
):
    """
    Closes a DM or Group_DM room on the sidebar
    By toggling the closed boolean field of the room document from False to True
    The function when called on a closed room, changes the closed field back to False
    Args:
        org_id (str): A unique identifier of an organisation
        room_id: A unique identifier of the room to be updated
        member_id: A unique identifier of the member initiating the request
        background_tasks: A parameter that allows tasks to be performed outside of the main function
    Returns:
        HTTP_200_OK: {
                        "status": "success",
                        "message": "conversation closed || conversation opened",
                        "data": {
                            "closed": true || false,
                            "role": "admin",
                            "starred": false
                        }
                    }
    Raises:
        HTTP_401_UNAUTHORIZED: member not in room
        HTTP_403_FORBIDDEN: cannot close a channel room
        HTTP_404_NOT_FOUND: room not found
        HTTP_424_FAILED_DEPENDENCY: unable to close conversation
    """
    DB = DataStorage(org_id)
    room = await get_room(org_id=org_id, room_id=room_id)

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="room not found"
        )

    if room["room_type"].upper() == RoomType.CHANNEL:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="cannot close a channel room"
        )

    if member_id not in room["room_members"].keys():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="member not in room"
        )

    member_room_data = room["room_members"].get(member_id)
    member_room_data["closed"] = member_room_data["closed"] is False
    data = {"room_members": room["room_members"]}

    update_response = await DB.update(
        ROOM_COLLECTION, document_id=room_id, data=data
    )  # updates the room data in the db collection

    background_tasks.add_task(
        sidebar.publish,
        org_id,
        member_id,
        room["room_type"],
    )  # publish to centrifugo in the background

    if update_response and update_response.get("status_code") is None:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=ResponseModel.success(
                data=member_room_data,
                message="conversation closed"
                if member_room_data["closed"]
                else "conversation opened",
            ),
        )

    raise HTTPException(
        status_code=status.HTTP_424_FAILED_DEPENDENCY,
        detail="unable to close conversation",
    )


@router.get(
    "/org/{org_id}/rooms",
    response_model=ResponseModel,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"detail": "failure to retrieve rooms"},
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


@router.get(
    "/org/{org_id}/rooms/{room_id}",
    response_model=ResponseModel,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"detail": "room not found"},
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
    if room:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=ResponseModel.success(
                data=room, 
                message="room found"
            ),
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="room not found"
        )


@router.get(
    "/org/{org_id}/rooms/{room_id}/members",
    response_model=ResponseModel,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"detail": "Room not found"},
        424: {"detail": "Failure to retrieve room members"},
    },
)
async def get_members(org_id: str, room_id: str):

    """Get room members.
    Returns all members in a room if the room is found in the database
    Raises HTTP_404_NOT_FOUND if the room is not found
    Raises HTTP_424_FAILED_DEPENDENCY if there is an error retrieving the room members
    Args:
        org_id (str): A unique identifier of an organisation
        room_id (str): A unique identifier of the room
    Returns:
        HTTP_200_OK (Room members retrieved successfully):

        {
            "status": "success",
            "message": "Room members retrieved",
            "data": {
                "61696f5ac4133ddaa309dcfe": {
                "closed": false,
                "role": "admin",
                "starred": false
                },
                "6169704bc4133ddaa309dd07": {
                "closed": false,
                "role": "admin",
                "starred": false
                }
            }
        }

    Raises:
        HTTPException [404]: Room not found
        HTTPException [424]: Failure to retrieve room members
    """
    room = await get_room(org_id, room_id)

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Room not found"
        )

    members = room["room_members"]
    if members and members.get("status_code") is not None:
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Failure to retrieve room members",
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=ResponseModel.success(
            data=members,
            message="Room members retrieved successfully",
        )
    )


# @router.get(
#     "/org/{org_id}/rooms/{room_id}/members",
#     response_model=ResponseModel,
#     status_code=status.HTTP_200_OK,
#     responses={
#         400: {"detail": "Invalid query supplied"},
#         404: {"detail": "Room not found"},
#         424: {"detail": "Failure to retrieve room members"},
#     },
# )
# async def get_members(org_id: str, room_id: str, query: Optional[str] = None):

#     """Get room members.
#     Returns all members in a room if the room is found in the database
#     Returns filtered members in a room if query is supplied
#     Raises HTTP_400_BAD_REQUEST if query supplied is not admin or member
#     Raises HTTP_404_NOT_FOUND if the room is not found
#     Raises HTTP_424_FAILED_DEPENDENCY if there is an error retrieving the room members
#     Args:
#         org_id (str): A unique identifier of an organisation
#         room_id (str): A unique identifier of the room
#     Returns:
#         HTTP_200_OK (Room members retrieved successfully):

#         {
#             "status": "success",
#             "message": "Room members retrieved",
#             "data": {
#                 "61696f5ac4133ddaa309dcfe": {
#                 "closed": false,
#                 "role": "admin",
#                 "starred": false
#                 },
#                 "6169704bc4133ddaa309dd07": {
#                 "closed": false,
#                 "role": "admin",
#                 "starred": false
#                 }
#             }
#         }

#     Raises:
#         HTTPException [400]: Invalid query supplied
#         HTTPException [404]: Room not found
#         HTTPException [424]: Failure to retrieve room members
#     """
#     room = await get_room(org_id, room_id)

#     if not room:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Room doesn't exist"
#         )

#     members = room["room_members"]
#     if members and members.get("status_code") is not None:
#         raise HTTPException(
#             status_code=status.HTTP_424_FAILED_DEPENDENCY,
#             detail="Failure to retrieve room members",
#         )

#     if query:  # if query is supplied
#         if query not in ["admin", "member", "starred", "closed"]:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Invalid query supplied",
#             )

#         if query in ["admin", "member"]:  # if query is admin or member
#             members_role = {
#                 member_id: member_data
#                 for member_id, member_data in members.items()
#                 if member_data["role"] == query
#             }
#             if query == "admin":
#                 return JSONResponse(
#                     status_code=status.HTTP_200_OK,
#                     content=ResponseModel.success(
#                         data=members_role,
#                         message="Admin members retrieved successfully",
#                     ),
#                 )
#             return JSONResponse(
#                 status_code=status.HTTP_200_OK,
#                 content=ResponseModel.success(
#                     data=members_role, message="Room members retrieved successfully"
#                 ),
#             )

#         if query == "starred":  # if query is starred
#             members_starred = {
#                 member_id: member_data
#                 for member_id, member_data in members.items()
#                 if member_data["starred"] is True
#             }
#             if members_starred == {}:
#                 return JSONResponse(
#                     status_code=status.HTTP_200_OK,
#                     content=ResponseModel.success(
#                         data=members_starred,
#                         message="No room member has starred this room",
#                     ),
#                 )
#             return JSONResponse(
#                 status_code=status.HTTP_200_OK,
#                 content=ResponseModel.success(
#                     data=members_starred,
#                     message="Starred room members retrieved successfully",
#                 ),
#             )

#         if query == "closed":  # if query is closed
#             members_closed = {
#                 member_id: member_data
#                 for member_id, member_data in members.items()
#                 if member_data["closed"] is True
#             }
#             if members_closed == {}:
#                 return JSONResponse(
#                     status_code=status.HTTP_200_OK,
#                     content=ResponseModel.success(
#                         data=members_closed,
#                         message="No room member has closed this room",
#                     ),
#                 )
#             return JSONResponse(
#                 status_code=status.HTTP_200_OK,
#                 content=ResponseModel.success(
#                     data=members_closed,
#                     message="Closed room members retrieved successfully",
#                 ),
#             )

#     # if query is not supplied
#     return JSONResponse(
#         status_code=status.HTTP_200_OK,
#         content=ResponseModel.success(
#             data=members,
#             message="All room members retrieved successfully",
#         ),
#     )


# @router.get(
#     "/org/{org_id}/rooms/{room_id}/memberslist",
#     response_model=ResponseModel,
#     status_code=status.HTTP_200_OK,
#     responses={
#         424: {"detail": "Failure to retrieve room members"},
#     },
# )
# async def get_members(org_id: str, room_id: str):
#     """
#     Get room members.
#     Returns all members in a room if the room is found in the database
#     Raises HTTP_424_FAILED_DEPENDENCY if there is an error retrieving the room members
#     Args:
#         org_id (str): A unique identifier of an organisation
#         room_id (str): A unique identifier of the room
#     Returns:
#         HTTP_200_OK (Room members)

#         {
#             "status": "success",
#             "message": "Room Members",
#             "data": [
#                 "61696f5ac4133ddaa309dcfe",
#                 "6169704bc4133ddaa309dd07",
#                 "619ba4671a5f54782939d385",
#                 "619baa5c1a5f54782939d386"
#             ]
#         }

#     Raises:
#         HTTPException [424]: Failed to retrieve room members
#     """
#     room_members = await get_room_members(org_id, room_id)

#     members = list(room_members)
#     if members:
#         return JSONResponse(
#             content=ResponseModel.success(data=members, message="Room Members"),
#             status_code=status.HTTP_200_OK,
#         )

#     raise HTTPException(
#         status_code=status.HTTP_424_FAILED_DEPENDENCY,
#         detail="Failed to retrieve room members",
#     )


@router.delete(
    "/org/{org_id}/rooms/{room_id}",
    response_model=ResponseModel,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"detail": "Room not found"},
        424: {"detail": "Failure to delete room"},
    },
)
async def delete_room(org_id: str, room_id: str, background_tasks: BackgroundTasks):
    """
    Delete a room.
    Deletes a room if the room is found in the database
    Raises HTTP_404_NOT_FOUND if the room is not found
    Raises HTTP_424_FAILED_DEPENDENCY if there is an error deleting the room
    Args:
        org_id (str): A unique identifier of an organisation
        room_id (str): A unique identifier of the room
        background_tasks (BackgroundTasks): Background tasks
    Returns:
        HTTP_200_OK (Room deleted)
        {
            "status": "success",
            "message": "Room deleted successfully"
        }
    Raises:
        HTTPException [404]: Room not found
        HTTPException [424]: Failure to delete room
    """
    DB = DataStorage(org_id)
    room = await get_room(org_id, room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Room not found"
        )
    
    room_id = room["_id"]
    remove = await DB.delete(ROOM_COLLECTION, room_id)
    
    background_tasks.add_task(
        sidebar.publish,
        org_id,
        room_id
    )  # publish to centrifugo in the background            
    
    if remove and remove.get("status_code") is not None:
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Failure to delete room",
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=ResponseModel.success(
            data=remove, 
            message="Room deleted successfully"
        ),
    )
    
        
        
    
        



