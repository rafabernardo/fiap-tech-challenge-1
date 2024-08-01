import copy
from datetime import datetime


def replace_id_key(document: dict):
    data = copy.deepcopy(document)
    if "_id" in data:
        data["id"] = str(data.pop("_id"))
    return data


def prepare_document_to_db(document: dict):
    data = copy.deepcopy(document)
    now = datetime.now()

    data.pop("id", None)
    data["updated_at"] = now
    if data.get("created_at") is None:
        data["created_at"] = now
    return data
