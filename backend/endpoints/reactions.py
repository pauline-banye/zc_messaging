# current fully functional in mssg

# @router.put( # ADD REACTION ONLY
#     "/org/{org_id}/rooms/{room_id}/messages/{message_id}/reaction/add",
#     response_model=ResponseModel,
#     status_code=status.HTTP_200_OK,
#     responses={
#         401: {"description": "Invalid room member"},
#         404: {"description": "Message not found"},
#         409: {"description": "Member already reacted with this emoji"},
#         424: {
#             "description": "Failed to retrieve room members || Failed to add reaction"
#         },
#     },
# )
# async def add_reactions(
#     request: Emoji,
#     org_id: str,
#     room_id: str,
#     message_id: str,
#     background_tasks: BackgroundTasks,
# ):
#     """
#     Checks if there are any reactions for the message.
#     Adds a reaction to a message.
#     Adds a user to list of reacted users if reaction already exists.

#     Args:
#         request: Request object
#         org_id: A unique identifier of the organization.
#         room_id: A unique identifier of the room.
#         message_id: A unique identifier of the message that is being edited.
#         background_tasks: A daemon thread for publishing to centrifugo

#     Returns:
#         HTTP_200_OK {Reaction added successfully}}:
#         A dict containing data about the reaction that was added or removed.

#         {
#             "room_id": "619e28c31a5f54782939d59a",
#             "message_id": "61cb65f378fb01b18fac147b",
#             "emojis": [{
#                 "name": "lol",
#                 "count": 2,
#                 "emoji": "lol",
#                 "reactedUsersId": [
#                     "619ba4671a5f54782939d385",
#                     "6169704bc4133ddaa309dd07"
#                 ]
#             }]
#         }

#     Raises:
#         HTTPException [401]: Invalid room member
#         HTTPException [404]: Message not found || Room not found
#         HTTPException [409]: Member already reacted with this emoji
#         HTTPException [424]: Failed to add reaction
#     """
#     DB = DataStorage(org_id)

#     message = await get_message(org_id, room_id, message_id)  # get message
#     if not message:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Message not found",
#         )
#     print ("message", message)
#     reactions = message.get("emojis")

#     room = await get_room(org_id, room_id)
#     if not room:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Room not found"
#         )
#     print ("room", room)
#     members = room.get("room_members", {})
#     print ("room members", members)
    
#     new_reaction = request.dict()
#     if new_reaction["reactedUsersId"][0] not in list(members):  # check if user is in list of room members
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid room member",
#         )  

#     print ("list of room members", list(members))
#     print ("new reaction user id", new_reaction["reactedUsersId"])
    
#     # if no reactions exist for the message
#     if not reactions:
#         reactions = [new_reaction]
#         updated_emoji = await DB.update(
#             MESSAGE_COLLECTION, document_id=message_id, data={"emojis": reactions}
#         )
#         if updated_emoji and updated_emoji.get("status_code") is not None:
#             raise HTTPException(
#                 status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                 detail="Failed to add reaction",
#             )
#         # publish to centrifugo in the background
#         background_tasks.add_task(
#             centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, new_reaction
#         )
#         return JSONResponse(
#             content=ResponseModel.success(data=new_reaction, message="Reaction added successfully"),
#             status_code=status.HTTP_200_OK,
#         )

#     # if reactions exist for the message
#     for emoji in reactions:
#         if emoji["name"] == new_reaction["name"]:  # if emoji is already in reactions

#             # if user hasn't reacted with the emoji
#             if new_reaction["reactedUsersId"][0] not in emoji["reactedUsersId"]:
#                 emoji["reactedUsersId"].append(new_reaction["reactedUsersId"][0])
#                 emoji["count"] += 1

#                 print(emoji)

#                 added = await DB.update(
#                     MESSAGE_COLLECTION,
#                     document_id=message_id,
#                     data={"emojis": reactions},
#                 )
#                 if added and added.get("status_code") is not None:
#                     raise HTTPException(
#                         status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                         detail="Failed to add reaction",
#                     )
#                 # publish to centrifugo in the background
#                 background_tasks.add_task(
#                     centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, emoji
#                 )
#                 return JSONResponse(
#                     content=ResponseModel.success(data=emoji, message="Reaction added successfully"),
#                     status_code=status.HTTP_200_OK,
#                 )
#             # if user has reacted with the emoji
#             raise HTTPException(
#                 status_code=status.HTTP_409_CONFLICT,
#                 detail="Member already reacted with this emoji",
#             )

#     # if emoji is not in reactions
#     reactions.append(new_reaction)
#     new = await DB.update(
#         MESSAGE_COLLECTION, document_id=message_id, data={"emojis": reactions}
#     )
#     if new and new.get("status_code") is not None:
#         raise HTTPException(
#             status_code=status.HTTP_424_FAILED_DEPENDENCY,
#             detail="Failed to add reaction",
#         )
#     # publish to centrifugo in the background
#     background_tasks.add_task(
#         centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, new_reaction
#     )
#     return JSONResponse(
#         content=ResponseModel.success(data=new_reaction, message="Reaction added successfully"),
#         status_code=status.HTTP_200_OK,
#     )



# @router.put(  # MERGED ADD AND REMOVE REACTIONS
#     "/org/{org_id}/rooms/{room_id}/messages/{message_id}/reaction",
#     response_model=ResponseModel,
#     status_code=status.HTTP_200_OK,
#     responses={
#         401: {"description": "Invalid room member"},
#         404: {"description": "Message not found"},
#         424: {"description": "Failed to retrieve room members"},
#     },
# )
# async def message_reactions(
#     request: Emoji,
#     org_id: str,
#     room_id: str,
#     message_id: str,
#     background_tasks: BackgroundTasks,
# ):
#     """
#     Checks if there are any reactions for the message.
#     Adds a reaction to a message.
#     Adds a user to list of reacted users if reaction already exists.
#     Removes the user from the list of reacted users if user already reacted to the message.
#     Removes a reaction from a message if reacted user count is 0.

#     Args:
#         request: Request object
#         org_id: A unique identifier of the organization.
#         room_id: A unique identifier of the room.
#         message_id: A unique identifier of the message that is being edited.
#         background_tasks: A daemon thread for publishing to centrifugo

#     Returns:
#         HTTP_200_OK {Reaction added successfully || Reaction removed successfully}:
#         A dict containing data about the reaction that was added or removed.

#         {
#             "room_id": "619e28c31a5f54782939d59a",
#             "message_id": "61cb65f378fb01b18fac147b",
#             "emojis": [{
#                 "name": "lol",
#                 "count": 2,
#                 "emoji": "lol",
#                 "reactedUsersId": [
#                     "619ba4671a5f54782939d385",
#                     "6169704bc4133ddaa309dd07"
#                 ]
#             }]
#         }

#     Raises:
#         HTTPException [401]: Invalid room member
#         HTTPException [404]: Message not found || Room not found
#         HTTPException [424]: Failed to add reaction || Failed to remove reaction
#     """
#     DB = DataStorage(org_id)

#     message = await get_message(org_id, room_id, message_id)
#     if not message:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Message not found",
#         )
#     print ("message", message)
#     reactions = message.get("emojis")

#     room = await get_room(org_id, room_id)
#     if not room:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Room not found"
#         )
#     print ("room", room)
#     members = room.get("room_members", {})
#     print ("room members", members)
    
#     new_reaction = request.dict()
#     if new_reaction["reactedUsersId"][0] not in list(members):  # check if user is in list of room members
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid room member",
#         )  

#     print ("list of room members", list(members))
#     print ("new reaction user id", new_reaction["reactedUsersId"])
    
#     # if no reactions exist for the message
#     if not reactions:
#         reactions = [new_reaction]
#         updated_emoji = await DB.update(
#             MESSAGE_COLLECTION, document_id=message_id, data={"emojis": reactions}
#         )
#         if updated_emoji and updated_emoji.get("status_code") is not None:
#             raise HTTPException(
#                 status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                 detail="Failed to add reaction",
#             )
#         # publish to centrifugo in the background
#         background_tasks.add_task(
#             centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, new_reaction
#         )
#         return JSONResponse(
#             content=ResponseModel.success(data=new_reaction, message="Reaction added successfully"),
#             status_code=status.HTTP_200_OK,
#         )

#         # if reactions exist for the message
#     for emoji in reactions:
#         if emoji["name"] == new_reaction["name"]:  # if emoji is already in reactions

#             # if user hasn't reacted with the emoji
#             if new_reaction["reactedUsersId"][0] not in emoji["reactedUsersId"]:
#                 emoji["reactedUsersId"].append(new_reaction["reactedUsersId"][0])
#                 emoji["count"] += 1

#                 print(emoji)
#                 added = await DB.update(
#                     MESSAGE_COLLECTION,
#                     document_id=message_id,
#                     data={"emojis": reactions},
#                 )
#                 if added and added.get("status_code") is not None:
#                     raise HTTPException(
#                         status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                         detail="Failed to add reaction",
#                     )
#                 # publish to centrifugo in the background
#                 background_tasks.add_task(
#                     centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, emoji
#                 )
#                 return JSONResponse(
#                     content=ResponseModel.success(
#                         data=emoji, message="Reaction added successfully"
#                     ),
#                     status_code=status.HTTP_200_OK,
#                 )

#             # if user has reacted with the emoji
#             emoji["reactedUsersId"].remove(new_reaction["reactedUsersId"][0])
#             emoji["count"] -= 1
#             # emoji.get("reactedUsersId").remove(new_reaction.get("reactedUsersId")[0])
#             # emoji["count"] -= 1
#             if emoji.get("count") != 0:
#                 updated = await DB.update(
#                     MESSAGE_COLLECTION,
#                     document_id=message_id,
#                     data={"emojis": reactions},
#                 )
#                 if updated and updated.get("status_code") is not None:
#                     raise HTTPException(
#                         status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                         detail="Failed to remove reaction",
#                     )
#                 # publish to centrifugo in the background
#                 background_tasks.add_task(
#                     centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, emoji
#                 )
#                 return JSONResponse(
#                     content=ResponseModel.success(
#                         data=emoji, message="Reaction removed successfully"
#                     ),
#                     status_code=status.HTTP_200_OK,
#                 )

#             reactions.remove(emoji)  # if emoji count is 0
#             removed = await DB.update(
#                 MESSAGE_COLLECTION, document_id=message_id, data={"emojis": reactions}
#             )
#             if removed and removed.get("status_code") is not None:
#                 raise HTTPException(
#                     status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                     detail="Failed to remove reaction",
#                 )
#             # publish to centrifugo in the background
#             background_tasks.add_task(
#                 centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, removed
#             )
#             return JSONResponse(
#                 content=ResponseModel.success(
#                     data=None, message="Reaction removed successfully"
#                 ),
#                 status_code=status.HTTP_200_OK,
#             )

