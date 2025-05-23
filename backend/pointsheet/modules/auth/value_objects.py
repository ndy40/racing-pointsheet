from enum import Enum


class UserRole(str, Enum):
    driver = "driver"
    admin = "admin"
