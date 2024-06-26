from pydantic import BaseModel, EmailStr, constr, HttpUrl, conint, validator, Field
from typing import List, Optional, Union
from typing import List, Optional, Union
from enum import Enum
from pydantic import BaseModel
import re


class UserSignupSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    @validator("password")
    def validate_password(cls, value):
        # Password must be at least 8 characters long
        if len(value) < 8 and value != "":
            raise ValueError("Password must be at least 8 characters long")


        return value

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class MovieEmbedSchema(BaseModel):
    _id: str
    title: str
    plot: str

class RRFQuerySchema(BaseModel):
    query: str

class UpdateUserDetails(BaseModel):
    new_name: Optional[str]=None
    new_email: Optional[EmailStr]=None

class CommentSchema(BaseModel):
    comment: str
    movie_id: str


class UpdatePasswordSchema(BaseModel):
    old_password: str
    new_password: str
    @validator("new_password")
    def validate_password(cls, value):
        # Password must be at least 8 characters long
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")


        return value

    repeat_password: str
    
class GoogleAuthLogin(BaseModel):
    name: str
    email: EmailStr
    profilePic: str