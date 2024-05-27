from typing import List

import pytest
from edi867_02.segment import Bpt, Ref, ReportType, Segment
from sqlalchemy import select
from sqlalchemy.orm import Session

from domain import model
from domain.repository import import_segments


def test_import_segments(session: Session) -> None:
    ref = Ref(id="12345678910111231")
    bpt = Bpt(
        report_id="200107310001",
        report_id_bgn06="2000107300003",
        date="20000731",
        report_type=ReportType.interval_meters,
    )

    segments: List[Segment] = [
        bpt,
        ref,
    ]
    import_segments(session, segments)

    [db_ref] = session.scalars(select(model.Ref)).all()
    [db_bpt] = session.scalars(select(model.TransactionSet)).all()
    assert db_ref.ref_id == ref.id
    assert db_ref.ref_id_qualifier == ref.id_qualifier

    assert db_bpt.report_id == bpt.report_id
    assert db_bpt.report_date == bpt.date
    assert db_bpt.report_type == bpt.report_type.value


def test_import_segments_fails_if_missing_ref(session: Session) -> None:
    segments: List[Segment] = [
        Bpt(
            report_id="200107310001",
            report_id_bgn06="2000107300003",
            date="20000731",
            report_type=ReportType.interval_meters,
        )
    ]

    with pytest.raises(AssertionError):
        import_segments(session, segments)
