from deetoo.models import SQLModel


def test_db():
    expected = ["items", "unique_items", "sets", "set_items"]
    assert len(SQLModel.metadata.tables) == len(expected)
    assert all(t in SQLModel.metadata.tables for t in expected)
