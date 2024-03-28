from fastapi import APIRouter, HTTPException, status
from fastapi import Depends
from src.routers.auth import get_current_user
from datetime import datetime
from src.db import Users, Movies, Comments, Watchlists
from typing import Optional, List
from bson.objectid import ObjectId
from src.schemas import UpdateUserDetails, CommentSchema, UpdatePasswordSchema
import bcrypt
from src.routers.movie import get_movies
from src.cache_system import r

router = APIRouter()


@router.get('/user/')
async def get_user(user: dict = Depends(get_current_user)):
    try:
        user['_id'] = str(user['_id'])
        user.pop('password')
        if not 'watchlist' in user:
            user['watchlist']=[]
        else :
            user['watchlist']=await get_watchlists(user['watchlist'])
        if not 'fav' in user:
            user['fav']=[]
        else:
            user['fav']=await get_movies(user['fav'])
        return user
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code = 500, detail=str(e))


@router.get('/user_basic/{user_id}')
async def get_user_basic(user_id: str):
    try:
        user=await Users.find_one({'_id': ObjectId(user_id)}, {'password':0, 'watchlist':0, 'fav':0})
        user['_id']=str(user['_id'])
        return user
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code = 500, detail=str(e))


@router.patch("/update_user/")
async def update_info(request: UpdateUserDetails , user: dict = Depends(get_current_user)):
    try:
        update_fields = {}
        if request.new_email:
            update_fields['email'] = request.new_email
        if request.new_name:
            update_fields['name'] = request.new_name
        await Users.update_one({"_id": ObjectId(user['_id'])}, {"$set": update_fields})
        user['_id'] = str(user['_id'])
        
        return {"message": "User updated successfully."}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code = 500, detail=str(e))


@router.patch("/update_password/")
async def update_password(request: UpdatePasswordSchema , user: dict = Depends(get_current_user)):
    try:
        hashed_password = user['password']
        if not bcrypt.checkpw(request.old_password.encode('utf-8'), hashed_password.encode('utf-8')):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Old password does not match')
        
        if(request.new_password==request.old_password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='New password cannot be same as old password')
        
        if (request.new_password!=request.repeat_password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Repeated password does not match the new password')
        hashed_password = bcrypt.hashpw(request.new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        await Users.update_one({'_id': user['_id']}, {'$set': {'password': hashed_password}})
        return {"message": "Password updated successfully."}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code = 500, detail=str(e))


@router.post("/comment/")
async def comment(request: CommentSchema, user: dict = Depends(get_current_user)):
    try:
        movie = await Movies.find_one({"_id": ObjectId(request.movie_id)})
        if not movie:
            return {"message": "Movie not found."}
        movie['_id'] = str(movie['_id'])
        user['_id'] = str(user['_id'])
        user['name'] = user['name']
        user['email'] = user['email']
        comment = {
            "name": user['name'],
            "email": user['email'],
            "movie_id": ObjectId(movie['_id']),
            "text": request.comment,
            "date": datetime.now()
        }
        await Comments.insert_one(comment)
        keys=r.keys(f"comment:{movie['_id']}:*")
        for key in keys:
            r.delete(key)
        return {"message": "Comment added successfully."}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code = 500, detail=str(e))


@router.delete('/delete_comment/{comment_id}')
async def delete_comment(comment_id: str, user: dict= Depends(get_current_user)):
    try:
        user["_id"] = str(user["_id"])
        email=user.get('email', '')
        comment= await Comments.find_one({"_id": ObjectId(comment_id)})
        if comment:
            comment["_id"]=str(comment["_id"])
            comment['movie_id']=str(comment['movie_id'])

            if True:
                if email == comment['email'] or user['role']!='user':
                    await Comments.delete_one({"_id": ObjectId(comment_id)})
                    keys=r.keys(f"comment:{comment['movie_id']}:*")
                    for key in keys:
                        r.delete(key)
                    return {"message": "Comment deleted successfully."}
                raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Comment does not belong to user")
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such comment exists")
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code = 500, detail=str(e))


@router.patch('/cancel_subs/')
async def cancel_subscription( user: dict = Depends(get_current_user)):
    try:
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
        return {"message": message}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code = 500, detail=str(e))

    
