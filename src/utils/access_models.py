from enum import Enum


class PortalAccess(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SERVICE = "SERVICE"