#     # if emoji is not in reactions
#     reactions.append(new_reaction)
#     new = await DB.update(
#         MESSAGE_COLLECTION, document_id=message_id, data={"emojis": reactions}
#     )
#     if new and new.get("status_code") is not None:
#         raise HTTPException(
#             status_code=status.HTTP_424_FAILED_DEPENDENCY,
#             detail="Failed to add new reaction",
#         )
#     # publish to centrifugo in the background
#     background_tasks.add_task(
#         centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, new_reaction
#     )
#     return JSONResponse(
#         content=ResponseModel.success(
#             data=new_reaction, message="Reaction added successfully"
#         ),
#         status_code=status.HTTP_200_OK,
#     )



# @router.put(  # fully functional remove reactions
#     "/org/{org_id}/rooms/{room_id}/messages/{message_id}/reaction/remove",
#     response_model=ResponseModel,
#     status_code=status.HTTP_200_OK,
#     responses={
#         401: {"description": "Invalid room member"},
#         404: {"description": "Message not found"},
#         424: {
#             "description": "Failed to retrieve room members || Failed to remove reaction"
#         },
#     },
# )
# async def remove_reactions(
#     request: Emoji,
#     org_id: str,
#     room_id: str,
#     message_id: str,
#     background_tasks: BackgroundTasks,
# ):
#     """
#     Checks if there are any reactions for the message.
#     Removes the user from the list of reacted users if user already reacted to the message.
#     Removes a reaction from a message if reacted user count is 0.
#     Args:
#         request: Request object
#         org_id: A unique identifier of the organization.
#         room_id: A unique identifier of the room.
#         message_id: A unique identifier of the message that is being edited.
#         background_tasks: A daemon thread for publishing to centrifugo
#     Returns:
#         HTTP_200_OK {reaction added}:
#         A dict containing data about the reaction that was added or removed.
#         {
#             "room_id": "619e28c31a5f54782939d59a",
#             "message_id": "61cb65f378fb01b18fac147b",
#             "emojis": [{
#                 "name": "lol",
#                 "count": 2,
#                 "emoji": "lol",
#                 "reactedUsersId": [
#                     "619ba4671a5f54782939d385",
#                     "6169704bc4133ddaa309dd07"
#                 ]
#             }]
#         }
#     Raises:
#         HTTPException [400]: No reactions exist for this message || Member hasn't reacted with emoji
#         HTTPException [401]: Invalid room member
#         HTTPException [404]: Message not found || Room not found
#         HTTPException [424]: Failed to retrieve room members || Failed to remove reaction
#     """
#     DB = DataStorage(org_id)

#     message = await get_message(org_id, room_id, message_id)  # get message
#     if not message:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Message not found",
#         )
#     print ("message", message)
#     reaction = message.get("emojis")

#     room = await get_room(org_id, room_id)
#     if not room:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Room not found"
#         )
#     print ("room", room)
#     members = room.get("room_members", {})
#     print ("room members", members)
    
#     new_reaction = request.dict()
#     if new_reaction["reactedUsersId"][0] not in list(members):  # check if user is in list of room members
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid room member",
#         )  

#     print ("list of room members", list(members))
#     print ("new reaction user id", new_reaction["reactedUsersId"])

#     # if no reactions exist for the message
#     if not reaction:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="No reactions exist for this message",
#         )

#     # if reactions exist for the message
#     for emoji in reaction:
#         if emoji["name"] == new_reaction["name"]:  # if emoji is already in reactions

#             # if user hasn't reacted with the emoji
#             if new_reaction["reactedUsersId"][0] not in emoji["reactedUsersId"]:
#                 raise HTTPException(
#                     status_code=status.HTTP_400_BAD_REQUEST,
#                     detail="Member hasn't reacted with this emoji",
#                 )
#             emoji["reactedUsersId"].remove(new_reaction["reactedUsersId"][0])
#             emoji["count"] -= 1
                
#             if emoji.get("count") != 0:
#                 updated = await DB.update(
#                     MESSAGE_COLLECTION,
#                     document_id=message_id,
#                     data={"emojis": reaction},
#                 )
#                 if updated and updated.get("status_code") is not None:
#                     raise HTTPException(
#                         status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                         detail="Failed to remove member's reaction",
#                     )
#                 # publish to centrifugo in the background
#                 background_tasks.add_task(
#                     centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, emoji
#                 )
#                 return JSONResponse(
#                     content=ResponseModel.success(
#                         data=emoji, message="member's reaction removed successfully"
#                     ),
#                     status_code=status.HTTP_200_OK,
#                 )

#             reaction.remove(emoji)  # if emoji count is 0
#             removed = await DB.update(
#                 MESSAGE_COLLECTION, document_id=message_id, data={"emojis": reaction}
#             )
#             if removed and removed.get("status_code") is not None:
#                 raise HTTPException(
#                     status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                     detail="Failed to remove reaction",
#                 )
#             # publish to centrifugo in the background
#             background_tasks.add_task(
#                 centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, removed
#             )
#             return JSONResponse(
#                 content=ResponseModel.success(
#                     data=None, message="reaction removed successfully"
#                 ),
#                 status_code=status.HTTP_200_OK,
#             )

#     # if emoji is not in reactions
#     raise HTTPException(
#         status_code=status.HTTP_400_BAD_REQUEST,
#         detail="No member reacted with this emoji",
#     )







# from fastapi import APIRouter, BackgroundTasks, HTTPException, status
# from schema.message import Emoji, Message, MessageRequest
# from schema.response import ResponseModel
# from starlette.responses import JSONResponse
# from utils.centrifugo import Events, centrifugo_client
# from utils.db import DataStorage
# from utils.message_utils import (MESSAGE_COLLECTION, get_message)
# from utils.room_utils import get_room

# router = APIRouter()


# @router.put( # ADD REACTION ONLY
#     "/org/{org_id}/rooms/{room_id}/messages/{message_id}/reaction/add",
#     response_model=ResponseModel,
#     status_code=status.HTTP_200_OK,
#     responses={
#         401: {"description": "Invalid room member"},
#         404: {"description": "Message not found"},
#         409: {"description": "Member already reacted with this emoji"},
#         424: {
#             "description": "Failed to retrieve room members || Failed to add reaction"
#         },
#     },
# )
# async def add_reactions(
#     request: Emoji,
#     org_id: str,
#     room_id: str,
#     message_id: str,
#     background_tasks: BackgroundTasks,
# ):
#     """
#     Checks if there are any reactions for the message.
#     Adds a reaction to a message.
#     Adds a user to list of reacted users if reaction already exists.

#     Args:
#         request: Request object
#         org_id: A unique identifier of the organization.
#         room_id: A unique identifier of the room.
#         message_id: A unique identifier of the message that is being edited.
#         background_tasks: A daemon thread for publishing to centrifugo

#     Returns:
#         HTTP_200_OK {Reaction added successfully}}:
#         A dict containing data about the reaction that was added or removed.

#         {
#             "room_id": "619e28c31a5f54782939d59a",
#             "message_id": "61cb65f378fb01b18fac147b",
#             "emojis": [{
#                 "name": "lol",
#                 "count": 2,
#                 "emoji": "lol",
#                 "reactedUsersId": [
#                     "619ba4671a5f54782939d385",
#                     "6169704bc4133ddaa309dd07"
#                 ]
#             }]
#         }

#     Raises:
#         HTTPException [401]: Invalid room member
#         HTTPException [404]: Message not found || Room not found
#         HTTPException [409]: Member already reacted with this emoji
#         HTTPException [424]: Failed to add reaction
#     """
#     DB = DataStorage(org_id)

#     message = await get_message(org_id, room_id, message_id)  # get message
#     if not message:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Message not found",
#         )
#     print ("message", message)
#     reactions = message.get("emojis")

#     room = await get_room(org_id, room_id)
#     if not room:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Room not found"
#         )
#     print ("room", room)
#     members = room.get("room_members", {})
#     print ("room members", members)
    
#     new_reaction = request.dict()
#     if new_reaction["reactedUsersId"][0] not in list(members):  # check if user is in list of room members
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid room member",
#         )  

#     print ("list of room members", list(members))
#     print ("new reaction user id", new_reaction["reactedUsersId"])
    
#     # if no reactions exist for the message
#     if not reactions:
#         reactions = [new_reaction]
#         updated_emoji = await DB.update(
#             MESSAGE_COLLECTION, document_id=message_id, data={"emojis": reactions}
#         )
#         if updated_emoji and updated_emoji.get("status_code") is not None:
#             raise HTTPException(
#                 status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                 detail="Failed to add reaction",
#             )
#         # publish to centrifugo in the background
#         background_tasks.add_task(
#             centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, new_reaction
#         )
#         return JSONResponse(
#             content=ResponseModel.success(data=new_reaction, message="Reaction added successfully"),
#             status_code=status.HTTP_200_OK,
#         )

#     # if reactions exist for the message
#     for emoji in reactions:
#         if emoji["name"] == new_reaction["name"]:  # if emoji is already in reactions

#             # if user hasn't reacted with the emoji
#             if new_reaction["reactedUsersId"][0] not in emoji["reactedUsersId"]:
#                 emoji["reactedUsersId"].append(new_reaction["reactedUsersId"][0])
#                 emoji["count"] += 1

#                 print(emoji)

#                 added = await DB.update(
#                     MESSAGE_COLLECTION,
#                     document_id=message_id,
#                     data={"emojis": reactions},
#                 )
#                 if added and added.get("status_code") is not None:
#                     raise HTTPException(
#                         status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                         detail="Failed to add reaction",
#                     )
#                 # publish to centrifugo in the background
#                 background_tasks.add_task(
#                     centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, emoji
#                 )
#                 return JSONResponse(
#                     content=ResponseModel.success(data=emoji, message="Reaction added successfully"),
#                     status_code=status.HTTP_200_OK,
#                 )
#             # if user has reacted with the emoji
#             raise HTTPException(
#                 status_code=status.HTTP_409_CONFLICT,
#                 detail="Member already reacted with this emoji",
#             )

#     # if emoji is not in reactions
#     reactions.append(new_reaction)
#     new = await DB.update(
#         MESSAGE_COLLECTION, document_id=message_id, data={"emojis": reactions}
#     )
#     if new and new.get("status_code") is not None:
#         raise HTTPException(
#             status_code=status.HTTP_424_FAILED_DEPENDENCY,
#             detail="Failed to add reaction",
#         )
#     # publish to centrifugo in the background
#     background_tasks.add_task(
#         centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, new_reaction
#     )
#     return JSONResponse(
#         content=ResponseModel.success(data=new_reaction, message="Reaction added successfully"),
#         status_code=status.HTTP_200_OK,
#     )



# @router.put(  # MERGED ADD AND REMOVE REACTIONS
#     "/org/{org_id}/rooms/{room_id}/messages/{message_id}/reaction",
#     response_model=ResponseModel,
#     status_code=status.HTTP_200_OK,
#     responses={
#         401: {"description": "Invalid room member"},
#         404: {"description": "Message not found"},
#         424: {"description": "Failed to retrieve room members"},
#     },
# )
# async def message_reactions(
#     request: Emoji,
#     org_id: str,
#     room_id: str,
#     message_id: str,
#     background_tasks: BackgroundTasks,
# ):
#     """
#     Checks if there are any reactions for the message.
#     Adds a reaction to a message.
#     Adds a user to list of reacted users if reaction already exists.
#     Removes the user from the list of reacted users if user already reacted to the message.
#     Removes a reaction from a message if reacted user count is 0.

