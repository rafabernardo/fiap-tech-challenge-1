from fastapi import HTTPException


class NoDocumentsFoundException(HTTPException):
    def __init__(self, detail: str = "No document found"):
        super().__init__(status_code=404, detail=detail)
