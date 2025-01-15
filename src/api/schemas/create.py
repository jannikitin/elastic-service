from pydantic import EmailStr

from .mixins import LoginMixin
from .mixins import PasswordMixin


class CreateUserSchema(LoginMixin, PasswordMixin):
    email: EmailStr


class CreateServiceSchema(LoginMixin, PasswordMixin):
    email: EmailStr
    key: str
