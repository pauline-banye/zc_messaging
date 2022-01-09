













        











    
# @router.put(
#     "/org/{org_id}/rooms/{room_id}/messages/{message_id}/reactions",
#     response_model=ResponseModel,
#     status_code=status.HTTP_200_OK,
#     responses={
#         400: {"description": "Failed to retrieve room members"},
#         401: {"description": "Invalid room member"},
#         404: {"description": "Message not found"},
#         424: {"description": "Failed to add reaction / Failed to remove reaction"},
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
#     Adds a reaction to a message.
#     If a reaction with the same payload already exists, the reaction will be removed.

#     Args:
#         request: Request object
#         org_id: A unique identifier of the organization.
#         room_id: A unique identifier of the room.
#         message_id: A unique identifier of the message that is being edited.
#         background_tasks: A daemon thread for publishing to centrifugo

#     Returns:
#         HTTP_200_OK {reaction added}:
#         A dict containing data about the reaction that was added or removed.

#             {
#                 "status": "success",
#                 "message": "reaction added / removed",
#                 "data": {
#                     "room_id": "619e28c31a5f54782939d59a",
#                     "message_id": "61cb65f378fb01b18fac147b",
#                     "emojis": [
#                         {
#                             "name": "lmao",
#                             "count": 1,
#                             "emoji": "lmao",
#                             "reactedUsersId": [
#                             "61696f5ac4133ddaa309dcfe"
#                             ]
#                         }
#                     ]
#                 }
#             }

#     Raises:
#         HTTPException [400]: Failed to retrieve room members
#         HTTPException [401]: Invalid room member
#         HTTPException [404]: Message not found
#         HTTPException [424]: Failed to add reaction / Failed to remove reaction
#     """
#     DB = DataStorage(org_id)
    
#     message = await get_message(org_id, room_id, message_id) # get message
#     if not message:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Message not found",
#         ) 
#     react = message.get("emojis") 
    
#     members = await get_room_members(org_id, room_id) # retrieve room members
#     if not members:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Failed to retrieve room members",
#         )
#     memberIds = list(members) # convert romm members to list
#     print (memberIds)
    
#     new_reaction = request.dict()
#     print (new_reaction["reactedUsersId"])

#     if new_reaction["reactedUsersId"][0] not in memberIds: # check if user is in room
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid room member",
#         )
#     print ("success member in room")
    
#     if len(react) != 0: # check if message has reactions
#         print ("react not 0")
       
#         for emoji in react:
#             # if emoji["data"]["name"] == new_reaction["name"]: # check if reaction already exists
#             if emoji["name"] == new_reaction["name"]: # check if reaction already exists
#             # if new_reaction["name"] in emoji["name"]: # check if reaction already exists
#                 print ("reaction name exists")
                
#                 if new_reaction["reactedUsersId"][0] not in emoji["reactedUsersId"]: # check if user has reacted to message
#                 # if new_reaction["reactedUsersId"][0] != emoji["reactedUsersId"]: # check if user has reacted to message
                    
#                     emoji["reactedUsersId"].append(new_reaction["reactedUsersId"][0])
#                     emoji["count"] = len(emoji["reactedUsersId"])
                    
#                     print (emoji)
#                     added = await DB.update(
#                         MESSAGE_COLLECTION,
#                         document_id=message_id,
#                         data={"emojis": react},
#                     )
#                     print ("success update 1")
#                     if added and added.get("status_code") is None:
#                         data = {
#                             "room_id": room_id,
#                             "message_id": message_id,
#                             "emojis": [new_reaction],
#                             }
#                         print("data added 1")
#                         # publish to centrifugo
#                         background_tasks.add_task(
#                             centrifugo_client.publish,
#                             room_id,
#                             Events.MESSAGE_UPDATE,
#                             emoji,
#                         )
#                         print ("added publish 1")
#                         return JSONResponse(
#                             content=ResponseModel.success(
#                                 data=emoji, 
#                                 message="Reaction added"
#                                 ),
#                             status_code=status.HTTP_200_OK,
#                         )
#                     print ("added return 1")
#                     raise HTTPException(
#                         status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                         detail="Failed to add reaction",
#                     )
#                 raise HTTPException(
#                     status_code=status.HTTP_409_CONFLICT,
#                     detail="Duplicate reaction",
#                 )    
                
