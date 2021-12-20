from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from schema.message import Message, MessageRequest, MessageUpdate, Reaction
from schema.response import ResponseModel
from starlette.responses import JSONResponse
from utils.centrifugo import Events, centrifugo_client
from utils.db import DataStorage
from utils.message_utils import (MESSAGE_COLLECTION, get_message,
                                 get_room_messages)
from utils.room_utils import get_room_members

router = APIRouter()


@router.post(
    "/org/{org_id}/rooms/{room_id}/sender/{sender_id}/messages",
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
    sender_id,
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
                "room_id": "61b3fb328f945e698c7eb396",
                "message_id": "61696f43c4133ddga309dcf6",
                "text": "str",
                "files": "HTTP url(s)"
                "sender_id": "619ba4671a5f54782939d385"
            }
    Raises:
        HTTPException [404]: Sender not in room
        HTTPException [404]: Room does not exist
        HTTPException [424]: "message not sent"
    """
    DB = DataStorage(org_id)
    message_obj = Message(
        **request.dict(), org_id=org_id, room_id=room_id, sender_id=sender_id
    )
    response = await DB.write(MESSAGE_COLLECTION, message_obj.dict())

    if response and response.get("status_code") is None:
        message_obj.message_id = response["data"]["object_id"]
        output_data = {
            "room_id": message_obj.room_id,
            "message_id": message_obj.message_id,
            "sender_id": message_obj.sender_id,
            "text": message_obj.text,
            "files": message_obj.files,
        }
        background_tasks.add_task(
            centrifugo_client.publish, room_id, Events.MESSAGE_CREATE, output_data
        )  # publish to centrifugo in the background
        return JSONResponse(
            content=ResponseModel.success(data=output_data, message="new message sent"),
            status_code=status.HTTP_201_CREATED,
        )
    raise HTTPException(
        status_code=status.HTTP_424_FAILED_DEPENDENCY,
        detail={"Message not sent": response},
    )


@router.get(
    "/org/{org_id}/rooms/{room_id}/messages",
    response_model=ResponseModel,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"detail": "Messages not found"},
        424: {"detail": "Failure to retrieve data"},
    },
)
async def get_all_messages(
    org_id: str,
    room_id: str,
):
    """Reads all messages in the collection.

    Args:
        org_id (str): A unique identifier of an organisation
        room_id: A unique identifier of the room where the message is being sent to.

    Returns:
        HTTP_200_OK {Messages retrieved}:
        A list containing data about all the messages in the collection.
        [
            {
                "_id": "61b8caec78fb01b18fac1410",
                "created_at": "2021-12-14 16:40:43.302519",
                "files": [],
                "message_id": null,
                "org_id": "619ba4671a5f54782939d384",
                "reactions": [
                    {
                        "character": "wink",
                        "sender_id": "6169704bc4133ddaa309dd07"
                    }
                ],
                "room_id": "619e28c31a5f54782939d59a",
                "saved_by": [],
                "sender_id": "61696f5ac4133ddaa309dcfe",
                "text": "testing messages",
                "threads": []
            }
        ]

    Raises:
        HTTPException [404]: Messages not found
        HTTPException [424]: Failure to retrieve data
    """
    messages = await get_room_messages(org_id, room_id)
    try:
        if messages:
            return JSONResponse(
                content=ResponseModel.success(
                    data=messages, message="Messages retrieved"
                ),
                status_code=status.HTTP_200_OK,
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"Messages not found": messages},
        )
    except HTTPException as error:
        raise HTTPException(
            data="Failure to retrieve data",
            status=status.HTTP_424_FAILED_DEPENDENCY,
        ) from error


@router.get(
    "/org/{org_id}/rooms/{room_id}/messages/{message_id}",
    response_model=ResponseModel,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"detail": "Message not found"},
        424: {"detail": "Failure to retrieve data"},
    },
)
async def get_message_by_id(
    org_id: str,
    room_id: str,
    message_id: str,
):
    """Retrieves a message in the collection.

    Args:
        org_id (str): A unique identifier of an organisation
        room_id: A unique identifier of the room where the message is being sent to.
        message_id: A unique identifier of the message to be retrieved

    Returns:
        HTTP_200_OK {Message retrieved}:
        A dict containing data about the message in the collection based on the message schema.
        {
            "_id": "61b8caec78fb01b18fac1410",
            "created_at": "2021-12-14 16:40:43.302519",
            "files": [
                "https://cdn.iconscout.com/icon/free/png-256/"
            ],
            "message_id": null,
            "org_id": "619ba4671a5f54782939d384",
            "reactions": [
                {
                    "character": "wink",
                    "sender_id": "6169704bc4133ddaa309dd07"
                }
            ],
            "room_id": "619e28c31a5f54782939d59a",
            "saved_by": [],
            "sender_id": "61696f5ac4133ddaa309dcfe",
            "text": "testing messages",
            "threads": []
        }

    Raises:
        HTTPException [404]: Message not found
        HTTPException [424]: Failure to retrieve data
    """
    message = await get_message(org_id, room_id, message_id)
    try:
        if message:
            return JSONResponse(
                content=ResponseModel.success(
                    data=message, message="message retrieved"
                ),
                status_code=status.HTTP_200_OK,
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"Message not found": message},
        )
    except HTTPException as error:
        raise HTTPException(
            data="Failure to retrieve data",
            status=status.HTTP_424_FAILED_DEPENDENCY,
        ) from error


# @router.put(
#     "/org/{org_id}/rooms/{room_id}/messages/{message_id}",
#     response_model=ResponseModel,
#     status_code=status.HTTP_200_OK,
#     responses={
#         401: {
#             "description": "you are not authorized to edit this message"
#         },
#         404: {"description": "message not found"},
#         424: {"description": "message not edited"},
#         424: {
#             "description": "Failure to publish to centrifugo"
#         },
#     },
# )
# async def update_message_old(
#     request: MessageUpdate,
#     org_id: str,
#     room_id: str,
#     message_id: str,
#     background_tasks: BackgroundTasks,
# ):
#     """
#     Update a message

