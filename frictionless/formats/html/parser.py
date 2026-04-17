from __future__ import annotations

import tempfile
from typing import TYPE_CHECKING

from ... import types
from ...platform import platform
from ...system import Parser, system
from .control import HtmlControl

if TYPE_CHECKING:
    from ...resources import TableResource


class HtmlParser(Parser):
    """HTML parser implementation."""

    requires_loader = True
    supported_types = [
        "string",
    ]

    # Read

    def read_cell_stream_create(self) -> types.ICellStream:
        pass

    # Write

    # NOTE:
    # We can rebase on pyquery for writing this html
    # It will give us an ability to support HtmlDialect
    def write_row_stream(self, source: TableResource):
        html = "<html><body><table>\n"
        with source:
            html += "<tr>"
            for name in source.schema.field_names:
                html += f"<td>{name}</td>"
            html += "</tr>\n"
            for row in source.row_stream:
                cells = row.to_list(types=self.supported_types)
                html += "<tr>"
                for cell in cells:
                    html += f"<td>{cell}</td>"
                html += "</tr>\n"
        html += "</table></body></html>"
        with tempfile.NamedTemporaryFile(
            "wt", delete=False, encoding=self.resource.encoding
        ) as file:
            file.write(html)
        loader = system.create_loader(self.resource)
        result = loader.write_byte_stream(file.name)
        return result
