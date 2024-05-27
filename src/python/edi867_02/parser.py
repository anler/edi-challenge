from abc import ABC
from typing import Collection, Iterator, List, Literal, TypeAlias, TypeVar

from . import segment

T = TypeVar("T")
Delim: TypeAlias = Literal["*", "|", "~"]


class SegmentParser(ABC):
    fields: Collection[Collection[str]]
    model: type[segment.Segment]

    def parse(self, lines: Iterator[str], delim: Delim = "~") -> List[segment.Segment]:
        line = next(lines)
        values = [value.strip() for value in line.split(delim)]
        for fields in self.fields:
            if len(values) == len(fields):
                return [self.model.model_validate(dict(zip(fields, values, strict=True)))]

        raise ValueError(f"Couldn't match segment fields. Expected {self.fields!r}. Got {values!r}")


class StParser(SegmentParser):
    model = segment.St
    fields = [["segment", "id_code", "control_number"]]


class BptParser(SegmentParser):
    model = segment.Bpt
    fields = [["segment", "purpose_code", "report_id", "date", "report_type", "", "", "", "", "report_id_bgn06"]]


class RefParser(SegmentParser):
    model = segment.Ref
    fields = [["segment", "id_qualifier", "", "id"]]


class TransactionParser(SegmentParser):
    def parse(self, lines: Iterator[str], delim: Delim = "~") -> List[segment.Segment]:
        # Heading
        while True:
            try:
                [st] = StParser().parse(lines)
            except ValueError:
                continue
            else:
                break

        [bpt] = BptParser().parse(lines)
        [ref] = RefParser().parse(lines)

        return [st, bpt, ref]
