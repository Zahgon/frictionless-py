from __future__ import annotations

import os
from typing import List

import typer
from rich.console import Console

from ...resource import Resource
from ...system import system
from .. import common, helpers
from ..console import console


@console.command(name="explore")
def console_explore(
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
    """Explore dataset with Visidata

    Please read the commands reference:
    - https://www.visidata.org/man/
    """
    pass
