from enum import Enum


class UserRole(str, Enum):
    """
    Workers and managers can access different scopes of API resources.
    For example, only managers can delete a disaster area.
    """

    WORKER = "worker"
    MANAGER = "manager"


class DisasterAreaStatus(str, Enum):
    """
    Active:
        The event is currently ongoing / being handled.

    Resolved:
        The event has been resolved / closed.

    Deleted:
        Soft-deleted.
        Visible only to database maintainers.
        Hidden from business-side users.
    """

    ACTIVE = "active"
    RESOLVED = "resolved"
    DELETED = "deleted"
