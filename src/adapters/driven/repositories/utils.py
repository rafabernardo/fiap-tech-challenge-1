def replace_id_key(data: dict):
    if "_id" in data:
        data["id"] = str(data.pop("_id"))
