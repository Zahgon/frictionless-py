from __future__ import annotations

import re
import warnings
from datetime import date, datetime, timezone
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from ...platform import platform
from ...schema import Field, Schema
from ...system import Parser
from . import settings

if TYPE_CHECKING:
    from ...resources import TableResource


class SpssParser(Parser):
    """Spss parser implementation."""

    supported_types = [
        "string",
    ]

    # Read

    def read_cell_stream_create(self):
        pass

    def __read_convert_schema(self, spss_schema: Any):
        pass

    def __read_convert_type(self, spss_type: Optional[str] = None):
        # Mapping
        pass

    # Write

    def write_row_stream(self, source: TableResource):
        sav = platform.sav_reader_writer
        warnings.filterwarnings("ignore", category=sav.SPSSIOWarning)  # type: ignore

        # Convert schema
        mapping = self.__write_convert_type()
        spss_schema = self.__write_convert_schema(source)

        # Write rows
        with sav.SavWriter(self.resource.normpath, ioUtf8=True, **spss_schema) as writer:  # type: ignore
            with source:
                for row in source.row_stream:  # type: ignore
                    cells: List[Any] = []
                    for field in source.schema.fields:  # type: ignore
                        cell = row[field.name]
                        if field.type in ["datetime", "date", "time"]:
                            if field.type == "datetime":
                                if cell.tzinfo is not None:
                                    dt = cell.astimezone(timezone.utc)
                                    cell = dt.replace(tzinfo=None)
                            if field.type == "time":
                                if cell.tzinfo is not None:
                                    dt = datetime.combine(date.min, cell)
                                    dt = dt.astimezone(timezone.utc)
                                    cell = dt.time()
                            format = settings.FORMAT_WRITE[field.type]
                            cell = cell.strftime(format).encode()
                            cell = writer.spssDateTime(cell, format)
                        elif field.type not in mapping:  # type: ignore
                            cell, _ = field.write_cell(cell)
                            cell = cell.encode("utf-8")
                        cells.append(cell)
                    writer.writerow(cells)

    def __write_convert_schema(self, source: TableResource):
        spss_schema: Dict[str, Any] = {
            "varNames": [],
            "varLabels": {},
            "varTypes": {},
            "formats": {},
        }
        with source:
            # Add fields
            sizes: Dict[str, int] = {}
            mapping = self.__write_convert_type()
            for field in source.schema.fields:
                spss_schema["varNames"].append(field.name)
                if field.title:
                    spss_schema["varLabels"][field.name] = field.title
                spss_type = mapping.get(field.type)  # type: ignore
                if spss_type:
                    spss_schema["varTypes"][field.name] = spss_type[0]
                    spss_schema["formats"][field.name] = spss_type[1]
                else:
                    sizes[field.name] = 0

            # Set string sizes
            for row in source.row_stream:
                for name in sizes.keys():
                    cell = row[name]
                    field = source.schema.get_field(name)
                    cell, _ = field.write_cell(cell)
                    size = len(cell.encode("utf-8"))
                    if size > sizes[name]:
                        sizes[name] = size
            for name, size in sizes.items():
                spss_schema["varTypes"][name] = size

        return spss_schema

    def __write_convert_type(self, type: Optional[str] = None):
        # Mapping
        mapping = {
            "integer": [0, "F10"],
            "number": [0, "F10.2"],
            "datetime": [0, "DATETIME20"],
            "date": [0, "DATE10"],
            "time": [0, "TIME8"],
            "year": [0, "F10"],
        }

        # Return type
        if type:
            return mapping.get(type)

        # Return mapping
        return mapping
