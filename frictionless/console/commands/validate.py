from __future__ import annotations

from typing import List

import typer
from rich.console import Console
from rich.table import Table

from ...resource import Resource
from ...system import system
from .. import common, helpers
from ..console import console


@console.command(name="validate")
def console_validate(
    # Source
    source: List[str] = common.source,
    name: str = common.resource_name,
    type: str = common.type,
    path: str = common.path,
    scheme: str = common.scheme,
    format: str = common.format,
    encoding: str = common.encoding,
    innerpath: str = common.innerpath,
    compression: str = common.compression,
    schema: str = common.schema,
    hash: str = common.hash,
    bytes: int = common.bytes,
    fields: int = common.fields,
    rows: int = common.rows,
    basepath: str = common.basepath,
    # Dialect
    dialect: str = common.dialect,
    header_rows: str = common.header_rows,
    header_join: str = common.header_join,
    comment_char: str = common.comment_char,
    comment_rows: str = common.comment_rows,
    sheet: str = common.sheet,
    table: str = common.table,
    keys: str = common.keys,
    keyed: bool = common.keyed,
    # Detector
    buffer_size: int = common.buffer_size,
    sample_size: int = common.sample_size,
    field_type: str = common.field_type,
    field_names: str = common.field_names,
    field_confidence: float = common.field_confidence,
    field_float_numbers: bool = common.field_float_numbers,
    field_missing_values: str = common.field_missing_values,
    schema_sync: bool = common.schema_sync,
    # Checklist
    checklist: str = common.checklist,
    checks: str = common.checks,
    pick_errors: str = common.pick_errors,
    skip_errors: str = common.skip_errors,
    # Command
    parallel: bool = common.parallel,
    limit_rows: int = common.limit_rows,
    limit_errors: int = common.limit_errors,
    yaml: bool = common.yaml,
    json: bool = common.json,
    debug: bool = common.debug,
    trusted: bool = common.trusted,
    standards: str = common.standards,
    # Deprecated
    resource_name: str = common.resource_name,
):
    """
    Validate a data source.

    Based on the inferred data source type it will validate resource or package.
    Default output format is YAML with a front matter.
    """
    pass
