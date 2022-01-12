from typing import Dict, List

from fastapi import APIRouter, BackgroundTasks, Body, HTTPException, status
from fastapi_pagination import Page, add_pagination, paginate
from schema.custom import ObjId
from schema.message import Emoji, Message, MessageRequest, Thread
from schema.response import ResponseModel
from starlette.responses import JSONResponse
from utils.centrifugo import Events, centrifugo_client
from utils.db import DataStorage
from utils.message_utils import (MESSAGE_COLLECTION, get_message,
                                 get_room_messages)
from utils.room_utils import get_room, get_room_members

router = APIRouter()


@router.post(
    "/org/{org_id}/rooms/{room_id}/messages",
    response_model=ResponseModel,
    status_code=status.HTTP_201_CREATED,
    responses={
        404: {"detail": "room or sender not found"},
        424: {"detail": "ZC Core Failed"},
    },
)
async def send_message(
    org_id,
    room_id,
    request: MessageRequest,
    background_tasks: BackgroundTasks,
):
    """Creates and sends a message from one user to another.
    Registers a new document to the chats database collection.
    Returns the message info and document id if message is successfully created
    while publishing to all members of the room in the background
    Args:
        org_id (str): A unique identifier of an organisation
        request: A pydantic schema that defines the message request parameters
        room_id: A unique identifier of the room where the message is being sent to.
        sender_id: A unique identifier of the user sending the message
        background_tasks: A daemon thread for publishing centrifugo
    Returns:
        HTTP_201_CREATED {new message sent}:
        A dict containing data about the message that was created (response_output).

            {
                "sender_id": "619ba4671a5f54782939d385",
                "emojis": [],
                "richUiData": {
                "blocks": [
                    {
                    "key": "eljik",
                    "text": "HI, I'm mark.. new here",
                    "type": "unstyled",
                    "depth": 0,
                    "inlineStyleRanges": [],
                    "entityRanges": [],
                    "data": {}
                    }
                ],
                "entityMap": {}
                },
                "files": [],
                "saved_by": [],
                "created_at": "2021-12-22 22:38:33.075643",
                "room_id": "619e28c31a5f54782939d59a",
                "org_id": "619ba4671a5f54782939d384",
                "message_id": "61c3aa9478fb01b18fac1465",
                "edited": false,
                "threads": []
            }

    Raises:
        HTTPException [404]: Sender not in room
        HTTPException [404]: Room does not exist
        HTTPException [424]: "message not sent"
    """
    DB = DataStorage(org_id)

    message_obj = Message(**request.dict(), org_id=org_id, room_id=room_id)

    response = await DB.write(
        MESSAGE_COLLECTION, message_obj.dict(exclude={"message_id"})
    )

    if response and response.get("status_code") is None:
        message_obj.message_id = response["data"]["object_id"]
        # Publish to centrifugo in the background.
        background_tasks.add_task(
            centrifugo_client.publish,
            room_id,
            Events.MESSAGE_CREATE,
            message_obj.dict(),
        )
        return JSONResponse(
            content=ResponseModel.success(
                data=message_obj.dict(), message="new message sent"
            ),
            status_code=status.HTTP_201_CREATED,
        )

    raise HTTPException(
        status_code=status.HTTP_424_FAILED_DEPENDENCY,
        detail={"Message not sent": response},
    )


