# from fastapi import APIRouter, BackgroundTasks, HTTPException, status
# from schema.message import Message, MessageRequest, MessageUpdate, Reaction, ReactionNew, Thread
# from schema.response import ResponseModel
# from starlette.responses import JSONResponse
# from typing import Dict
# from utils.centrifugo import Events, centrifugo_client
# from utils.db import DataStorage
# from utils.message_utils import (MESSAGE_COLLECTION, get_message,
#                                  get_room_messages)
# from utils.room_utils import get_room_members

# router = APIRouter()


# # @router.put(
# #     "/org/{org_id}/rooms/{room_id}/messages/{message_id}/reactions",
# #     response_model=ResponseModel,
# #     status_code=status.HTTP_200_OK,
# #     responses={
# #         401: {"description": "invalid room member"},
# #         404: {"description": "message not found"},
# #         424: {"description": "Message not updated"},
# #     },
# # )
# # async def add_or_remove_reaction(
# #     request: Reaction,
# #     org_id: str,
# #     room_id: str,
# #     message_id: str,
# #     background_tasks: BackgroundTasks,
# # ):
# #     """
# #     Retrieves the message
# #     Checks if the user reacting to the message is a member of the room.
# #     Check if reaction is already in the message reactions array
# #     Add/removes a reaction to/from the message.
# #     - A payload consisting of the sender_id and character is added to the reactions array.
# #     - If the same payload is already in the reactions array, the reaction is removed.

# #     Args:
# #         request: Request object
# #         org_id: A unique identifier of the organization.
# #         room_id: A unique identifier of the room.
# #         message_id: A unique identifier of the message.

# #     Returns:
# #         - For reactions added.
# #         HTTP_200_OK {reaction added}

# #         - For reactions removed.
# #         HTTP_200_OK {reaction removed}

# #         A dict containing data about the reaction that was added or removed (response_output).
# #        {
# #             "room_id": "619e28c31a5f54782939d59a",
# #             "message_id": "61bc6b6078fb01b18fac1427",
# #             "reactions": [{
# #                 "sender_id": "619ba4671a5f54782939d385",
# #                 "character": "taxi"
# #             }]
# #         }

# #     Raises:
# #         HTTPException [401]: Invalid room member
# #         HTTPException [404]: Message not found
# #         HTTPException [424]: Message not updated
# #     """
# #     DB = DataStorage(org_id)
# #     message = await get_message(org_id, room_id, message_id)
# #     if not message:
# #         raise HTTPException(
# #             status_code=status.HTTP_404_NOT_FOUND, detail="Message not found"
# #         )

# #     new_reaction = {"sender_id": request.sender_id, "character": request.character}

    # members = await get_room_members(org_id, room_id)
    # if (
    #     new_reaction["sender_id"] not in members
    # ):  # check if the user reacting to message is a room member
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid room member"
    #     )

# #     emoji = message["reactions"]
# #     if (
# #         new_reaction not in emoji
# #     ):  # check if reaction is already in the message reactions array

# #         emoji.append(new_reaction)  # add reaction to reactions array
# #         added = await DB.update(
# #             MESSAGE_COLLECTION, document_id=message_id, data={"reactions": emoji}
# #         )
# #         if added:
# #             data = {
# #                 "room_id": room_id,
# #                 "message_id": message_id,
# #                 "reactions": [
# #                     {
# #                         "sender_id": new_reaction["sender_id"],
# #                         "character": new_reaction["character"],
# #                     }
# #                 ],
# #             }
# #             background_tasks.add_task(
# #                 centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, data
# #             )  # publish to centrifugo in the background
# #             return JSONResponse(
# #                 content=ResponseModel.success(data=data, message="reaction added"),
# #                 status_code=status.HTTP_200_OK,
# #             )
# #         raise HTTPException(
# #             status_code=status.HTTP_424_FAILED_DEPENDENCY, detail={"Reaction not added"}
# #         )

# #     emoji.remove(new_reaction)  # remove reaction from reactions array
# #     removed = await DB.update(
# #         MESSAGE_COLLECTION, document_id=message_id, data={"reactions": emoji}
# #     )
# #     if removed:
# #         data = {
# #             "room_id": room_id,
# #             "message_id": message_id,
# #             "reactions": [
# #                 {
# #                     "sender_id": new_reaction["sender_id"],
# #                     "character": new_reaction["character"],
# #                 }
# #             ],
# #         }
# #         background_tasks.add_task(
# #             centrifugo_client.publish,
# #             room_id,
# #             Events.MESSAGE_UPDATE,
# #             data,
# #         )  # publish to centrifugo in the background
# #         return JSONResponse(
# #             content=ResponseModel.success(data=data, message="reaction removed"),
# #             status_code=status.HTTP_200_OK,
# #         )
# #     raise HTTPException(
# #         status_code=status.HTTP_424_FAILED_DEPENDENCY,
# #         detail={"Reaction not removed"},
# #     )


# # # @router.put(
# # #     "/org/{org_id}/rooms/{room_id}/messages/{message_id}/reactions/add",
# # #     response_model=ResponseModel,
# # #     status_code=status.HTTP_200_OK,
# # #     responses={
# # #         401: {"description": "Invalid room member"},
# # #         404: {"description": "message not found"},
# # #         424: {"description": "reaction not added"},
# # #     },
# # # )
# # # async def add_reaction(
# # #     request: Reaction,
# # #     org_id: str,
# # #     room_id: str,
# # #     message_id: str,
# # #     background_tasks: BackgroundTasks,
# # # ):
# # #     """
# # #     Add a reaction to a message

# # #     Args:
# # #         request: Request object
# # #         org_id: A unique identifier of the organization.
# # #         room_id: A unique identifier of the room.
# # #         message_id: A unique identifier of the message that is being edited.
# # #         background_tasks: A daemon thread for publishing to centrifugo

# # #     Returns:
# # #         HTTP_200_OK {reaction added successfully}:
# # #         A dict containing data about the reaction that was added.
# # #             {
# # #                 "room_id": "619e28c31a5f54782939d59a",
# # #                 "message_id": "61ba9b0378fb01b18fac1420",
# # #                 "sender_id": "619ba4671a5f54782939d385",
# # #                 "character": "lol"
# # #             }

# # #     Raises:
# # #         HTTPException [401]: Invalid room member
# # #         HTTPException [404]: Message not found
# # #         HTTPException [409]: Reaction already exists
# # #         HTTPException [424]: Reaction not added
# # #     """
# # #     DB = DataStorage(org_id)
# # #     members = await get_room_members(org_id, room_id)
# # #     message = await get_message(org_id, room_id, message_id)

# # #     if not message:
# # #         raise HTTPException(
# # #             status_code=status.HTTP_404_NOT_FOUND,
# # #             detail="Message not found"
# # #         )
# # #     react = message["reactions"]

# # #     new_reaction = {
# # #         "sender_id": request.sender_id,
# # #         "character": request.character
# # #         }

# # #     if (
# # #         new_reaction["sender_id"] not in members
# # #     ):  # check if the user reacting to message is a room member
# # #         raise HTTPException(
# # #             status_code=status.HTTP_401_UNAUTHORIZED,
# # #             detail="invalid room member"
# # #         )
# # #     if (
# # #         new_reaction not in react
# # #     ):  # check if reaction is already in the message reactions array

# # #         react.append(new_reaction)  # add reaction to reactions array
# # #         added = await DB.update(
# # #             MESSAGE_COLLECTION, document_id=message_id, data={"reactions": react}
# # #         )
# # #         if added:
# # #             data = {
# # #                 "room_id": room_id,
# # #                 "message_id": message_id,
# # #                 "reactions": [{
# # #                 "sender_id": new_reaction["sender_id"],
# # #                 "character": new_reaction["character"],
# # #                 }],
# # #             }
# # #             background_tasks.add_task(
# # #                 centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, data
# # #             )  # publish to centrifugo in the background
# # #             return JSONResponse(
# # #                 content=ResponseModel.success(data=data, message="reaction added"),
# # #                 status_code=status.HTTP_200_OK,
# # #             )
# # #         raise HTTPException(
# # #             status_code=status.HTTP_424_FAILED_DEPENDENCY, detail={"Reaction not added"}
# # #         )
# # #     raise HTTPException(
# # #         status_code=status.HTTP_409_CONFLICT,
# # #         detail={"Reaction already exists"}
# # #     )