#             print ("reaction name does not exist")
#             react.append(new_reaction)
#             emoji["count"] = len(emoji["reactedUsersId"])
            
#             added = await DB.update(
#                 MESSAGE_COLLECTION, document_id=message_id, data={"emojis": react}
#                 )
#             print("success update 2")
#             if added:
#                 data = {
#                     "room_id": room_id,
#                     "message_id": message_id,
#                     "emojis": [new_reaction],
#                     }
#                 print ("added 2")
#                 background_tasks.add_task(
#                     centrifugo_client.publish,
#                     room_id,
#                     Events.MESSAGE_UPDATE,
#                     react
#                 )
#                 print("success publish 2")
#                 return JSONResponse(
#                     content=ResponseModel.success(
#                     data=data, message="Reaction added"
#                         ),
#                     status_code=status.HTTP_200_OK,
#                     )
#             print ("success return 2")
#             raise HTTPException(        
#                 status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                 detail="Failed to add reaction",
#                 )
#     # else:
#     print ("react is 0")
#     react.append(new_reaction)
#     new_reaction["count"] = len(new_reaction["reactedUsersId"])
#     added = await DB.update(
#         MESSAGE_COLLECTION, document_id=message_id, data={"emojis": react}
#         )
#     print("success update 3")
#     if added:
#         data = {
#             "room_id": room_id,
#             "message_id": message_id,
#             "emojis": [new_reaction],
#             }
#         print ("added 3")
#         background_tasks.add_task(
#             centrifugo_client.publish,
#             room_id,
#             Events.MESSAGE_UPDATE,
#             react
#         )
#         print("success publish 3")
#         return JSONResponse(
#             content=ResponseModel.success(
#             data=data, message="Reaction added"
#                 ),
#             status_code=status.HTTP_200_OK,
#             )
#     print ("success return 3")
#     raise HTTPException(        
#         status_code=status.HTTP_424_FAILED_DEPENDENCY,
#         detail="Failed to add reaction",
#         )




# @router.put(
#     "/org/{org_id}/rooms/{room_id}/messages/{message_id}/reactions", # add only: functional for first use case
#     response_model=ResponseModel,
#     status_code=status.HTTP_200_OK,
#     responses={
#         400: {"description": "Failed to retrieve room members"},
#         401: {"description": "Invalid room member"},
#         404: {"description": "Message not found"},
#         424: {"description": "Failed to add reaction / Failed to remove reaction"},
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
#     Adds a reaction to a message.
#     If a reaction with the same payload already exists, the reaction will be removed.

#     Args:
#         request: Request object
#         org_id: A unique identifier of the organization.
#         room_id: A unique identifier of the room.
#         message_id: A unique identifier of the message that is being edited.
#         background_tasks: A daemon thread for publishing to centrifugo

#     Returns:
#         HTTP_200_OK {reaction added}:
#         A dict containing data about the reaction that was added or removed.

#             {
#                 "status": "success",
#                 "message": "reaction added / removed",
#                 "data": {
#                     "room_id": "619e28c31a5f54782939d59a",
#                     "message_id": "61cb65f378fb01b18fac147b",
#                     "emojis": [
#                         {
#                             "name": "lmao",
#                             "count": 1,
#                             "emoji": "lmao",
#                             "reactedUsersId": [
#                             "61696f5ac4133ddaa309dcfe"
#                             ]
#                         }
#                     ]
#                 }
#             }

#     Raises:
#         HTTPException [400]: Failed to retrieve room members
#         HTTPException [401]: Invalid room member
#         HTTPException [404]: Message not found
#         HTTPException [424]: Failed to add reaction / Failed to remove reaction
#     """
#     DB = DataStorage(org_id)
    
#     message = await get_message(org_id, room_id, message_id) # get message
#     if not message:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Message not found",
#         ) 
#     react = message.get("emojis") 
    
