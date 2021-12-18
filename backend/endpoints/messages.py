from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from schema.message import Message, MessageRequest, MessageUpdate, Reaction
from schema.response import ResponseModel
from starlette.responses import JSONResponse
from utils.centrifugo import Events, centrifugo_client
from utils.db import DataStorage
from utils.mssg_utils import get_mssg
from utils.room_utils import get_room_members


router = APIRouter()

MESSAGE_COLLECTION = "messages"


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
        HTTP_200_OK {messages retrieved}:
        A list containing data about all the messages in the collection.
            {
                "status": "success",
                "message": "messages retrieved",
                "data": [
                    {
                    "_id": "61b8ca9878fb01b18fac140f",
                    "created_at": "2021-12-15 20:49:52.445747",
                    "files": [
                        "https://cdn.iconscout.com/icon/free/png-256/"
                    ],
                    "message_id": null,
                    "org_id": "619ba4671a5f54782939d384",
                    "reactions": [],
                    "room_id": "619e28c31a5f54782939d59a",
                    "saved_by": [],
                    "sender_id": "61696f5ac4133ddaa309dcfe",
                    "text": "test after switching back to Any",
                    "threads": []
                    }
                ]

    Raises:
        HTTP_404_NOT_FOUND: "Messages not found"
    """
    DB = DataStorage(org_id)
    messages = await DB.read(MESSAGE_COLLECTION, {"org_id": org_id, "room_id": room_id})

    try:
        if messages:
            return JSONResponse(
                content=ResponseModel.success(
                    data=messages, message="messages retrieved"
                ),
                status_code=status.HTTP_200_OK,
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"Messages not found": messages},
        )
    except Exception as e:
        raise e


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
    """Retrieves a message in the collection.

    Args:
        org_id (str): A unique identifier of an organisation
        room_id: A unique identifier of the room where the message is being sent to.
        message_id: A unique identifier of the message to be retrieved

    Returns:
        HTTP_200_OK {message retrieved}:
        A dict containing data about the message in the collection based on the message schema.
            {
                "status": "success",
                "message": "message retrieved",
                "data": {
                    "_id": "61bc6b6078fb01b18fac1427",
                    "created_at": "2021-12-17 10:47:22.673050",
                    "files": [],
                    "message_id": null,
                    "org_id": "619ba4671a5f54782939d384",
                    "reactions": [],
                    "room_id": "619e28c31a5f54782939d59a",
                    "saved_by": [],
                    "sender_id": "619ba4671a5f54782939d385",
                    "text": "yet another check",
                    "threads": []
                    }
                }
                
    Raises:
        HTTP_HTTP_404_NOT_FOUND: Message not found
    """
    DB = DataStorage(org_id)
    message = await DB.read(
        MESSAGE_COLLECTION, {"org_id": org_id, "room_id": room_id, "_id": message_id}
    )
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
    except Exception as e:
        raise e
   

@router.put(
    "/org/{org_id}/rooms/{room_id}/messages/{message_id}",
    response_model=ResponseModel,
    responses={
        status.HTTP_200_OK: {"description": "message edited"},
        status.HTTP_404_NOT_FOUND: {"description": "message not found"},
        status.HTTP_403_FORBIDDEN: {
            "description": "you are not authorized to edit this message"
        },
        status.HTTP_424_FAILED_DEPENDENCY: {"description": "message not edited"},
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
        sender_id: A unique identifier of the sender.
        message_id: A unique identifier of the message that is being edited.

    Returns:
        HTTP_200_OK {message updated successfully}:
        A dict containing data about the message that was updated (response_output).
            {
                "room_id": "619e28c31a5f54782939d59a",
                "message_id": "61bc5e5378fb01b18fac1426",
                "sender_id": "619ba4671a5f54782939d385",
                "text": "testing edits",
                "edited_at": "2021-12-17 11:47:22.678046"
            }

    Raises:
        HTTP_404_FAILED_DEPENDENCY: Message not found
        HTTP_424_FAILED_DEPENDENCY: Message not edited
        HTTP_403_FORBIDDEN: You are not authorized to edit this message
    """
    DB = DataStorage(org_id)
    message = await get_mssg(org_id=org_id, room_id=room_id, message_id=message_id)

    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Message not found"
        )

    payload = request.dict()
    if message["sender_id"] != payload["sender_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to edit this message",
        )
        
    try:
        edit_message = await DB.update(
            MESSAGE_COLLECTION, document_id=message_id, data=payload
        )
        if edit_message:
            data = {
                "room_id": room_id,
                "message_id": message_id,
                "sender_id": payload["sender_id"],
                "text": payload["text"],
                "edited_at": payload["edited_at"],
            }
            background_tasks.add_task(
                centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, data
            )  # publish to centrifugo in the background
            return JSONResponse(
                content=ResponseModel.success(
                    data=data, message="message edited"
                ),
                status_code=status.HTTP_200_OK,
            )
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail={"message not edited": edit_message},
        )
    except Exception as e:
        raise e