@router.put(
    "/org/{org_id}/rooms/{room_id}/messages/{message_id}",
    response_model=ResponseModel,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"description": "you are not authorized to edit this message"},
        404: {"description": "message not found"},
        424: {"description": "message not edited"},
    },
)
async def update_message(
    request: MessageRequest,
    org_id: str,
    room_id: str,
    message_id: str,
    background_tasks: BackgroundTasks,
):
    """
    Update a message
    Args:
        request: Request object
        org_id: A unique identifier of the organization.
        room_id: A unique identifier of the room.
        message_id: A unique identifier of the message that is being edited.
        background_tasks: A daemon thread for publishing to centrifugo

        {
        "emojis": [],
        "richUiData": {
                "blocks": [
                    {
                    "data": {},
                    "depth": 0,
                    "entityRanges": [],
                    "inlineStyleRanges": [],
                    "key": "eljik",
                    "text": "HI, I'm mark",
                    "type": "unstyled"
                    }
                ],
                "entityMap": {}
                },
        "sender_id": "619ba4671a5f54782939d385",
        "timestamp": 0
        }

    Returns:
        HTTP_200_OK {Message edited}:
        A dict containing data about the message that was edited.

            {
                "_id": "61c3aa9478fb01b18fac1465",
                "created_at": "2021-12-22 22:38:33.075643",
                "edited": true,
                "emojis": [
                {
                    "count": 1,
                    "emoji": "👹",
                    "name": "frown",
                    "reactedUsersId": [
                    "619ba4671a5f54782939d385"
                    ]
                }
                ],
                "files": [],
                "org_id": "619ba4671a5f54782939d384",
                "richUiData": {
                "blocks": [
                    {
                    "data": {},
                    "depth": 0,
                    "entityRanges": [],
                    "inlineStyleRanges": [],
                    "key": "eljik",
                    "text": "HI, I'm mark.. new here",
                    "type": "unstyled"
                    }
                ],
                "entityMap": {}
                },
                "room_id": "619e28c31a5f54782939d59a",
                "saved_by": [],
                "sender_id": "619ba4671a5f54782939d385",
                "text": "string",
                "threads": []
            }

    Raises:
        HTTPException [401]: You are not authorized to edit this message
        HTTPException [404]: Message not found
        HTTPException [424]: Message not edited
    """
    DB = DataStorage(org_id)
    message = await get_message(org_id, room_id, message_id)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Message not found"
        )

    payload = request.dict(exclude_unset=True)
    if message["sender_id"] != payload["sender_id"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to edit this message",
        )

    message.update(payload)
    message["edited"] = True
    edited_message = await DB.update(
        MESSAGE_COLLECTION, document_id=message_id, data=message
    )

    if edited_message and edited_message.get("status_code") is None:
        # Publish to centrifugo in the background.
        background_tasks.add_task(
            centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, message
        )
        return JSONResponse(
            content=ResponseModel.success(data=message, message="Message edited"),
            status_code=status.HTTP_200_OK,
        )
    raise HTTPException(
        status_code=status.HTTP_424_FAILED_DEPENDENCY,
        detail={"message not edited": edited_message},
    )


@router.get(
    "/org/{org_id}/rooms/{room_id}/messages",
    response_model=Page[Message],
    status_code=status.HTTP_200_OK,
    responses={424: {"detail": "ZC Core failed"}},
)
async def get_messages(org_id, room_id):
    """Fetches all messages sent in a particular room.

    Args:
        org_id (str): A unique identifier of an organization
        room_id (str): A unique identifier of the room where messages are fetched from

    Returns:
        A list of message objects

    Raises:
        HTTPException [424]: Zc Core failed
    """
    response = await get_room_messages(org_id, room_id)
    if response is None or "status_code" in response:
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Zc Core failed",
        )
    # return JSONResponse(
    #     content=ResponseModel.success(data=response, message="Messages retrieved"),
    #     status_code=status.HTTP_200_OK,
    # )
    return paginate(response)


add_pagination(router)


@router.get(
    "/org/{org_id}/rooms/{room_id}/messages/{message_id}",
    response_model=ResponseModel,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"detail": "Message not found"},
    },
)
async def get_message_detail(
    org_id: str,
    room_id: str,
    message_id: str,
):
    """Retrieves a message in the room.
    Args:
        org_id (str): A unique identifier of an organisation
        room_id: A unique identifier of the room where the message is being sent to.
        message_id: A unique identifier of the message to be retrieved
    Returns:
        HTTP_200_OK {Message retrieved}:
        A dict containing data about the message in the room based on the message schema.

        {
            "_id": "61cb65f378fb01b18fac147b",
            "created_at": "2021-12-22 22:38:33.075643",
            "edited": true,
            "emojis": [
            {
                "count": 1,
                "emoji": "👹",
                "name": "smile",
                "reactedUsersId": [
                "619ba4671a5f54782939d385"
                ]
            }
            ],
            "files": [],
            "org_id": "619ba4671a5f54782939d384",
            "richUiData": {
            "blocks": [
                {
                "data": {},
                "depth": 0,
                "entityRanges": [],
                "inlineStyleRanges": [],
                "key": "eljik",
                "text": "HI, I'm mark.. new here",
                "type": "unstyled"
                }
            ],
            "entityMap": {}
            },
            "room_id": "619e28c31a5f54782939d59a",
            "saved_by": [],
            "sender_id": "619ba4671a5f54782939d385",
            "text": "string",
            "threads": []
        }

    Raises:
        HTTPException [404]: Message not found
    """
    message = await get_message(org_id, room_id, message_id)
    if message and message.get("status_code") is None:
        return JSONResponse(
            content=ResponseModel.success(data=message, message="message retrieved"),
            status_code=status.HTTP_200_OK,
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Message not found",
    )