# # @router.delete(
# #     "/org/{org_id}/rooms/{room_id}/messages/{message_id}/reactions/remove",
# #     response_model=ResponseModel,
# #     status_code=status.HTTP_200_OK,
# #     responses={
# #         401: {"description": "Invalid room member"},
# #         404: {"description": "Reaction not found"},
# #         404: {"description": "message not found"},
# #         424: {"description": "reaction not removed"},
# #     },
# # )
# # async def remove_reaction(
# #     request: Reaction,
# #     org_id: str,
# #     room_id: str,
# #     message_id: str,
# #     background_tasks: BackgroundTasks,
# # ):
# #     """
# #     Remove a reaction to a message

# #     Args:
# #         request: Request object
# #         org_id: A unique identifier of the organization.
# #         room_id: A unique identifier of the room.
# #         message_id: A unique identifier of the message that is being edited.
# #         background_tasks: A daemon thread for publishing to centrifugo

# #     Returns:
# #         HTTP_200_OK {reaction removed successfully}:
# #         A dict containing data about the reaction that was removed.
# #         {
# #             "room_id": "619e28c31a5f54782939d59a",
# #             "message_id": "61ba9b0378fb01b18fac1420",
# #             "sender_id": "619ba4671a5f54782939d385",
# #             "character": "lol"
# #         }

# #     Raises:
# #         HTTPException [401]: Invalid room member
# #         HTTPException [404]: Message not found
# #         HTTPException [424]: Reaction not removed
# #     """
# #     DB = DataStorage(org_id)
# #     members = await get_room_members(org_id, room_id)
# #     message = await get_message(org_id, room_id, message_id)

# #     if not message:
# #         raise HTTPException(
# #             status_code=status.HTTP_404_NOT_FOUND, detail="Message not found"
# #         )
# #     react = message["reactions"]

# #     payload = {"sender_id": request.sender_id, "character": request.character}

# #     if (
# #         payload["sender_id"] not in members
# #     ):  # check if the user reacting to message is a room member
# #         raise HTTPException(
# #             status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid room member"
# #         )

# #     if payload in react:  # check if reaction is already in the message reactions array
# #         react.remove(payload)
# #         removed = await DB.update(
# #             MESSAGE_COLLECTION, document_id=message_id, data={"reactions": react}
# #         )
# #         if removed:
# #             data = {
# #                 "room_id": room_id,
# #                 "message_id": message_id,
# #                 "reactions": [
# #                     {
# #                         "sender_id": payload["sender_id"],
# #                         "character": payload["character"],
# #                     }
# #                 ],
# #             }
# #             background_tasks.add_task(
# #                 centrifugo_client.publish,
# #                 room_id,
# #                 Events.MESSAGE_UPDATE,
# #                 data,
# #             )  # publish to centrifugo in the background
# #             return JSONResponse(
# #                 content=ResponseModel.success(data=data, message="reaction removed"),
# #                 status_code=status.HTTP_200_OK,
# #             )
# #         raise HTTPException(
# #             status_code=status.HTTP_424_FAILED_DEPENDENCY,
# #             detail={"Reaction not removed"},
# #         )
# #     raise HTTPException(
# #         status_code=status.HTTP_404_NOT_FOUND, detail={"Reaction not found"}
# #     )


# # @router.put(
# #     "/org/{org_id}/rooms/{room_id}/messages/{message_id}/reactions/addcheck",
# #     response_model=ResponseModel,
# #     status_code=status.HTTP_200_OK,
# #     responses={
# #         401: {"description": "Invalid room member"},
# #         404: {"description": "message not found"},
# #         409: {"description": "User already reacted to this message"},
# #         424: {"description": "reaction not added"},
# #     },
# # )
# # async def add_reaction_check(
# #     request: ReactionNew,
# #     org_id: str,
# #     room_id: str,
# #     message_id: str,
# #     background_tasks: BackgroundTasks,
# # ):
# #     """
# #     Add a reaction to a message

# #     Args:
# #         request: Request object
# #         org_id: A unique identifier of the organization.
# #         room_id: A unique identifier of the room.
# #         message_id: A unique identifier of the message that is being edited.
# #         background_tasks: A daemon thread for publishing to centrifugo

# #     Returns:
# #         HTTP_200_OK {reaction added successfully}:
# #         A dict containing data about the reaction that was added.
# #             {
# #                 "room_id": "619e28c31a5f54782939d59a",
# #                 "message_id": "61ba9b0378fb01b18fac1420",
# #                 "sender_id": "619ba4671a5f54782939d385",
# #                 "character": "lol"
# #             }

# #     Raises:
# #         HTTPException [401]: Invalid room member
# #         HTTPException [404]: Message not found
# #         HTTPException [409]: Reaction already exists
# #         HTTPException [424]: Reaction not added
# #     """
# #     DB = DataStorage(org_id)
# #     members = await get_room_members(org_id, room_id)
# #     message = await get_message(org_id, room_id, message_id)

# #     if not message:  # retrieve message
# #         raise HTTPException(
# #             status_code=status.HTTP_404_NOT_FOUND, detail="Message not found"
# #         )
# #     react = message["reactions"]

# #     new_reaction = {"character": request.character, "sender_id": [request.sender_id]}

# #     if (
# #         new_reaction["sender_id"] not in members
# #     ):  # check if the user reacting to message is a room member
# #         raise HTTPException(
# #             status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid room member"
# #         )

# #     if (
# #         new_reaction["character"] in react
# #         and new_reaction["sender_id"] not in react["sender_id"]
# #     ):
# #         react["sender_id"].append(new_reaction["sender_id"])

# #     if new_reaction["character"] not in react:
# #         react.append(new_reaction)

# #         added = await DB.update(
# #             MESSAGE_COLLECTION, document_id=message_id, data={"reactions": react}
# #         )
# #         if added:
# #             data = {
# #                 "room_id": room_id,
# #                 "message_id": message_id,
# #                 "reactions": [
# #                     {
# #                         "character": new_reaction["character"],
# #                         "sender_id": [new_reaction["sender_id"]],
# #                         "count": len(react["sender_id"]),
# #                     }
# #                 ],
# #             }
# #             background_tasks.add_task(
# #                 centrifugo_client.publish,
# #                 room_id,
# #                 Events.MESSAGE_UPDATE,
# #                 data,
# #             )
# #             return JSONResponse(
# #                 content=ResponseModel.success(data=data, message="reaction added"),
# #                 status_code=status.HTTP_200_OK,
# #             )
# #         raise HTTPException(
# #             status_code=status.HTTP_424_FAILED_DEPENDENCY, detail={"Reaction not added"}
# #         )
# #     raise HTTPException(
# #         status_code=status.HTTP_409_CONFLICT,
# #         detail={"User already reacted to this message"},
# #     )


# # @router.put(
# #     "/org/{org_id}/rooms/{room_id}/messages/{message_id}/reactions/add",
# #     response_model=ResponseModel,
# #     status_code=status.HTTP_200_OK,
# #     responses={
# #         401: {"description": "Invalid room member"},
# #         404: {"description": "message not found"},
# #         424: {"description": "reaction not added"},
# #     },
# # )
# # async def add_reaction(
# #     request: ReactionNew,
# #     org_id: str,
# #     room_id: str,
# #     message_id: str,
# #     background_tasks: BackgroundTasks,
# # ):
# #     """
# #     Add a reaction to a message

# #     Args:
# #         request: Request object
# #         org_id: A unique identifier of the organization.
# #         room_id: A unique identifier of the room.
# #         message_id: A unique identifier of the message that is being edited.
# #         background_tasks: A daemon thread for publishing to centrifugo

# #     Returns:
# #         HTTP_200_OK {reaction added successfully}:
# #         A dict containing data about the reaction that was added.
# #             {
# #                 "room_id": "619e28c31a5f54782939d59a",
# #                 "message_id": "61ba9b0378fb01b18fac1420",
# #                 "sender_id": "619ba4671a5f54782939d385",
# #                 "character": "lol"
# #             }

