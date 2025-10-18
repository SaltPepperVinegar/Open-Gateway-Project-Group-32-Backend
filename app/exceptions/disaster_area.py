class DisasterAreaDoesNotExistError(Exception):
    """Raised when trying to access disaster area data which does not exist."""

    def __init__(self) -> None:
        self.message = "The target disaster area does not exist."
        super().__init__(self.message)