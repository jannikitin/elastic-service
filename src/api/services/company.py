from typing import Type

from api.schemas.create import CreateCompanySchema
from database import CompanyOrm
from database import EmployeeOrm
from database import UserOrm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from utils.access_models import CompanyRole


class CompanyService:
    async def register_company(
        self, company_schema: CreateCompanySchema, user: UserOrm, session: AsyncSession
    ) -> CompanyOrm:
        async with session.begin():

            company = CompanyOrm(
                name=company_schema.company_name,
                owner_id=user.id,
            )
            owner = EmployeeOrm(role=CompanyRole.OWNER)

            owner.user = user
            session.add(owner)
            await session.flush()

            company.owner = owner
            owner.company = company
            session.add(company)
            await session.flush()
        return company

    async def get_company_by_id(
        self, company_id: str, session: AsyncSession
    ) -> Type[CompanyOrm]:
        async with session.begin():
            company = await session.get(CompanyOrm, company_id)
            return company

    async def get_company_member(self):
        pass

    async def get_employee_by_user_id(
        self, user_id: str, session: AsyncSession
    ) -> str | None:
        async with session.begin():
            q = select(EmployeeOrm).filter(EmployeeOrm.user_id == user_id)
            res = await session.execute(q)
            return res.scalar()
