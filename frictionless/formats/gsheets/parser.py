from __future__ import annotations

import re
from typing import Any, List

from ... import errors, types
from ...exception import FrictionlessException
from ...platform import platform
from ...resources import TableResource
from ...system import Parser
from .control import GsheetsControl


class GsheetsParser(Parser):
    """Google Sheets parser implementation."""

    supported_types = [
        "string",
    ]

    # Read

    def read_cell_stream_create(self) -> types.ICellStream:
        pass

    # Write

    def write_row_stream(self, source: TableResource):
        assert self.resource.normpath
        path = self.resource.normpath
        control = GsheetsControl.from_dialect(self.resource.dialect)
        match = re.search(r".*/d/(?P<key>[^/]+)/.*?(?:gid=(?P<gid>\d+))?$", path)
        if not match:
            error = errors.FormatError(note=f"Cannot save {path}")
            raise FrictionlessException(error)
        key = match.group("key")
        gid = match.group("gid")
        gc = platform.pygsheets.authorize(service_account_file=control.credentials)
        sh = gc.open_by_key(key)
        wks = sh.worksheet_by_id(gid) if gid else sh[0]  # type: ignore
        data: List[Any] = []
        with source:
            data.append(source.schema.field_names)
            for row in source.row_stream:
                data.append(row.to_list())
        wks.update_values("A1", data)  # type: ignore
        return path
