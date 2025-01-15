from .mixins import FirstAndLastNameMixin
from .mixins import LoginMixin


class UserUpdateSchema(LoginMixin, FirstAndLastNameMixin):
    name: str | None = None
    lastname: str | None = None
    email: str | None = None
    login: str | None = None