#     Args:
#         request: Request object
#         org_id: A unique identifier of the organization.
#         room_id: A unique identifier of the room.
#         message_id: A unique identifier of the message that is being edited.
#         background_tasks: A daemon thread for publishing to centrifugo

#     Returns:
#         HTTP_200_OK {message updated successfully}:
#         A dict containing data about the message that was edited.
#             {
#                 "room_id": "619e28c31a5f54782939d59a",
#                 "message_id": "61ba9b0378fb01b18fac1420",
#                 "sender_id": "619ba4671a5f54782939d385",
#                 "text": "xxxxxxxxxxxxxxxxx"
#             }

#     Raises:
#         HTTPException [401]: You are not authorized to edit this message
#         HTTPException [404]: Message not found
#         HTTPException [424]: Message not edited
#         HTTPException [424]: Failure to publish to centrifugo
#     """
#     DB = DataStorage(org_id)
#     message = await get_message(org_id, room_id, message_id)
#     if message:
#         payload = request.dict()
#         if message["sender_id"] == payload["sender_id"]:
#             edited_message = await DB.update(
#                 MESSAGE_COLLECTION, document_id=message_id, data=payload
#             )
#             if edited_message:
#                 new_data = {
#                     "room_id": room_id,
#                     "message_id": message_id,
#                     "sender_id": payload["sender_id"],
#                     "text": payload["text"],
#                 }
#                 try:
#                     background_tasks.add_task(
#                         centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, new_data
#                     )  # publish to centrifugo in the background
#                     return JSONResponse(
#                         content=ResponseModel.success(data=new_data, message="message edited"),
#                         status_code=status.HTTP_200_OK,
#                     )
#                 except Exception as error:
#                     raise HTTPException(
#                         status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                         detail={"Failure to publish to centrifugo"},
#                     ) from error
#             raise HTTPException(
#                 status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                 detail={"message not edited": edited_message},
#             )
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="You are not authorized to edit this message",
#         )
#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND, 
#         detail="Message not found"
#         )


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
    request: MessageUpdate,
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

    Returns:
        HTTP_200_OK {Message edited}:
        A dict containing data about the message that was edited.
            {
                "room_id": "619e28c31a5f54782939d59a",
                "message_id": "61ba9b0378fb01b18fac1420",
                "sender_id": "619ba4671a5f54782939d385",
                "text": "xxxxxxxxxxxxxxxxx"
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

    payload = request.dict()
    if message["sender_id"] != payload["sender_id"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to edit this message",
        )

    edited_message = await DB.update(
        MESSAGE_COLLECTION, document_id=message_id, data=payload
    )
    if edited_message:
        new_data = {
            "room_id": room_id,
            "message_id": message_id,
            "sender_id": payload["sender_id"],
            "text": payload["text"],
            "edited": True,
        }
        try:
            background_tasks.add_task(
                centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, new_data
            )  # publish to centrifugo in the background
            return JSONResponse(
                content=ResponseModel.success(data=new_data, message="Message edited"),
                status_code=status.HTTP_200_OK,
            )
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail={"Failure to publish to centrifugo"},
            ) from error
    raise HTTPException(
        status_code=status.HTTP_424_FAILED_DEPENDENCY,
        detail={"message not edited": edited_message},
    )


