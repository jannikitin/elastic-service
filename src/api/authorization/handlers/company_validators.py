from database import CompanyOrm
from database import UserOrm
from utils.access_models import CompanyRole
from utils.access_models import PortalAccess

from .base import BaseValidator


class CanPerform(BaseValidator):

    _PERMISSION_TABLE = {
        PortalAccess.SERVICE: True,
        PortalAccess.ADMIN: True,
        PortalAccess.USER: False,
    }

    def validate(self, user: UserOrm, **kwargs):
        if not self._PERMISSION_TABLE[user.access_level]:
            return super().validate(user, **kwargs)


class IsEmployee(BaseValidator):
    def validate(self, user: UserOrm, **kwargs):
        if not user.employee:
            raise self._auth_exception
        return super().validate(user, **kwargs)


class IsCompanyMember(BaseValidator):
    def validate(self, user: UserOrm, target: CompanyOrm):
        if user.employee.company_id == target.id:
            return super().validate(user, target)
        raise self._auth_exception


class CanInvite(BaseValidator):
    def validate(self, user: UserOrm, target: CompanyOrm):
        if user.employee.role not in {CompanyRole.OWNER, CompanyRole.HR}:
            raise self._auth_exception
        return super().validate(user, target)