# #     Raises:
# #         HTTPException [401]: Invalid room member
# #         HTTPException [404]: Message not found
# #         HTTPException [409]: Reaction already exists
# #         HTTPException [424]: Reaction not added
# #     """
# #     DB = DataStorage(org_id)
# #     members = await get_room_members(org_id, room_id)
# #     message = await get_message(org_id, room_id, message_id)

# #     if not message:
# #         raise HTTPException(
# #             status_code=status.HTTP_404_NOT_FOUND,
# #             detail="Message not found"
# #         )
# #     react = message["reactions"]

# #     new_reaction = {
# #         "sender_id": request.sender_id,
# #         "character": request.character
# #         }

# #     if (
# #         new_reaction["sender_id"] not in members
# #     ):  # check if the user reacting to message is a room member
# #         raise HTTPException(
# #             status_code=status.HTTP_401_UNAUTHORIZED,
# #             detail="invalid room member"
# #         )
# #     if (
# #         new_reaction not in react
# #     ):  # check if reaction is already in the message reactions array

# #         react.append(new_reaction)  # add reaction to reactions array
# #         added = await DB.update(
# #             MESSAGE_COLLECTION, document_id=message_id, data={"reactions": react}
# #         )
# #         if added:
# #             data = {
# #                 "room_id": room_id,
# #                 "message_id": message_id,
# #                 "reactions": [
# #                     {
# #                         "sender_id": new_reaction["sender_id"],
# #                         "character": [new_reaction["character"]],
# #                     }
# #                 ],
# #             }
# #             background_tasks.add_task(
# #                 centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, data
# #             )  # publish to centrifugo in the background
# #             return JSONResponse(
# #                 content=ResponseModel.success(data=data, message="reaction added"),
# #                 status_code=status.HTTP_200_OK,
# #             )
# #         raise HTTPException(
# #             status_code=status.HTTP_424_FAILED_DEPENDENCY, detail={"Reaction not added"}
# #         )
# #     raise HTTPException(
# #         status_code=status.HTTP_409_CONFLICT, detail={"Reaction already exists"}
# #     )


# # @router.get(
# #     "/org/{org_id}/rooms/{room_id}/messages",
# #     response_model=ResponseModel,
# #     status_code=status.HTTP_200_OK,
# #     responses={424: {"detail": "ZC Core failed"}},
# # )
# # async def get_messages(org_id, room_id):
# #     """Fetches all messages sent in a particular room.

# #     Args:
# #         org_id (str): A unique identifier of an organization
# #         room_id (str): A unique identifier of the room where messages are fetched from

# #     Returns:
# #         A list of message objects

# #     Raises:
# #         HTTPException [424]: Zc Core failed
# #     """
# #     response = await get_room_messages(org_id, room_id)
# #     if response is None or "status_code" in response:
# #         raise HTTPException(
# #             status_code=status.HTTP_424_FAILED_DEPENDENCY,
# #             detail="Zc Core failed",
# #         )
# #     return JSONResponse(
# #         content=ResponseModel.success(data=response, message="Messages retrieved"),
# #         status_code=status.HTTP_200_OK,
# #     )
# #         status_code=status.HTTP_409_CONFLICT,
# #         detail={"Reaction already exists"}
# #     )


# @router.delete(
#     "/org/{org_id}/rooms/{room_id}/messages/{message_id}/reactions/remove",
#     response_model=ResponseModel,
#     status_code=status.HTTP_200_OK,
#     responses={
#         401: {"description": "Invalid room member"},
#         404: {"description": "Reaction not found"},
#         404: {"description": "message not found"},
#         424: {"description": "reaction not removed"},
#     },
# )
# async def remove_reaction(
#     request: Reaction,
#     org_id: str,
#     room_id: str,
#     message_id: str,
#     background_tasks: BackgroundTasks,
# ):
#     """
#     Remove a reaction to a message

#     Args:
#         request: Request object
#         org_id: A unique identifier of the organization.
#         room_id: A unique identifier of the room.
#         message_id: A unique identifier of the message that is being edited.
#         background_tasks: A daemon thread for publishing to centrifugo

#     Returns:
#         HTTP_200_OK {reaction removed successfully}:
#         A dict containing data about the reaction that was removed.
#         {
#             "room_id": "619e28c31a5f54782939d59a",
#             "message_id": "61ba9b0378fb01b18fac1420",
#             "sender_id": "619ba4671a5f54782939d385",
#             "character": "lol"
#         }

#     Raises:
#         HTTPException [401]: Invalid room member
#         HTTPException [404]: Message not found
#         HTTPException [424]: Reaction not removed
#     """
#     DB = DataStorage(org_id)
#     members = await get_room_members(org_id, room_id)
#     message = await get_message(org_id, room_id, message_id)

#     if not message:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Message not found"
#         )
#     react = message["reactions"]

#     payload = {
#         "sender_id": request.sender_id,
#         "character": request.character
#         }

#     if (
#         payload["sender_id"] not in members
#     ):  # check if the user reacting to message is a room member
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="invalid room member"
#         )

#     if (
#         payload in react
#     ):  # check if reaction is already in the message reactions array
#         react.remove(payload)
#         removed = await DB.update(
#             MESSAGE_COLLECTION, document_id=message_id, data={"reactions": react}
#         )
#         if removed:
#             data = {
#             "room_id": room_id,
#             "message_id": message_id,
#             "reactions": [{
#                 "sender_id": payload["sender_id"],
#                 "character": payload["character"],
#                 }],
#             }
#             background_tasks.add_task(
#                 centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, data,
#             )  # publish to centrifugo in the background
#             return JSONResponse(
#                 content=ResponseModel.success(data=data, message="reaction removed"),
#                 status_code=status.HTTP_200_OK,
#             )
#         raise HTTPException(
#             status_code=status.HTTP_424_FAILED_DEPENDENCY,
#             detail={"Reaction not removed"}
#         )
#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail={"Reaction not found"}
#     )
    

# @router.put(
#     "/org/{org_id}/rooms/{room_id}/messages/{message_id}/reactions/addcheck",
#     response_model=ResponseModel,
#     status_code=status.HTTP_200_OK,
#     responses={
#         401: {"description": "Invalid room member"},
#         404: {"description": "message not found"},
#         409: {"description": "User already reacted to this message"},
#         424: {"description": "reaction not added"}
#     },
# )
# async def add_reaction_check(
#     request: ReactionNew,
#     org_id: str,
#     room_id: str,
#     message_id: str,
#     background_tasks: BackgroundTasks,
# ):
#     """
#     Add a reaction to a message

#     Args:
#         request: Request object
#         org_id: A unique identifier of the organization.
#         room_id: A unique identifier of the room.
#         message_id: A unique identifier of the message that is being edited.
#         background_tasks: A daemon thread for publishing to centrifugo

#     Returns:
#         HTTP_200_OK {reaction added successfully}:
#         A dict containing data about the reaction that was added.
#             {
#                 "room_id": "619e28c31a5f54782939d59a",
#                 "message_id": "61ba9b0378fb01b18fac1420",
#                 "sender_id": "619ba4671a5f54782939d385",
#                 "character": "lol"
#             }

#     Raises:
#         HTTPException [401]: Invalid room member
#         HTTPException [404]: Message not found
#         HTTPException [409]: Reaction already exists
#         HTTPException [424]: Reaction not added
#     """
#     DB = DataStorage(org_id)
#     members = await get_room_members(org_id, room_id)
#     message = await get_message(org_id, room_id, message_id)

#     if not message: # retrieve message
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Message not found"
#         )
#     react = message["reactions"]

#     new_reaction = {
#         "character": request.character,
#         "sender_id": [request.sender_id]
#         }

#     if new_reaction["sender_id"] not in members: # check if the user reacting to message is a room member
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="invalid room member"
#         )

#     if new_reaction["character"] in react and new_reaction[
#         "sender_id"] not in react["sender_id"]:
#         react["sender_id"].append(new_reaction["sender_id"])

#     if (
#         new_reaction["character"] not in react):
#         react.append(new_reaction)

