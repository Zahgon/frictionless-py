from __future__ import annotations

from typing import List

import typer
from rich.console import Console
from rich.progress import track

from ...exception import FrictionlessException
from ...platform import platform
from ...resource import Resource
from ...system import system
from .. import common, helpers
from ..console import console


@console.command(name="convert")
def console_convert(
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
    # Command
    to_path: str = common.path,
    to_format: str = common.format,
    to_dialect: str = common.dialect,
    to_csv_delimiter: str = typer.Option(default=None),
    # System
    debug: bool = common.debug,
    trusted: bool = common.trusted,
    standards: str = common.standards,
):
    """
    Convert data table
    """
    pass
