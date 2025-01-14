import re

from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field
from pydantic import field_validator
from starlette import status


LOGIN_REGEXP = r"^(?!.*[._]{2})[a-zA-Z0-9](?:[a-zA-Z0-9._]{1,30}[a-zA-Z0-9])?$"


class CreateUserSchema(BaseModel):
    login: str = Field(..., min_length=4, max_length=32)
    password: str = Field(..., min_length=8, max_length=64)
    email: EmailStr

    @field_validator("login")
    @classmethod
    def validate_login(cls, value):
        if not re.match(LOGIN_REGEXP, value):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Invalid login {value}",
            )
        return value
