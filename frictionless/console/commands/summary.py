from __future__ import annotations

import typer

from ...resource import Resource
from ...system import system
from .. import common
from ..console import console


@console.command(name="summary", hidden=True)
def console_summary(
    source: str = common.source,
    # Command
    debug: bool = common.debug,
    trusted: bool = common.trusted,
    standards: str = common.standards,
):
    """Summary of data source.

    It will return schema, sample of the data and validation report for the resource.
    """
    pass
