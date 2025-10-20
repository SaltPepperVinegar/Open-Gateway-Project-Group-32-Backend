class InvalidObjectIDStringError(Exception):
    """Raised when a string cannot be converted into ObjectID."""

    def __init__(self) -> None:
        self.message = "Provided string cannot be converted into an ObjectID."
        super().__init__(self.message)
