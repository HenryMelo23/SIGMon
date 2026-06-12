class BusinessError(Exception):
    pass


def require_fields(data, fields):
    missing = [field for field in fields if not data.get(field)]
    if missing:
        raise BusinessError(f"Preencha os campos obrigatórios: {', '.join(missing)}")
