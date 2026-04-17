from __future__ import annotations

import atexit
import os
import re
import tempfile
from typing import List

import typer
from rich.console import Console

from ...helpers import write_file
from ...resource import Resource
from ...system import system
from .. import common, helpers
from ..console import console


@console.command(name="script")
def console_script(
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
    """Script data"""
    pass


# Internal


def generate_startup(database: str, *, names: List[str]) -> str:
    pass


def generate_dfname(name: str) -> str:
    pass
