from datetime import datetime


def validate_date(value: str) -> str:
    datetime.strptime(value, "%Y%m%d")
    return value


def validate_alnum(value: str) -> str:
    if value.isalnum():
        return value.upper()
    raise ValueError("Invalid value, expected alphanumeric.")
