from __future__ import annotations

import io
from typing import TYPE_CHECKING, Optional

from ... import types
from ...platform import platform
from ...system import Loader, system
from .control import RemoteControl

if TYPE_CHECKING:
    from requests import Session


class RemoteLoader(Loader):
    """Remote loader implementation."""

    remote = True

    # Read

    def read_byte_stream_create(self):  # type: ignore
        pass

    # Write

    def write_byte_stream_save(self, byte_stream: types.IByteStream):
        assert self.resource.normpath
        file = f"{self.resource.name}.{self.resource.format}"
        url = self.resource.normpath.replace(file, "")
        response = system.http_session.post(url, files={file: byte_stream})
        response.raise_for_status()
        return response


# Internal


class RemoteByteStream:
    def __init__(self, source: str, *, session: Session, timeout: int):
        self.__source = source
        self.__session = session
        self.__timeout = timeout

    def __iter__(self):  # type: ignore
        while True:
            bytes = self.read(8192)
            if not bytes:
                break
            yield from bytes.splitlines(keepends=True)

    def readable(self):
        pass

    def writable(self):
        pass

    def seekable(self):
        pass

    @property
    def closed(self):
        pass

    def open(self):
        pass

    def close(self):
        self.__closed = True

    def tell(self):
        pass

    def flush(self):
        pass

    def read(self, size: Optional[int] = -1):
        if size == -1:
            size = None
        return self.__response.raw.read(size)

    def read1(self, size: int = -1):
        return self.read(size)

    def seek(self, offset: int, whence: int = 0):
        assert offset == 0
        assert whence == 0
        self.__response = self.__session.get(
            self.__source, stream=True, timeout=self.__timeout
        )
        self.__response.raise_for_status()
        self.__response.raw.decode_content = True
