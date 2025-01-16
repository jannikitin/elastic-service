from database import EmployeeOrm

from .base import BaseValidator


class IsCompanyMemberValidator(BaseValidator):
    def validate(self, user: EmployeeOrm, **kwargs):
        pass
