from fastapi import HTTPException, status


class NoDocumentsFoundException(HTTPException):
    def __init__(self, detail: str = "No document found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class InternalServerErrorException(HTTPException):
    def __init__(self, detail: str = "Internal server error"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
        )