#         added = await DB.update(
#             MESSAGE_COLLECTION, document_id=message_id, data={"reactions": react}
#         )
#         if added:
#             data = {
#             "room_id": room_id,
#             "message_id": message_id,
#             "reactions": [{
#                 "character": new_reaction["character"],
#                 "sender_id": [new_reaction["sender_id"]],
#                 "count": len(react["sender_id"])
#                 }],
#             }
#             background_tasks.add_task(
#                 centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, data,
#             )
#             return JSONResponse(
#                 content=ResponseModel.success(data=data, message="reaction added"),
#                 status_code=status.HTTP_200_OK,
#             )
#         raise HTTPException(
#             status_code=status.HTTP_424_FAILED_DEPENDENCY,
#             detail={"Reaction not added"}
#         )
#     raise HTTPException(
#         status_code=status.HTTP_409_CONFLICT,
#         detail={"User already reacted to this message"}
#     )

 
# @router.put(
#     "/org/{org_id}/rooms/{room_id}/messages/{message_id}/reactions/add",
#     response_model=ResponseModel,
#     status_code=status.HTTP_200_OK,
#     responses={
#         401: {"description": "Invalid room member"},
#         404: {"description": "message not found"},
#         424: {"description": "reaction not added"},
#     },
# )
# async def add_reaction(
#     request: ReactionNew,
#     org_id: str,
#     room_id: str,
#     message_id: str,
#     background_tasks: BackgroundTasks,
# ):
#     """
#     Add a reaction to a message

#     Args:
#         request: Request object
#         org_id: A unique identifier of the organization.
#         room_id: A unique identifier of the room.
#         message_id: A unique identifier of the message that is being edited.
#         background_tasks: A daemon thread for publishing to centrifugo

#     Returns:
#         HTTP_200_OK {reaction added successfully}:
#         A dict containing data about the reaction that was added.
#             {
#                 "room_id": "619e28c31a5f54782939d59a",
#                 "message_id": "61ba9b0378fb01b18fac1420",
#                 "sender_id": "619ba4671a5f54782939d385",
#                 "character": "lol"
#             }

#     Raises:
#         HTTPException [401]: Invalid room member
#         HTTPException [404]: Message not found
#         HTTPException [409]: Reaction already exists
#         HTTPException [424]: Reaction not added
#     """
#     DB = DataStorage(org_id)
#     members = await get_room_members(org_id, room_id)
#     message = await get_message(org_id, room_id, message_id)

#     if not message:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Message not found"
#         )
#     react = message["reactions"]

#     new_reaction = {
#         "sender_id": request.sender_id,
#         "character": request.character
#         }

#     if (
#         new_reaction["sender_id"] not in members
#     ):  # check if the user reacting to message is a room member
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="invalid room member"
#         )
#     if (
#         new_reaction not in react
#     ):  # check if reaction is already in the message reactions array

#         react.append(new_reaction)  # add reaction to reactions array
#         added = await DB.update(
#             MESSAGE_COLLECTION, document_id=message_id, data={"reactions": react}
#         )
#         if added:
#             data = {
#                 "room_id": room_id,
#                 "message_id": message_id,
#                 "reactions": [{
#                 "sender_id": new_reaction["sender_id"],
#                 "character": [new_reaction["character"]],
#                 }],
#             }
#             background_tasks.add_task(
#                 centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, data
#             )  # publish to centrifugo in the background
#             return JSONResponse(
#                 content=ResponseModel.success(data=data, message="reaction added"),
#                 status_code=status.HTTP_200_OK,
#             )
#         raise HTTPException(
#             status_code=status.HTTP_424_FAILED_DEPENDENCY, detail={"Reaction not added"}
#         )
#     raise HTTPException(
#         status_code=status.HTTP_409_CONFLICT,
#         detail={"Reaction already exists"}
#     )

#added 7th jan

      
# @router.put(
#     "/org/{org_id}/rooms/{room_id}/messages/{message_id}/reactions/addpnly",
#     response_model=ResponseModel,
#     status_code=status.HTTP_200_OK,
#     responses={
#         401: {"description": "Invalid room member"},
#         404: {"description": "message not found"},
#         424: {"description": "reaction not added"},
#     },
# )
# async def add_reaction(
#     request: Emoji,
#     org_id: str,
#     room_id: str,
#     message_id: str,
#     background_tasks: BackgroundTasks,
#     # members: List[ObjId] = Body(...),
# ):
#     """
#     Add a reaction to a message

#     Args:
#         request: Request object
#         org_id: A unique identifier of the organization.
#         room_id: A unique identifier of the room.
#         message_id: A unique identifier of the message that is being edited.
#         background_tasks: A daemon thread for publishing to centrifugo

#     Returns:
#         HTTP_200_OK {reaction added successfully}:
#         A dict containing data about the reaction that was added.
        
#             {
#                 "room_id": "619e28c31a5f54782939d59a",
#                 "message_id": "61ba9b0378fb01b18fac1420",
#                 "emojis": [
#                     "name": "smile",
#                     "count": 1,
#                     "reactedUsersId": [
#                         "619ba4671a5f54782939d385"
#                         ]
#                     "emoji": "👹"   
#                 ]
#             }

#     Raises:
#         HTTPException [401]: Invalid room member
#         HTTPException [404]: Message not found
#         HTTPException [409]: Reaction already exists
#         HTTPException [424]: Reaction not added
#     """
#     DB = DataStorage(org_id)
#     members = await get_room_members(org_id, room_id)
#     message = await get_message(org_id, room_id, message_id)

#     if not message:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Message not found"
#         )
#     # reaction = message.get("emojis")

#     new_reaction = {
#         "name": request.name,
#         "emoji": request.emoji,
#         "reactedUsersId": [request.reactedUsersId]
#         }

#     if (
#         new_reaction["reactedUsersId"] not in members
#     ):  # check if the user reacting to message is a room member
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="invalid room member"
#         )
        
#     reaction = message["emojis"]
#     if (
#         new_reaction not in reaction
#     ):  # check if reaction is already in the message reactions array

#         reaction.append(new_reaction)  # add reaction to reactions array
#         added = await DB.update(
#             MESSAGE_COLLECTION, document_id=message_id, data={"reactions": reaction}
#         )
#         if added:
#             data = {
#                 "room_id": room_id,
#                 "message_id": message_id,
#                 "emojis": [
#                     {
#                         "name": new_reaction["name"],
#                         "emoji": new_reaction["emoji"],
#                         "reactedUsersId": [new_reaction["reactedUsersId"]],
#                         "count": len(new_reaction["reactedUsersId"])
#                     }
#                 ],
#             }
#             background_tasks.add_task(
#                 centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, data
#             )  # publish to centrifugo in the background
#             return JSONResponse(
#                 content=ResponseModel.success(data=data, message="reaction added"),
#                 status_code=status.HTTP_200_OK,
#             )
#         raise HTTPException(
#             status_code=status.HTTP_424_FAILED_DEPENDENCY, detail={"Reaction not added"}
#         )
    # raise HTTPException(
    #     status_code=status.HTTP_409_CONFLICT,
    #     detail={"Reaction already exists"}
    # )




# @router.put(
#     "/org/{org_id}/rooms/{room_id}/messages/{message_id}/reactions/addcheck",
#     response_model=ResponseModel,
#     status_code=status.HTTP_200_OK,
#     responses={
#         401: {"description": "Invalid room member"},
#         404: {"description": "message not found"},
#         424: {"description": "reaction not added"},
#     },
# )
# async def add_reaction(
#     request: Emoji,
#     org_id: str,
#     room_id: str,
#     message_id: str,
#     background_tasks: BackgroundTasks,
# ):
#     """
#     Add a reaction to a message

#     Args:
#         request: Request object
#         org_id: A unique identifier of the organization.
#         room_id: A unique identifier of the room.
#         message_id: A unique identifier of the message that is being edited.
#         background_tasks: A daemon thread for publishing to centrifugo

#     Returns:
#         HTTP_200_OK {reaction added successfully}:
#         A dict containing data about the reaction that was added.

#             {
#                 "room_id": "619e28c31a5f54782939d59a",
#                 "message_id": "61ba9b0378fb01b18fac1420",
#                 "name": "lol",
#                 "count": 1
#                 "emoji": "😂"
#                 "reactedUsersId": ["619ba4671a5f54782939d385"]
#             }

#     Raises:
#         HTTPException [401]: Invalid room member
#         HTTPException [404]: Message not found
#         HTTPException [424]: Reaction not added
#     """
#     DB = DataStorage(org_id)
    
