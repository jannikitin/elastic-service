from api.schemas.create import CreateCompanySchema
from database import UserOrm
from sqlalchemy.ext.asyncio import AsyncSession

from .handlers import CanDeleteUser
from .handlers import CanReadUser
from .handlers import CanRemoveAdminAccess
from .handlers import CanUpdateUser


class AuthorizationSystem:
    @staticmethod
    def can_delete(user: UserOrm, target: UserOrm):
        verificator = CanDeleteUser()
        verificator.validate(user, target)

    @staticmethod
    def can_read(user: UserOrm, target: UserOrm):
        verificator = CanReadUser()
        verificator.validate(user, target)

    @staticmethod
    def can_update(user: UserOrm, target: UserOrm):
        verificator = CanUpdateUser()
        verificator.validate(user, target)

    @staticmethod
    def can_remove_admin_access(user: UserOrm, target: UserOrm):
        verificator = CanRemoveAdminAccess()
        verificator.validate(user, target)

    @staticmethod
    def can_create_company(
        user: UserOrm, company: CreateCompanySchema, session: AsyncSession
    ):
        # is company member -> is company under user id
        pass