@router.put(
    "/org/{org_id}/rooms/{room_id}/messages/{message_id}/reactions",
    response_model=ResponseModel,
    responses={
        status.HTTP_200_OK: {"description": "reaction added"},
        status.HTTP_403_FORBIDDEN: {"description": "invalid room member"},
        status.HTTP_404_NOT_FOUND: {"description": "message not found"},
        status.HTTP_424_FAILED_DEPENDENCY: {"description": "Message not updated"}
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
    Checks if the user reacting to the message is a member of the room.
    Add/removes a reaction to/from a message. 
    If a reaction is added, a payload consisting of the sender_id and character is added to the reactions array.
    If the same payload is already in the reactions array, the reaction is removed.
    
    Args:
        request: Request object
        org_id: A unique identifier of the organization.
        room_id: A unique identifier of the room.
        message_id: A unique identifier of the message.

    Returns:
        - For reactions added.
 
        HTTP_200_OK {reaction added}:
        A dict containing data about the reaction that was added (response_output).
        {
            "status": "success",
            "message": "reaction added",
            "data": {
                "room_id": "619e28c31a5f54782939d59a",
                "message_id": "61bc6b6078fb01b18fac1427",
                "reactions": [
                    {
                        "sender_id": "619ba4671a5f54782939d385",
                        "character": "taxi"
                    }
                ]
            }
        }

        - For removing reactions.
           
        HTTP_200_OK {reaction removed}:
        A dict containing data about the reaction that was removed (response_output).
        {
            "status": "success",
            "message": "reaction removed",
            "data": {
                "room_id": "619e28c31a5f54782939d59a",
                "message_id": "61bc6b6078fb01b18fac1427",
                "reactions": [
                    {
                        "sender_id": "619ba4671a5f54782939d385",
                        "character": "taxi"
                    }
                ]
            }
        }
                
        Raises:
            HTTP_424_FAILED_DEPENDENCY: Message not updated
    """
    DB = DataStorage(org_id)
    message = await get_mssg(org_id=org_id, room_id=room_id, message_id=message_id) # retrieve message
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Message not found"
        )
    react = message["reactions"]

    members = await get_room_members(org_id=org_id, room_id=room_id) # get room members
    payload = {
        "sender_id": request.sender_id,
        "character": request.character
    }

    if payload["sender_id"] not in members: # check if the user reacting to message is a room member
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="invalid room member"
        )

    try:
        if payload not in react: # check if reaction is already in the message reactions array

            react.append(payload) # add reaction to reactions array
            message_obj = await DB.update(
                MESSAGE_COLLECTION, document_id=message_id, data={"reactions": react}
            )
            if message_obj:
                data = {
                    "room_id": room_id,
                    "message_id": message_id,
                    "reactions" : [
                        {
                            "sender_id": payload["sender_id"],
                            "character": payload["character"]
                        }
                    ]
                }
                background_tasks.add_task(
                    centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, data
                )  # publish to centrifugo in the background

                return JSONResponse(
                    content=ResponseModel.success(
                        data=data, message="reaction added"
                    ),
                    status_code=status.HTTP_200_OK,
                )
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail={"Message not updated": message_obj},
            )
        
        react.remove(payload) # remove reaction from reactions array
        message_obj = await DB.update(
            MESSAGE_COLLECTION, document_id=message_id, data={"reactions": react}
        )
        if message_obj:
            data = {
                "room_id": room_id,
                "message_id": message_id,
                "reactions" : [
                    {
                        "sender_id": payload["sender_id"],
                        "character": payload["character"]
                    }
                ]
            }
            background_tasks.add_task(
                centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, data
            )  # publish to centrifugo in the background
            return JSONResponse(
                content=ResponseModel.success(
                    data=data, message="reaction removed"
                ),
                status_code=status.HTTP_200_OK,
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"Message not updated": message_obj},
        )
    except Exception as e:
        raise e
        