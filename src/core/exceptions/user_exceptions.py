class UserAlreadyExistsError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class UserInvalidFormatDataError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
