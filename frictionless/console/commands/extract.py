from __future__ import annotations

import json as pyjson
from typing import TYPE_CHECKING, List, Optional

import typer
from rich.console import Console
from rich.table import Table

from ...exception import FrictionlessException
from ...helpers import stringify_csv_string
from ...platform import platform
from ...resource import Resource
from ...system import system
from .. import common, helpers
from ..console import console

if TYPE_CHECKING:
    from ... import types


DEFAULT_MAX_FIELDS = 10
DEFAULT_MAX_ROWS = 10


@console.command(name="extract")
def console_extract(
    # Resource
    source: List[str] = common.source,
    name: str = common.resource_name,
    type: str = common.type,
    path: str = common.path,
    scheme: str = common.scheme,
    format: str = common.format,
    compression: str = common.compression,
    innerpath: str = common.innerpath,
    encoding: str = common.encoding,
    schema: str = common.schema,
    basepath: str = common.basepath,
    # Dialect
    dialect: str = common.dialect,
    header_rows: str = common.header_rows,
    header_join: str = common.header_join,
    comment_char: str = common.comment_char,
    comment_rows: str = common.skip_rows,
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
    # Command
    valid: bool = common.valid_rows,
    invalid: bool = common.invalid_rows,
    limit_rows: int = common.limit_rows,
    yaml: bool = common.yaml,
    json: bool = common.json,
    csv: bool = common.csv,
    # System
    debug: bool = common.debug,
    trusted: bool = common.trusted,
    standards: str = common.standards,
    # Deprecated
    resource_name: str = common.resource_name,
    keep_delimiter: bool = common.keep_delimiter,
):
    """
    Extract rows from a data source.

    Based on the inferred data source type it will return resource or package data.
    Default output format is tabulated with a front matter. Output will be utf-8 encoded.
    """
    pass
