from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from schema.message import Message, MessageRequest, MessageUpdate, Reaction
from schema.response import ResponseModel
from starlette.responses import JSONResponse
from utils.centrifugo import Events, centrifugo_client
from utils.db import DataStorage
from utils.mssg_utils import get_mssg


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
async def get_all_messages(org_id: str, room_id: str):
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
async def get_message_by_id(org_id: str, room_id: str, message_id: str):
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


   
    # if message:
    #     try:
    #         # for reaction in message["reactions"]:
    #         for message_obj in message:
    #             if message_obj:
    #                 return JSONResponse(
    #                     content=ResponseModel.success(
    #                         data=message, message="message retrieved"
    #                     ),
    #                     status_code=status.HTTP_200_OK,
    #                 )
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail={"Message not found": message},
    #         )
    #     except Exception as e:
    #         raise e
    # raise HTTPException(
    #     status_code=status.HTTP_400_BAD_REQUEST,
    #     detail={"Message not found": message},

    # )






# @router.post(
#     "/org/{org_id}/rooms/{room_id}/messages/{message_id}/reactions",
#     response_model=ResponseModel,
#     responses={
#         status.HTTP_200_OK: {"description": "reaction added"},
#         status.HTTP_404_NOT_FOUND: {"description": "message not found"},
#         status.HTTP_403_FORBIDDEN: {"description": "you are not authorized to add a reaction"}
#         })
# async def add_reaction(
#     request: Reaction,
#     org_id: str,
#     room_id: str,
#     message_id: str,
#     background_tasks: BackgroundTasks
# ):
#     """
#     Add a reaction to a message

#     Args:
#         request: Request object
#         org_id: A unique identifier of the organization.
#         room_id: A unique identifier of the room.
#         message_id: A unique identifier of the message.

#     Returns:
#         HTTP_200_OK {reaction added}:
#         A dict containing data about the reaction that was added (response_output).
#             {
#                 "room_id": "619e28c31a5f54782939d59a",
#                 "message_id": "61bc5e5378fb01b18fac1426",
#                 "sender_id": "619ba4671a5f54782939d385",
#                 "reaction": [
#                     {
#                         "sender_id": "619ba4671a5f54782939d385",
#                         "character": "love"
#                     }
#                 ]
#             }
            
#     Raises:
#         HTTP_404_NOT_FOUND: Message not found
#     """
#     DB = DataStorage(org_id)
#     if org_id and room_id and message_id is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Invalid parameters",
#         )
#     mssg = await get_mssg(org_id=org_id, room_id=room_id, message_id=message_id)
#     if not mssg:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Message not found"
#         )

#     # payload = request.dict()
#     # react = mssg.get("reaction", [])
#     react = mssg.get("reaction", [])

#     # if payload["sender_id"] in react:
#     #     raise HTTPException(
#     #         status_code=status.HTTP_403_FORBIDDEN,    
#     #         detail="You are not authorized to add a reaction"
    
#     react.append(request.dict())
#     payload = {"reaction": react}
#     # react.append(payload)
#     # payload["reaction"] = react
#     try:
#         message = await DB.update(
#             MESSAGE_COLLECTION, document_id=message_id, data=payload
#         )
#         if message:
#             background_tasks.add_task(
#                 centrifugo_client.publish, room_id, Events.MESSAGE_REACTION, payload
#             )  # publish to centrifugo in the background
#             return JSONResponse(
#                 content=ResponseModel.success(
#                     data=payload, message="reaction added"
#                 ),
#                 status_code=status.HTTP_200_OK,
#             )
#         raise HTTPException(
#             status_code=status.HTTP_424_FAILED_DEPENDENCY,
#             detail={"reaction not added": message},
#         )
#     except Exception as e:
#         raise e
        






    # try:
    #     message = await DB.write(
    #         MESSAGE_COLLECTION,
    #         document_id=message_id,
    #         data={"$push": {"reaction": payload}},
    #     )
    #     if message:
    #         background_tasks.add_task(
    #             centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, payload
    #         )  # publish to centrifugo in the background
    #         return JSONResponse(
    #             content=ResponseModel.success(
    #                 data=payload, message="reaction added"
    #             ),
    #             status_code=status.HTTP_200_OK,
    #         )
    #     raise HTTPException(
    #         status_code=status.HTTP_424_FAILED_DEPENDENCY,
    #         detail={"reaction not added": message},
    #     )
    # except Exception as e:
    #     raise e




    # if sender_id not in mssg["reaction"]:
    #     payload = request.dict()
    #     payload["sender_id"] = sender_id
    #     try:
    #         message = await DB.update(
    #             MESSAGE_COLLECTION, document_id=message_id, data=payload
    #         )
    #         if message:
    #             background_tasks.add_task(
    #                 centrifugo_client.publish, room_id, Events.MESSAGE_REACTION, payload
    #             )  # publish to centrifugo in the background
    #             return JSONResponse(
    #                 content=ResponseModel.success(
    #                     data=payload, message="reaction added"
    #                 ),
    #                 status_code=status.HTTP_200_OK,
    #             )
    #         raise HTTPException(
    #             status_code=status.HTTP_424_FAILED_DEPENDENCY,
    #             detail={"message not edited": message},
    #         )
    #     except Exception as e:
    #         raise e




    # def post(self, request, org_id, *args, **kwargs):

    #     """
    #     This endpoint persists the information about users who like or unlike a song and the total number of likes a song has. When a user likes a song, the informmation is saved to the database and the like count increases. If the same user likes the same song, the song is unliked and the counter reduces",

    #     Sample request body

    #     {
    #         "userId": "juztiz5000kdkdkdkdkdkdkd",
    #         "songId": "61ae1e7b5a3812d0a9d0b213"
    #     }

    #     """
    #     helper = DataStorage()
    #     helper.organization_id = org_id
    #     serializer = SongLikeCountSerializer(data=request.data)
    #     if serializer.is_valid():
    #         songId = request.data["songId"]
    #         userId = request.data["userId"]

    #         songs = read_data(settings.SONG_COLLECTION, object_id=songId)
    #         likedBy = songs["data"]["likedBy"]

    #         if userId in likedBy:
    #             likedBy.remove(userId)
    #             unlike_count = len(likedBy)
    #             helper.update("songs", songId, {"likedBy": likedBy})

    #             return Response(
    #                 {
    #                     "unlikedBy": userId,
    #                     "songId": songId,
    #                     "total_likes": unlike_count,
    #                 },
    #                 status=status.HTTP_200_OK,
    #             )

    #         likedBy.append(userId)
    #         like_count = len(likedBy)
    #         helper.update("songs", songId, {"likedBy": likedBy})

    #         return Response(
    #             {
    #                 "likedBy": userId,
    #                 "songId": songId,
    #                 "total_likes": like_count,
    #             },
    #             status=status.HTTP_200_OK,
    #         )
    #     return Response(data={"Bad request"}, status=status.HTTP_400_BAD_REQUEST)



