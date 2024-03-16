from fastapi import APIRouter, Depends, HTTPException, Request, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
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

@router.post("/signup")
async def signup(request: schemas.UserSignupSchema):
    hashed_password = bcrypt.hashpw(request.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    db_user = await User.find_one({"email": request.email.lower()})
    if db_user is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists.")
    user = {
        "name": request.name,
        "email": request.email.lower(),
        "password": hashed_password,
    }
    
    await User.insert_one(user)
    if '_id' in user:
        user['_id'] = str(user['_id'])
    # db_user = await User.find_one({'email': request.email.lower()})
    # # if db_user:
    # #     print("Found")
    return {"message": "User created successfully.", "user": user}


@router.post('/login')
async def login(payload: schemas.UserLoginSchema):
    db_user = await User.find_one({'email': payload.email.lower()})
    # print(db_user)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect email')
    hashed_password = db_user.get('password')
    _id = db_user.get("_id")
    if not _id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User ID not found')
    if not bcrypt.checkpw(payload.password.encode('utf-8'), hashed_password.encode('utf-8')):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect email or password')
    token = jwt.encode(payload={"user_id": str(_id)}, key=config["JWT_KEY"], algorithm="HS256")
    return {'status': 'success', 'token': token}

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> dict:
    token = credentials.credentials
    try:
        token_data = jwt.decode(token, config["JWT_KEY"], algorithms=["HS256"])
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = await Users.find_one({'_id': ObjectId(token_data["user_id"])})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user