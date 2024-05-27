import pytest
from pydantic import ValidationError

from edi867_02.segment import Bpt, Ref, ReportType, St

from .parser import BptParser, RefParser, StParser


def test_parse_bpt_ok() -> None:
    assert BptParser().parse(iter(["BPT~52~200107310001~20000731~C1~~~~~2000107300003"])) == [
        Bpt(
            report_id="200107310001",
            report_id_bgn06="2000107300003",
            date="20000731",
            report_type=ReportType.interval_meters,
        )
    ]


def test_parse_invalid_bpt() -> None:
    parser = BptParser()
    with pytest.raises(ValueError):
        parser.parse(iter([""]))

    with pytest.raises(ValidationError):
        parser.parse(iter(["xxx~52~200107310001~20000731~C1~~~~~2000107300003"]))

    with pytest.raises(ValidationError):
        parser.parse(iter(["BPT~02~200107310001~20000731~C1~~~~~2000107300003"]))


def test_parse_st_ok() -> None:
    assert StParser().parse(iter(["ST~867~0001"])) == [St(control_number="0001")]


def test_parse_invalid_st() -> None:
    parser = StParser()
    with pytest.raises(ValueError):
        parser.parse(iter([""]))

    with pytest.raises(ValidationError):
        parser.parse(iter(["xxx~867~0001"]))

    with pytest.raises(ValidationError):
        parser.parse(iter(["ST~008~0001"]))


def test_parse_ref_ok() -> None:
    assert RefParser().parse(iter(["REF~Q5~~12345678910111231"])) == [Ref(id="12345678910111231")]


def test_parse_invalid_ref() -> None:
    parser = RefParser()
    with pytest.raises(ValueError):
        parser.parse(iter([""]))

    with pytest.raises(ValidationError):
        parser.parse(iter(["xxx~Q5~~12345678910111231"]))

    with pytest.raises(ValidationError):
        parser.parse(iter(["REF~05~~12345678910111231"]))
