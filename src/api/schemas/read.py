from typing import Annotated
from uuid import UUID

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

from .mixins import LoginMixin


class ShowUserSchema(LoginMixin):
    id: UUID | str | None = None
    email: Annotated[EmailStr, Field(...)]
    name: str | None = None
    lastname: str | None = None


class ShowCompany(BaseModel):
    id: UUID | str | None = None
    name: str | None = None
    owner_id: UUID | str | None = None
