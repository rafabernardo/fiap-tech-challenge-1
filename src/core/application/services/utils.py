def clean_cpf_to_db(cpf: str) -> str:
    return cpf.replace(".", "").replace("-", "")