#     members = await get_room_members(org_id, room_id) # retrieve room members
#     if not members:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Failed to retrieve room members",
#         )
#     memberIds = list(members) # convert romm members to list
#     print (memberIds)
    
#     new_reaction = request.dict()
#     print (new_reaction["reactedUsersId"])

#     if new_reaction["reactedUsersId"][0] not in memberIds: # check if user is in room
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid room member",
#         )
#     print ("success member in room")
    
#     if len(react) != 0: # check if message has reactions
#         print ("react not 0")
       
#         for emoji in react:
#             if emoji["name"] == new_reaction["name"]: # check if reaction already exists
#                 print ("reaction name exists")
                
#                 if new_reaction["reactedUsersId"][0] not in emoji["reactedUsersId"]: # check if user has reacted to message
#                     emoji["reactedUsersId"].append(new_reaction["reactedUsersId"][0])
#                     emoji["count"] = len(emoji["reactedUsersId"])
                    
#                     print (emoji)
#                     added = await DB.update(
#                         MESSAGE_COLLECTION,
#                         document_id=message_id,
#                         data={"emojis": react},
#                     )
#                     print ("success update 1")
#                     if added and added.get("status_code") is None:
#                         data = {
#                             "room_id": room_id,
#                             "message_id": message_id,
#                             "emojis": [new_reaction],
#                             }
#                         print("data added 1")
#                         # publish to centrifugo
#                         background_tasks.add_task(
#                             centrifugo_client.publish,
#                             room_id,
#                             Events.MESSAGE_UPDATE,
#                             emoji,
#                         )
#                         print ("added publish 1")
#                         return JSONResponse(
#                             content=ResponseModel.success(
#                                 data=emoji, 
#                                 message="Reaction added"
#                                 ),
#                             status_code=status.HTTP_200_OK,
#                         )
#                     print ("added return 1")
#                     raise HTTPException(
#                         status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                         detail="Failed to add reaction",
#                     )
#                 raise HTTPException(
#                     status_code=status.HTTP_409_CONFLICT,
#                     detail="Duplicate reaction",
#                 )    
#             print ("reaction name does not exist")
#             react.append(new_reaction)
#             emoji["count"] = len(emoji["reactedUsersId"])
            
#             added = await DB.update(
#                 MESSAGE_COLLECTION, document_id=message_id, data={"emojis": react}
#                 )
#             print("success update 2")
#             if added:
#                 data = {
#                     "room_id": room_id,
#                     "message_id": message_id,
#                     "emojis": [new_reaction],
#                     }
#                 print ("added 2")
#                 background_tasks.add_task(
#                     centrifugo_client.publish,
#                     room_id,
#                     Events.MESSAGE_UPDATE,
#                     react
#                 )
#                 print("success publish 2")
#                 return JSONResponse(
#                     content=ResponseModel.success(
#                     data=data, message="Reaction added"
#                         ),
#                     status_code=status.HTTP_200_OK,
#                     )
#             print ("success return 2")
#             raise HTTPException(        
#                 status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                 detail="Failed to add reaction",
#                 )
#     # else:
#     print ("react is 0")
#     react.append(new_reaction)
#     new_reaction["count"] = len(new_reaction["reactedUsersId"])
#     added = await DB.update(
#         MESSAGE_COLLECTION, document_id=message_id, data={"emojis": react}
#         )
#     print("success update 3")
#     if added:
#         data = {
#             "room_id": room_id,
#             "message_id": message_id,
#             "emojis": [new_reaction],
#             }
#         print ("added 3")
#         background_tasks.add_task(
#             centrifugo_client.publish,
#             room_id,
#             Events.MESSAGE_UPDATE,
#             react
#         )
#         print("success publish 3")
#         return JSONResponse(
#             content=ResponseModel.success(
#             data=data, message="Reaction added"
#                 ),
#             status_code=status.HTTP_200_OK,
#             )
#     print ("success return 3")
#     raise HTTPException(        
#         status_code=status.HTTP_424_FAILED_DEPENDENCY,
#         detail="Failed to add reaction",
#         )
                    
    


