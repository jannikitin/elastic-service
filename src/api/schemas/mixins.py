import re

from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator
from starlette import status

LOGIN_REGEXP = r"^(?!.*[._]{2})[a-zA-Z0-9](?:[a-zA-Z0-9._]{1,30}[a-zA-Z0-9])?$"


class LoginMixin(BaseModel):
    login: str = Field(
        ...,
        min_length=4,
        max_length=32,
    )

    @field_validator("login")
    @classmethod
    def validate_login(cls, value):
        if not re.match(LOGIN_REGEXP, value):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Invalid login {value}",
            )
        return value


class FirstAndLastNameMixin(BaseModel):

    name: str = Field(..., min_length=2, max_length=64)
    lastname: str = Field(..., min_length=2, max_length=64)

    @field_validator("name")
    @classmethod
    def validate_first_name(cls, value: str):
        if not value.isalpha():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="First name should contain only letters",
            )
        return value

    @field_validator("lastname")
    @classmethod
    def validate_last_name(cls, value: str):
        if not value.isalpha():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Last name should contain only letters",
            )
        return value


class PasswordMixin(BaseModel):
    password: str = Field(..., min_length=8, max_length=64)
