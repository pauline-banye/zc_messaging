from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from schema.message import Emoji, Message, MessageRequest
from schema.response import ResponseModel
from starlette.responses import JSONResponse
from utils.centrifugo import Events, centrifugo_client
from utils.message_utils import (create_message, edit_message,
                                 get_member_emoji, get_message,
                                 get_room_messages, toggle_reaction,
                                 update_reaction)
from utils.room_utils import get_room

router = APIRouter()


@router.post(
    "/org/{org_id}/rooms/{room_id}/messages",
    response_model=ResponseModel,
    status_code=status.HTTP_201_CREATED,
    responses={
        404: {"description": "Room or sender not found"},
        424: {"description": "ZC Core failed"},
    },
)
async def send_message(
    org_id: str,
    room_id: str,
    request: MessageRequest,
    background_tasks: BackgroundTasks,
):
    """Creates and sends a message from a user inside a room.

    Registers a new document to the messages database collection while
    publishing to all members of the room in the background.

    Args:
        org_id (str): A unique identifier of an organisation.
        request (MessageRequest): A pydantic schema that defines the message request parameters.
        room_id (str): A unique identifier of the room where the message is being sent to.
        background_tasks (BackgroundTasks): A background task for publishing to all
                                            members of the room.

    Returns:
        A dict containing data about the message that was created.

        {
            "status": "success",
            "message": "new message sent",
            "data": {
                "sender_id": "619bab3b1a5f54782939d400",
                "emojis": [],
                "richUiData": {
                "blocks": [
                    {
                    "key": "eljik",
                    "text": "Larry Gaaga",
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
                "timestamp": 0,
                "created_at": "2022-02-01 19:20:55.891264",
                "room_id": "61e6855e65934b58b8e5d1df",
                "org_id": "619ba4671a5f54782939d384",
                "message_id": "61f98d0665934b58b8e5d286",
                "edited": false,
                "threads": []
            }
        }

    Raises:
        HTTPException [404]: Room does not exist || Sender not a member of this room.
        HTTPException [424]: Message not sent.
    """

    message = Message(**request.dict(), org_id=org_id, room_id=room_id)

    response = await create_message(org_id=org_id, message=message)

    if not response or response.get("status_code"):
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail={"Message not sent": response},
        )

    message.message_id = response["data"]["object_id"]

    # Publish to centrifugo in the background.
    background_tasks.add_task(
        centrifugo_client.publish,
        room_id,
        Events.MESSAGE_CREATE,
        message.dict(),
    )

    return JSONResponse(
        content=ResponseModel.success(data=message.dict(), message="new message sent"),
        status_code=status.HTTP_201_CREATED,
    )


@router.put(
    "/org/{org_id}/rooms/{room_id}/messages/{message_id}",
    response_model=ResponseModel,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"description": "You are not authorized to edit this message"},
        404: {"description": "Message not found"},
        424: {"description": "Message not edited"},
    },
)
async def update_message(
    org_id: str,
    room_id: str,
    message_id: str,
    request: MessageRequest,
    background_tasks: BackgroundTasks,
):
    """Updates a message sent in a room.

    Edits an existing message document in the messages database collection while
    publishing to all members of the room in the background.

    Args:
        org_id: A unique identifier of the organization.
        room_id: A unique identifier of the room.
        message_id: A unique identifier of the message that is being edited.
        request: A pydantic schema that defines the message request parameters.
        background_tasks: A background task for publishing to all
                          members of the room.

    Returns:
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
                "room_id": "61e75a0a65934b58b8e5d222",
                "saved_by": [],
                "sender_id": "619ba4671a5f54782939d385",
                "text": "string",
                "threads": []
            }

    Raises:
        HTTPException [401]: You are not authorized to edit this message.
        HTTPException [404]: Message not found.
        HTTPException [424]: Message not edited.
    """
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

    edited_message = await edit_message(org_id, message_id, payload)

    if not edited_message or edited_message.get("status_code"):
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail={"message not edited": edited_message},
        )

    payload["edited"] = True
    message.update(payload)

    # Publish to centrifugo in the background.
    background_tasks.add_task(
        centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, message
    )

    return JSONResponse(
        content=ResponseModel.success(data=message, message="Message edited"),
        status_code=status.HTTP_200_OK,
    )


