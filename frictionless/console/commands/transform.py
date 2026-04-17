from __future__ import annotations

from typing import List

import typer
from rich.console import Console

from ...exception import FrictionlessException
from ...platform import platform
from ...resource import Resource
from ...system import system
from .. import common, helpers
from ..console import console


@console.command(name="transform", hidden=True)
def console_transform(
    # Source
    source: List[str] = common.source,
    path: str = common.path,
    # Pipeline
    pipeline: str = common.pipeline,
    steps: str = common.steps,
    # Command
    debug: bool = common.debug,
    trusted: bool = common.trusted,
    standards: str = common.standards,
):
    """Transform data using a provided pipeline.

    Please read more about Transform pipelines to write a pipeline
    that can be accepted by this function.
    """
    pass
