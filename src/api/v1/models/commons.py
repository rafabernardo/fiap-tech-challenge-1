from pydantic import BaseModel


class DeleteDocumentV1Response(BaseModel):
    deleted_document: str
