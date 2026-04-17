import typer

from ...checklist import Checklist
from ...detector import Detector
from ...dialect import Dialect
from ...inquiry import Inquiry
from ...package import Package
from ...pipeline import Pipeline
from ...report import Report
from ...resource import Resource
from ...schema import Schema
from ...system import system
from .. import common
from ..console import console


@console.command(name="convert", hidden=True)
def console_convert(
    # Source
    source: str = common.source,
    # Command
    path: str = common.output_path,
    json: bool = common.json,
    yaml: bool = common.yaml,
    er_diagram: bool = common.er_diagram,
    markdown: bool = common.markdown,
    debug: bool = common.debug,
    trusted: bool = common.trusted,
    standards: str = common.standards,
):
    """Convert metadata to various output"""
    pass
