from folio_db.migration_filters import include_name
from folio_db.tables import metadata


def test_naming_convention_has_standard_keys() -> None:
    assert set(metadata.naming_convention) == {"ix", "uq", "ck", "fk", "pk"}


def test_include_name_excludes_langgraph_schema() -> None:
    assert include_name("langgraph", "schema", {}) is False


def test_include_name_keeps_other_schemas() -> None:
    assert include_name("public", "schema", {}) is True
    assert include_name(None, "schema", {}) is True


def test_include_name_excludes_tables_inside_langgraph_schema() -> None:
    assert include_name("checkpoints", "table", {"schema_name": "langgraph"}) is False
    assert include_name("papers", "table", {"schema_name": None}) is True
