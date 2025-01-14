import enum
from typing import TYPE_CHECKING

from database.base import Base
from database.base import created_at
from database.base import pk_uuid
from sqlalchemy import Boolean
from sqlalchemy import Enum as SaEnum
from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from utils.access_models import PortalAccess


if TYPE_CHECKING:
    from .employee import EmployeeOrm


class UserOrm(Base):
    __tablename__ = "users"

    id: Mapped[pk_uuid]
    login: Mapped[str] = mapped_column(String(32), nullable=False)
    email: Mapped[str] = mapped_column(String(256), nullable=False)
    hpass: Mapped[str] = mapped_column(String(60), nullable=False)
    registration_date: Mapped[created_at]
    access_level: Mapped[enum.Enum] = mapped_column(
        SaEnum(PortalAccess), nullable=False, default=PortalAccess.USER
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    name: Mapped[str] = mapped_column(String(256), nullable=True)
    lastname: Mapped[str] = mapped_column(String(256), nullable=True)

    __table_args__ = (
        UniqueConstraint("login", name="users_login_UK"),
        UniqueConstraint("email", name="users_email_UK"),
    )

    employee: Mapped["EmployeeOrm"] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
