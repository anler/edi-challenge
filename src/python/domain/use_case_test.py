from unittest import mock

from edi867_02.parser import TransactionParser
from sqlalchemy.orm import Session, sessionmaker

from domain.use_case import ImportTexasEdi867_02


def test_ImportTexasEdi867_02(Session: sessionmaker[Session]) -> None:
    edi = ["ST~867~0001", "BPT~52~200107310001~20000731~C1~~~~~2000107300003", "REF~Q5~~12345678910111231"]
    transaction = TransactionParser().parse(iter(edi))
    use_case = ImportTexasEdi867_02(Session)
    with mock.patch("domain.use_case.import_segments") as repository:
        use_case.execute(edi)

    repository.assert_called_once_with(mock.ANY, transaction)
