from __future__ import annotations

import io

from ... import types
from ...system import Loader


class BufferLoader(Loader):
    """Buffer loader implementation."""

    # Read

    def read_byte_stream_create(self):
        pass

    # Write

    def write_byte_stream_save(self, byte_stream: types.IByteStream):
        self.resource.data = byte_stream.read()