#     Args:
#         request: Request object
#         org_id: A unique identifier of the organization.
#         room_id: A unique identifier of the room.
#         message_id: A unique identifier of the message that is being edited.
#         background_tasks: A daemon thread for publishing to centrifugo

#     Returns:
#         HTTP_200_OK {Reaction added successfully || Reaction removed successfully}:
#         A dict containing data about the reaction that was added or removed.

#         {
#             "room_id": "619e28c31a5f54782939d59a",
#             "message_id": "61cb65f378fb01b18fac147b",
#             "emojis": [{
#                 "name": "lol",
#                 "count": 2,
#                 "emoji": "lol",
#                 "reactedUsersId": [
#                     "619ba4671a5f54782939d385",
#                     "6169704bc4133ddaa309dd07"
#                 ]
#             }]
#         }

#     Raises:
#         HTTPException [401]: Invalid room member
#         HTTPException [404]: Message not found || Room not found
#         HTTPException [424]: Failed to add reaction || Failed to remove reaction
#     """
#     DB = DataStorage(org_id)

#     message = await get_message(org_id, room_id, message_id)
#     if not message:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Message not found",
#         )
#     print ("message", message)
#     reactions = message.get("emojis")

#     room = await get_room(org_id, room_id)
#     if not room:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Room not found"
#         )
#     print ("room", room)
#     members = room.get("room_members", {})
#     print ("room members", members)
    
#     new_reaction = request.dict()
#     if new_reaction["reactedUsersId"][0] not in list(members):  # check if user is in list of room members
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid room member",
#         )  

#     print ("list of room members", list(members))
#     print ("new reaction user id", new_reaction["reactedUsersId"])
    
#     # if no reactions exist for the message
#     if not reactions:
#         reactions = [new_reaction]
#         updated_emoji = await DB.update(
#             MESSAGE_COLLECTION, document_id=message_id, data={"emojis": reactions}
#         )
#         if updated_emoji and updated_emoji.get("status_code") is not None:
#             raise HTTPException(
#                 status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                 detail="Failed to add reaction",
#             )
#         # publish to centrifugo in the background
#         background_tasks.add_task(
#             centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, new_reaction
#         )
#         return JSONResponse(
#             content=ResponseModel.success(data=new_reaction, message="Reaction added successfully"),
#             status_code=status.HTTP_200_OK,
#         )

#     # if reactions exist for the message
#     for emoji in reactions:
#         if emoji.get("name") == new_reaction.get("name"):
#             if new_reaction.get("reactedUsersId")[0] not in emoji.get("reactedUsersId"):
#                 emoji.get("reactedUsersId").append(
#                     new_reaction.get("reactedUsersId")[0]
#                 )
#                 emoji["count"] += 1

#                 added = await DB.update(
#                     MESSAGE_COLLECTION,
#                     document_id=message_id,
#                     data={"emojis": reactions},
#                 )
#                 if added and added.get("status_code") is not None:
#                     raise HTTPException(
#                         status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                         detail="Failed to add reaction",
#                     )
#                 # publish to centrifugo in the background
#                 background_tasks.add_task(
#                     centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, emoji
#                 )
#                 return JSONResponse(
#                     content=ResponseModel.success(
#                         data=emoji, message="Reaction added successfully"
#                     ),
#                     status_code=status.HTTP_200_OK,
#                 )

#             # if user has reacted with the emoji
#             emoji.get("reactedUsersId").remove(new_reaction.get("reactedUsersId")[0])
#             emoji["count"] -= 1

#             if emoji.get("count") != 0:
#                 updated = await DB.update(
#                     MESSAGE_COLLECTION,
#                     document_id=message_id,
#                     data={"emojis": reactions},
#                 )
#                 if updated and updated.get("status_code") is not None:
#                     raise HTTPException(
#                         status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                         detail="Failed to remove reaction",
#                     )
#                 # publish to centrifugo in the background
#                 background_tasks.add_task(
#                     centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, emoji
#                 )
#                 return JSONResponse(
#                     content=ResponseModel.success(
#                         data=emoji, message="Reaction removed successfully"
#                     ),
#                     status_code=status.HTTP_200_OK,
#                 )

#             reactions.remove(emoji)  # if emoji count is 0
#             removed = await DB.update(
#                 MESSAGE_COLLECTION, document_id=message_id, data={"emojis": reactions}
#             )
#             if removed and removed.get("status_code") is not None:
#                 raise HTTPException(
#                     status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                     detail="Failed to remove reaction",
#                 )
#             # publish to centrifugo in the background
#             background_tasks.add_task(
#                 centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, removed
#             )
#             return JSONResponse(
#                 content=ResponseModel.success(
#                     data=None, message="Reaction removed successfully"
#                 ),
#                 status_code=status.HTTP_200_OK,
#             )

#     # if emoji is not in reactions
#     reactions.append(new_reaction)
#     new = await DB.update(
#         MESSAGE_COLLECTION, document_id=message_id, data={"emojis": reactions}
#     )
#     if new and new.get("status_code") is not None:
#         raise HTTPException(
#             status_code=status.HTTP_424_FAILED_DEPENDENCY,
#             detail="Failed to add new reaction",
#         )
#     # publish to centrifugo in the background
#     background_tasks.add_task(
#         centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, new_reaction
#     )
#     return JSONResponse(
#         content=ResponseModel.success(
#             data=new_reaction, message="Reaction added successfully"
#         ),
#         status_code=status.HTTP_200_OK,
#     )


# @router.put(  # REMOVE REACTION
#     "/org/{org_id}/rooms/{room_id}/messages/{message_id}/reaction/remove",
#     response_model=ResponseModel,
#     status_code=status.HTTP_200_OK,
#     responses={
#         400: {"No reactions exist for this message || No reaction with this emoji"},
#         401: {"description": "Invalid room member"},
#         404: {"description": "Message not found || Room not found"},
#         424: {"description": "Failed to remove reaction"},
#     }
# )
# async def remove_reactions(
#     request: Emoji,
#     org_id: str,
#     room_id: str,
#     message_id: str,
#     background_tasks: BackgroundTasks,
# ):
#     """
#     Checks if there are any reactions for the message.
#     Removes the user from the list of reacted users if user already reacted to the message.
#     Removes a reaction from a message if reacted user count is 0.

#     Args:
#         request: Request object
#         org_id: A unique identifier of the organization.
#         room_id: A unique identifier of the room.
#         message_id: A unique identifier of the message that is being edited.
#         background_tasks: A daemon thread for publishing to centrifugo

#     Returns:
#         HTTP_200_OK {Reaction removed successfully}:
#         A dict containing data about the reaction that was added or removed.

#         {
#             "room_id": "619e28c31a5f54782939d59a",
#             "message_id": "61cb65f378fb01b18fac147b",
#             "emojis": [{
#                 "name": "lol",
#                 "count": 2,
#                 "emoji": "lol",
#                 "reactedUsersId": [
#                     "619ba4671a5f54782939d385",
#                     "6169704bc4133ddaa309dd07"
#                 ]
#             }]
#         }

#     Raises:
#         HTTPException [400]: No reactions exist for this message || No reaction with this emoji
#         HTTPException [401]: Invalid room member
#         HTTPException [404]: Message not found || Room not found
#         HTTPException [424]: Failed to remove reaction
#     """
#     DB = DataStorage(org_id)

#     message = await get_message(org_id, room_id, message_id)  # get message
#     if not message:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Message not found",
#         )
#     print ("message", message)
#     reactions = message.get("emojis")

#     room = await get_room(org_id, room_id)
#     if not room:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Room not found"
#         )
#     print ("room", room)
#     members = room.get("room_members", {})
#     print ("room members", members)
    
#     new_reaction = request.dict()
#     if new_reaction["reactedUsersId"][0] not in list(members):  # check if user is in list of room members
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid room member",
#         )  

#     print ("list of room members", list(members))
#     print ("new reaction user id", new_reaction["reactedUsersId"])
    

#     # if no reactions exist for the message
#     if not reactions:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="No reactions exist for this message",
#         )

#     # if reactions exist for the message
#     for emoji in reactions:
#         if emoji.get("name") == new_reaction.get("name"):
#             if new_reaction.get("reactedUsersId")[0] not in emoji.get("reactedUsersId"):
#                 raise HTTPException(
#                     status_code=status.HTTP_400_BAD_REQUEST,
#                     detail="No member reacted with this emoji",
#                 )

#             # if user has reacted with the emoji
#             emoji.get("reactedUsersId").remove(new_reaction.get("reactedUsersId")[0])
#             emoji["count"] -= 1

#             if emoji.get("count") != 0:
#                 updated = await DB.update(
#                     MESSAGE_COLLECTION,
#                     document_id=message_id,
#                     data={"emojis": reactions},
#                 )
#                 if updated and updated.get("status_code") is not None:
#                     raise HTTPException(
#                         status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                         detail="Failed to remove reaction",
#                     )
#                 # publish to centrifugo in the background
#                 background_tasks.add_task(
#                     centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, emoji
#                 )
#                 return JSONResponse(
#                     content=ResponseModel.success(
#                         data=emoji, message="Reaction removed successfully"
#                     ),
#                     status_code=status.HTTP_200_OK,
#                 )

#             reactions.remove(emoji)  # if emoji count is 0
#             removed = await DB.update(
#                 MESSAGE_COLLECTION, document_id=message_id, data={"emojis": reactions}
#             )
#             if removed and removed.get("status_code") is not None:
#                 raise HTTPException(
#                     status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                     detail="Failed to remove reaction",
#                 )
#             # publish to centrifugo in the background
#             background_tasks.add_task(
#                 centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, removed
#             )
#             return JSONResponse(
#                 content=ResponseModel.success(
#                     data=None, message="Reaction removed successfully"
#                 ),
#                 status_code=status.HTTP_200_OK,
#             )

#     # if emoji is not in reactions
#     raise HTTPException(
#         status_code=status.HTTP_400_BAD_REQUEST,
#         detail="No reaction with this emoji",
#     )



# 23rd jan


# @router.put(  # fully functional (merged) add and remove reactions
#     "/org/{org_id}/rooms/{room_id}/messages/{message_id}/reaction",
#     response_model=ResponseModel,
#     status_code=status.HTTP_200_OK,
#     responses={
#         401: {"description": "Invalid room member"},
#         404: {"description": "Message not found"},
#         424: {
#             "description": "Failed to retrieve room members || Failed to add reaction or remove reaction"
#         }
#         # 424: {
#         #     "description": "Failed to retrieve room members / Failed to add reaction or remove reaction"
#         # }
#     },
# )
# async def reactions(
#     request: Emoji,
#     org_id: str,
#     room_id: str,
#     message_id: str,
#     background_tasks: BackgroundTasks,
# ):
#     """
#     Checks if there are any reactions for the message.
#     Adds a reaction to a message.
#     Adds a user to list of reacted users if reaction already exists.
#     Removes the user from the list of reacted users if user already reacted to the message.
#     Removes a reaction from a message if reacted user count is 0.

