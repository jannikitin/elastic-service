from .auth import AuthenticationService
from .company import CompanyService
from .user import UserService

user_service = UserService()
auth_service = AuthenticationService()
company_service = CompanyService()