#     # if room_type in (RoomType.GROUP_DM, RoomType.DM):
#     #     for room in rooms:
#     #         if set(room["room_members"].keys()) == set(room_members.keys()):
#     #             raise HTTPException(
#     #                 status_code=status.HTTP_200_OK,
#     #                 detail={
#     #                     "message": "room already exists",
#     #                     "room_id": room["_id"],
#     #                         },
#     #                     )
                        
#     members = await get_room_members(org_id, room_id) # retrieve room members
#     # member_keys = [*members]
#     memberIds = list(members)
#     # memberIds = list(members.keys())
#     print (memberIds)
    
#     message = await get_message(org_id, room_id, message_id) # retrieve message
#     if not message:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Message not found"
#         )
#     # react = message["emojis"]
#     react = message.get("emojis")
#     print (react)
    
#     new_reaction = request.dict()
#     # new_reaction = {
#     #     "name": request.name,
#     #     "emoji": request.emoji,
#     #     "reactedUsersId": [request.reactedUsersId],
#     #     "count": 1
#     # }
    
#     if new_reaction["reactedUsersId"] in [memberIds]: # check if reactor is a room member
#         print ("user found")
#         if new_reaction["name"] not in react:
#             react.append(new_reaction)
#             added = await DB.update(
#                 MESSAGE_COLLECTION, document_id=message_id, data={"emojis": new_reaction}
#             )
#             if added:
#                 data = {
#                     "room_id": room_id,
#                     "message_id": message_id,
#                     "emojis": [
#                         {
#                             "name": new_reaction["name"],
#                             "emoji": new_reaction["emoji"],
#                             "reactedUsersId": [new_reaction["reactedUsersId"]],
#                             # "count": len(new_reaction["reactedUsersId"])
#                             "count": +1
#                         }
#                     ],
#                 }
#                 background_tasks.add_task(
#                     centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, data
#                 )  # publish to centrifugo in the background
#                 return JSONResponse(
#                     content=ResponseModel.success(data=data, message="reaction added"),
#                     status_code=status.HTTP_200_OK,
#                 )
#             raise HTTPException(
#                 status_code=status.HTTP_424_FAILED_DEPENDENCY, detail={"Reaction not added"}
#             )
#         if new_reaction["reactedUsersId"] not in react:
#             react.append(new_reaction["reactedUsersId"])
#             added = await DB.update(
#                 MESSAGE_COLLECTION, document_id=message_id, data={"emojis": react}
#             )
#             if added:
#                 data = {
#                     "room_id": room_id,
#                     "message_id": message_id,
#                     "emojis": [
#                         {
#                             "name": react["name"],
#                             "emoji": react["emoji"],
#                             "reactedUsersId": [new_reaction["reactedUsersId"]],
#                             "count": len(react["reactedUsersId"])
#                         }
#                     ],
#                 }
#                 background_tasks.add_task(
#                     centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, data
#                 )  # publish to centrifugo in the background
#                 return JSONResponse(
#                     content=ResponseModel.success(data=data, message="reaction added"),
#                     status_code=status.HTTP_200_OK,
#                 )
#             raise HTTPException(
#                 status_code=status.HTTP_424_FAILED_DEPENDENCY, detail={"Reaction not added"}
#             )
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail={"Reaction already exists"},
#         )
#     raise HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid room member"
#     )
                
                




# @router.put(
#     "/org/{org_id}/rooms/{room_id}/messages/{message_id}/reactions/addcheck",
#     response_model=ResponseModel,
#     status_code=status.HTTP_200_OK,
#     responses={
#         401: {"description": "Invalid room member"},
#         404: {"description": "message not found"},
#         424: {"description": "reaction not added"},
#     },
# )
# async def add_reaction(
#     request: Emoji,
#     org_id: str,
#     room_id: str,
#     message_id: str,
#     background_tasks: BackgroundTasks,
# ):
#     """
#     Add a reaction to a message

#     Args:
#         request: Request object
#         org_id: A unique identifier of the organization.
#         room_id: A unique identifier of the room.
#         message_id: A unique identifier of the message that is being edited.
#         background_tasks: A daemon thread for publishing to centrifugo

#     Returns:
#         HTTP_200_OK {reaction added successfully}:
#         A dict containing data about the reaction that was added.

#             {
#                 "room_id": "619e28c31a5f54782939d59a",
#                 "message_id": "61ba9b0378fb01b18fac1420",
#                 "name": "lol",
#                 "count": 1,
#                 "emoji": "😂",
#                 "reactedUsersId": ["619ba4671a5f54782939d385"]
#             }

#     Raises:
#         HTTPException [401]: Invalid room member
#         HTTPException [404]: Message not found
#         HTTPException [424]: Reaction not added
#     """
#     DB = DataStorage(org_id)
    
#     members = await get_room_members(org_id, room_id) # retrieve room members
    
#     # memberIds = str(list(members)) # convert room members to string
#     memberIds = [str(member) for member in members] # convert room members to string
    
#     # memberIds = list(members) # convert room members to string
#     print (memberIds)
#     print (type(memberIds))
    
#     message = await get_message(org_id, room_id, message_id) # retrieve message
#     if not message:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Message not found"
#         )
        
#     react = message.get("emojis")
#     print (react)
    
#     new_reaction = request.dict()
    
#     if new_reaction["reactedUsersId"] in [memberIds]: # check if reactor is a room member
#         print ("user found")
#         if new_reaction["name"] not in react:
#             react.append(new_reaction)
#             added = await DB.update(
#                 MESSAGE_COLLECTION, document_id=message_id, data={"emojis": new_reaction}
#             )
#             if added:
#                 data = {
#                     "room_id": room_id,
#                     "message_id": message_id,
#                     "emojis": [
#                         {
#                             "name": new_reaction["name"],
#                             "emoji": new_reaction["emoji"],
#                             "reactedUsersId": [new_reaction["reactedUsersId"]],
#                             "count": +1
#                         }
#                     ],
#                 }
#                 background_tasks.add_task(
#                     centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, data
#                 )  # publish to centrifugo in the background
#                 return JSONResponse(
#                     content=ResponseModel.success(data=data, message="reaction added"),
#                     status_code=status.HTTP_200_OK,
#                 )
#             raise HTTPException(
#                 status_code=status.HTTP_424_FAILED_DEPENDENCY, detail={"Reaction not added"}
#             )
#         if new_reaction["reactedUsersId"] not in react:
#             react.append(new_reaction["reactedUsersId"])
#             added = await DB.update(
#                 MESSAGE_COLLECTION, document_id=message_id, data={"emojis": react}
#             )
#             if added:
#                 data = {
#                     "room_id": room_id,
#                     "message_id": message_id,
#                     "emojis": [
#                         {
#                             "name": react["name"],
#                             "emoji": react["emoji"],
#                             "reactedUsersId": [new_reaction["reactedUsersId"]],
#                             "count": len(react["reactedUsersId"])
#                         }
#                     ],
#                 }
#                 background_tasks.add_task(
#                     centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, data
#                 )  # publish to centrifugo in the background
#                 return JSONResponse(
#                     content=ResponseModel.success(data=data, message="reaction added"),
#                     status_code=status.HTTP_200_OK,
#                 )
#             raise HTTPException(
#                 status_code=status.HTTP_424_FAILED_DEPENDENCY, detail={"Reaction not added"}
#             )
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail={"Reaction already exists"},
#         )
#     raise HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid room member"
#     )
                
                        
    
    
# @router.put(
#     "/org/{org_id}/rooms/{room_id}/messages/{message_id}/reactions/addcheck",
#     response_model=ResponseModel,
#     status_code=status.HTTP_200_OK,
#     responses={
#         401: {"description": "Invalid room member"},
#         404: {"description": "message not found"},
#         424: {"description": "reaction not added"},
#     },
# )
# async def add_reaction(
#     # request: ReactionNew,
#     request: Emoji,
#     org_id: str,
#     room_id: str,
#     message_id: str,
#     background_tasks: BackgroundTasks,
# ):
#     """
#     Add a reaction to a message

#     Args:
#         request: Request object
#         org_id: A unique identifier of the organization.
#         room_id: A unique identifier of the room.
#         message_id: A unique identifier of the message that is being edited.
#         background_tasks: A daemon thread for publishing to centrifugo

