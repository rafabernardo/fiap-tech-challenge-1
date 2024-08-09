class NoDocumentsFoundException(Exception):
    def __init__(self, message: str = "No document found"):
        self.message = message
        super().__init__(self.message)


class DataConflictException(Exception):
    def __init__(self, message: str = "Data conflict"):
        self.message = message
        super().__init__(self.message)
