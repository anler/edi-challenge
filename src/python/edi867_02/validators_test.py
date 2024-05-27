import pytest

from .validators import validate_alnum, validate_date


def test_validate_alnum_ok() -> None:
    assert validate_alnum("abc1234") == "ABC1234"


def test_validate_alnum_not_empty() -> None:
    with pytest.raises(ValueError):
        validate_alnum("")


def test_validate_alnum_not_alnum() -> None:
    with pytest.raises(ValueError):
        validate_alnum("~")


def test_validate_date_ok() -> None:
    assert validate_date("20081111") == "20081111"


def test_validate_date_not_ok() -> None:
    with pytest.raises(ValueError):
        validate_date("20081311")