#     Args:
#         request: Request object
#         org_id: A unique identifier of the organization.
#         room_id: A unique identifier of the room.
#         message_id: A unique identifier of the message that is being edited.
#         background_tasks: A daemon thread for publishing to centrifugo

#     Returns:
#         HTTP_200_OK {reaction added}:
#         A dict containing data about the reaction that was added or removed.

#         {
#             "room_id": "619e28c31a5f54782939d59a",
#             "message_id": "61cb65f378fb01b18fac147b",
#             "emojis": [{
#                 "name": "lol",
#                 "count": 2,
#                 "emoji": "lol",
#                 "reactedUsersId": [
#                     "619ba4671a5f54782939d385",
#                     "6169704bc4133ddaa309dd07"
#                 ]
#             }]
#         }

#     Raises:
#         HTTPException [401]: Invalid room member
#         HTTPException [404]: Message not found
#         HTTPException [424]: Failed to retrieve room members
#         HTTPException [424]: Failed to add reaction
#         HTTPException [424]: Failed to remove reaction
#     """
#     DB = DataStorage(org_id)

#     message = await get_message(org_id, room_id, message_id)  # get message
#     if not message:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Message not found",
#         )
#     reactions = message.get("emojis")  # original
#     # reactions = message["emojis"]  # functional

#     members = await get_room_members(org_id, room_id)  # retrieve room members
#     if not members:
#         raise HTTPException(
#             status_code=status.HTTP_424_FAILED_DEPENDENCY,
#             detail="Failed to retrieve room members",
#         )

#     new_reaction = request.dict()
#     if new_reaction.get("reactedUsersId")[0] not in list(members):
#         # if new_reaction.request.get("reactedUsersId") not in list(members):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid room member",
#         )
#     # if new_reaction["reactedUsersId"][0] not in list(
#     #     members
#     # ):  # check if user is in list of room members
#     # raise HTTPException(
#     #     status_code=status.HTTP_401_UNAUTHORIZED,
#     #     detail="Invalid room member",
#     # )

#     # if no reactions exist for the message
#     if not reactions:
#         reactions = [new_reaction]
#         updated_emoji = await DB.update(
#             MESSAGE_COLLECTION, document_id=message_id, data={"emojis": reactions}
#         )
#         if updated_emoji and updated_emoji.get("status_code") is not None:
#             raise HTTPException(
#                 status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                 detail="Failed to add reaction",
#             )
#         # publish to centrifugo in the background
#         background_tasks.add_task(
#             centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, new_reaction
#         )
#         return JSONResponse(
#             content=ResponseModel.success(data=new_reaction, message="New reaction added successfully"),
#             status_code=status.HTTP_200_OK,
#         )

#     # if reactions exist for the message
#     for emoji in reactions:
#         if emoji.get("name") == new_reaction.get("name"):
#             # if emoji["name"] == new_reaction["name"]:  # if emoji is already in reactions

#             # if user hasn't reacted with the emoji
#             # if new_reaction["reactedUsersId"][0] not in emoji["reactedUsersId"]:
#             #     emoji["reactedUsersId"].append(new_reaction["reactedUsersId"][0])
#             #     emoji["count"] += 1
#             if new_reaction.get("reactedUsersId")[0] not in emoji.get("reactedUsersId"):
                 
#                 # emoji.get("count") + 1
#                 emoji["count"] += 1

#                 added = await DB.update(
#                     MESSAGE_COLLECTION,
#                     document_id=message_id,
#                     data={"emojis": reactions},
#                 )
#                 if added and added.get("status_code") is not None:
#                     raise HTTPException(
#                         status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                         detail="Failed to add member's reaction",
#                     )
#                 # publish to centrifugo in the background
#                 background_tasks.add_task(
#                     centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, emoji
#                 )
#                 return JSONResponse(
#                     content=ResponseModel.success(data=emoji, message="new member reacted with the emoji"),
#                     status_code=status.HTTP_200_OK,
#                 )

#             # if user has reacted with the emoji
#             # emoji["reactedUsersId"].remove(new_reaction["reactedUsersId"][0])
#             # emoji["count"] -= 1
#             emoji.get("reactedUsersId").remove(new_reaction.get("reactedUsersId")[0])
#             emoji["count"] -= 1
#             # emoji["reactedUsersId"] = list(set(emoji.get("reactedUsersId")))

#             if emoji.get("count") != 0:
#                 # if emoji["count"] != 0:  # if emoji count is not 0
#                 updated = await DB.update(
#                     MESSAGE_COLLECTION,
#                     document_id=message_id,
#                     data={"emojis": reactions},
#                 )
#                 if updated and updated.get("status_code") is not None:
#                     raise HTTPException(
#                         status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                         detail="Failed to remove member's reaction",
#                     )
#                 # publish to centrifugo in the background
#                 background_tasks.add_task(
#                     centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, emoji
#                 )
#                 return JSONResponse(
#                     content=ResponseModel.success(
#                         data=emoji, message="member's reaction removed successfully"
#                     ),
#                     status_code=status.HTTP_200_OK,
#                 )

#             reactions.remove(emoji)  # if emoji count is 0
#             removed = await DB.update(
#                 MESSAGE_COLLECTION, document_id=message_id, data={"emojis": reactions}
#             )
#             if removed and removed.get("status_code") is not None:
#                 raise HTTPException(
#                     status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                     detail="Failed to remove reaction",
#                 )
#             # publish to centrifugo in the background
#             background_tasks.add_task(
#                 centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, removed
#             )
#             return JSONResponse(
#                 content=ResponseModel.success(data=None, message="reaction removed successfully"),
#                 status_code=status.HTTP_200_OK,
#             )

#     # if emoji is not in reactions
#     reactions.append(new_reaction)
#     new = await DB.update(
#         MESSAGE_COLLECTION, document_id=message_id, data={"emojis": reactions}
#     )
#     if new and new.get("status_code") is not None:
#         raise HTTPException(
#             status_code=status.HTTP_424_FAILED_DEPENDENCY,
#             detail="Failed to add new reaction",
#         )
#     # publish to centrifugo in the background
#     background_tasks.add_task(
#         centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, new_reaction
#     )
#     return JSONResponse(
#         content=ResponseModel.success(data=new_reaction, message="another  reaction added successfully"),
#         status_code=status.HTTP_200_OK,
#     )


# @router.put(
#     "/org/{org_id}/rooms/{room_id}/messages/{message_id}/reaction/add",
#     response_model=ResponseModel,
#     status_code=status.HTTP_200_OK,
#     responses={
#         401: {"description": "Invalid room member"},
#         404: {"description": "Message not found"},
#         409: {"description": "Member already reacted with this emoji"},
#         424: {
#             "description": "Failed to retrieve room members || Failed to add reaction"
#         },
#     },
# )
# async def reactions(
#     request: Emoji,
#     org_id: str,
#     room_id: str,
#     message_id: str,
#     background_tasks: BackgroundTasks,
# ):
#     """
#     Checks if there are any reactions for the message.
#     Adds a reaction to a message.
#     Adds a user to list of reacted users if reaction already exists.

#     Args:
#         request: Request object
#         org_id: A unique identifier of the organization.
#         room_id: A unique identifier of the room.
#         message_id: A unique identifier of the message that is being edited.
#         background_tasks: A daemon thread for publishing to centrifugo

#     Returns:
#         HTTP_200_OK {reaction added}:
#         A dict containing data about the reaction that was added or removed.

#         {
#             "room_id": "619e28c31a5f54782939d59a",
#             "message_id": "61cb65f378fb01b18fac147b",
#             "emojis": [{
#                 "name": "lol",
#                 "count": 2,
#                 "emoji": "lol",
#                 "reactedUsersId": [
#                     "619ba4671a5f54782939d385",
#                     "6169704bc4133ddaa309dd07"
#                 ]
#             }]
#         }

#     Raises:
#         HTTPException [401]: Invalid room member
#         HTTPException [404]: Message not found
#         HTTPException [409]: Member already reacted with this emoji
#         HTTPException [424]: Failed to retrieve room members
#         HTTPException [424]: Failed to add reaction
#     """
#     DB = DataStorage(org_id)

#     message = await get_message(org_id, room_id, message_id)  # get message
#     if not message:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Message not found",
#         )
#     reactions = message.get("emojis")

#     members = await get_room_members(org_id, room_id)  # retrieve room members
#     if not members:
#         raise HTTPException(
#             status_code=status.HTTP_424_FAILED_DEPENDENCY,
#             detail="Failed to retrieve room members",
#         )

#     new_reaction = request.dict()
#     if new_reaction["reactedUsersId"][0] not in list(
#         members
#     ):  # check if user is in list of room members
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid room member",
#         )

#     # if no reactions exist for the message
#     if not reactions:
#         reactions = [new_reaction]
#         updated_emoji = await DB.update(
#             MESSAGE_COLLECTION, document_id=message_id, data={"emojis": reactions}
#         )
#         if updated_emoji and updated_emoji.get("status_code") is not None:
#             raise HTTPException(
#                 status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                 detail="Failed to add reaction",
#             )
#         # publish to centrifugo in the background
#         background_tasks.add_task(
#             centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, new_reaction
#         )
#         return JSONResponse(
#             content=ResponseModel.success(data=new_reaction, message="reaction added"),
#             status_code=status.HTTP_200_OK,
#         )

#     # if reactions exist for the message
#     for emoji in reactions:
#         if emoji["name"] == new_reaction["name"]:  # if emoji is already in reactions

#             # if user hasn't reacted with the emoji
#             if new_reaction["reactedUsersId"][0] not in emoji["reactedUsersId"]:
#                 emoji["reactedUsersId"].append(new_reaction["reactedUsersId"][0])
#                 emoji["count"] += 1

#                 added = await DB.update(
#                     MESSAGE_COLLECTION,
#                     document_id=message_id,
#                     data={"emojis": reactions},
#                 )
#                 if added and added.get("status_code") is not None:
#                     raise HTTPException(
#                         status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                         detail="Failed to add reaction",
#                     )
#                 # publish to centrifugo in the background
#                 background_tasks.add_task(
#                     centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, emoji
#                 )
#                 return JSONResponse(
#                     content=ResponseModel.success(data=emoji, message="reaction added"),
#                     status_code=status.HTTP_200_OK,
#                 )
            # # if user has reacted with the emoji
            # raise HTTPException(
            #     status_code=status.HTTP_409_CONFLICT,
            #     detail="Member already reacted with this emoji",
            # )

#     # if emoji is not in reactions
#     reactions.append(new_reaction)
#     new = await DB.update(
#         MESSAGE_COLLECTION, document_id=message_id, data={"emojis": reactions}
#     )
#     if new and new.get("status_code") is not None:
#         raise HTTPException(
#             status_code=status.HTTP_424_FAILED_DEPENDENCY,
#             detail="Failed to add reaction",
#         )
#     # publish to centrifugo in the background
#     background_tasks.add_task(
#         centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, new_reaction
#     )
#     return JSONResponse(
#         content=ResponseModel.success(data=new_reaction, message="reaction added"),
#         status_code=status.HTTP_200_OK,
#     )


