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
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")

        # Password must contain at least one uppercase letter
        if not any(char.isupper() for char in value):
            raise ValueError("Password must contain at least one uppercase letter")

        # Password must contain at least one lowercase letter
        if not any(char.islower() for char in value):
            raise ValueError("Password must contain at least one lowercase letter")

        # Password must contain at least one digit
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one digit")

        # Password must contain at least one special character
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password must contain at least one special character")

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