@router.delete(
    "/org/{org_id}/rooms/{room_id}/message/{message_id}",
    response_model=ResponseModel,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"detail": "You are not authorized to delete this message"},
        404: {"detail": "message not found"},
        424: {"detail": "Failure to delete message"},
    },
)
async def delete_message(
    org_id: str,
    room_id: str,
    message_id: str,
    sender_id: str,
    background_tasks: BackgroundTasks,
):
    """Deletes a message in the room.
    Args:
        org_id: (str): A unique identifier of an organisation
        room_id: A unique identifier of the room.
        message_id: A unique identifier of the message to be retrieved
        sender_id: A unique identifier of the user who is deleting the message
    Returns:
        HTTP_200_OK {Message deleted}:
    Raises:
        HTTPException [401]: You are not authorized to delete this message,
        HTTPException [404]: Message not found,
        HTTPException [424]: Failure to delete message,
    """
    DB = DataStorage(org_id)
    message = await get_message(org_id, room_id, message_id)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found",
        )  # check if message exists

    if message.get("sender_id") != sender_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to delete this message",
        )  # check if person deleting is the sender of the message

    remove_message = await DB.delete(
        MESSAGE_COLLECTION,
        document_id=message_id,
    )

    if remove_message and remove_message.get("status_code") is None:
        # publish to centrifugo in the background
        background_tasks.add_task(
            centrifugo_client.publish,
            room_id,
            message_id,
            Events.MESSAGE_DELETE,
        )
        return JSONResponse(
            content=ResponseModel.success(
                data=remove_message, message="message deleted"
            ),
            status_code=status.HTTP_200_OK,
        )
    raise HTTPException(
        status_code=status.HTTP_424_FAILED_DEPENDENCY,
        detail="Failure to delete message",
    )


