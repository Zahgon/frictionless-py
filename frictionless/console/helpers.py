from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Any, List, Optional

import typer
from rich.console import Console
from rich.markup import escape
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from .. import helpers
from ..checklist import Check, Checklist
from ..detector import Detector
from ..dialect import Dialect
from ..exception import FrictionlessException
from ..pipeline import Pipeline, Step
from ..platform import platform

if TYPE_CHECKING:
    from ..resource import Resource


# Source


def create_source(source: Any, *, path: Optional[str] = None) -> Any:
    # Support stdin
    pass


# Dialect


def create_dialect(
    *,
    descriptor: Optional[str] = None,
    header_rows: Optional[str] = None,
    header_join: Optional[str] = None,
    comment_char: Optional[str] = None,
    comment_rows: Optional[str] = None,
    sheet: Optional[str] = None,
    table: Optional[str] = None,
    keys: Optional[str] = None,
    keyed: Optional[bool] = None,
    csv_delimiter: Optional[str] = None,
) -> Optional[Dialect]:
    pass


# Detector


def create_detector(
    *,
    buffer_size: Optional[int] = None,
    sample_size: Optional[int] = None,
    field_type: Optional[str] = None,
    field_names: Optional[str] = None,
    field_confidence: Optional[float] = None,
    field_float_numbers: Optional[bool] = None,
    field_missing_values: Optional[str] = None,
    schema_sync: Optional[bool] = None,
) -> Detector:
    # Detector
    pass


# Checklist


def create_checklist(
    *,
    descriptor: Optional[str] = None,
    checks: Optional[str] = None,
    pick_errors: Optional[str] = None,
    skip_errors: Optional[str] = None,
):
    # Checklist
    pass


# Pipeline


def create_pipeline(
    descriptor: Optional[str] = None,
    steps: Optional[str] = None,
):
    # Pipeline
    pass


# Index


def index_resource(
    console: Console,
    *,
    resource: Resource,
    database: str,
    fast: bool = False,
    use_fallback: bool = False,
    qsv_path: Optional[str] = None,
    debug: bool = False,
) -> List[str]:
    # Ensure type
    pass


# Console


def print_success(console: Console, *, note: str, title: str = "Success") -> None:
    pass


def print_error(console: Console, *, note: str, title: str = "Error") -> None:
    pass


def print_exception(
    console: Console,
    *,
    exception: Exception,
    debug: Optional[bool] = False,
) -> None:
    pass
