import uuid
from typing import TYPE_CHECKING

from database.base import Base
from database.base import created_at
from database.base import pk_uuid
from sqlalchemy import Enum as SaEnum
from sqlalchemy import ForeignKeyConstraint
from sqlalchemy import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from utils.access_models import CompanyRole


if TYPE_CHECKING:
    from .user import UserOrm
    from .company import CompanyOrm


class EmployeeOrm(Base):
    __tablename__ = "employees"

    user_id: Mapped[pk_uuid]
    company_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=True)
    role: Mapped[CompanyRole] = mapped_column(SaEnum(CompanyRole), nullable=False)
    took_office_date: Mapped[created_at]

    __table_args__ = (
        ForeignKeyConstraint(
            ["user_id"], ["users.id"], name="employee_user_id_FK", ondelete="CASCADE"
        ),
        ForeignKeyConstraint(
            ["company_id"],
            ["companies.id"],
            name="employee_company_id_FK",
            ondelete="CASCADE",
        ),
    )

    company: Mapped["CompanyOrm"] = relationship(
        back_populates="employees", foreign_keys=[company_id]
    )
    user: Mapped["UserOrm"] = relationship(back_populates="employee")
