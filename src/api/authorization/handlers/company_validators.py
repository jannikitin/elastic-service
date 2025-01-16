from database import CompanyOrm
from database import UserOrm
from utils.access_models import PortalAccess

from .base import BaseValidator


class CanReadCompany(BaseValidator):

    _PERMISSION_TABLE = {
        PortalAccess.SERVICE: True,
        PortalAccess.ADMIN: True,
        PortalAccess.USER: False,
    }

    def __init__(self):
        super().__init__(IsCompanyMember())

    def validate(self, user: UserOrm, target: CompanyOrm):
        if not self._PERMISSION_TABLE[user.access_level]:
            return super().validate(user, target)


class IsCompanyMember(BaseValidator):
    def validate(self, user: UserOrm, target: CompanyOrm):
        if user.employee:
            if user.employee.company_id == target.id:
                return super().validate(user, target)
        raise self._auth_exception