@router.put(
    "/org/{org_id}/rooms/{room_id}/messages/{message_id}/reactions",
    response_model=ResponseModel,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"description": "invalid room member"},
        404: {"description": "message not found"},
        424: {"description": "Message not updated"},
        424: {"description": "Failure to publish to centrifugo"},
    },
)
async def add_or_remove_reaction(
    request: Reaction,
    org_id: str,
    room_id: str,
    message_id: str,
    background_tasks: BackgroundTasks,
):
    """
    Retrieves the message
    Checks if the user reacting to the message is a member of the room.
    Check if reaction is already in the message reactions array
    Add/removes a reaction to/from the message.
    - A payload consisting of the sender_id and character is added to the reactions array.
    - If the same payload is already in the reactions array, the reaction is removed.

    Args:
        request: Request object
        org_id: A unique identifier of the organization.
        room_id: A unique identifier of the room.
        message_id: A unique identifier of the message.

    Returns:
        - For reactions added.
        HTTP_200_OK {reaction added}

        - For reactions removed.
        HTTP_200_OK {reaction removed}

        A dict containing data about the reaction that was added or removed (response_output).
       {
            "room_id": "619e28c31a5f54782939d59a",
            "message_id": "61bc6b6078fb01b18fac1427",
            "reactions": [
                {
                    "sender_id": "619ba4671a5f54782939d385",
                    "character": "taxi"
                }
            ]
        }

    Raises:
        HTTPException [401]: Invalid room member
        HTTPException [404]: Message not found
        HTTPException [424]: Message not updated
        HTTPException [424]: Failure to publish to centrifugo
    """
    DB = DataStorage(org_id)
    message = await get_message(org_id, room_id, message_id)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Message not found"
        )

    new_reaction = {"sender_id": request.sender_id, "character": request.character}

    members = await get_room_members(org_id, room_id)
    if (
        new_reaction["sender_id"] not in members
    ):  # check if the user reacting to message is a room member
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid room member"
        )

    emoji = message["reactions"]
    if (
        new_reaction not in emoji
    ):  # check if reaction is already in the message reactions array

        emoji.append(new_reaction)  # add reaction to reactions array
        added = await DB.update(
            MESSAGE_COLLECTION, document_id=message_id, data={"reactions": emoji}
        )
        if added:
            data = {
                "room_id": room_id,
                "message_id": message_id,
                "reactions": [
                    {
                        "sender_id": new_reaction["sender_id"],
                        "character": new_reaction["character"],
                    }
                ],
            }
            try:
                background_tasks.add_task(
                    centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, data
                )  # publish to centrifugo in the background
                return JSONResponse(
                    content=ResponseModel.success(data=data, message="reaction added"),
                    status_code=status.HTTP_200_OK,
                )
            except Exception as error:
                raise HTTPException(
                    status_code=status.HTTP_424_FAILED_DEPENDENCY,
                    detail={"Failure to publish to centrifugo"},
                ) from error
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY, detail={"Reaction not added"}
        )

    emoji.remove(new_reaction)  # remove reaction from reactions array
    removed = await DB.update(
        MESSAGE_COLLECTION, document_id=message_id, data={"reactions": emoji}
    )
    if removed:
        data = {
            "room_id": room_id,
            "message_id": message_id,
            "reactions": [
                {
                    "sender_id": new_reaction["sender_id"],
                    "character": new_reaction["character"],
                }
            ],
        }
        try:
            background_tasks.add_task(
                centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, data,
            )  # publish to centrifugo in the background

            return JSONResponse(
                content=ResponseModel.success(data=data, message="reaction removed"),
                status_code=status.HTTP_200_OK,
            )
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail={"Failure to publish to centrifugo"},
            ) from error
    raise HTTPException(
        status_code=status.HTTP_424_FAILED_DEPENDENCY,
        detail={"Reaction not removed"},
    )


