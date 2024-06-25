from rolepermissions.roles import AbstractUserRole

from tools.project.common.constants.model_cons import UserRoleChoice


class Customer(AbstractUserRole):
    role_name = UserRoleChoice.CUSTOMER
    available_permissions = {
        "message_exchange": True,
    }


class Admin(AbstractUserRole):
    role_name = UserRoleChoice.ADMIN
    available_permissions = {
        "portal_verification_login": True,
    }
