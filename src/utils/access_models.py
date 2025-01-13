from enum import Enum


class PortalAccess(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SERVICE = "SERVICE"


class CompanyRole(str, Enum):
    OWNER = "OWNER"
    HR = "HR"
    MASTER_MENTOR = "MASTER_MENTOR"
    MENTOR = "MENTOR"
