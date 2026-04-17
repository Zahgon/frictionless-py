from __future__ import annotations

import atexit
import hashlib
import io
import os
import shutil
import tempfile
from typing import TYPE_CHECKING, Any, Optional, cast

from .. import errors, settings
from ..exception import FrictionlessException
from ..platform import platform

if TYPE_CHECKING:
    from .. import types
    from ..resource import Resource


# NOTE:
# Probably we need to rework the way we calculate stats
# First of all, it's not really reliable as read/read1(size) can be called many times
# Secondly, for now, we stream compressed files twice (see loader.read_byte_stream_decompress)
# Although, we need to review how we collect buffer - cab it be less IO operations?


# TODO: migrate to dataclass?
class Loader:
    """Loader representation

    Parameters:
        resource (Resource): resource

    """

    remote: bool = False
    """
    Specifies if the resource is remote.
    """

    def __init__(self, resource: Resource):
        self.__resource: Resource = resource
        self.__buffer: Optional[types.IBuffer] = None
        self.__byte_stream: Optional[types.IByteStream] = None
        self.__text_stream: Optional[types.ITextStream] = None

    def __enter__(self):
        if self.closed:
            self.open()
        return self

    def __exit__(self, type, value, traceback):  # type: ignore
        self.close()

    @property
    def resource(self) -> Resource:
        """
        Returns:
            resource (Resource): resource
        """
        return self.__resource

    @property
    def buffer(self) -> types.IBuffer:
        """
        Returns:
            Loader: buffer
        """
        pass

    @property
    def byte_stream(self) -> types.IByteStream:
        """Resource byte stream

        The stream is available after opening the loader

        Returns:
            io.ByteStream: resource byte stream
        """
        pass

    @property
    def text_stream(self) -> types.ITextStream:
        """Resource text stream

        The stream is available after opening the loader

        Returns:
            io.TextStream: resource text stream
        """
        pass

    # Open/Close

    def open(self):
        """Open the loader as "io.open" does"""
        pass

    def close(self) -> None:
        """Close the loader as "filelike.close" does"""
        if self.__byte_stream:
            self.__byte_stream.close()
        self.__byte_stream = None

    @property
    def closed(self) -> bool:
        """Whether the loader is closed

        Returns:
            bool: if closed
        """
        pass

    # Read

    def read_byte_stream(self) -> types.IByteStream:
        """Read bytes stream

        Returns:
            io.ByteStream: resource byte stream
        """
        pass

    def read_byte_stream_create(self) -> types.IByteStream:
        """Create bytes stream

        Returns:
            io.ByteStream: resource byte stream
        """
        raise NotImplementedError()

    def read_byte_stream_process(
        self,
        byte_stream: types.IByteStream,
    ) -> ByteStreamWithStatsHandling:
        """Process byte stream

        Parameters:
            byte_stream (io.ByteStream): resource byte stream

        Returns:
            io.ByteStream: resource byte stream
        """
        pass

    # TODO: move to formats
    def read_byte_stream_decompress(
        self, byte_stream: types.IByteStream
    ) -> types.IByteStream:
        """Decompress byte stream

        Parameters:
            byte_stream (io.ByteStream): resource byte stream

        Returns:
            io.ByteStream: resource byte stream
        """
        pass

    def read_byte_stream_buffer(self, byte_stream: types.IByteStream):
        """Buffer byte stream

        Parameters:
            byte_stream (io.ByteStream): resource byte stream

        Returns:
            bytes: buffer
        """
        pass

    def read_byte_stream_analyze(self, buffer: bytes):
        """Detect metadta using sample

        Parameters:
            buffer (bytes): byte buffer
        """
        pass

    def read_text_stream(self):
        """Read text stream

        Returns:
            io.TextStream: resource text stream
        """
        pass

    # Write

    def write_byte_stream(self, path: str) -> Any:
        """Write from a temporary file

        Parameters:
            path (str): path to a temporary file

        Returns:
            any: result of writing e.g. resulting path
        """
        byte_stream = self.write_byte_stream_create(path)
        result = self.write_byte_stream_save(byte_stream)
        return result

    def write_byte_stream_create(self, path: str) -> types.IByteStream:
        """Create byte stream for writing

        Parameters:
            path (str): path to a temporary file

        Returns:
            io.ByteStream: byte stream
        """
        atexit.register(os.remove, path)
        file = open(path, "rb")
        return file

    def write_byte_stream_save(self, byte_stream: types.IByteStream) -> Any:
        """Store byte stream"""
        raise NotImplementedError()


# Internal


# NOTE:
# We can try buffering byte buffer especially for remote
# Also, currently read/read1/item implementation is not complete
# As an option, we can think of subclassing some io.* class


class ByteStreamWithStatsHandling:
    def __init__(self, byte_stream: types.IByteStream, *, resource: Resource):
        self.__byte_stream = byte_stream
        self.__resource = resource
        self.__md5 = hashlib.new("md5")
        self.__sha256 = hashlib.new("sha256")
        self.__bytes = 0

    def __getattr__(self, name: str):
        return getattr(self.__byte_stream, name)

    def __iter__(self):  # type: ignore
        while True:
            bytes = self.read1(settings.DEFAULT_BUFFER_SIZE)
            if not bytes:
                break
            yield from bytes.splitlines(keepends=True)

    @property
    def closed(self):
        pass

    def read1(self, size: Optional[int] = -1):
        size = -1 if size is None else size
        chunk = cast(bytes, self.__byte_stream.read1(size))  # type: ignore

        # Calculate
        self.__md5.update(chunk)
        self.__sha256.update(chunk)
        self.__bytes += len(chunk)

        # Store (hash on EOF)
        if size == -1 or not chunk:
            self.__resource.stats.md5 = self.__md5.hexdigest()
            self.__resource.stats.sha256 = self.__sha256.hexdigest()
        self.__resource.stats.bytes = self.__bytes

        return chunk
