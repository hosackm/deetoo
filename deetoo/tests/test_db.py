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
    tables = get_database(database_file).tables()
    assert len(tables) == 1
    assert tables.pop() == "base_items"


def test_read_tables_with(database_file):
    with db_context(database_file) as db:
        tables = db.tables()
        assert len(tables) == 1
        assert tables.pop() == "base_items"
