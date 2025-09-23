from enum import Enum


class UserRole(str, Enum):
    WORKER = "worker"
    MANAGER = "manager"
