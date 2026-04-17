from __future__ import annotations

from typing import List

import typer
from rich.console import Console
from rich.table import Table

from ...helpers import to_json, to_yaml
from ...resource import Resource
from ...system import system
from .. import common, helpers
from ..console import console


@console.command(name="list")
def console_describe(
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
    # Command
    basepath: str = common.basepath,
    yaml: bool = common.yaml,
    json: bool = common.json,
    # System
    debug: bool = common.debug,
    trusted: bool = common.trusted,
    standards: str = common.standards,
):
    """
    List a data source.
    """
    pass