@router.get(
    "/org/{org_id}/rooms/{room_id}/messages",
    response_model=ResponseModel,
    status_code=status.HTTP_200_OK,
    responses={424: {"detail": "ZC Core failed"}},
)
async def get_messages(org_id: str, room_id: str):
    """Fetches all messages sent in a particular room.

    Args:
        org_id (str): A unique identifier of an organization.
        room_id (str): A unique identifier of the room where messages are fetched from.

    Returns:
        A dict containing a list of message objects.
        {
            "status": "success",
            "message": "Messages retrieved",
            "data": [
                {
                "_id": "61e75bc065934b58b8e5d223",
                "created_at": "2022-02-02 17:57:02.630439",
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
                ...
                },
                {...},
                ...
            ]
        }

    Raises:
        HTTPException [424]: Zc Core failed
    """

    response = await get_room_messages(org_id, room_id)
    if response == []:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room does not exist or no message found",
        )

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Zc Core failed",
        )

    return JSONResponse(
        content=ResponseModel.success(data=response, message="Messages retrieved"),
        status_code=status.HTTP_200_OK,
    )


@router.put(
    "org/{org_id}/rooms/{room_id}/messages/{message_id}/reactions",
    response_model=ResponseModel,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"description": "Invalid room member"},
        404: {"description": "Message not found || Room not found"},
        424: {"description": "Failed to add reaction || Failed to update reaction"},
    },
)
async def message_reaction(
    request: Emoji,
    org_id: str,
    room_id: str,
    message_id: str,
    background_tasks: BackgroundTasks,
):
    """Checks if there are any reactions for the message.
        Adds or removes a reaction to and from a message
        Adds a user to the list of reacted users if reaction already exists.
        Removes a user's reaction if a duplicate payload is sent.

    Args:
        request: Request object
        org_id: A unique identifier of the organization.
        room_id: A unique identifier of the room.
        message_id: A unique identifier of the message that is being edited.
        background_tasks: A daemon thread for publishing to centrifugo

    Returns:
        HTTP_200_OK {Reaction added successfully || Reaction updated successfully}}:
        A dict containing data about the reaction that was added.

        {
            "status": "success",
            "message": "Reaction updated successfully",
            "data": {
                "count": 3,
                "emoji": "lol",
                "name": "lol",
                "reactedUsersId": [
                    "6169704bc4133ddaa309dd07",
                    "619bab3b1a5f54782939d400",
                    "61696f5ac4133ddaa309dcfe"
                ]
            }
        }

    Raises:
        HTTPException [401]: Invalid room member
        HTTPException [404]: Message not found || Room not found
        HTTPException [424]: Failed to add reaction || Failed to update reaction
    """
    message = await get_message(org_id, room_id, message_id)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found",
        )
    reactions = message.get("emojis")

    room = await get_room(org_id, room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found",
        )
    members = room.get("room_members", {})

    reaction_payload = request.dict()
    if reaction_payload["reactedUsersId"][0] not in list(members):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid room member",
        )

    if reactions:
        if emoji := get_member_emoji(reaction_payload["name"], reactions):
            toggle_reaction(emoji, Emoji(**reaction_payload), reactions)

            updated_reaction = await update_reaction(org_id, message)
            if not updated_reaction:
                raise HTTPException(
                    status_code=status.HTTP_424_FAILED_DEPENDENCY,
                    detail="Failed to update reaction",
                )
            # publish to centrifugo in the background
            background_tasks.add_task(
                centrifugo_client.publish,
                room_id,
                Events.MESSAGE_UPDATE,
                reaction_payload,
            )
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=ResponseModel.success(
                    data=emoji,
                    message="Reaction updated successfully",
                ),
            )

    reactions.append(reaction_payload)
    new_reaction = await update_reaction(org_id, message)
    if not new_reaction:
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Failed to add reaction",
        )
    # publish to centrifugo in the background
    background_tasks.add_task(
        centrifugo_client.publish,
        room_id,
        Events.MESSAGE_UPDATE,
        reaction_payload,
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=ResponseModel.success(
            data=reaction_payload,
            message="Reaction added successfully",
        ),
    )