#     Returns:
#         HTTP_200_OK {reaction added successfully}:
#         A dict containing data about the reaction that was added.

#             {
#                 "room_id": "619e28c31a5f54782939d59a",
#                 "message_id": "61ba9b0378fb01b18fac1420",
#                 "name": "lol",
#                 "count": 1
#                 "emoji": "😂"
#                 "reactedUsersId": ["619ba4671a5f54782939d385"]
#             }

#     Raises:
#         HTTPException [401]: Invalid room member
#         HTTPException [404]: Message not found
#         HTTPException [424]: Reaction not added
#     """
#     DB = DataStorage(org_id)
    
#     members = await get_room_members(org_id, room_id) # retrieve room members
#     # member_keys = [*members]
#     member_keys = list(members)
#     print (member_keys)
    
#     message = await get_message(org_id, room_id, message_id) # retrieve message
#     if not message:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Message not found"
#         )
#     # react = message["emojis"]
#     react = message.get("emojis")
#     print (react)
    
#     new_reaction = request.dict()    
    # if new_reaction["reactedUsersId"] not in member_keys: # check that the reactor is a room member
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid room member"
    #     )

    # if new_reaction["name"] not in react: # check that the message reaction doesn't exist 
    #     react.append(new_reaction)

    #     added = await DB.update(
    #         MESSAGE_COLLECTION, document_id=message_id, data={"emojis": new_reaction}
    #         # MESSAGE_COLLECTION, document_id=message_id, data={"emojis": message["emojis"]}
    #         # MESSAGE_COLLECTION, document_id=message_id, data={message["emojis"]}
    #     )
    #     if added:
    #         data = {
    #             "room_id": room_id,
    #             "message_id": message_id,
    #             "emojis": [
    #                 {
    #                     "name": new_reaction["name"],
    #                     "count": len(react["reactedUsersId"]),
    #                     "emoji": new_reaction["emoji"],
    #                     "reactedUsersId": new_reaction["reactedUsersId"],
    #                 }
    #             ],
    #         }
    #         background_tasks.add_task(
    #             centrifugo_client.publish,
    #             room_id,
    #             message_id,
    #             Events.MESSAGE_UPDATE,
    #             data,
    #         )
    #         return JSONResponse(
    #             content=ResponseModel.success(data=data, message="reaction added"),
    #             status_code=status.HTTP_200_OK,
    #         )
    #     raise HTTPException(
    #         status_code=status.HTTP_424_FAILED_DEPENDENCY, detail={"Reaction not added"}
    #     )

    # if new_reaction["reactedUsersId"] not in react["reactedUsersId"]:
    #     # check that the id of the reactor is in the reactedUsersId array
    #     react["reactedUsersId"].append(new_reaction["reactedUsersId"])
        
    #     added = await DB.update(
    #         MESSAGE_COLLECTION, document_id=message_id, data={"emojis": message["emojis"]}
    #     )
    #     if added:
    #         data = {
    #             "room_id": room_id,
    #             "message_id": message_id,
    #             "emojis": [
    #                 {
    #                     "name": react["name"],
    #                     "count": len(react["reactedUsersId"]),
    #                     "emoji": react["emoji"],
    #                     "reactedUsersId": react["reactedUsersId"],
    #                 }
    #             ],
    #         }
    #         background_tasks.add_task(
    #             centrifugo_client.publish,
    #             room_id,
    #             message_id,
    #             Events.MESSAGE_UPDATE,
    #             data,
    #         )
    #         return JSONResponse(
    #             content=ResponseModel.success(data=data, message="reaction added"),
    #             status_code=status.HTTP_200_OK,
    #         )
    #     raise HTTPException(
    #         status_code=status.HTTP_424_FAILED_DEPENDENCY, detail={"Reaction not added"}
    #     )
    # raise HTTPException(
    #     status_code=status.HTTP_409_CONFLICT,
    #     detail={"Reaction already exists"}
    # )





    # if new_reaction["emojis"][0]["reactedUsersId"] not in members:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid room member"
    #     )
        
    # if new_reaction["name"] in react:
    #     if new_reaction["reactedUsersId"] not in react["emojis"][0]["reactedUsersId"]:
    #         # react[new_reaction["reactedUsersId"]]["count"] += 1
    #         # react[new_reaction["name"]]["reactedUsersId"].append(
    #         #     new_reaction["reactedUsersId"]
    #         # )
    #         react["reactedUsersId"].append(new_reaction["reactedUsersId"])
    #         #     new_reaction["reactedUsersId"]
    #         # )
    #         added = await DB.update(
    #             MESSAGE_COLLECTION, document_id=message_id, data={"emojis": react}
    #         )
    #         if added:
    #             data = {
    #                 "room_id": room_id,
    #                 "message_id": message_id,
    #                 "emojis": [
    #                     {
    #                         "name": new_reaction["name"],
    #                         "count": len(react["reactedUsersId"]),
    #                         "emoji": new_reaction["emoji"],
    #                         "reactedUsersId": new_reaction["reactedUsersId"],
    #                     }
    #                 ],
    #             }
    #             background_tasks.add_task(
    #                 centrifugo_client.publish,
    #                 room_id,
    #                 Events.MESSAGE_UPDATE,
    #                 data,
    #             )
    #             return JSONResponse(
    #                 content=ResponseModel.success(data=data, message="reaction added"),
    #                 status_code=status.HTTP_200_OK,
    #             )
    #         raise HTTPException(
    #             status_code=status.HTTP_424_FAILED_DEPENDENCY,
    #             detail={"Reaction not added"},
    #         )
    #     raise HTTPException(
    #         status_code=status.HTTP_409_CONFLICT,
    #         detail={"User already reacted to this message"},
    #         )

    # react.append(new_reaction)
    # added = await DB.update(
    #     MESSAGE_COLLECTION, document_id=message_id, data={"emojis": react}
    # )
    # if added:
    #     data = {
    #         "room_id": room_id,
    #         "message_id": message_id,
    #         "emojis": [
    #             {
    #                 "name": new_reaction["name"],
    #                 "count": 1,
    #                 "emoji": new_reaction["emoji"],
    #                 "reactedUsersId": [new_reaction["reactedUsersId"]],
    #             }
    #         ],
    #     }
    #     background_tasks.add_task(
    #         centrifugo_client.publish,
    #         room_id,
    #         Events.MESSAGE_UPDATE,
    #         data,
    #     )
    #     return JSONResponse(
    #         content=ResponseModel.success(data=data, message="reaction added"),
    #         status_code=status.HTTP_200_OK,
    #     )
    # raise HTTPException(
    #     status_code=status.HTTP_424_FAILED_DEPENDENCY, detail={"Reaction not added"}
    # )




   
    # react[new_reaction["name"]] = {
    #     "count": 1,
    #     "emoji": new_reaction["emoji"],
    #     "reactedUsersId": [new_reaction["reactedUsersId"]],
    #     }




    # users = members["room_members"][0]["_id"]
    # if new_reaction["reactedUsersId"] not in users:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid room member"
    #     )
    
    # if new_reaction["name"] not in react["name"]:
    #     react.append(new_reaction)
    #     added = await DB.update(
    #         MESSAGE_COLLECTION, document_id=message_id, data={"emojis": react}
    #     )
    #     if added:
    #         data = {
    #             "room_id": room_id,
    #             "message_id": message_id,
    #             "emojis": [
    #                 {
    #                     "name": new_reaction["name"],
    #                     "count": len(react["name"]),
    #                     "emoji": new_reaction["emoji"],
    #                     "reactedUsersId": [new_reaction["reactedUsersId"]],
    #                 }
    #             ],
    #         }
    #         background_tasks.add_task(
    #             centrifugo_client.publish,
    #             room_id,
    #             Events.MESSAGE_UPDATE,
    #             data,
    #         )
    #         return JSONResponse(
    #             content=ResponseModel.success(data=data, message="reaction added"),
    #             status_code=status.HTTP_200_OK,
    #         )
    #     raise HTTPException(
    #         status_code=status.HTTP_424_FAILED_DEPENDENCY, detail={"Reaction not added"}
    #     )

    # if new_reaction["reactUsersId"] not in react["reactedUsersId"]:
    #     react.append(new_reaction["reactedUsersId"])
    #     added = await DB.update(
    #         MESSAGE_COLLECTION, document_id=message_id, data={"emojis": react}
    #     )
    #     if added:
    #         data = {
    #             "room_id": room_id,
    #             "message_id": message_id,
    #             "emojis": [
    #                 {
    #                     "name": new_reaction["name"],
    #                     "count": len(react["name"]),
    #                     "emoji": new_reaction["emoji"],
    #                     "reactedUsersId": [new_reaction["reactedUsersId"]],
    #                 }
    #             ],
    #         }
    #         background_tasks.add_task(
    #             centrifugo_client.publish,
    #             room_id,
    #             Events.MESSAGE_UPDATE,
    #             data,
    #         )
    #         return JSONResponse(
    #             content=ResponseModel.success(data=data, message="reaction added"),
    #             status_code=status.HTTP_200_OK,
    #         )
    #     raise HTTPException(
    #         status_code=status.HTTP_424_FAILED_DEPENDENCY, detail={"Reaction not added"}
    #     )
    # raise HTTPException(
    #     status_code=status.HTTP_409_CONFLICT,
    #     detail={"User already reacted to this message"},
    # )






