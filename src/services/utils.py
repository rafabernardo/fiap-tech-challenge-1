from datetime import datetime


def clean_cpf_to_db(cpf: str) -> str:
    return cpf.replace(".", "").replace("-", "")


def get_seconds_diff(dt: datetime) -> float:
    now = datetime.now()
    diff = now - dt
    total_seconds = diff.total_seconds()
    return total_seconds