# @router.put(  # fully functional remove reactions
#     "/org/{org_id}/rooms/{room_id}/messages/{message_id}/reaction/remove",
#     response_model=ResponseModel,
#     status_code=status.HTTP_200_OK,
#     responses={
#         401: {"description": "Invalid room member"},
#         404: {"description": "Message not found"},
#         424: {
#             "description": "Failed to retrieve room members || Failed to remove reaction"
#         },
#     },
# )
# async def reactions(
#     request: Emoji,
#     org_id: str,
#     room_id: str,
#     message_id: str,
#     background_tasks: BackgroundTasks,
# ):
#     """
#     Checks if there are any reactions for the message.
#     Removes the user from the list of reacted users if user already reacted to the message.
#     Removes a reaction from a message if reacted user count is 0.

#     Args:
#         request: Request object
#         org_id: A unique identifier of the organization.
#         room_id: A unique identifier of the room.
#         message_id: A unique identifier of the message that is being edited.
#         background_tasks: A daemon thread for publishing to centrifugo

#     Returns:
#         HTTP_200_OK {reaction added}:
#         A dict containing data about the reaction that was added or removed.

#         {
#             "room_id": "619e28c31a5f54782939d59a",
#             "message_id": "61cb65f378fb01b18fac147b",
#             "emojis": [{
#                 "name": "lol",
#                 "count": 2,
#                 "emoji": "lol",
#                 "reactedUsersId": [
#                     "619ba4671a5f54782939d385",
#                     "6169704bc4133ddaa309dd07"
#                 ]
#             }]
#         }

#     Raises:
#         HTTPException [401]: Invalid room member
#         HTTPException [404]: Message not found
#         HTTPException [424]: Failed to retrieve room members
#         HTTPException [424]: Failed to add reaction
#         HTTPException [424]: Failed to remove reaction
#     """
#     DB = DataStorage(org_id)

#     message = await get_message(org_id, room_id, message_id)  # get message
#     if not message:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Message not found",
#         )
#     reactions = message.get("emojis")  # original

#     members = await get_room_members(org_id, room_id)  # retrieve room members
#     if not members:
#         raise HTTPException(
#             status_code=status.HTTP_424_FAILED_DEPENDENCY,
#             detail="Failed to retrieve room members",
#         )

#     new_reaction = request.dict()
#     if new_reaction["reactedUsersId"][0] not in list(
#         members
#     ):  # check if user is in list of room members
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid room member",
#         )

#     # if no reactions exist for the message
    # if not reactions:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="No reactions found",
    #     )

#     # if reactions exist for the message
#     for emoji in reactions:
#         if emoji["name"] == new_reaction["name"]:  # if emoji is already in reactions

#             # if user hasn't reacted with the emoji
#             if new_reaction["reactedUsersId"][0] not in emoji["reactedUsersId"]:
                # raise HTTPException(
                #     status_code=status.HTTP_400_BAD_REQUEST,
                #     detail="Member hasn't reacted with this emoji",
                # )
#             # if user has reacted with the emoji
#             emoji["reactedUsersId"].remove(new_reaction["reactedUsersId"][0])
#             emoji["count"] -= 1

#             if emoji["count"] != 0:  # if emoji count is not 0
#                 updated = await DB.update(
#                     MESSAGE_COLLECTION,
#                     document_id=message_id,
#                     data={"emojis": reactions},
#                 )
#                 if updated and updated.get("status_code") is not None:
#                     raise HTTPException(
#                         status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                         detail="Failed to remove user's reaction",
#                     )
#                 # publish to centrifugo in the background
#                 background_tasks.add_task(
#                     centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, emoji
#                 )
#                 return JSONResponse(
#                     content=ResponseModel.success(
#                         data=emoji, message="user's reaction removed"
#                     ),
#                     status_code=status.HTTP_200_OK,
#                 )

#             reactions.remove(emoji)  # if emoji count is 0
#             removed = await DB.update(
#                 MESSAGE_COLLECTION, document_id=message_id, data={"emojis": reactions}
#             )
#             if removed and removed.get("status_code") is not None:
#                 raise HTTPException(
#                     status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                     detail="Failed to remove reaction",
#                 )
#             # publish to centrifugo in the background
#             background_tasks.add_task(
#                 centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, removed
#             )
#             return JSONResponse(
#                 content=ResponseModel.success(data=emoji, message="reaction removed"),
#                 status_code=status.HTTP_200_OK,
#             )

    # # if emoji is not in reactions
    # raise HTTPException(
    #     status_code=status.HTTP_404_NOT_FOUND,
    #     detail="Emoji not found",
    # )
 



# 20th jan 2022

# @router.put(  # fully functional (merged) add and remove reactions
#     "/org/{org_id}/rooms/{room_id}/messages/{message_id}/reaction",
#     response_model=ResponseModel,
#     status_code=status.HTTP_200_OK,
#     responses={
#         401: {"description": "Invalid room member"},
#         404: {"description": "Message not found"},
#         424: {
#             "description": "Failed to retrieve room members || Failed to add reaction or remove reaction"
#         }
#         # 424: {
#         #     "description": "Failed to retrieve room members / Failed to add reaction or remove reaction"
#         # }
#     },
# )
# async def reactions(
#     request: Emoji,
#     org_id: str,
#     room_id: str,
#     message_id: str,
#     background_tasks: BackgroundTasks,
# ):
#     """
#     Checks if there are any reactions for the message.
#     Adds a reaction to a message.
#     Adds a user to list of reacted users if reaction already exists.
#     Removes the user from the list of reacted users if user already reacted to the message.
#     Removes a reaction from a message if reacted user count is 0.

#     Args:
#         request: Request object
#         org_id: A unique identifier of the organization.
#         room_id: A unique identifier of the room.
#         message_id: A unique identifier of the message that is being edited.
#         background_tasks: A daemon thread for publishing to centrifugo

#     Returns:
#         HTTP_200_OK {reaction added}:
#         A dict containing data about the reaction that was added or removed.

#         {
#             "room_id": "619e28c31a5f54782939d59a",
#             "message_id": "61cb65f378fb01b18fac147b",
#             "emojis": [{
#                 "name": "lol",
#                 "count": 2,
#                 "emoji": "lol",
#                 "reactedUsersId": [
#                     "619ba4671a5f54782939d385",
#                     "6169704bc4133ddaa309dd07"
#                 ]
#             }]
#         }

#     Raises:
#         HTTPException [401]: Invalid room member
#         HTTPException [404]: Message not found
#         HTTPException [424]: Failed to retrieve room members
#         HTTPException [424]: Failed to add reaction
#         HTTPException [424]: Failed to remove reaction
#     """
#     DB = DataStorage(org_id)

#     message = await get_message(org_id, room_id, message_id)  # get message
#     if not message:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Message not found",
#         )
#     reactions = message.get("emojis")  # original
#     # reactions = message["emojis"]  # functional

#     members = await get_room_members(org_id, room_id)  # retrieve room members
#     if not members:
#         raise HTTPException(
#             status_code=status.HTTP_424_FAILED_DEPENDENCY,
#             detail="Failed to retrieve room members",
#         )
#     # memberIds = list(members) # convert romm members to list

#     new_reaction = request.dict()
#     if new_reaction["reactedUsersId"][0] not in list(
#         members
#     ):  # check if user is in list of room members
#         # if new_reaction["reactedUsersId"][0] not in memberIds: # check if user is a room member
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid room member",
#         )

#     # if no reactions exist for the message
#     if not reactions:
#         reactions = [new_reaction]
#         updated_emoji = await DB.update(
#             MESSAGE_COLLECTION, document_id=message_id, data={"emojis": reactions}
#         )
#         if updated_emoji and updated_emoji.get("status_code") is not None:
#             raise HTTPException(
#                 status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                 detail="Failed to add reaction",
#             )
#         # publish to centrifugo in the background
#         background_tasks.add_task(
#             centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, new_reaction
#         )
#         return JSONResponse(
#             content=ResponseModel.success(data=new_reaction, message="reaction added"),
#             status_code=status.HTTP_200_OK,
#         )

#     # if reactions exist for the message
#     for emoji in reactions:
#         if emoji["name"] == new_reaction["name"]:  # if emoji is already in reactions

#             # if user hasn't reacted with the emoji
#             if new_reaction["reactedUsersId"][0] not in emoji["reactedUsersId"]:
#                 emoji["reactedUsersId"].append(new_reaction["reactedUsersId"][0])
#                 emoji["count"] += 1

#                 added = await DB.update(
#                     MESSAGE_COLLECTION,
#                     document_id=message_id,
#                     data={"emojis": reactions},
#                 )
#                 if added and added.get("status_code") is not None:
#                     raise HTTPException(
#                         status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                         detail="Failed to add reaction",
#                     )
#                 # publish to centrifugo in the background
#                 background_tasks.add_task(
#                     centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, emoji
#                 )
#                 return JSONResponse(
#                     content=ResponseModel.success(data=emoji, message="reaction added"),
#                     status_code=status.HTTP_200_OK,
#                 )

#             # if user has reacted with the emoji
#             emoji["reactedUsersId"].remove(new_reaction["reactedUsersId"][0])
#             emoji["count"] -= 1

#             if emoji["count"] != 0:  # if emoji count is not 0
#                 updated = await DB.update(
#                     MESSAGE_COLLECTION,
#                     document_id=message_id,
#                     data={"emojis": reactions},
#                 )
#                 if updated and updated.get("status_code") is not None:
#                     raise HTTPException(
#                         status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                         detail="Failed to remove user's reaction",
#                     )
#                 # publish to centrifugo in the background
#                 background_tasks.add_task(
#                     centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, emoji
#                 )
#                 return JSONResponse(
#                     content=ResponseModel.success(
#                         data=emoji, message="user's reaction removed"
#                     ),
#                     status_code=status.HTTP_200_OK,
#                 )

#             reactions.remove(emoji)  # if emoji count is 0
#             removed = await DB.update(
#                 MESSAGE_COLLECTION, document_id=message_id, data={"emojis": reactions}
#             )
#             if removed and removed.get("status_code") is not None:
#                 raise HTTPException(
#                     status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                     detail="Failed to remove reaction",
#                 )
#             # publish to centrifugo in the background
#             background_tasks.add_task(
#                 centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, removed
#             )
#             return JSONResponse(
#                 content=ResponseModel.success(data=emoji, message="reaction removed"),
#                 status_code=status.HTTP_200_OK,
#             )

#     # if emoji is not in reactions
#     reactions.append(new_reaction)
#     new = await DB.update(
#         MESSAGE_COLLECTION, document_id=message_id, data={"emojis": reactions}
#     )
#     if new and new.get("status_code") is not None:
#         raise HTTPException(
#             status_code=status.HTTP_424_FAILED_DEPENDENCY,
#             detail="Failed to add reaction",
#         )
#     # publish to centrifugo in the background
#     background_tasks.add_task(
#         centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, new_reaction
#     )
#     return JSONResponse(
#         content=ResponseModel.success(data=new_reaction, message="reaction added"),
#         status_code=status.HTTP_200_OK,
#     )


