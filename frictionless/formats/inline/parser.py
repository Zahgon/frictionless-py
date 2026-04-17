from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

from ... import errors
from ...exception import FrictionlessException
from ...system import Parser
from .control import InlineControl

if TYPE_CHECKING:
    from ...resources import TableResource


class InlineParser(Parser):
    """Inline parser implementation."""

    supported_types = [
        "array",
        "boolean",
        "date",
        "datetime",
        "duration",
        "geojson",
        "geopoint",
        "integer",
        "number",
        "object",
        "string",
        "time",
        "year",
        "yearmonth",
    ]

    # Read

    def read_cell_stream_create(self):  # type: ignore
        pass

    # Write

    def write_row_stream(self, source: TableResource):
        data: List[Any] = []
        control = InlineControl.from_dialect(self.resource.dialect)
        with source:
            if self.resource.dialect.header and not control.keyed:
                data.append(source.schema.field_names)
            for row in source.row_stream:
                item = row.to_dict() if control.keyed else row.to_list()
                data.append(item)
        self.resource.data = data
