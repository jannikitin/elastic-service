from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

from .mixins import LoginMixin
from .mixins import PasswordMixin


class CreateUserSchema(LoginMixin, PasswordMixin):
    email: EmailStr


class CreateServiceSchema(LoginMixin, PasswordMixin):
    email: EmailStr
    key: str


class CreateCompanySchema(BaseModel):
    company_name: str = Field(..., min_length=4, max_length=64)
    owner_id: str
