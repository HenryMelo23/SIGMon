from datetime import date, datetime


def parse_date(value) -> date:
    if isinstance(value, date):
        return value
    return datetime.strptime(value, "%Y-%m-%d").date()


def hoje() -> date:
    return date.today()


def data_entre(inicio: str, fim: str) -> bool:
    atual = hoje()
    return parse_date(inicio) <= atual <= parse_date(fim)