# @router.put(
#     "/org/{org_id}/rooms/{room_id}/messages/{message_id}/reactions", # add and remove: not fully functional
#     response_model=ResponseModel,
#     status_code=status.HTTP_200_OK,
#     responses={
#         400: {"description": "Failed to retrieve room members"},
#         401: {"description": "Invalid room member"},
#         404: {"description": "Message not found"},
#         424: {"description": "Failed to add reaction / Failed to remove reaction"},
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
#     Adds a reaction to a message.
#     If a reaction with the same payload already exists, the reaction will be removed.

#     Args:
#         request: Request object
#         org_id: A unique identifier of the organization.
#         room_id: A unique identifier of the room.
#         message_id: A unique identifier of the message that is being edited.
#         background_tasks: A daemon thread for publishing to centrifugo

#     Returns:
#         HTTP_200_OK {reaction added}:
#         A dict containing data about the reaction that was added or removed.

#             {
#                 "status": "success",
#                 "message": "reaction added / removed",
#                 "data": {
#                     "room_id": "619e28c31a5f54782939d59a",
#                     "message_id": "61cb65f378fb01b18fac147b",
#                     "emojis": [
#                         {
#                             "name": "lmao",
#                             "count": 1,
#                             "emoji": "lmao",
#                             "reactedUsersId": [
#                             "61696f5ac4133ddaa309dcfe"
#                             ]
#                         }
#                     ]
#                 }
#             }

#     Raises:
#         HTTPException [400]: Failed to retrieve room members
#         HTTPException [401]: Invalid room member
#         HTTPException [404]: Message not found
#         HTTPException [424]: Failed to add reaction / Failed to remove reaction
#     """
#     DB = DataStorage(org_id)
    
#     message = await get_message(org_id, room_id, message_id) # get message
#     if not message:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Message not found",
#         ) 
#     react = message.get("emojis") 
    
#     members = await get_room_members(org_id, room_id) # retrieve room members
#     if not members:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Failed to retrieve room members",
#         )
#     memberIds = list(members) # convert romm members to list
#     print (memberIds)
    
#     new_reaction = request.dict()
#     print (new_reaction["reactedUsersId"])

#     if new_reaction["reactedUsersId"][0] not in memberIds: # check if user is in room
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid room member",
#         )
#     print ("success member in room")
    
#     if len(react) != 0: # check if message has reactions
#         print ("react not 0")
       
#         for emoji in react:
#             if emoji["name"] == new_reaction["name"]: # check if reaction already exists
#                 print ("reaction name exists")
                
#                 if new_reaction["reactedUsersId"][0] not in emoji["reactedUsersId"]: # check if user has reacted to message
#                     emoji["reactedUsersId"].append(new_reaction["reactedUsersId"][0])
#                     emoji["count"] = len(emoji["reactedUsersId"])
                    
#                     print (emoji)
#                     added = await DB.update(
#                         MESSAGE_COLLECTION,
#                         document_id=message_id,
#                         data={"emojis": react},
#                     )
#                     print ("success update 1")
#                     if added and added.get("status_code") is None:
#                         data = {
#                             "room_id": room_id,
#                             "message_id": message_id,
#                             "emojis": [new_reaction],
#                             }
#                         print("data added 1")
#                         # publish to centrifugo
#                         background_tasks.add_task(
#                             centrifugo_client.publish,
#                             room_id,
#                             Events.MESSAGE_UPDATE,
#                             emoji,
#                         )
#                         print ("added publish 1")
#                         return JSONResponse(
#                             content=ResponseModel.success(
#                                 data=data, 
#                                 message="Reaction added"
#                                 ),
#                             status_code=status.HTTP_200_OK,
#                         )
#                     print ("added return 1")
#                     raise HTTPException(
#                         status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                         detail="Failed to add reaction",
#                     )
                    
#                 if len(emoji["reactedUsersId"]) > 1: # check if user is not the only one who reacted to message
#                     emoji["reactedUsersId"].remove(new_reaction["reactedUsersId"][0]) # remove user from list