# @router.put(
#     "/org/{org_id}/rooms/{room_id}/messages/{message_id}/reaction/add",
#     response_model=ResponseModel,
#     status_code=status.HTTP_200_OK,
#     responses={
#         401: {"description": "Invalid room member"},
#         404: {"description": "Message not found"},
#         409: {"description": "Member already reacted with this emoji"},
#         424: {
#             "description": "Failed to retrieve room members || Failed to add reaction"
#         },
#     },
# )
# async def reactions(
#     request: Emoji,
#     org_id: str,
#     room_id: str,
#     message_id: str,
#     background_tasks: BackgroundTasks,
# ):
#     """
#     Checks if there are any reactions for the message.
#     Adds a reaction to a message.
#     Adds a user to list of reacted users if reaction already exists.

#     Args:
#         request: Request object
#         org_id: A unique identifier of the organization.
#         room_id: A unique identifier of the room.
#         message_id: A unique identifier of the message that is being edited.
#         background_tasks: A daemon thread for publishing to centrifugo

#     Returns:
#         HTTP_200_OK {reaction added}:
#         A dict containing data about the reaction that was added or removed.

#         {
#             "room_id": "619e28c31a5f54782939d59a",
#             "message_id": "61cb65f378fb01b18fac147b",
#             "emojis": [{
#                 "name": "lol",
#                 "count": 2,
#                 "emoji": "lol",
#                 "reactedUsersId": [
#                     "619ba4671a5f54782939d385",
#                     "6169704bc4133ddaa309dd07"
#                 ]
#             }]
#         }

#     Raises:
#         HTTPException [401]: Invalid room member
#         HTTPException [404]: Message not found
#         HTTPException [409]: Member already reacted with this emoji
#         HTTPException [424]: Failed to retrieve room members
#         HTTPException [424]: Failed to add reaction
#     """
#     DB = DataStorage(org_id)

#     message = await get_message(org_id, room_id, message_id)  # get message
#     if not message:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Message not found",
#         )
#     reactions = message.get("emojis")

#     members = await get_room_members(org_id, room_id)  # retrieve room members
#     if not members:
#         raise HTTPException(
#             status_code=status.HTTP_424_FAILED_DEPENDENCY,
#             detail="Failed to retrieve room members",
#         )

#     new_reaction = request.dict()
#     if new_reaction["reactedUsersId"][0] not in list(
#         members
#     ):  # check if user is in list of room members
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid room member",
#         )

#     # if no reactions exist for the message
#     if not reactions:
#         reactions = [new_reaction]
#         updated_emoji = await DB.update(
#             MESSAGE_COLLECTION, document_id=message_id, data={"emojis": reactions}
#         )
#         if updated_emoji and updated_emoji.get("status_code") is not None:
#             raise HTTPException(
#                 status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                 detail="Failed to add reaction",
#             )
#         # publish to centrifugo in the background
#         background_tasks.add_task(
#             centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, new_reaction
#         )
#         return JSONResponse(
#             content=ResponseModel.success(data=new_reaction, message="reaction added"),
#             status_code=status.HTTP_200_OK,
#         )

#     # if reactions exist for the message
#     for emoji in reactions:
#         if emoji["name"] == new_reaction["name"]:  # if emoji is already in reactions

#             # if user hasn't reacted with the emoji
#             if new_reaction["reactedUsersId"][0] not in emoji["reactedUsersId"]:
#                 emoji["reactedUsersId"].append(new_reaction["reactedUsersId"][0])
#                 emoji["count"] += 1

#                 added = await DB.update(
#                     MESSAGE_COLLECTION,
#                     document_id=message_id,
#                     data={"emojis": reactions},
#                 )
#                 if added and added.get("status_code") is not None:
#                     raise HTTPException(
#                         status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                         detail="Failed to add reaction",
#                     )
#                 # publish to centrifugo in the background
#                 background_tasks.add_task(
#                     centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, emoji
#                 )
#                 return JSONResponse(
#                     content=ResponseModel.success(data=emoji, message="reaction added"),
#                     status_code=status.HTTP_200_OK,
#                 )
#             # if user has reacted with the emoji
#             raise HTTPException(
#                 status_code=status.HTTP_409_CONFLICT,
#                 detail="Member already reacted with this emoji",
#             )

#     # if emoji is not in reactions
#     reactions.append(new_reaction)
#     new = await DB.update(
#         MESSAGE_COLLECTION, document_id=message_id, data={"emojis": reactions}
#     )
#     if new and new.get("status_code") is not None:
#         raise HTTPException(
#             status_code=status.HTTP_424_FAILED_DEPENDENCY,
#             detail="Failed to add reaction",
#         )
#     # publish to centrifugo in the background
#     background_tasks.add_task(
#         centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, new_reaction
#     )
#     return JSONResponse(
#         content=ResponseModel.success(data=new_reaction, message="reaction added"),
#         status_code=status.HTTP_200_OK,
#     )


# @router.put(  # fully functional remove reactions
#     "/org/{org_id}/rooms/{room_id}/messages/{message_id}/reaction/remove",
#     response_model=ResponseModel,
#     status_code=status.HTTP_200_OK,
#     responses={
#         401: {"description": "Invalid room member"},
#         404: {"description": "Message not found"},
#         424: {
#             "description": "Failed to retrieve room members || Failed to remove reaction"
#         },
#     },
# )
# async def reactions(
#     request: Emoji,
#     org_id: str,
#     room_id: str,
#     message_id: str,
#     background_tasks: BackgroundTasks,
# ):
#     """
#     Checks if there are any reactions for the message.
#     Removes the user from the list of reacted users if user already reacted to the message.
#     Removes a reaction from a message if reacted user count is 0.

#     Args:
#         request: Request object
#         org_id: A unique identifier of the organization.
#         room_id: A unique identifier of the room.
#         message_id: A unique identifier of the message that is being edited.
#         background_tasks: A daemon thread for publishing to centrifugo

#     Returns:
#         HTTP_200_OK {reaction added}:
#         A dict containing data about the reaction that was added or removed.

#         {
#             "room_id": "619e28c31a5f54782939d59a",
#             "message_id": "61cb65f378fb01b18fac147b",
#             "emojis": [{
#                 "name": "lol",
#                 "count": 2,
#                 "emoji": "lol",
#                 "reactedUsersId": [
#                     "619ba4671a5f54782939d385",
#                     "6169704bc4133ddaa309dd07"
#                 ]
#             }]
#         }

#     Raises:
#         HTTPException [401]: Invalid room member
#         HTTPException [404]: Message not found
#         HTTPException [424]: Failed to retrieve room members
#         HTTPException [424]: Failed to add reaction
#         HTTPException [424]: Failed to remove reaction
#     """
#     DB = DataStorage(org_id)

#     message = await get_message(org_id, room_id, message_id)  # get message
#     if not message:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Message not found",
#         )
#     reactions = message.get("emojis")  # original

#     members = await get_room_members(org_id, room_id)  # retrieve room members
#     if not members:
#         raise HTTPException(
#             status_code=status.HTTP_424_FAILED_DEPENDENCY,
#             detail="Failed to retrieve room members",
#         )

#     new_reaction = request.dict()
#     if new_reaction["reactedUsersId"][0] not in list(
#         members
#     ):  # check if user is in list of room members
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid room member",
#         )

#     # if no reactions exist for the message
#     if not reactions:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="No reactions found",
#         )

#     # if reactions exist for the message
#     for emoji in reactions:
#         if emoji["name"] == new_reaction["name"]:  # if emoji is already in reactions

#             # if user hasn't reacted with the emoji
#             if new_reaction["reactedUsersId"][0] not in emoji["reactedUsersId"]:
#                 raise HTTPException(
#                     status_code=status.HTTP_400_BAD_REQUEST,
#                     detail="Member hasn't reacted with this emoji",
#                 )
#             # if user has reacted with the emoji
#             emoji["reactedUsersId"].remove(new_reaction["reactedUsersId"][0])
#             emoji["count"] -= 1

#             if emoji["count"] != 0:  # if emoji count is not 0
#                 updated = await DB.update(
#                     MESSAGE_COLLECTION,
#                     document_id=message_id,
#                     data={"emojis": reactions},
#                 )
#                 if updated and updated.get("status_code") is not None:
#                     raise HTTPException(
#                         status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                         detail="Failed to remove user's reaction",
#                     )
#                 # publish to centrifugo in the background
#                 background_tasks.add_task(
#                     centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, emoji
#                 )
#                 return JSONResponse(
#                     content=ResponseModel.success(
#                         data=emoji, message="user's reaction removed"
#                     ),
#                     status_code=status.HTTP_200_OK,
#                 )

#             reactions.remove(emoji)  # if emoji count is 0
#             removed = await DB.update(
#                 MESSAGE_COLLECTION, document_id=message_id, data={"emojis": reactions}
#             )
#             if removed and removed.get("status_code") is not None:
#                 raise HTTPException(
#                     status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                     detail="Failed to remove reaction",
#                 )
#             # publish to centrifugo in the background
#             background_tasks.add_task(
#                 centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, removed
#             )
#             return JSONResponse(
#                 content=ResponseModel.success(data=emoji, message="reaction removed"),
#                 status_code=status.HTTP_200_OK,
#             )

#     # if emoji is not in reactions
#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail="Emoji not found",
#     )


# older ones

# # from typing import Dict, List

# # from fastapi import (APIRouter, BackgroundTasks, HTTPException,  # , Body,
# #                      status)
# from fastapi import APIRouter, BackgroundTasks, HTTPException, status
# # from fastapi_pagination import Page, add_pagination, paginate
# # from schema.message import Emoji, Message, MessageRequest  # , Thread
# from schema.message import Emoji, Message, MessageRequest
# from schema.response import ResponseModel
# from starlette.responses import JSONResponse
# from utils.centrifugo import Events, centrifugo_client
# from utils.db import DataStorage
# from utils.message_utils import (MESSAGE_COLLECTION, get_message,
#                                  get_room_messages)
# # from utils.room_utils import get_room_members  # ,get_room,
# from utils.room_utils import get_room_members

# router = APIRouter()


# @router.put( # fully functional (merged) add and remove reactions
#     "/org/{org_id}/rooms/{room_id}/messages/{message_id}/reaction",
#     response_model=ResponseModel,
#     status_code=status.HTTP_200_OK,
#     responses={
#         401: {"description": "Invalid room member"},
#         404: {"description": "Message not found"},
#         424: {
#             "description": "Failed to retrieve room members || Failed to add reaction or remove reaction"
#         }
#         # 424: {
#         #     "description": "Failed to retrieve room members / Failed to add reaction or remove reaction"
#         # }
#     },
# )
# async def reactions(
#     request: Emoji,
#     org_id: str,
#     room_id: str,
#     message_id: str,
#     background_tasks: BackgroundTasks,
# ):
#     """
#     Checks if there are any reactions for the message.
#     Adds a reaction to a message.
#     Adds a user to list of reacted users if reaction already exists.
#     Removes the user from the list of reacted users if user already reacted to the message.
#     Removes a reaction from a message if reacted user count is 0.

