from fastapi import APIRouter, BackgroundTasks, HTTPException, status, Body
from schema.message import Message, MessageRequest, Emoji, Thread
from schema.response import ResponseModel
from schema.custom import ObjId
from starlette.responses import JSONResponse
from typing import Dict, List
from utils.centrifugo import Events, centrifugo_client
from utils.db import DataStorage
from utils.message_utils import (MESSAGE_COLLECTION, get_message,
                                 get_room_messages)
from utils.room_utils import get_room_members, get_room
from schema.custom import ObjId

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

    message["richUiData"] = payload["richUiData"]
    payload["edited"] = True
    edited_message = await DB.update(
        MESSAGE_COLLECTION, document_id=message_id, data=payload
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
    response_model=ResponseModel,
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
    return JSONResponse(
        content=ResponseModel.success(data=response, message="Messages retrieved"),
        status_code=status.HTTP_200_OK,
    )


@router.get(
    "/org/{org_id}/rooms/{room_id}/messages/{message_id}",
    response_model=ResponseModel,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"detail": "Message not found"},
    },
)
async def get_message_by_id(
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
            "_id": "61c3aa9478fb01b18fac1465",
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
        ) # check if message exists
        
    if message.get("sender_id") != sender_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to delete this message",
        ) # check if person deleting is the sender of the message
    
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
                data=remove_message, 
                message="message deleted"
                ),
            status_code=status.HTTP_200_OK,
        )
    raise HTTPException(
        status_code=status.HTTP_424_FAILED_DEPENDENCY,
        detail="Failure to delete message",
    )
    
           
        

@router.put(
    "/org/{org_id}/rooms/{room_id}/messages/{message_id}/reactions/addcheck",
    response_model=ResponseModel,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"description": "Invalid room member"},
        404: {"description": "message not found"},
        424: {"description": "reaction not added"},
    },
)
async def add_reaction(
    request: Emoji,
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
                "name": "lol",
                "count": 1,
                "emoji": "😂",
                "reactedUsersId": ["619ba4671a5f54782939d385"]
            }

    Raises:
        HTTPException [401]: Invalid room member
        HTTPException [404]: Message not found
        HTTPException [424]: Reaction not added
    """
    DB = DataStorage(org_id)
    
    message = await get_message(org_id, room_id, message_id) # retrieve message
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found",
        ) # check if message exists
    react = message.get("emojis") # get reactions
    
    new_reaction = request.dict()
    
    members = await get_room_members(org_id, room_id) # retrieve room members
    # memberIds = list(members)
    memberIds = str(list(members))
    print (memberIds)
    
    if new_reaction["reactedUsersId"] not in memberIds:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid room member",
        )
    
    for reaction in react:
        if reaction["name"] == new_reaction["name"]:
            if reaction["reactedUsersId"] not in reaction["reactedUsersId"]:
                reaction["reactedUsersId"].append(new_reaction["reactedUsersId"])
                reaction["count"] += 1
                
                print (reaction)
                
                added = await DB.update(
                    MESSAGE_COLLECTION, document_id=message_id, data={"emojis": reaction}
                )
                
                if added:    
                    data = {
                        "room_id": room_id,
                        "message_id": message_id,
                        "emojis": [reaction],
                    }
                    background_tasks.add_task(
                        centrifugo_client.publish,
                        room_id,
                        message_id,
                        Events.MESSAGE_UPDATE,
                    )
                    return JSONResponse(
                        content=ResponseModel.success(
                            data=data, message="reaction added successfully"
                        ),
                        status_code=status.HTTP_200_OK,
                    )
                raise HTTPException(
                    status_code=status.HTTP_424_FAILED_DEPENDENCY,
                    detail="Failure to add reaction",
                )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Reaction already exists",
            )
            
        react.append(new_reaction)
        added = await DB.update(
            MESSAGE_COLLECTION, document_id=message_id, data={"emojis": new_reaction}
            )
        if added:
            data = {
                "room_id": room_id,
                "message_id": message_id,
                "emojis": [new_reaction],
                }
            background_tasks.add_task(
                centrifugo_client.publish,
                room_id,
                message_id,
                Events.MESSAGE_UPDATE,
            )
            return JSONResponse(
                content=ResponseModel.success(
                data=data, message="reaction added successfully"
                 ),
                status_code=status.HTTP_200_OK,
                )
        raise HTTPException(        
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Failure to add reaction",
            )
            
                    
                