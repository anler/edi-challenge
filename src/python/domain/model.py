from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column, relationship


class Base(MappedAsDataclass, DeclarativeBase):
    ...


class TransactionSet(Base):
    __tablename__ = "transaction_set"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    ref_id: Mapped[int] = mapped_column(ForeignKey("ref.id"), init=False)
    ref: Mapped["Ref"] = relationship()

    report_id: Mapped[str] = mapped_column(unique=True)
    report_type: Mapped[str]
    report_date: Mapped[str]


class Ref(Base):
    __tablename__ = "ref"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    ref_id_qualifier: Mapped[str]
    ref_id: Mapped[str] = mapped_column(unique=True)
