import pytest
from pathlib import Path
from tempfile import TemporaryDirectory

from deetoo.data.generate import write_database
from deetoo.models.db import get_database, db_context


@pytest.fixture
def tmpdir():
    tempdir = TemporaryDirectory()
    yield tempdir.name


@pytest.fixture
def database_file(tmpdir):
    filepath = Path(tmpdir) / "test.json"
    write_database(filepath)
    yield filepath


def test_db_generate_creates_tables(database_file):
    assert len(get_database(database_file).tables()) == 9


def test_read_tables_with(database_file):
    with db_context(database_file) as db:
        assert len(db.tables()) == 9
