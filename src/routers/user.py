from fastapi import APIRouter, HTTPException
from fastapi import Depends
from src.routers.auth import get_current_user
from datetime import datetime
from src.db import Users, Movies, Comments
from typing import Optional
from bson.objectid import ObjectId
from src.schemas import UpdateUserDetails, CommentSchema

router = APIRouter()

@router.patch("/update_user/")
async def update_info(request: UpdateUserDetails , user: dict = Depends(get_current_user)):
    update_fields = {}
    if "new_email" in request.dict():
        update_fields['email'] = request.new_email
    if "new_pass" in request.dict():
        update_fields['password'] = request.new_pass
    await Users.update_one({"_id": ObjectId(user['_id'])}, {"$set": update_fields})
    user['_id'] = str(user['_id'])
    return {"message": "User updated successfully.", "user": user}


@router.post("/comment/")
async def comment(request: CommentSchema, user: dict = Depends(get_current_user)):
    movie = await Movies.find_one({"title": request.movie_name})
    if not movie:
        return {"message": "Movie not found."}
    movie['_id'] = str(movie['_id'])
    user['_id'] = str(user['_id'])
    user['name'] = user['name']
    user['email'] = user['email']
    comment = {
        "name": user['name'],
        "email": user['email'],
        "movie_id": movie['_id'],
        "text": request.comment,
        "date": datetime.now()
    }
    await Comments.insert_one(comment)
    return {"message": "Comment added successfully."}
    

@router.patch('/cancel_subs/')
async def cancel_subscription( user: dict = Depends(get_current_user)):
    
        subtype = user["subtype"]
        user["_id"] = str(user["_id"])
        if subtype in ["Gold", "Silver"]:
            # Update the user's subtype to "Basic"
            await Users.update_one(
                {"_id": ObjectId(user["_id"])},
                {"$set": {"subtype": "Basic"}}
            )
            message = f"Your subscription has been changed from {subtype} to Basic."
        else:
            message = "Your subscription remains on Basic."
        user["subtype"] = "Basic"
        return {"message": message, "user": user}
    

    
@router.patch('/update_subs/{new_subscription}/')
async def update_subscription_patch( new_subscription: str,user: dict = Depends(get_current_user)):
    try:
            current_subscription = user["subtype"]
            message = ""
            user_id = str(user["_id"])
            if current_subscription == new_subscription:
                message = f"You are already using {current_subscription} membership."
            else:
                message = f"Your subscription has been changed from {current_subscription} to {new_subscription} ."
                await Users.update_one({"_id": ObjectId(user_id)}, {"$set": {"subtype": new_subscription}})
            user["_id"] = str(user["_id"])
            user["subtype"] = new_subscription
            return {"message": message, "user": user}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")