#     Args:
#         request: Request object
#         org_id: A unique identifier of the organization.
#         room_id: A unique identifier of the room.
#         message_id: A unique identifier of the message that is being edited.
#         background_tasks: A daemon thread for publishing to centrifugo

#     Returns:
#         HTTP_200_OK {reaction added}:
#         A dict containing data about the reaction that was added or removed.

#         {
#             "room_id": "619e28c31a5f54782939d59a",
#             "message_id": "61cb65f378fb01b18fac147b",
#             "emojis": [{
#                 "name": "lol",
#                 "count": 2,
#                 "emoji": "lol",
#                 "reactedUsersId": [
#                     "619ba4671a5f54782939d385",
#                     "6169704bc4133ddaa309dd07"
#                 ]
#             }]
#         }

#     Raises:
#         HTTPException [401]: Invalid room member
#         HTTPException [404]: Message not found
#         HTTPException [424]: Failed to retrieve room members
#         HTTPException [424]: Failed to add reaction
#         HTTPException [424]: Failed to remove reaction
#     """
#     DB = DataStorage(org_id)

#     message = await get_message(org_id, room_id, message_id)  # get message
#     if not message:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Message not found",
#         )
#     reactions = message.get("emojis") #original
#     # reactions = message["emojis"]  # functional

#     members = await get_room_members(org_id, room_id)  # retrieve room members
#     if not members:
#         raise HTTPException(
#             status_code=status.HTTP_424_FAILED_DEPENDENCY,
#             detail="Failed to retrieve room members",
#         )
#     # memberIds = list(members) # convert romm members to list

#     new_reaction = request.dict()
#     if new_reaction["reactedUsersId"][0] not in list(
#         members
#     ):  # check if user is in list of room members
#         # if new_reaction["reactedUsersId"][0] not in memberIds: # check if user is a room member
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid room member",
#         )

#     # if no reactions exist for the message
#     if not reactions:
#         reactions = [new_reaction]
#         updated_emoji = await DB.update(
#             MESSAGE_COLLECTION, document_id=message_id, data={"emojis": reactions}
#         )
#         if updated_emoji and updated_emoji.get("status_code") is not None:
#             raise HTTPException(
#                 status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                 detail="Failed to add reaction",
#             )
#         # publish to centrifugo in the background
#         background_tasks.add_task(
#             centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, new_reaction
#         )
#         return JSONResponse(
#             content=ResponseModel.success(data=new_reaction, message="reaction added"),
#             status_code=status.HTTP_200_OK,
#         )

#     # if reactions exist for the message
#     for emoji in reactions:
#         if emoji["name"] == new_reaction["name"]:  # if emoji is already in reactions

#             # if user hasn't reacted with the emoji
#             if new_reaction["reactedUsersId"][0] not in emoji["reactedUsersId"]:
#                 emoji["reactedUsersId"].append(new_reaction["reactedUsersId"][0])
#                 emoji["count"] += 1

#                 added = await DB.update(
#                     MESSAGE_COLLECTION,
#                     document_id=message_id,
#                     data={"emojis": reactions},
#                 )
#                 if added and added.get("status_code") is not None:
#                     raise HTTPException(
#                         status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                         detail="Failed to add reaction",
#                     )
#                 # publish to centrifugo in the background
#                 background_tasks.add_task(
#                     centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, emoji
#                 )
#                 return JSONResponse(
#                     content=ResponseModel.success(data=emoji, message="reaction added"),
#                     status_code=status.HTTP_200_OK,
#                 )

#             # if user has reacted with the emoji
#             emoji["reactedUsersId"].remove(new_reaction["reactedUsersId"][0])
#             emoji["count"] -= 1

#             if emoji["count"] != 0:  # if emoji count is not 0
#                 updated = await DB.update(
#                     MESSAGE_COLLECTION,
#                     document_id=message_id,
#                     data={"emojis": reactions},
#                 )
#                 if updated and updated.get("status_code") is not None:
#                     raise HTTPException(
#                         status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                         detail="Failed to remove user's reaction",
#                     )
#                 # publish to centrifugo in the background
#                 background_tasks.add_task(
#                     centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, emoji
#                 )
#                 return JSONResponse(
#                     content=ResponseModel.success(
#                         data=emoji, message="user's reaction removed"
#                     ),
#                     status_code=status.HTTP_200_OK,
#                 )

#             reactions.remove(emoji)  # if emoji count is 0
#             removed = await DB.update(
#                 MESSAGE_COLLECTION, document_id=message_id, data={"emojis": reactions}
#             )
#             if removed and removed.get("status_code") is not None:
#                 raise HTTPException(
#                     status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                     detail="Failed to remove reaction",
#                 )
#             # publish to centrifugo in the background
#             background_tasks.add_task(
#                 centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, removed
#             )
#             return JSONResponse(
#                 content=ResponseModel.success(data=emoji, message="reaction removed"),
#                 status_code=status.HTTP_200_OK,
#             )

#     # if emoji is not in reactions
#     reactions.append(new_reaction)
#     new = await DB.update(
#         MESSAGE_COLLECTION, document_id=message_id, data={"emojis": reactions}
#     )
#     if new and new.get("status_code") is not None:
#         raise HTTPException(
#             status_code=status.HTTP_424_FAILED_DEPENDENCY,
#             detail="Failed to add reaction",
#         )
#     # publish to centrifugo in the background
#     background_tasks.add_task(
#         centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, new_reaction
#     )
#     return JSONResponse(
#         content=ResponseModel.success(data=new_reaction, message="reaction added"),
#         status_code=status.HTTP_200_OK,
#     )


# @router.put(
#     "/org/{org_id}/rooms/{room_id}/messages/{message_id}/reaction/add",
#     response_model=ResponseModel,
#     status_code=status.HTTP_200_OK,
#     responses={
#         401: {"description": "Invalid room member"},
#         404: {"description": "Message not found"},
#         409: {"description": "Member already reacted with this emoji"},
#         424: {
#             "description": "Failed to retrieve room members || Failed to add reaction"
#         }
#     },
# )
# async def reactions(
#     request: Emoji,
#     org_id: str,
#     room_id: str,
#     message_id: str,
#     background_tasks: BackgroundTasks,
# ):
#     """
#     Checks if there are any reactions for the message.
#     Adds a reaction to a message.
#     Adds a user to list of reacted users if reaction already exists.

#     Args:
#         request: Request object
#         org_id: A unique identifier of the organization.
#         room_id: A unique identifier of the room.
#         message_id: A unique identifier of the message that is being edited.
#         background_tasks: A daemon thread for publishing to centrifugo

#     Returns:
#         HTTP_200_OK {reaction added}:
#         A dict containing data about the reaction that was added or removed.

#         {
#             "room_id": "619e28c31a5f54782939d59a",
#             "message_id": "61cb65f378fb01b18fac147b",
#             "emojis": [{
#                 "name": "lol",
#                 "count": 2,
#                 "emoji": "lol",
#                 "reactedUsersId": [
#                     "619ba4671a5f54782939d385",
#                     "6169704bc4133ddaa309dd07"
#                 ]
#             }]
#         }

#     Raises:
#         HTTPException [401]: Invalid room member
#         HTTPException [404]: Message not found
#         HTTPException [409]: Member already reacted with this emoji
#         HTTPException [424]: Failed to retrieve room members
#         HTTPException [424]: Failed to add reaction
#     """
#     DB = DataStorage(org_id)

#     message = await get_message(org_id, room_id, message_id)  # get message
#     if not message:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Message not found",
#         )
#     reactions = message.get("emojis")

#     members = await get_room_members(org_id, room_id)  # retrieve room members
#     if not members:
#         raise HTTPException(
#             status_code=status.HTTP_424_FAILED_DEPENDENCY,
#             detail="Failed to retrieve room members",
#         )

#     new_reaction = request.dict()
#     if new_reaction["reactedUsersId"][0] not in list(
#         members
#     ):  # check if user is in list of room members
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid room member",
#         )

#     # if no reactions exist for the message
#     if not reactions:
#         reactions = [new_reaction]
#         updated_emoji = await DB.update(
#             MESSAGE_COLLECTION, document_id=message_id, data={"emojis": reactions}
#         )
#         if updated_emoji and updated_emoji.get("status_code") is not None:
#             raise HTTPException(
#                 status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                 detail="Failed to add reaction",
#             )
#         # publish to centrifugo in the background
#         background_tasks.add_task(
#             centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, new_reaction
#         )
#         return JSONResponse(
#             content=ResponseModel.success(data=new_reaction, message="reaction added"),
#             status_code=status.HTTP_200_OK,
#         )

#     # if reactions exist for the message
#     for emoji in reactions:
#         if emoji["name"] == new_reaction["name"]:  # if emoji is already in reactions

#             # if user hasn't reacted with the emoji
#             if new_reaction["reactedUsersId"][0] not in emoji["reactedUsersId"]:
#                 emoji["reactedUsersId"].append(new_reaction["reactedUsersId"][0])
#                 emoji["count"] += 1

#                 added = await DB.update(
#                     MESSAGE_COLLECTION,
#                     document_id=message_id,
#                     data={"emojis": reactions},
#                 )
#                 if added and added.get("status_code") is not None:
#                     raise HTTPException(
#                         status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                         detail="Failed to add reaction",
#                     )
#                 # publish to centrifugo in the background
#                 background_tasks.add_task(
#                     centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, emoji
#                 )
#                 return JSONResponse(
#                     content=ResponseModel.success(data=emoji, message="reaction added"),
#                     status_code=status.HTTP_200_OK,
#                 )
#             # if user has reacted with the emoji
#             raise HTTPException(
#                 status_code=status.HTTP_409_CONFLICT,
#                 detail="Member already reacted with this emoji",
#             )

#     # if emoji is not in reactions
#     reactions.append(new_reaction)
#     new = await DB.update(
#         MESSAGE_COLLECTION, document_id=message_id, data={"emojis": reactions}
#     )
#     if new and new.get("status_code") is not None:
#         raise HTTPException(
#             status_code=status.HTTP_424_FAILED_DEPENDENCY,
#             detail="Failed to add reaction",
#         )
#     # publish to centrifugo in the background
#     background_tasks.add_task(
#         centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, new_reaction
#     )
#     return JSONResponse(
#         content=ResponseModel.success(data=new_reaction, message="reaction added"),
#         status_code=status.HTTP_200_OK,
#     )


# @router.put( # fully functional (merged) add and remove reactions
#     "/org/{org_id}/rooms/{room_id}/messages/{message_id}/reaction/remove",
#     response_model=ResponseModel,
#     status_code=status.HTTP_200_OK,
#     responses={
#         401: {"description": "Invalid room member"},
#         404: {"description": "Message not found"},
#         424: {
#             "description": "Failed to retrieve room members || Failed to remove reaction"
#         }
#     },
# )
# async def reactions(
#     request: Emoji,
#     org_id: str,
#     room_id: str,
#     message_id: str,
#     background_tasks: BackgroundTasks,
# ):
#     """
#     Checks if there are any reactions for the message.
#     Removes the user from the list of reacted users if user already reacted to the message.
#     Removes a reaction from a message if reacted user count is 0.

