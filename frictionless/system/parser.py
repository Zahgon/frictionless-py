from __future__ import annotations

from itertools import chain
from typing import TYPE_CHECKING, Any, ClassVar, List, Optional, cast

from .. import errors
from ..exception import FrictionlessException
from ..platform import platform
from .system import system

if TYPE_CHECKING:
    from .. import types
    from ..resource import Resource
    from ..resources import TableResource
    from .loader import Loader


class Parser:
    """Parser representation

    Parameters:
        resource (Resource): resource

    """

    requires_loader: ClassVar[bool] = False
    """
    Specifies if parser requires the loader to load the
    data.
    """

    supported_types: ClassVar[List[str]] = []
    """
    Data types supported by the parser.
    """

    def __init__(self, resource: Resource):
        self.__resource: Resource = resource
        self.__loader: Optional[Loader] = None
        self.__sample: Optional[types.ISample] = None
        self.__cell_stream: Optional[types.ICellStream] = None

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
            Resource: resource
        """
        return self.__resource

    @property
    def loader(self) -> Loader:
        """
        Returns:
            Loader: loader
        """
        pass

    @property
    def sample(self) -> types.ISample:
        """
        Returns:
            Loader: sample
        """
        pass

    @property
    def cell_stream(self) -> types.ICellStream:
        """
        Yields:
            any[][]: list stream
        """
        pass

    # Open/Close

    def open(self):
        """Open the parser as "io.open" does"""
        pass

    def close(self) -> None:
        """Close the parser as "filelike.close" does"""
        if self.__loader:
            self.__loader.close()

    @property
    def closed(self) -> bool:
        """Whether the parser is closed

        Returns:
            bool: if closed
        """
        pass

    # Read

    def read_loader(self) -> Optional[Loader]:
        """Create and open loader

        Returns:
            Loader: loader
        """
        pass

    def read_cell_stream(self) -> types.ICellStream:
        """Read list stream

        Returns:
            gen<any[][]>: list stream
        """
        pass

    def read_cell_stream_create(self) -> types.ICellStream:
        """Create list stream from loader

        Parameters:
            loader (Loader): loader

        Returns:
            gen<any[][]>: list stream
        """
        raise NotImplementedError()

    def read_cell_stream_handle_errors(
        self,
        cell_stream: types.ICellStream,
    ) -> CellStreamWithErrorHandling:
        """Wrap list stream into error handler

        Parameters:
            gen<any[][]>: list stream

        Returns:
            gen<any[][]>: list stream
        """
        pass

    # Write

    def write_row_stream(self, source: TableResource) -> Any:
        """Write row stream from the source resource

        Parameters:
            source (Resource): source resource
        """
        raise NotImplementedError()


# Internal


# NOTE:
# Here we catch some Loader related errors
# We can consider moving it to Loader if it's possible


class CellStreamWithErrorHandling:
    def __init__(self, cell_stream: types.ICellStream):
        self.cell_stream = cell_stream

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return cast(List[Any], self.cell_stream.__next__())  # type: ignore
        except StopIteration:
            raise
        except FrictionlessException:
            raise
        except (platform.zipfile.BadZipFile, platform.gzip.BadGzipFile) as exception:
            error = errors.CompressionError(note=str(exception))
            raise FrictionlessException(error)
        except UnicodeDecodeError as exception:
            error = errors.EncodingError(note=str(exception))
            raise FrictionlessException(error) from exception
        except Exception as exception:
            error = errors.SourceError(note=str(exception))
            raise FrictionlessException(error) from exception
