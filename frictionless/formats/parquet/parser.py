from __future__ import annotations

from ... import types
from ...platform import platform
from ...resources import TableResource
from ...system import Parser
from .control import ParquetControl


class ParquetParser(Parser):
    """Parquet parser implementation."""

    supported_types = [
        "array",
        "boolean",
        "datetime",
        "date",
        "duration",
        "integer",
        "number",
        "object",
        "string",
        "time",
    ]

    # Read

    def read_cell_stream_create(self) -> types.ICellStream:
        pass

    # Write

    def write_row_stream(self, source: TableResource):
        import pyarrow as pa  # type: ignore[reportMissingTypeStubs]

        pq = platform.pyarrow_parquet
        df = source.to_pandas()
        table = pa.Table.from_pandas(df)  # type: ignore[reportUnknownMemberType]
        pq.write_table(table, self.resource.normpath)
