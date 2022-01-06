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

