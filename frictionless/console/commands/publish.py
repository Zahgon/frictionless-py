from __future__ import annotations

from typing import List

import typer
from rich.console import Console
from rich.progress import track
from rich.prompt import Prompt

from ...exception import FrictionlessException
from ...package import Package
from ...platform import platform
from ...resource import Resource
from ...system import system
from .. import common, helpers
from ..console import console


@console.command(name="publish")
def console_publish(
    # Resource
    source: List[str] = common.source,
    name: str = common.resource_name,
    type: str = common.type,
    path: str = common.path,
    # Command
    target: str = typer.Option(default=...),
    title: str = typer.Option(default=None),
    # System
    debug: bool = common.debug,
    trusted: bool = common.trusted,
    standards: str = common.standards,
):
    """Script data"""
    pass