@router.put(
    "/org/{org_id}/rooms/{room_id}/messages/{message_id}/reaction",
    response_model=ResponseModel,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"description": "Invalid room member"},
        404: {"description": "Message not found"},
        424: {
            "description": "Failed to retrieve room members / Failed to add reaction or remove reaction"
        },
    },
)
async def reactions(
    request: Emoji,
    org_id: str,
    room_id: str,
    message_id: str,
    background_tasks: BackgroundTasks,
):
    """
    Checks if there are any reactions for the message.
    Adds a reaction to a message.
    Adds a user to list of reacted users if reaction already exists.
    Removes the user from the list of reacted users if user already reacted to the message.
    Removes a reaction from a message if reacted user count is 0.

    Args:
        request: Request object
        org_id: A unique identifier of the organization.
        room_id: A unique identifier of the room.
        message_id: A unique identifier of the message that is being edited.
        background_tasks: A daemon thread for publishing to centrifugo

    Returns:
        HTTP_200_OK {reaction added}:
        A dict containing data about the reaction that was added or removed.

        {
            "room_id": "619e28c31a5f54782939d59a",
            "message_id": "61cb65f378fb01b18fac147b",
            "emojis": [{
                "name": "lol",
                "count": 2,
                "emoji": "lol",
                "reactedUsersId": [
                    "619ba4671a5f54782939d385",
                    "6169704bc4133ddaa309dd07"
                ]
            }]
        }

    Raises:
        HTTPException [401]: Invalid room member
        HTTPException [404]: Message not found
        HTTPException [424]: Failed to retrieve room members
        HTTPException [424]: Failed to add reaction
        HTTPException [424]: Failed to remove reaction
    """
    DB = DataStorage(org_id)

    message = await get_message(org_id, room_id, message_id)  # get message
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found",
        )
    reactions = message.get("emojis")

    members = await get_room_members(org_id, room_id)  # retrieve room members
    if not members:
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Failed to retrieve room members",
        )
    # memberIds = list(members) # convert romm members to list

    new_reaction = request.dict()
    if new_reaction["reactedUsersId"][0] not in list(
        members
    ):  # check if user is in list of room members
        # if new_reaction["reactedUsersId"][0] not in memberIds: # check if user is a room member
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid room member",
        )

    # if no reactions exist for the message
    if not reactions:
        reactions = [new_reaction]
        updated_emoji = await DB.update(
            MESSAGE_COLLECTION, document_id=message_id, data={"emojis": reactions}
        )
        if updated_emoji and updated_emoji.get("status_code") is not None:
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail="Failed to add reaction",
            )
        # publish to centrifugo in the background
        background_tasks.add_task(
            centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, new_reaction
        )
        return JSONResponse(
            content=ResponseModel.success(data=new_reaction, message="reaction added"),
            status_code=status.HTTP_200_OK,
        )

    # if reactions exist for the message
    for emoji in reactions:
        if emoji["name"] == new_reaction["name"]:  # if emoji is already in reactions

            # if user hasn't reacted with the emoji
            if new_reaction["reactedUsersId"][0] not in emoji["reactedUsersId"]:
                emoji["reactedUsersId"].append(new_reaction["reactedUsersId"][0])
                emoji["count"] += 1

                added = await DB.update(
                    MESSAGE_COLLECTION,
                    document_id=message_id,
                    data={"emojis": reactions},
                )
                if added and added.get("status_code") is not None:
                    raise HTTPException(
                        status_code=status.HTTP_424_FAILED_DEPENDENCY,
                        detail="Failed to add reaction",
                    )
                # publish to centrifugo in the background
                background_tasks.add_task(
                    centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, emoji
                )
                return JSONResponse(
                    content=ResponseModel.success(data=emoji, message="reaction added"),
                    status_code=status.HTTP_200_OK,
                )

            # if user has reacted with the emoji
            emoji["reactedUsersId"].remove(new_reaction["reactedUsersId"][0])
            emoji["count"] -= 1

            if emoji["count"] != 0:  # if emoji count is not 0
                updated = await DB.update(
                    MESSAGE_COLLECTION,
                    document_id=message_id,
                    data={"emojis": reactions},
                )
                if updated and updated.get("status_code") is not None:
                    raise HTTPException(
                        status_code=status.HTTP_424_FAILED_DEPENDENCY,
                        detail="Failed to remove user's reaction",
                    )
                # publish to centrifugo in the background
                background_tasks.add_task(
                    centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, emoji
                )
                return JSONResponse(
                    content=ResponseModel.success(
                        data=emoji, message="user's reaction removed"
                    ),
                    status_code=status.HTTP_200_OK,
                )

            reactions.remove(emoji)  # if emoji count is 0
            removed = await DB.update(
                MESSAGE_COLLECTION, document_id=message_id, data={"emojis": reactions}
            )
            if removed and removed.get("status_code") is not None:
                raise HTTPException(
                    status_code=status.HTTP_424_FAILED_DEPENDENCY,
                    detail="Failed to remove reaction",
                )
            # publish to centrifugo in the background
            background_tasks.add_task(
                centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, removed
            )
            return JSONResponse(
                content=ResponseModel.success(data=emoji, message="reaction removed"),
                status_code=status.HTTP_200_OK,
            )

    # if emoji is not in reactions
    reactions.append(new_reaction)
    new = await DB.update(
        MESSAGE_COLLECTION, document_id=message_id, data={"emojis": reactions}
    )
    if new and new.get("status_code") is not None:
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Failed to add reaction",
        )
    # publish to centrifugo in the background
    background_tasks.add_task(
        centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, new_reaction
    )
    return JSONResponse(
        content=ResponseModel.success(data=new_reaction, message="reaction added"),
        status_code=status.HTTP_200_OK,
    )
