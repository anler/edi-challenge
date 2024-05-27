from typing import List

from edi867_02.segment import Bpt, Ref, Segment, St
from sqlalchemy import select
from sqlalchemy.orm import Session

from . import model


def import_segments(session: Session, segments: List[Segment]) -> None:
    ref_segment = None
    bpt_segment = None

    for segment in segments:
        match segment:
            case Ref() as ref_segment_:
                ref_segment = ref_segment_
            case Bpt() as bpt_segment_:
                bpt_segment = bpt_segment_
            case St():
                pass

    assert ref_segment, "Unexpectedly None"
    assert bpt_segment, "Unexpectedly None"

    ref = session.scalars(select(model.Ref).where(model.Ref.ref_id == ref_segment.id)).one_or_none()
    if ref is None:
        ref = model.Ref(ref_id_qualifier=ref_segment.id_qualifier, ref_id=ref_segment.id)

    transaction_set = model.TransactionSet(
        ref=ref,
        report_id=bpt_segment.report_id,
        report_date=bpt_segment.date,
        report_type=bpt_segment.report_type.value,
    )

    session.add(transaction_set)
