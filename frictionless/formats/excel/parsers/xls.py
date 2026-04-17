from __future__ import annotations

import sys
import tempfile
from typing import TYPE_CHECKING, Any, List

from .... import errors
from ....exception import FrictionlessException
from ....platform import platform
from ....system import Parser, system
from ..control import ExcelControl

if TYPE_CHECKING:
    from ....resources import TableResource


# TODO: support ExcelControl.stringified


class XlsParser(Parser):
    """XLS parser implementation."""

    requires_loader = True
    supported_types = [
        "boolean",
        "date",
        "datetime",
        "integer",
        "number",
        "string",
        "time",
        "year",
    ]

    # Read

    def read_cell_stream_create(self):
        pass

    # Write

    def write_row_stream(self, source: TableResource):
        control = ExcelControl.from_dialect(self.resource.dialect)
        book = platform.xlwt.Workbook()
        title = control.sheet
        if isinstance(title, int):
            title = f"Sheet {control.sheet}"
        sheet = book.add_sheet(title)
        with source:
            if self.resource.dialect.header:
                for field_index, name in enumerate(source.schema.field_names):
                    sheet.write(0, field_index, name)
            for index, row in enumerate(source.row_stream):
                row_index = index + 1 if self.resource.dialect.header else index
                cells = row.to_list(types=self.supported_types)
                for field_index, cell in enumerate(cells):
                    sheet.write(row_index, field_index, cell)
        file = tempfile.NamedTemporaryFile(delete=False)
        file.close()
        book.save(file.name)
        loader = system.create_loader(self.resource)
        loader.write_byte_stream(file.name)
