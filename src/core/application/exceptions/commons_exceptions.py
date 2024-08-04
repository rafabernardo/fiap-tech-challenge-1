class NoDocumentsFoundException(Exception):
    def __init__(self, message: str = "No document found"):
        self.message = message
        super().__init__(self.message)
