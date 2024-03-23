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

r = redis.Redis(host='10.105.12.4',port=8045, decode_responses=True)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/signup/")
async def signup(request: schemas.UserSignupSchema):
    try:
        hashed_password = bcrypt.hashpw(request.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        db_user = await User.find_one({"email": request.email.lower()})
        if db_user is not None:
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


@router.post('/login/')
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



@router.get("/login/google")
async def login_google():
    return {
        "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={config['GOOGLE_CLIENT_ID']}&redirect_uri={config['GOOGLE_REDIRECT_URI']}&scope=openid%20profile%20email&access_type=offline"
    }

@router.get("http://40.81.24.53:8000/auth/callback")
async def auth_google(request: Request, response: Response, code: str = None):
    if "error" in request.query_params:
        raise HTTPException(status_code=400, detail="Error: " + request.query_params["error"])
    if code is None:
        raise HTTPException(status_code=400, detail="Authorization code not provided")
    
    token_url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "code": code,
        "client_id": config['GOOGLE_CLIENT_ID'],
        "client_secret": config['GOOGLE_CLIENT_SECRET'],
        "redirect_uri": config['GOOGLE_REDIRECT_URI'],
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    access_token = response.json().get("access_token")
    user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo", headers={"Authorization": f"Bearer {access_token}"})
    print(user_info.json())
    if user_info:
        
        email=user_info.json()['email']
        db_user = await User.find_one({'email': email.lower()})
        if db_user:
            token = jwt.encode(payload={"user_id": str(db_user['_id']), 'exp': datetime.now(timezone.utc)+timedelta(hours=24)}, key=config["JWT_KEY"], algorithm="HS256")
            return {'status': 'success', 'token': token, 'fav': db_user.get('fav', []), 'watchlist': db_user.get('watchlist', [])}
        RedirectResponse(url='/')
    return user_info.json()

@router.get("/token")
async def get_token(token: str = Depends(oauth2_scheme)):
    return jwt.decode(token, config['GOOGLE_CLIENT_SECRET'], algorithms=["HS256"])