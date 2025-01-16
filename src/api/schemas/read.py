from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field
from utils.access_models import CompanyRole

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


class ShowNewMember(BaseModel):
    user_id: UUID
    name: str | None = None
    company_id: UUID
    role: CompanyRole
    took_office_date: datetime | None = None