#                     removed = await DB.update(
#                         MESSAGE_COLLECTION,
#                         document_id=message_id,
#                         data={"emojis": react},
#                     )
#                     print ("removed update 1")
                    
#                     if removed and removed.get("status_code") is None:
#                         data = {
#                             "room_id": room_id,
#                             "message_id": message_id,
#                             "emojis": [new_reaction],
#                             }
#                         print ("data removed 1")
#                         # publish to centrifugo
#                         background_tasks.add_task(
#                             centrifugo_client.publish,
#                             room_id,
#                             Events.MESSAGE_UPDATE,
#                             emoji,
#                         )
#                         print ("removed publish 1")
#                         return JSONResponse(
#                             content=ResponseModel.success(
#                                 data=data, 
#                                 message="Reaction removed"
#                                 ),
#                             status_code=status.HTTP_200_OK,
#                         )
#                     print ("removed return 1")
#                     raise HTTPException(
#                         status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                         detail="Failed to remove reaction",
#                     )
                    
#                 react.remove(emoji) # remove reaction from list
#                 removed = await DB.update(
#                     MESSAGE_COLLECTION,
#                     document_id=message_id,
#                     data={"emojis": react},
#                 )
#                 print ("removed update 2")
                
#                 if removed and removed.get("status_code") is None:
#                     data = {
#                         "room_id": room_id,
#                         "message_id": message_id,
#                         "emojis": [new_reaction],
#                         }
#                     print ("data removed 2")
#                     # publish to centrifugo
#                     background_tasks.add_task(
#                         centrifugo_client.publish,
#                         room_id,
#                         Events.MESSAGE_UPDATE,
#                         emoji,
#                     )
#                     print ("removed publish 2")
#                     return JSONResponse(
#                         content=ResponseModel.success(
#                             data=data, 
#                             message="Reaction removed"
#                             ),
#                         status_code=status.HTTP_200_OK,
#                     )
#                 print ("removed return 2")
#                 raise HTTPException(
#                     status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                     detail="Failed to remove reaction",
#                 )
                    
#             print ("reaction name does not exist")
#             react.append(new_reaction)
#             emoji["count"] = len(emoji["reactedUsersId"])
            
#             added = await DB.update(
#                 MESSAGE_COLLECTION, document_id=message_id, data={"emojis": react}
#                 )
#             print("success update 2")
#             if added:
#                 data = {
#                     "room_id": room_id,
#                     "message_id": message_id,
#                     "emojis": [new_reaction],
#                     }
#                 print ("added 2")
#                 background_tasks.add_task(
#                     centrifugo_client.publish,
#                     room_id,
#                     Events.MESSAGE_UPDATE,
#                     react
#                 )
#                 print("success publish 2")
#                 return JSONResponse(
#                     content=ResponseModel.success(
#                     data=data, message="Reaction added"
#                         ),
#                     status_code=status.HTTP_200_OK,
#                     )
#             print ("success return 2")
#             raise HTTPException(        
#                 status_code=status.HTTP_424_FAILED_DEPENDENCY,
#                 detail="Failed to add reaction",
#                 )
#     # else:
#     print ("react is 0")
#     react.append(new_reaction)
#     new_reaction["count"] = len(new_reaction["reactedUsersId"])
#     added = await DB.update(
#         MESSAGE_COLLECTION, document_id=message_id, data={"emojis": react}
#         )
#     print("success update 3")
#     if added:
#         data = {
#             "room_id": room_id,
#             "message_id": message_id,
#             "emojis": [new_reaction],
#             }
#         print ("added 3")
#         background_tasks.add_task(
#             centrifugo_client.publish,
#             room_id,
#             Events.MESSAGE_UPDATE,
#             react
#         )
#         print("success publish 3")
#         return JSONResponse(
#             content=ResponseModel.success(
#             data=data, message="Reaction added"
#                 ),
#             status_code=status.HTTP_200_OK,
#             )
#     print ("success return 3")
#     raise HTTPException(        
#         status_code=status.HTTP_424_FAILED_DEPENDENCY,
#         detail="Failed to add reaction",
#         )
  