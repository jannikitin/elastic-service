import uuid
from typing import List
from typing import TYPE_CHECKING

from database.base import Base
from database.base import pk_uuid
from sqlalchemy import ForeignKeyConstraint
from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from sqlalchemy import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from .employee import EmployeeOrm


class CompanyOrm(Base):
    __tablename__ = "companies"

    id: Mapped[pk_uuid]
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    owner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)

    __table_args__ = (
        UniqueConstraint("name", name="companies_name_UK"),
        ForeignKeyConstraint(
            ["owner_id"],
            ["employees.user_id"],
            name="company_employee_owner_user_id_FK",
        ),
    )

    employees: Mapped[List["EmployeeOrm"]] = relationship(back_populates="company")
