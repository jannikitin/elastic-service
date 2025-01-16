from database import EmployeeOrm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CompanyService:
    async def register_company(self):
        pass

    async def get_company_member(self):
        pass

    async def get_employee_company_id(
        self, user_id: str, session: AsyncSession
    ) -> str | None:
        q = select(EmployeeOrm.company_id).filter(EmployeeOrm.user_id == user_id)
        res = await session.execute(q)
        if res:
            return res.one()[0]
