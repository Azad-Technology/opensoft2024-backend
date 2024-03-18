from fastapi import APIRouter, HTTPException
from fastapi import Depends
from src.routers.auth import get_current_user
from datetime import datetime
from src.db import Users 
from typing import Optional
from bson.objectid import ObjectId

router = APIRouter()

@router.patch("/update_email")
async def update_info(new_pass: str , new_email : str, user: dict = Depends(get_current_user)):
    user = await Users.find_one({"_id": user['_id']})
    if not user:
        return {"message": "User not found."}
    user['_id'] = str(user['_id'])
    update_fields = {}
    if new_pass:
        update_fields['password'] = new_pass
    if new_email:
        update_fields['email'] = new_email
    
    await Users.update_one({"_id": user['_id']}, {"$set": update_fields})
    if '_id' in user:
        user['_id'] = str(user['_id'])

    return {"message": "Email updated successfully.", "user": user}

@router.patch("/update_pass")
async def update_info(new_pass: str ,  user: dict = Depends(get_current_user)):
    user = await Users.find_one({"_id": user['_id']})
    if not user:
        return {"message": "User not found."}
    user['_id'] = str(user['_id'])
    update_fields = {}
    if new_pass:
        update_fields['password'] = new_pass
    
    await Users.update_one({"_id": user['_id']}, {"$set": update_fields})
    if '_id' in user:
        user['_id'] = str(user['_id'])

    return {"message": "Password updated successfully.", "user": user}