#     Args:
#         request: Request object
#         org_id: A unique identifier of the organization.
#         room_id: A unique identifier of the room.
#         message_id: A unique identifier of the message that is being edited.
#         background_tasks: A daemon thread for publishing to centrifugo

#     Returns:
#         HTTP_200_OK {reaction added}:
#         A dict containing data about the reaction that was added or removed.

#         {
#             "room_id": "619e28c31a5f54782939d59a",
#             "message_id": "61cb65f378fb01b18fac147b",
#             "emojis": [{
#                 "name": "lol",
#                 "count": 2,
#                 "emoji": "lol",
#                 "reactedUsersId": [
#                     "619ba4671a5f54782939d385",
#                     "6169704bc4133ddaa309dd07"
#                 ]
#             }]
#         }

#     Raises:
#         HTTPException [401]: Invalid room member
#         HTTPException [404]: Message not found
#         HTTPException [424]: Failed to retrieve room members
#         HTTPException [424]: Failed to add reaction
#         HTTPException [424]: Failed to remove reaction
#     """
#     DB = DataStorage(org_id)

#     message = await get_message(org_id, room_id, message_id)  # get message
#     if not message:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Message not found",
#         )
#     reactions = message.get("emojis") #original

#     members = await get_room_members(org_id, room_id)  # retrieve room members
#     if not members:
#         raise HTTPException(
#             status_code=status.HTTP_424_FAILED_DEPENDENCY,
#             detail="Failed to retrieve room members",
#         )

#     new_reaction = request.dict()
#     if new_reaction["reactedUsersId"][0] not in list(
#         members
#     ):  # check if user is in list of room members
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid room member",
#         )

#     # if no reactions exist for the message
#     if not reactions:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="No reactions found",
#         )

#     # if reactions exist for the message
#     for emoji in reactions:
#         if emoji["name"] == new_reaction["name"]:  # if emoji is already in reactions

#             # if user hasn't reacted with the emoji
#             if new_reaction["reactedUsersId"][0] not in emoji["reactedUsersId"]:
#                 raise HTTPException(
#                     status_code=status.HTTP_400_BAD_REQUEST,
#                     detail="Member hasn't reacted with this emoji",
#                 )
#             # if user has reacted with the emoji
#             emoji["reactedUsersId"].remove(new_reaction["reactedUsersId"][0])
#             emoji["count"] -= 1

#             if emoji["count"] != 0:  # if emoji count is not 0
#                 updated = await DB.update(
#                     MESSAGE_COLLECTION,
#                     document_id=message_id,
#                     data={"emojis": reactions},
#                 )
#                 if updated and updated.get("status_code") is not None:
#                     raise HTTPException(
#                         status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                         detail="Failed to remove user's reaction",
#                     )
#                 # publish to centrifugo in the background
#                 background_tasks.add_task(
#                     centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, emoji
#                 )
#                 return JSONResponse(
#                     content=ResponseModel.success(
#                         data=emoji, message="user's reaction removed"
#                     ),
#                     status_code=status.HTTP_200_OK,
#                 )

#             reactions.remove(emoji)  # if emoji count is 0
#             removed = await DB.update(
#                 MESSAGE_COLLECTION, document_id=message_id, data={"emojis": reactions}
#             )
#             if removed and removed.get("status_code") is not None:
#                 raise HTTPException(
#                     status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                     detail="Failed to remove reaction",
#                 )
#             # publish to centrifugo in the background
#             background_tasks.add_task(
#                 centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, removed
#             )
#             return JSONResponse(
#                 content=ResponseModel.success(data=emoji, message="reaction removed"),
#                 status_code=status.HTTP_200_OK,
#             )

#     # if emoji is not in reactions
#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail="Emoji not found",
#     )


# # @router.put( # fully functional (merged) add and remove reactions using message[emojis]
# #     "/org/{org_id}/rooms/{room_id}/messages/{message_id}/reaction",
# #     response_model=ResponseModel,
# #     status_code=status.HTTP_200_OK,
# #     responses={
# #         401: {"description": "Invalid room member"},
# #         404: {"description": "Message not found"},
# #         424: {
# #             "description": "Failed to retrieve room members || Failed to add reaction or remove reaction"
# #         }
# #         # 424: {
# #         #     "description": "Failed to retrieve room members / Failed to add reaction or remove reaction"
# #         # }
# #     },
# # )
# # async def reactions(
# #     request: Emoji,
# #     org_id: str,
# #     room_id: str,
# #     message_id: str,
# #     background_tasks: BackgroundTasks,
# # ):
# #     """
# #     Checks if there are any reactions for the message.
# #     Adds a reaction to a message.
# #     Adds a user to list of reacted users if reaction already exists.
# #     Removes the user from the list of reacted users if user already reacted to the message.
# #     Removes a reaction from a message if reacted user count is 0.

# #     Args:
# #         request: Request object
# #         org_id: A unique identifier of the organization.
# #         room_id: A unique identifier of the room.
# #         message_id: A unique identifier of the message that is being edited.
# #         background_tasks: A daemon thread for publishing to centrifugo

# #     Returns:
# #         HTTP_200_OK {reaction added}:
# #         A dict containing data about the reaction that was added or removed.

# #         {
# #             "room_id": "619e28c31a5f54782939d59a",
# #             "message_id": "61cb65f378fb01b18fac147b",
# #             "emojis": [{
# #                 "name": "lol",
# #                 "count": 2,
# #                 "emoji": "lol",
# #                 "reactedUsersId": [
# #                     "619ba4671a5f54782939d385",
# #                     "6169704bc4133ddaa309dd07"
# #                 ]
# #             }]
# #         }

# #     Raises:
# #         HTTPException [401]: Invalid room member
# #         HTTPException [404]: Message not found
# #         HTTPException [424]: Failed to retrieve room members
# #         HTTPException [424]: Failed to add reaction
# #         HTTPException [424]: Failed to remove reaction
# #     """
# #     DB = DataStorage(org_id)

# #     message = await get_message(org_id, room_id, message_id)  # get message
# #     if not message:
# #         raise HTTPException(
# #             status_code=status.HTTP_404_NOT_FOUND,
# #             detail="Message not found",
# #         )

# #     members = await get_room_members(org_id, room_id)  # retrieve room members
# #     if not members:
# #         raise HTTPException(
# #             status_code=status.HTTP_424_FAILED_DEPENDENCY,
# #             detail="Failed to retrieve room members",
# #         )

# #     new_reaction = request.dict()
# #     if new_reaction["reactedUsersId"][0] not in list(
# #         members
# #     ):  # check if user is in list of room members
# #         # if new_reaction["reactedUsersId"][0] not in memberIds: # check if user is a room member
# #         raise HTTPException(
# #             status_code=status.HTTP_401_UNAUTHORIZED,
# #             detail="Invalid room member",
# #         )

# #     # if no reactions exist for the message
# #     # if not message["emojis"]:
# #     if not message.get("emojis"):
# #         message["emojis"] = [new_reaction]
# #         updated_emoji = await DB.update(
# #             MESSAGE_COLLECTION, document_id=message_id, data={"emojis": message["emojis"]}
# #         )
# #         if updated_emoji and updated_emoji.get("status_code") is not None:
# #             raise HTTPException(
# #                 status_code=status.HTTP_424_FAILED_DEPENDENCY,
# #                 detail="Failed to add reaction",
# #             )
# #         # publish to centrifugo in the background
# #         background_tasks.add_task(
# #             centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, new_reaction
# #         )
# #         return JSONResponse(
# #             content=ResponseModel.success(data=new_reaction, message="reaction added"),
# #             status_code=status.HTTP_200_OK,
# #         )

# #     # if reactions exist for the message
# #     for emoji in message["emojis"]:
# #         if emoji["name"] == new_reaction["name"]:  # if emoji is already in reactions

# #             # if user hasn't reacted with the emoji
# #             if new_reaction["reactedUsersId"][0] not in emoji["reactedUsersId"]:
# #                 emoji["reactedUsersId"].append(new_reaction["reactedUsersId"][0])
# #                 emoji["count"] += 1

# #                 added = await DB.update(
# #                     MESSAGE_COLLECTION,
# #                     document_id=message_id,
# #                     data={"emojis": message["emojis"]},
# #                 )
# #                 if added and added.get("status_code") is not None:
# #                     raise HTTPException(
# #                         status_code=status.HTTP_424_FAILED_DEPENDENCY,
# #                         detail="Failed to add reaction",
# #                     )
# #                 # publish to centrifugo in the background
# #                 background_tasks.add_task(
# #                     centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, emoji
# #                 )
# #                 return JSONResponse(
# #                     content=ResponseModel.success(data=emoji, message="reaction added"),
# #                     status_code=status.HTTP_200_OK,
# #                 )

# #             # if user has reacted with the emoji
# #             emoji["reactedUsersId"].remove(new_reaction["reactedUsersId"][0])
# #             emoji["count"] -= 1

# #             if emoji["count"] != 0:  # if emoji count is not 0
# #                 updated = await DB.update(
# #                     MESSAGE_COLLECTION,
# #                     document_id=message_id,
# #                     data={"emojis": message["emojis"]},
# #                 )
# #                 if updated and updated.get("status_code") is not None:
# #                     raise HTTPException(
# #                         status_code=status.HTTP_424_FAILED_DEPENDENCY,
# #                         detail="Failed to remove user's reaction",
# #                     )
# #                 # publish to centrifugo in the background
# #                 background_tasks.add_task(
# #                     centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, emoji
# #                 )
# #                 return JSONResponse(
# #                     content=ResponseModel.success(
# #                         data=emoji, message="user's reaction removed"
# #                     ),
# #                     status_code=status.HTTP_200_OK,
# #                 )

# #             message["emojis"].remove(emoji)  # if emoji count is 0
# #             removed = await DB.update(
# #                 MESSAGE_COLLECTION, document_id=message_id, data={"emojis": message["emojis"]}
# #             )
# #             if removed and removed.get("status_code") is not None:
# #                 raise HTTPException(
# #                     status_code=status.HTTP_424_FAILED_DEPENDENCY,
# #                     detail="Failed to remove reaction",
# #                 )
# #             # publish to centrifugo in the background
# #             background_tasks.add_task(
# #                 centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, removed
# #             )
# #             return JSONResponse(
# #                 content=ResponseModel.success(data=emoji, message="reaction removed"),
# #                 status_code=status.HTTP_200_OK,
# #             )

# #     # if emoji is not in reactions
# #     message["emojis"].append(new_reaction)
# #     new = await DB.update(
# #         MESSAGE_COLLECTION, document_id=message_id, data={"emojis": message["emojis"]}
# #     )
# #     if new and new.get("status_code") is not None:
# #         raise HTTPException(
# #             status_code=status.HTTP_424_FAILED_DEPENDENCY,
# #             detail="Failed to add reaction",
# #         )
# #     # publish to centrifugo in the background
# #     background_tasks.add_task(
# #         centrifugo_client.publish, room_id, Events.MESSAGE_UPDATE, new_reaction
# #     )
# #     return JSONResponse(
# #         content=ResponseModel.success(data=new_reaction, message="reaction added"),
# #         status_code=status.HTTP_200_OK,
# #     )