# @router.put(
#     "/org/{org_id}/rooms/{room_id}/messages/{message_id}/reactions/addcheck",
#     response_model=ResponseModel,
#     status_code=status.HTTP_200_OK,
#     responses={
#         401: {"description": "Invalid room member"},
#         404: {"description": "message not found"},
#         424: {"description": "reaction not added"},
#     },
# )
# async def add_reaction(
#     request: Emoji,
#     org_id: str,
#     room_id: str,
#     message_id: str,
#     background_tasks: BackgroundTasks,
# ):
#     """
#     Add a reaction to a message

#     Args:
#         request: Request object
#         org_id: A unique identifier of the organization.
#         room_id: A unique identifier of the room.
#         message_id: A unique identifier of the message that is being edited.
#         background_tasks: A daemon thread for publishing to centrifugo

#     Returns:
#         HTTP_200_OK {reaction added successfully}:
#         A dict containing data about the reaction that was added.

#             {
#                 "room_id": "619e28c31a5f54782939d59a",
#                 "message_id": "61ba9b0378fb01b18fac1420",
#                 "name": "lol",
#                 "count": 1,
#                 "emoji": "😂",
#                 "reactedUsersId": ["619ba4671a5f54782939d385"]
#             }

#     Raises:
#         HTTPException [401]: Invalid room member
#         HTTPException [404]: Message not found
#         HTTPException [424]: Reaction not added
#     """
#     DB = DataStorage(org_id)
    
#     message = await get_message(org_id, room_id, message_id) # retrieve message
#     if not message:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Message not found",
#         ) # check if message exists
#     react = message.get("emojis") # get reactions
    
#     new_reaction = request.json # get new reaction
#     # new_reaction = request.dict()
    
#     members = await get_room_members(org_id, room_id) # retrieve room members
#     memberIds = members.keys()
    
#     print (memberIds)
    
#     if new_reaction["reactedUserId"] not in memberIds:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid room member",
#         ) # check if user is in room
    
#     for reaction in react:
#         if reaction["name"] == new_reaction["name"]:
#             if reaction["reactedUserId"] not in reaction["reactedUsersId"]:
#                 reaction["reactedUsersId"].append(new_reaction["reactedUserId"])
#                 reaction["count"] += 1
#                 added = await DB.update(
#                     MESSAGE_COLLECTION, document_id=message_id, data={"emojis": react}
#                 )
#                 if added:    
#                     data = {
#                         "room_id": room_id,
#                         "message_id": message_id,
#                         "emojis": [react],
#                     }
#                     background_tasks.add_task(
#                         centrifugo_client.publish,
#                         room_id,
#                         message_id,
#                         Events.MESSAGE_UPDATE,
#                     )
#                     return JSONResponse(
#                         content=ResponseModel.success(
#                             data=data, message="reaction added successfully"
#                         ),
#                         status_code=status.HTTP_200_OK,
#                     )
#                 raise HTTPException(
#                     status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                     detail="Failure to add reaction",
#                 )
#             raise HTTPException(
#                 status_code=status.HTTP_409_CONFLICT,
#                 detail="Reaction already exists",
#             )
#         # else:
#         #     if reaction["name"] != new_reaction["name"]:
#         react.append(new_reaction)
#         added = await DB.update(
#             MESSAGE_COLLECTION, document_id=message_id, data={"emojis": new_reaction}
#             )
#         if added:
#             data = {
#                 "room_id": room_id,
#                 "message_id": message_id,
#                 "emojis": [new_reaction],
#                 }
#             background_tasks.add_task(
#                 centrifugo_client.publish,
#                 room_id,
#                 message_id,
#                 Events.MESSAGE_UPDATE,
#             )
#             return JSONResponse(
#                 content=ResponseModel.success(
#                 data=data, message="reaction added successfully"
#                  ),
#                 status_code=status.HTTP_200_OK,
#                 )
#         raise HTTPException(        
#             status_code=status.HTTP_424_FAILED_DEPENDENCY,
#             detail="Failure to add reaction",
#             )
            
                    
                
    
    
    
# @router.put(
#     "/org/{org_id}/rooms/{room_id}/messages/{message_id}/reactions/addcheck",
#     response_model=ResponseModel,
#     status_code=status.HTTP_200_OK,
#     responses={
#         401: {"description": "Invalid room member"},
#         404: {"description": "message not found"},
#         424: {"description": "reaction not added"},
#     },
# )
# async def add_reaction(
#     request: Emoji,
#     org_id: str,
#     room_id: str,
#     message_id: str,
#     background_tasks: BackgroundTasks,
# ):
#     """
#     Add a reaction to a message

#     Args:
#         request: Request object
#         org_id: A unique identifier of the organization.
#         room_id: A unique identifier of the room.
#         message_id: A unique identifier of the message that is being edited.
#         background_tasks: A daemon thread for publishing to centrifugo

#     Returns:
#         HTTP_200_OK {reaction added successfully}:
#         A dict containing data about the reaction that was added.

#             {
#                 "room_id": "619e28c31a5f54782939d59a",
#                 "message_id": "61ba9b0378fb01b18fac1420",
#                 "name": "lol",
#                 "count": 1,
#                 "emoji": "😂",
#                 "reactedUsersId": ["619ba4671a5f54782939d385"]
#             }

#     Raises:
#         HTTPException [401]: Invalid room member
#         HTTPException [404]: Message not found
#         HTTPException [424]: Reaction not added
#     """
#     DB = DataStorage(org_id)
    
#     message = await get_message(org_id, room_id, message_id) # retrieve message
#     if not message:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Message not found",
#         ) # check if message exists
#     react = message.get("emojis") # get reactions
    
#     new_reaction = request.json # get new reaction
#     # new_reaction = request.dict()
    
#     members = await get_room_members(org_id, room_id) # retrieve room members
#     memberIds = members.keys()
    
#     print (memberIds)
    
#     if new_reaction["reactedUserId"] not in memberIds:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid room member",
#         ) # check if user is in room
    
#     if new_reaction["name"] not in react.keys():
#         react.append(new_reaction)
#         added = await DB.update(
#             MESSAGE_COLLECTION, document_id=message_id, data={"emojis": new_reaction}
#         )
#         if added: # and added.get("status_code") is None:
#             data = {
#                 "room_id": room_id,
#                 "message_id": message_id,
#                 "emojis": [new_reaction],
#             }   
                
#             background_tasks.add_task(
#                 centrifugo_client.publish,
#                 room_id,
#                 message_id,
#                 Events.MESSAGE_UPDATE,
#             )
#             return JSONResponse(
#                 content=ResponseModel.success(
#                     data=data, message="reaction added successfully"
#                 ),
#                 status_code=status.HTTP_200_OK,
#             )
#         raise HTTPException(
#             status_code=status.HTTP_424_FAILED_DEPENDENCY,
#             detail="Failure to add reaction",
#         )
    
