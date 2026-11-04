from folio_db.migration_filters import include_name
from folio_db.tables import metadata


def test_naming_convention_has_standard_keys() -> None:
    assert set(metadata.naming_convention) == {"ix", "uq", "ck", "fk", "pk"}


def test_include_name_keeps_default_schema() -> None:
    assert include_name(None, "schema", {}) is True
    assert include_name("public", "schema", {}) is True


def test_include_name_excludes_langgraph_schema() -> None:
    assert include_name("langgraph", "schema", {}) is False


def test_include_name_excludes_paradedb_schema() -> None:
    assert include_name("paradedb", "schema", {}) is False


def test_include_name_excludes_every_unknown_schema() -> None:
    assert include_name("anything_else", "schema", {}) is False


def test_include_name_excludes_objects_inside_other_schemas() -> None:
    assert include_name("checkpoints", "table", {"schema_name": "langgraph"}) is False
    assert include_name("bm25_idx", "index", {"schema_name": "paradedb"}) is False


def test_include_name_keeps_objects_in_default_schema() -> None:
    assert include_name("filings", "table", {"schema_name": None}) is True
    assert include_name("filings", "table", {"schema_name": "public"}) is True
