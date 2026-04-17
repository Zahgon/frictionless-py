from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar, Dict, List, Optional, Union

import attrs
from tabulate import tabulate

from .. import settings
from ..errors import Error, ReportError
from ..exception import FrictionlessException
from ..metadata import Metadata
from . import types
from .task import ReportTask

if TYPE_CHECKING:
    from ..resource import Resource


@attrs.define(kw_only=True, repr=False)
class Report(Metadata):
    """Report representation.

    A class that stores the summary of the validation action.

    """

    name: Optional[str] = None
    """
    A short url-usable (and preferably human-readable) name.
    This MUST be lower-case and contain only alphanumeric characters
    along with “_” or “-” characters.
    """

    type: ClassVar[Union[str, None]] = None
    """
    Type of the package
    """

    title: Optional[str] = None
    """
    A human-oriented title for the Report.
    """

    description: Optional[str] = None
    """
    A brief description of the Detector.
    """

    valid: bool
    """
    Flag to specify if the data is valid or not.
    """

    stats: types.IReportStats
    """
    Additional statistics of the data as defined in Stats class.
    """

    warnings: List[str] = attrs.field(factory=list)
    """
    List of warnings raised while validating the data.
    """

    errors: List[Error] = attrs.field(factory=list)
    """
    List of errors raised while validating the data.
    """

    tasks: List[ReportTask] = attrs.field(factory=list)
    """
    List of task that were applied during data validation.
    """

    @property
    def error(self):
        """Validation error (if there is only one)"""
        pass

    @property
    def task(self):
        """Validation task (if there is only one)"""
        pass

    # Flatten

    def flatten(
        self, spec: List[str] = ["taskNumber", "rowNumber", "fieldNumber", "type"]
    ):
        """Flatten the report

        Parameters
            spec (str[]): flatten specification

        Returns:
            any[]: flatten report
        """
        pass

    # Convert

    @staticmethod
    def from_validation(
        *,
        time: float = 0,
        tasks: List[ReportTask] = [],
        errors: List[Error] = [],
        warnings: List[str] = [],
    ):
        """Create a report from a validation"""
        tasks = tasks.copy()
        errors = errors.copy()
        warnings = warnings.copy()
        error_count = len(errors) + sum(task.stats["errors"] or 0 for task in tasks)
        stats = types.IReportStats(
            tasks=len(tasks),
            errors=error_count,
            warnings=len(warnings),
            seconds=time,
        )
        return Report(
            valid=not error_count,
            stats=stats,
            warnings=warnings,
            errors=errors,
            tasks=tasks,
        )

    @staticmethod
    def from_validation_task(
        resource: Resource,
        *,
        time: float,
        labels: List[str] = [],
        errors: List[Error] = [],
        warnings: List[str] = [],
    ):
        """Create a report from a validation task"""
        errors = errors.copy()
        warnings = warnings.copy()
        task_stats = types.IReportTaskStats(
            errors=len(errors), warnings=len(warnings), seconds=time
        )
        if resource.stats.md5:
            task_stats["md5"] = resource.stats.md5
        if resource.stats.sha256:
            task_stats["sha256"] = resource.stats.sha256
        if resource.stats.bytes:
            task_stats["bytes"] = resource.stats.bytes
        if resource.stats.fields:
            task_stats["fields"] = resource.stats.fields
        if resource.stats.rows:
            task_stats["rows"] = resource.stats.rows
        report_stats = types.IReportStats(
            tasks=1,
            errors=len(errors),
            warnings=len(warnings),
            seconds=time,
        )
        return Report(
            valid=not errors,
            stats=report_stats,
            warnings=[],
            errors=[],
            tasks=[
                ReportTask(
                    valid=not errors,
                    name=resource.name,  # type: ignore
                    type=resource.type,  # type: ignore
                    place=resource.place,  # type: ignore
                    labels=labels,
                    stats=task_stats,
                    errors=errors,
                    warnings=warnings,
                )
            ],
        )

    @staticmethod
    def from_validation_reports(
        *,
        time: float,
        reports: List[Report],
    ):
        """Create a report from a set of validation reports"""
        tasks: List[ReportTask] = []
        errors: List[Error] = []
        warnings: List[str] = []
        for report in reports:
            tasks.extend(report.tasks)
            errors.extend(report.errors)
            warnings.extend(report.warnings)
        return Report.from_validation(
            time=time,
            warnings=warnings,
            errors=errors,
            tasks=tasks,
        )

    # TODO: move to ReportTask
    def to_summary(self):
        """Summary of the report

        Returns:
            str: validation report
        """
        pass

    # Metadata

    metadata_type = "report"
    metadata_Error = ReportError
    metadata_profile = {
        "type": "object",
        "required": ["valid", "stats", "warnings", "errors", "tasks"],
        "properties": {
            "name": {"type": "string", "pattern": settings.NAME_PATTERN},
            "type": {"type": "string", "pattern": settings.TYPE_PATTERN},
            "title": {"type": "string"},
            "description": {"type": "string"},
            "valid": {"type": "boolean"},
            "stats": {"type": "object"},
            "warnings": {"type": "array"},
            "errors": {"type": "array"},
            "tasks": {"type": "array"},
        },
    }

    @classmethod
    def metadata_select_property_class(cls, name: str):
        if name == "errors":
            return Error
        elif name == "tasks":
            return ReportTask

    # TODO: validate valid/errors count
