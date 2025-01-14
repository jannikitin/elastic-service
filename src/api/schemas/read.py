from typing import Annotated
from uuid import UUID

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field


class ShowUser(BaseModel):
    id: Annotated[UUID, Field(...)]
    login: Annotated[str, Field(..., min_length=4, max_length=32)]
    email: Annotated[EmailStr, Field(...)]
    name: str | None = None
    lastname: str | None = None
