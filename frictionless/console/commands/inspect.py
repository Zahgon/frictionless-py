from __future__ import annotations

import atexit
import os
import tempfile
from typing import List

import typer
from rich.console import Console

from ...resource import Resource
from ...system import system
from .. import common, helpers
from ..console import console


# TODO: figure out how we can reduce duplication among commands like this: query/etc
@console.command(name="inspect", hidden=True)
def console_inspect(
    # Resource
    source: List[str] = common.source,
    name: str = common.resource_name,
    type: str = common.type,
    path: str = common.path,
    # System
    debug: bool = common.debug,
    trusted: bool = common.trusted,
    standards: str = common.standards,
):
    """Query data"""
    pass