@router.post('/webhook')
async def update_subscription_patch(request):
    request = request.json
    print(f"Received Webhook:  \n{request}")
    try:
        user_email = request['data']['attributes']['user_email']
        print(f"User Email: {user_email}")
        invoice_link = request['data']['attributes']['urls']['invoice_url']
        print(f"Invoice Link: {invoice_link}")
        user = await Users.find_one({"email": user_email})
        print(f"User: {user}")
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.") 
        amount_payed = request['data']['attributes']['subtotal_formatted'][1:]
        amount_payed = float(amount_payed)
        if amount_payed >= 95:
            new_subscription = "Gold"
        elif amount_payed >= 45:
            new_subscription = "Silver"
        else:
            new_subscription = "Basic"
        print(f"New Subscription: {new_subscription}")
        current_subscription = user["subtype"]
        message = ""
        user_id = str(user["_id"])
        if not (new_subscription in ["Gold", "Silver", "Basic"]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No subscription exists.")
        
        if current_subscription == new_subscription:
            message = f"You are already using {current_subscription} membership."
        else:
            message = f"Your subscription has been changed from {current_subscription} to {new_subscription} ."
            # Get current date
            current_date = datetime.now().date()

            # Convert date to string format
            date_string = current_date.strftime("%Y-%m-%d")
            await Users.update_one({"_id": ObjectId(user_id)}, {"$set": {"subtype": new_subscription, "last_change":date_string, "invoice_url": invoice_link, "amount_payed": amount_payed}})   
        user["_id"] = str(user["_id"])
        user["subtype"] = new_subscription
        print(f"Message: {message}")
        return {"message": message}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch('/add_favourite/{movie_id}')
async def add_favourite(movie_id: str, user: dict = Depends(get_current_user)):
    try:
        movie = await Movies.find_one({"_id": ObjectId(movie_id)})
        if not movie:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Movie not found.")
        if '_id' in movie:
            movie['_id'] = str(movie['_id'])
        if '_id' in user:
            user['_id'] = str(user['_id'])
        
        fav=user.get('fav', [])
        
        if not movie_id in fav:
            fav.append(movie_id)
            await Users.update_one({"_id": ObjectId(user['_id'])}, {'$set': {'fav': fav}})
            return {"message": "Movie added in favourites successfully.", 'added':1}
        
        else:
            fav.remove(movie_id)
            await Users.update_one({"_id": ObjectId(user['_id'])}, {'$set': {'fav': fav}})
            return {"message": "Movies removed from favourites successfully.", 'added':0}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/add_watchlist/{watchlist_name}')
async def add_watchlist(watchlist_name:str, user: dict = Depends(get_current_user)):
    try:
        
        if '_id' in user:
            user['_id'] = str(user['_id'])
        user_watchlists=user.get('watchlist',[])
        watchlist={
            'name': watchlist_name, 
            'user_id': user['_id'], 
            'movies': []
        }
        await Watchlists.insert_one(watchlist)
        
        _id= str(watchlist['_id'])
        
        user_watchlists.append(_id)
        
        await Users.update_one({"_id": ObjectId(user['_id'])}, {'$set': {'watchlist':user_watchlists}})
        
        return {"message": "Watchlist added successfully.", 'watchlist': _id, 'user_watchlist': user_watchlists}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete('/remove_watchlist/{watchlist_id}')
async def remove_watchlist(watchlist_id:str, user: dict = Depends(get_current_user)):
    try:
        watchlist=await Watchlists.find_one({"_id": ObjectId(watchlist_id)})
        
        
        if not watchlist:
            raise HTTPException(status_code= 404, detail="Watchlist not found.")
        
        
        if '_id' in user:
            user['_id'] = str(user['_id'])
        if '_id' in watchlist :
            watchlist['_id']=str(watchlist['_id'])
        
        if watchlist['user_id']!=user['_id'] and user['role']=='user':
            raise HTTPException(status_code =status.HTTP_401_UNAUTHORIZED, detail="Watchlist does not belong to user")
        
        user_watchlist=user.get('watchlist', [])
        if watchlist['user_id'] != user['_id']:
            user2=await Users.find_one({"_id": ObjectId(watchlist['user_id'])})
            user2['_id']=str(user2['_id'])
            user_watchlist=user2.get('watchlist', [])
        
        
        user_watchlist.remove(watchlist['_id'])
        
        
        await Users.update_one({"_id": ObjectId(user['_id'])}, {'$set': {'watchlist':user_watchlist}})
        await Watchlists.delete_one({"_id": ObjectId(watchlist['_id'])})
        
        return {"message": "Watchlist removed successfully.", 'user_watchlist': user_watchlist}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch('/add_movie_to_watchlist/{watchlist_id}/{movie_id}')
async def add_remove_movie_in_watchlist(watchlist_id:str, movie_id: str, user: dict = Depends(get_current_user)):
    try:
        movie = await Movies.find_one({"_id": ObjectId(movie_id)})
        watchlist=await Watchlists.find_one({"_id": ObjectId(watchlist_id)})
        
        if not movie:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Movie not found.")
        if not watchlist:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Watchlist not found.")
        
        if '_id' in movie:
            movie['_id'] = str(movie['_id'])
        if '_id' in user:
            user['_id'] = str(user['_id'])
        if '_id' in watchlist :
            watchlist['_id']=str(watchlist['_id'])
        
        if watchlist['user_id']!=user['_id'] and user['role']=='user':
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Watchlist does not belong to user")
        
        watchlist_movies=watchlist.get('movies', [])
        
        
        if not movie_id in watchlist_movies:
            watchlist_movies.append(movie_id)
            await Watchlists.update_one({"_id": ObjectId(watchlist['_id'])}, {'$set': {'movies': watchlist_movies}})
            return {"message": "Movie added in watchlist successfully.", 'added':1, "movies": watchlist_movies}
        
        else:
            watchlist_movies.remove(movie_id)
            await Watchlists.update_one({"_id": ObjectId(watchlist['_id'])}, {'$set': {'movies': watchlist_movies}})
            return {"message": "Movies removed from watchlist successfully.", 'added': 0, "movies": watchlist_movies}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/watchlist/{watchlist_id}')
async def get_watchlist(watchlist_id:str):
    try:
        watchlist=await Watchlists.find_one({"_id": ObjectId(watchlist_id)})
        if watchlist:
            watchlist['_id']=str(watchlist['_id'])
            watchlist['movies']=await get_movies(movies_ids=watchlist['movies'])
            return watchlist
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/watchlists_list/")
async def get_watchlists(watchlist_ids: List[str]):
    try:
        bson_watchlist_ids = [ObjectId(oid) for oid in watchlist_ids]

        watchlists = await Watchlists.find({"_id": {"$in": bson_watchlist_ids}}).to_list(length=None)

        for watchlist in watchlists:
            watchlist['_id']=str(watchlist['_id'])
            watchlist['movies']= await get_movies(movies_ids=watchlist['movies'])
        
        movies_dict = {str(movie['_id']): movie for movie in watchlists}
        ret = [movies_dict[str(movie_id)] for movie_id in watchlist_ids]
        return ret
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/users_list/")
async def get_users(users_ids: List[str]):
    try:

        bson_users_ids = [ObjectId(oid) for oid in users_ids]


        users = await Users.find({"_id": {"$in": bson_users_ids}}, {"password":0, "watchlist":0, "fav":0}).to_list(length=None)

        for user in users:
            user['_id']=str(user['_id'])
        movies_dict = {str(movie['_id']): movie for movie in users}
        ret = [movies_dict[str(movie_id)] for movie_id in users_ids]
        return ret

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/user_comments/{user_id}')
async def get_user_comments(user_id : str, count: Optional[int] = 10):
    try:
        if count<1:
            return []
        user=await Users.find_one({"_id": ObjectId(user_id)})
        if not user:
            return []
        comments=await Comments.find({'email':user.get("email", '')}).sort([("date", -1)]).limit(count).to_list(length=None)
        for comment in comments:
            comment['_id']=str(comment['_id'])
            comment['movie_id']=str(comment['movie_id'])
            comment['date']=comment['date'].strftime('%Y-%m-%d %H:%M:%S')
        return comments
    except Exception as e:
        raise HTTPException(status_code = 500, detail=str(e))