#     for reaction in react:
#         if reaction["name"] == new_reaction["name"]:
#             if reaction["reactedUserId"] not in reaction["reactedUsersId"]:
#                 reaction["reactedUsersId"].append(new_reaction["reactedUserId"])
#                 reaction["count"] += 1
#                 added = await DB.update(
#                     MESSAGE_COLLECTION, document_id=message_id, data={"emojis": react}
#                 )
#                 if added:    
#                     data = {
#                         "room_id": room_id,
#                         "message_id": message_id,
#                         "emojis": [react],
#                     }
#                     background_tasks.add_task(
#                         centrifugo_client.publish,
#                         room_id,
#                         message_id,
#                         Events.MESSAGE_UPDATE,
#                     )
#                     return JSONResponse(
#                         content=ResponseModel.success(
#                             data=data, message="reaction added successfully"
#                         ),
#                         status_code=status.HTTP_200_OK,
#                     )
#                 raise HTTPException(
#                     status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                     detail="Failure to add reaction",
#                 )
#             raise HTTPException(
#                 status_code=status.HTTP_409_CONFLICT,
#                 detail="Reaction already exists",
#             )
#         raise HTTPException(        
#             status_code=status.HTTP_424_FAILED_DEPENDENCY,
#             detail="Failure to add reaction",
#             )
                         
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # if new_reaction["name"] in react.keys():
    #     # check if reaction already exists
    #     for reaction in react[new_reaction["name"]]:
    #         if reaction["reactedUserId"] == new_reaction["reactedUserId"]:
    #             raise HTTPException(
    #                 status_code=status.HTTP_424_FAILED_DEPENDENCY,
    #                 detail="Reaction not added",
    #             )
                
                
    # if new_reaction["reactedUserId"] in react.keys():
    #     if new_reaction["name"] in react[new_reaction["reactedUserId"]].keys():
    #         react[new_reaction["reactedUserId"]][new_reaction["name"]] += 1
    #     else:
    #         react[new_reaction["reactedUserId"]][new_reaction["name"]] = 1
        
        
        
        
        
        
        
        
        
        
        
    # memberIds = str(list(members)) # convert room members to string
    
    # # memberIds = list(members) # convert room members to string
    # print (memberIds)
    # print (type(memberIds))
    
    # message = await get_message(org_id, room_id, message_id) # retrieve message
    # if not message:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND, detail="Message not found"
    #     )
        
    # react = message.get("emojis")
    # print (react)
    
    # new_reaction = request.dict()
    
    # if new_reaction["reactedUsersId"] in [memberIds]: # check if reactor is a room member
    #     print ("user found")
    #     if new_reaction["name"] not in react:
    #         react.append(new_reaction)
    #         added = await DB.update(
    #             MESSAGE_COLLECTION, document_id=message_id, data={"emojis": new_reaction}
    #         )
    #         if added:
    #             data = {
    #                 "room_id": room_id,
    #                 "message_id": message_id,
    #                 "emojis": [
    #                     {
    #                         "name": new_reaction["name"],
    #                         "emoji": new_reaction["emoji"],
    #                         "reactedUsersId": [new_reaction["reactedUsersId"]],
    #                         "count": +1
    #                     }
    #                 ],
    #             }
    #             background_tasks.add_task(
    #                 centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, data
    #             )  # publish to centrifugo in the background
    #             return JSONResponse(
    #                 content=ResponseModel.success(data=data, message="reaction added"),
    #                 status_code=status.HTTP_200_OK,
    #             )
    #         raise HTTPException(
    #             status_code=status.HTTP_424_FAILED_DEPENDENCY, detail={"Reaction not added"}
    #         )
    #     if new_reaction["reactedUsersId"] not in react:
    #         react.append(new_reaction["reactedUsersId"])
    #         added = await DB.update(
    #             MESSAGE_COLLECTION, document_id=message_id, data={"emojis": react}
    #         )
    #         if added:
    #             data = {
    #                 "room_id": room_id,
    #                 "message_id": message_id,
    #                 "emojis": [
    #                     {
    #                         "name": react["name"],
    #                         "emoji": react["emoji"],
    #                         "reactedUsersId": [new_reaction["reactedUsersId"]],
    #                         "count": len(react["reactedUsersId"])
    #                     }
    #                 ],
    #             }
    #             background_tasks.add_task(
    #                 centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, data
    #             )  # publish to centrifugo in the background
    #             return JSONResponse(
    #                 content=ResponseModel.success(data=data, message="reaction added"),
    #                 status_code=status.HTTP_200_OK,
    #             )
    #         raise HTTPException(
    #             status_code=status.HTTP_424_FAILED_DEPENDENCY, detail={"Reaction not added"}
    #         )
    #     raise HTTPException(
    #         status_code=status.HTTP_409_CONFLICT,
    #         detail={"Reaction already exists"},
    #     )
    # raise HTTPException(
    #     status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid room member"
    # )
                
                
        




                    
    
    
    # if new_reaction["name"] in react.keys():
    #     # check if reaction already exists
    #     for reaction in react[new_reaction["name"]]:
    #         if reaction["reactedUserId"] == new_reaction["reactedUserId"]:
    #             raise HTTPException(
    #                 status_code=status.HTTP_424_FAILED_DEPENDENCY,
    #                 detail="Reaction not added",
    #             )
                
                
    # if new_reaction["reactedUserId"] in react.keys():
    #     if new_reaction["name"] in react[new_reaction["reactedUserId"]].keys():
    #         react[new_reaction["reactedUserId"]][new_reaction["name"]] += 1
    #     else:
    #         react[new_reaction["reactedUserId"]][new_reaction["name"]] = 1
        
        
        
        
        
        
        
        
        
        
        
    # memberIds = str(list(members)) # convert room members to string
    
    # # memberIds = list(members) # convert room members to string
    # print (memberIds)
    # print (type(memberIds))
    
    # message = await get_message(org_id, room_id, message_id) # retrieve message
    # if not message:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND, detail="Message not found"
    #     )
        
    # react = message.get("emojis")
    # print (react)
    
    # new_reaction = request.dict()
    
    # if new_reaction["reactedUsersId"] in [memberIds]: # check if reactor is a room member
    #     print ("user found")
    #     if new_reaction["name"] not in react:
    #         react.append(new_reaction)
    #         added = await DB.update(
    #             MESSAGE_COLLECTION, document_id=message_id, data={"emojis": new_reaction}
    #         )
    #         if added:
    #             data = {
    #                 "room_id": room_id,
    #                 "message_id": message_id,
    #                 "emojis": [
    #                     {
    #                         "name": new_reaction["name"],
    #                         "emoji": new_reaction["emoji"],
    #                         "reactedUsersId": [new_reaction["reactedUsersId"]],
    #                         "count": +1
    #                     }
    #                 ],
    #             }
    #             background_tasks.add_task(
    #                 centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, data
    #             )  # publish to centrifugo in the background
    #             return JSONResponse(
    #                 content=ResponseModel.success(data=data, message="reaction added"),
    #                 status_code=status.HTTP_200_OK,
    #             )
    #         raise HTTPException(
    #             status_code=status.HTTP_424_FAILED_DEPENDENCY, detail={"Reaction not added"}
    #         )
    #     if new_reaction["reactedUsersId"] not in react:
    #         react.append(new_reaction["reactedUsersId"])
    #         added = await DB.update(
    #             MESSAGE_COLLECTION, document_id=message_id, data={"emojis": react}
    #         )
    #         if added:
    #             data = {
    #                 "room_id": room_id,
    #                 "message_id": message_id,
    #                 "emojis": [
    #                     {
    #                         "name": react["name"],
    #                         "emoji": react["emoji"],
    #                         "reactedUsersId": [new_reaction["reactedUsersId"]],
    #                         "count": len(react["reactedUsersId"])
    #                     }
    #                 ],
    #             }
    #             background_tasks.add_task(
    #                 centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, data
    #             )  # publish to centrifugo in the background
    #             return JSONResponse(
    #                 content=ResponseModel.success(data=data, message="reaction added"),
    #                 status_code=status.HTTP_200_OK,
    #             )
    #         raise HTTPException(
    #             status_code=status.HTTP_424_FAILED_DEPENDENCY, detail={"Reaction not added"}
    #         )
    #     raise HTTPException(
    #         status_code=status.HTTP_409_CONFLICT,
    #         detail={"Reaction already exists"},
    #     )
    # raise HTTPException(
    #     status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid room member"
    # )
                
                
        