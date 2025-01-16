from database import UserOrm
from utils.access_models import PortalAccess

from .base import BaseValidator
from .mixins import UserRelationMixin


class CanDeleteUser(BaseValidator, UserRelationMixin):
    _PERMISSION_TABLE = {
        PortalAccess.SERVICE: {
            PortalAccess.USER: True,
            PortalAccess.ADMIN: True,
            PortalAccess.SERVICE: False,
        },
        PortalAccess.ADMIN: {
            PortalAccess.USER: True,
            PortalAccess.ADMIN: False,
            PortalAccess.SERVICE: False,
        },
        PortalAccess.USER: {
            PortalAccess.USER: False,
            PortalAccess.ADMIN: False,
            PortalAccess.SERVICE: False,
        },
    }

    def validate(self, user: UserOrm, target: UserOrm):
        if not super()._is_self_target_operation(user, target):
            if self._PERMISSION_TABLE[user.access_level][target.access_level]:
                return super().validate(user, target)
        raise self._auth_exception


class CanReadUser(BaseValidator, UserRelationMixin):
    _PERMISSION_TABLE = {
        PortalAccess.SERVICE: {
            PortalAccess.USER: True,
            PortalAccess.ADMIN: True,
            PortalAccess.SERVICE: True,
        },
        PortalAccess.ADMIN: {
            PortalAccess.USER: True,
            PortalAccess.ADMIN: True,
            PortalAccess.SERVICE: False,
        },
        PortalAccess.USER: {
            PortalAccess.USER: True,
            PortalAccess.ADMIN: False,
            PortalAccess.SERVICE: False,
        },
    }

    def validate(self, user: UserOrm, target: UserOrm):
        if super()._is_self_target_operation(user, target):
            if self._PERMISSION_TABLE[user.access_level][target.access_level]:
                return super().validate(user, target)
        raise self._auth_exception


class CanUpdateUser(BaseValidator, UserRelationMixin):
    _PERMISSION_TABLE = {
        PortalAccess.SERVICE: {
            PortalAccess.USER: True,
            PortalAccess.ADMIN: True,
            PortalAccess.SERVICE: True,
        },
        PortalAccess.ADMIN: {
            PortalAccess.USER: True,
            PortalAccess.ADMIN: False,
            PortalAccess.SERVICE: False,
        },
        PortalAccess.USER: {
            PortalAccess.USER: False,
            PortalAccess.ADMIN: False,
            PortalAccess.SERVICE: False,
        },
    }

    def validate(self, user: UserOrm, target: UserOrm):
        if not self._is_self_target_operation(user, target):
            if self._PERMISSION_TABLE[user.access_level][target.access_level] is False:
                raise self._auth_exception

        return super().validate(user, target)


class CanRemoveAdminAccess(BaseValidator, UserRelationMixin):

    _PERMISSION_TABLE = {
        PortalAccess.SERVICE: {
            PortalAccess.USER: True,
            PortalAccess.ADMIN: True,
            PortalAccess.SERVICE: False,
        },
        PortalAccess.ADMIN: {
            PortalAccess.USER: True,
            PortalAccess.ADMIN: False,
            PortalAccess.SERVICE: False,
        },
        PortalAccess.USER: {
            PortalAccess.USER: False,
            PortalAccess.ADMIN: False,
            PortalAccess.SERVICE: False,
        },
    }

    def validate(self, user: UserOrm, target: UserOrm):
        if self._is_self_target_operation(user, target):
            raise self._auth_exception
        if self._PERMISSION_TABLE[user.access_level][target.access_level] is False:
            raise self._auth_exception
        return super().validate(user, target)
