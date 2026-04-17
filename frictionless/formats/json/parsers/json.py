from __future__ import annotations

import json
import tempfile
from typing import Any, List

from .... import errors, types
from ....exception import FrictionlessException
from ....platform import platform
from ....resources import TableResource
from ....system import Parser, system
from ...inline import InlineControl
from ..control import JsonControl


class JsonParser(Parser):
    """JSON parser implementation."""

    requires_loader = True
    supported_types = [
        "array",
        "boolean",
        "geojson",
        "integer",
        "object",
        "string",
        "year",
    ]

    # Read

    def read_cell_stream_create(self) -> types.ICellStream:
        pass

    # Write

    def write_row_stream(self, source: TableResource):
        data: List[Any] = []
        control = JsonControl.from_dialect(self.resource.dialect)
        with source:
            if self.resource.dialect.header and not control.keyed:
                data.append(source.schema.field_names)
            for row in source.row_stream:
                cells = row.to_list(json=True)
                item = dict(zip(row.field_names, cells)) if control.keyed else cells
                data.append(item)
        with tempfile.NamedTemporaryFile("wt", delete=False) as file:
            json.dump(data, file, indent=2)
        loader = system.create_loader(self.resource)
        loader.write_byte_stream(file.name)