@router.put(
    "/org/{org_id}/rooms/{room_id}/messages/{message_id}/reactions/add",
    response_model=ResponseModel,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"description": "Invalid room member"},
        404: {"description": "message not found"},
        424: {"description": "reaction not added"},
        424: {"description": "Failure to publish to centrifugo"},
    },
)
async def add_reaction(
    request: Reaction,
    org_id: str,
    room_id: str,
    message_id: str,
    background_tasks: BackgroundTasks,
):
    """
    Add a reaction to a message

    Args:
        request: Request object
        org_id: A unique identifier of the organization.
        room_id: A unique identifier of the room.
        message_id: A unique identifier of the message that is being edited.
        background_tasks: A daemon thread for publishing to centrifugo

    Returns:
        HTTP_200_OK {reaction added successfully}:
        A dict containing data about the reaction that was added.
            {
                "room_id": "619e28c31a5f54782939d59a",
                "message_id": "61ba9b0378fb01b18fac1420",
                "sender_id": "619ba4671a5f54782939d385",
                "character": "lol"
            }

    Raises:
        HTTPException [401]: Invalid room member
        HTTPException [404]: Message not found
        HTTPException [409]: Reaction already exists
        HTTPException [424]: Reaction not added
        HTTPException [424]: Failure to publish to centrifugo
    """
    DB = DataStorage(org_id)
    members = await get_room_members(org_id, room_id)
    message = await get_message(org_id, room_id, message_id)

    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    react = message["reactions"]

    payload = {
        "sender_id": request.sender_id,
        "character": request.character
        }

    if (
        payload["sender_id"] not in members
    ):  # check if the user reacting to message is a room member
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid room member"
        )

    if (
        payload not in react
    ):  # check if reaction is already in the message reactions array

        react.append(payload)  # add reaction to reactions array
        added = await DB.update(
            MESSAGE_COLLECTION, document_id=message_id, data={"reactions": react}
        )
        if added:
            data = {
                "room_id": room_id,
                "message_id": message_id,
                "reactions": [
                    {
                        "sender_id": payload["sender_id"],
                        "character": payload["character"],
                    }
                ],
            }
            try:
                background_tasks.add_task(
                    centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, data
                )  # publish to centrifugo in the background
                return JSONResponse(
                    content=ResponseModel.success(data=data, message="reaction added"),
                    status_code=status.HTTP_200_OK
                )
            except Exception as error:
                raise HTTPException(
                    status_code=status.HTTP_424_FAILED_DEPENDENCY,
                    detail={"Failure to publish to centrifugo"},
                ) from error
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail={"Reaction not added"}
        )
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail={"Reaction already exists"}
    )


@router.delete(
    "/org/{org_id}/rooms/{room_id}/messages/{message_id}/reactions/remove",
    response_model=ResponseModel,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"description": "Invalid room member"},
        404: {"description": "Reaction not found"},
        404: {"description": "message not found"},
        424: {"description": "reaction not removed"},
        424: {"description": "Failure to publish to centrifugo"},
    },
)
async def remove_reaction(
    request: Reaction,
    org_id: str,
    room_id: str,
    message_id: str,
    background_tasks: BackgroundTasks,
):
    """
    Remove a reaction to a message

    Args:
        request: Request object
        org_id: A unique identifier of the organization.
        room_id: A unique identifier of the room.
        message_id: A unique identifier of the message that is being edited.
        background_tasks: A daemon thread for publishing to centrifugo

    Returns:
        HTTP_200_OK {reaction removed successfully}:
        A dict containing data about the reaction that was removed.
        {
            "room_id": "619e28c31a5f54782939d59a",
            "message_id": "61ba9b0378fb01b18fac1420",
            "sender_id": "619ba4671a5f54782939d385",
            "character": "lol"
        }

    Raises:
        HTTPException [401]: Invalid room member
        HTTPException [404]: Message not found
        HTTPException [424]: Reaction not removed
        HTTPException [424]: Failure to publish to centrifugo
    """
    DB = DataStorage(org_id)
    members = await get_room_members(org_id, room_id)
    message = await get_message(org_id, room_id, message_id)

    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    react = message["reactions"]

    payload = {
        "sender_id": request.sender_id,
        "character": request.character
        }

    if (
        payload["sender_id"] not in members
    ):  # check if the user reacting to message is a room member
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid room member"
        )

    if (
        payload in react
    ):  # check if reaction is already in the message reactions array
        react.remove(payload)
        removed = await DB.update(
            MESSAGE_COLLECTION, document_id=message_id, data={"reactions": react}
        )
        if removed:
            data = {
                "room_id": room_id,
                "message_id": message_id,
                "reactions": [
                    {
                        "sender_id": payload["sender_id"],
                        "character": payload["character"],
                    }
                ],
            }
            try:
                background_tasks.add_task(
                    centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, data
                )  # publish to centrifugo in the background
                return JSONResponse(
                    content=ResponseModel.success(data=data, message="reaction removed"),
                    status_code=status.HTTP_200_OK
                )
            except Exception as error:
                raise HTTPException(
                    status_code=status.HTTP_424_FAILED_DEPENDENCY,
                    detail={"Failure to publish to centrifugo"},
                ) from error
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail={"Reaction not removed"}
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"Reaction not found"}
    )
