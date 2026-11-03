from collections.abc import MutableMapping
from typing import Literal

INCLUDED_SCHEMAS = frozenset({None, "public"})
SCHEMA_KEY = "schema_name"

type NameType = Literal[
    "schema",
    "table",
    "column",
    "index",
    "unique_constraint",
    "foreign_key_constraint",
    "check_constraint",
]
type ParentKey = Literal["schema_name", "table_name", "schema_qualified_table_name"]
type ParentNames = MutableMapping[ParentKey, str | None]


def include_name(name: str | None, type_: NameType, parent_names: ParentNames) -> bool:
    if type_ == "schema":
        return name in INCLUDED_SCHEMAS
    return parent_names.get(SCHEMA_KEY) in INCLUDED_SCHEMAS
