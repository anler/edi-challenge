from enum import Enum
from typing import Annotated, Literal

from pydantic import AfterValidator, BaseModel

from .validators import validate_alnum, validate_date

TransferAndResaleReport = Literal["867"]
HistoricalMeterReading = Literal["52"]
ElectricServiceProvider = Literal["Q5"]

Date = Annotated[str, AfterValidator(validate_date)]
Alnum = Annotated[str, AfterValidator(validate_alnum)]


class ReportType(Enum):
    interval_meters = "C1"
    non_interval_metered_unmetered = "DD"
    mixed = "DR"


class St(BaseModel):
    segment: Literal["ST"] = "ST"
    id_code: TransferAndResaleReport = "867"
    control_number: str


class Bpt(BaseModel):
    segment: Literal["BPT"] = "BPT"
    purpose_code: HistoricalMeterReading = "52"
    report_id: Alnum
    report_id_bgn06: str
    date: Date
    report_type: ReportType


class Ref(BaseModel):
    segment: Literal["REF"] = "REF"
    id_qualifier: ElectricServiceProvider = "Q5"
    id: Alnum


Segment = St | Bpt | Ref
