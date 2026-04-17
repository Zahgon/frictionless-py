from __future__ import annotations

import os

from ... import errors, types
from ...exception import FrictionlessException
from ...system import Loader


class StreamLoader(Loader):
    """Stream loader implementation."""

    # Read

    def read_byte_stream_create(self):  # type: ignore
        pass

    # Write

    def write_byte_stream_save(self, byte_stream: types.IByteStream):
        self.resource.data = byte_stream


# Internal


class ReusableByteStream:
    def __init__(self, byte_stream: types.IByteStream):
        self.__byte_stream = byte_stream

    def __getattr__(self, name: str):
        return getattr(self.__byte_stream, name)

    def read(self, size: int = -1):
        if self.__byte_stream.closed:
            try:
                self.__byte_stream = open(self.__byte_stream.name, "rb")
            except Exception:
                note = "cannot re-open a byte stream: {self.__byte_stream}"
                raise FrictionlessException(errors.SchemeError(note=note))
        return self.__byte_stream.read(size)
