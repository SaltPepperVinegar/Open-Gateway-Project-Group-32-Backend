class UserAlreadyRegisteredError(Exception):
    """Raised when a UID has already been registered via register_user."""

    def __init__(self) -> None:
        self.message = (
            "The UID has already been registered via the register_user endpoint."
        )
        super().__init__(self.message)


class UserDoesNotExistError(Exception):
    """Raised when trying to access user data which does not exist."""

    def __init__(self) -> None:
        self.message = (
            "The target user does not exist."
        )
        super().__init__(self.message)