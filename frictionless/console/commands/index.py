from __future__ import annotations

from typing import List

import typer
from rich.console import Console

from ...resource import Resource
from ...system import system
from .. import common, helpers
from ..console import console


@console.command(name="index")
def console_index(
    # Resource
    source: List[str] = common.source,
    name: str = common.resource_name,
    type: str = common.type,
    path: str = common.path,
    # Command
    database: str = common.required_database,
    fast: bool = common.fast,
    fallback: bool = common.fallback,
    qsv: str = common.qsv,
    # System
    debug: bool = common.debug,
    trusted: bool = common.trusted,
    standards: str = common.standards,
):
    """Index a tabular data resource"""
    pass
