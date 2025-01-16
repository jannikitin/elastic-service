from abc import ABC
from abc import abstractmethod
from typing import Any

from api.exc import forbidden_exception
from database import UserOrm
from fastapi import HTTPException
from utils.access_models import PortalAccess


class ValidatorMixinInterface(ABC):
    @abstractmethod
    def _is_self_target_operation(self, operator, target):
        pass


class BaseValidator:

    _PERMISSION_TABLE: dict[PortalAccess:dict]

    def __init__(self, next_validator=None):
        self._next_validator = next_validator

    def validate(self, user: UserOrm, target: Any):
        if self._next_validator:
            self._next_validator.validate(user, target)
        return

    @property
    def _auth_exception(self) -> HTTPException:
        return forbidden_exception
