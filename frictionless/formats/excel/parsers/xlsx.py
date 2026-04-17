from __future__ import annotations

import atexit
import datetime
import hashlib
import os
import shutil
import tempfile
import warnings
from itertools import chain
from typing import TYPE_CHECKING, Any, List

from .... import errors
from ....exception import FrictionlessException
from ....platform import platform
from ....resource import Resource
from ....system import Parser, system
from .. import settings
from ..control import ExcelControl

if TYPE_CHECKING:
    from ....resources import TableResource


class XlsxParser(Parser):
    """XLSX parser implementation."""

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

    def read_loader(self):
        pass

    def read_cell_stream_create(self):
        pass

    # Write

    def write_row_stream(self, source: TableResource):
        control = ExcelControl.from_dialect(self.resource.dialect)
        book = platform.openpyxl.Workbook(write_only=True)
        title = control.sheet
        if isinstance(title, int):
            title = f"Sheet {control.sheet}"
        sheet = book.create_sheet(title)
        with source:
            if self.resource.dialect.header:
                sheet.append(source.schema.field_names)
            for row in source.row_stream:
                cells = row.to_list(types=self.supported_types)
                sheet.append(cells)
        file = tempfile.NamedTemporaryFile(delete=False)
        file.close()
        book.save(file.name)
        loader = system.create_loader(self.resource)
        loader.write_byte_stream(file.name)


# Internal


def extract_row_values(
    row: List[Any],
    preserve_formatting: bool = False,
    adjust_floating_point_error: bool = False,
    stringified: bool = False,
):
    pass


def convert_excel_number_format_string(excel_number: str, value: Any):
    # A basic attempt to convert excel number_format to a number string
    # The important goal here is to get proper amount of rounding
    pass


def convert_excel_date_format_string(excel_date: str):
    # Created using documentation here:
    # https://support.office.com/en-us/article/review-guidelines-for-customizing-a-number-format-c0a1d1fa-d3f4-4018-96b7-9c9354dd99f5

    # The python date string that is being built
    pass
