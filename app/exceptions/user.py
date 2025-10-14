class UserAlreadyRegisteredError(Exception):
    """Raised when a UID has already been registered via register_user."""

    def __init__(self) -> None:
        self.message = (
            "The UID has already been registered via the register_user endpoint."
        )
        super().__init__(self.message)
