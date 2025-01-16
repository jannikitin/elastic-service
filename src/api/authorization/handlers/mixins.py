from database import UserOrm

from .base import ValidatorMixinInterface


class UserRelationMixin(ValidatorMixinInterface):
    def _is_self_target_operation(self, operator: UserOrm, target: UserOrm):
        if operator.id == target.id:
            return True
        return False
