from fastapi import APIRouter, Depends, HTTPException, Request, status, Security,Depends,Response   
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field, ValidationError, validator
import re
import bcrypt
from src import schemas
from src.db import Users as User
import jwt
from src.config import config
router = APIRouter()
from bson.objectid import ObjectId
from src.db import Users
from datetime import datetime, timedelta, timezone
import redis,json
from fastapi.security import OAuth2PasswordBearer
import requests
from src.cache_system import r

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/signup")
async def signup(request: schemas.UserSignupSchema):
    try:
        hashed_password = bcrypt.hashpw(request.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        db_user = await User.find_one({"email": request.email.lower()})
        empty_pwd=""
        
        if db_user is not None:
            hash_pwd=db_user.get('password','')
            print(empty_pwd.encode('utf-8'), hash_pwd.encode('utf-8'))
            if empty_pwd == hash_pwd:
                token = jwt.encode(payload={"user_id": str(db_user.get('_id'))}, key=config["JWT_KEY"], algorithm="HS256")
                result = await User.update_one({"email": request.email.lower()},{'$set':{'password':hashed_password,'name':request.name}})
                if result is None:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password was not change,signup again")
                return {'status': 'success','message':'Password Changed successfully', 'token': token, 'fav': db_user.get('fav', []), 'watchlist': db_user.get('watchlist', [])}
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists.")
        user = {
            "name": request.name,
            "email": request.email.lower(),
            "password": hashed_password,
            "subtype": "Basic",
            "role": "user",
            'fav': [],
            'watchlist':[]
        }
        
        await User.insert_one(user)
        if '_id' in user:
            _id = str(user['_id'])
            
            

        token = jwt.encode(payload={"user_id": str(_id)}, key=config["JWT_KEY"], algorithm="HS256")
        return {'status': 'success',"message": "User created successfully.", 'token': token, 'fav': [], 'watchlist':[]}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    # return {"message": "User created successfully.", "user": user}


@router.post('/login')
async def login(payload: schemas.UserLoginSchema):
    try:
        db_user = await User.find_one({'email': payload.email.lower()})
        # print(db_user)
        if not db_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='No user found!!')
        hashed_password = db_user.get('password')
        _id = db_user.get("_id")
        if not _id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User ID not found')
        empty_pwd=""
        if empty_pwd == hashed_password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User does not exist')
        if not bcrypt.checkpw(payload.password.encode('utf-8'), hashed_password.encode('utf-8')):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect email or password')
        token = jwt.encode(payload={"user_id": str(_id), 'exp': datetime.now(timezone.utc)+timedelta(hours=24)}, key=config["JWT_KEY"], algorithm="HS256")
        return {'status': 'success', 'token': token, 'fav': db_user.get('fav', []), 'watchlist': db_user.get('watchlist', [])}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> dict:
    try:
        token = credentials.credentials
        try:
            token_data = jwt.decode(token, config["JWT_KEY"], algorithms=["HS256"], verify=True)
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Expired token')
        except jwt.PyJWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        user = await Users.find_one({'_id': ObjectId(token_data["user_id"])})
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")        
        return user

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code = 500, detail=str(e))

@router.post("/auth/callback")
async def auth_google(request: schemas.GoogleAuthLogin):
    try:
        name=request.name
        email=request.email.lower()
        profilePic=request.profilePic
        hashed_password = bcrypt.hashpw("".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        db_user = await User.find_one({'email': email.lower()})
        if db_user:
            token = jwt.encode(payload={"user_id": str(db_user['_id']), 'exp': datetime.now(timezone.utc)+timedelta(hours=24)}, key=config["JWT_KEY"], algorithm="HS256")
            return {'status': 'success', 'token': token, 'fav': db_user.get('fav', []), 'watchlist': db_user.get('watchlist', [])}
        user = {
            "name": name,
            "email": email,
            "password": "",
            "subtype": "Basic",
            "role": "user",
            'fav': [],
            'watchlist':[],
            'profilePic':profilePic
        }
            
        await User.insert_one(user)
        if '_id' in user:
            _id = str(user['_id'])
            
        token = jwt.encode(payload={"user_id": str(_id)}, key=config["JWT_KEY"], algorithm="HS256")
        return {'status': 'success',"message": "User created successfully.", 'token': token, 'fav': [], 'watchlist':[]}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))