from __future__ import annotations

import builtins
import os
import warnings
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Union

from frictionless.schema.field import Field

from .. import errors, helpers
from ..analyzer import Analyzer
from ..dialect import Dialect
from ..exception import FrictionlessException
from ..indexer import Indexer
from ..platform import platform
from ..resource import Resource
from ..system import system
from ..table import Header, Lookup, Row, Table
from ..transformer import Transformer

if TYPE_CHECKING:
    from .. import types
    from ..indexer import IOnProgress, IOnRow
    from ..pipeline import Pipeline
    from ..system import Loader, Parser
    from ..table import IRowStream


class TableResource(Resource):
    type = "table"
    datatype = "table"
    tabular = True

    def __attrs_post_init__(self):
        self.__loader: Optional[Loader] = None
        self.__parser: Optional[Parser] = None
        self.__buffer: Optional[types.IBuffer] = None
        self.__sample: Optional[types.ISample] = None
        self.__labels: Optional[types.ILabels] = None
        self.__fragment: Optional[types.IFragment] = None
        self.__header: Optional[Header] = None
        self.__lookup: Optional[Lookup] = None
        self.__row_stream: Optional[IRowStream] = None
        super().__attrs_post_init__()

    # Open/Close

    @property
    def buffer(self) -> types.IBuffer:
        """File's bytes used as a sample

        These buffer bytes are used to infer characteristics of the
        source file (e.g. encoding, ...).
        """
        pass

    @property
    def sample(self) -> types.ISample:
        """Table's lists used as sample.

        These sample rows are used to infer characteristics of the
        source file (e.g. schema, ...).

        Returns:
            list[]?: table sample
        """
        pass

    @property
    def labels(self) -> types.ILabels:
        """
        Returns:
            str[]?: table labels
        """
        pass

    @property
    def fragment(self) -> types.IFragment:
        """Table's lists used as fragment.

        These fragment rows are used internally to infer characteristics of the
        source file (e.g. schema, ...).

        Returns:
            list[]?: table fragment
        """
        pass

    @property
    def header(self) -> Header:
        """
        Returns:
            str[]?: table header
        """
        pass

    @property
    def lookup(self) -> Lookup:
        """
        Returns:
            str[]?: table lookup
        """
        pass

    @property
    def cell_stream(self) -> types.ICellStream:
        """Cell stream in form of a generator

        Yields:
            gen<any[][]>?: cell stream
        """
        pass

    @property
    def row_stream(self) -> IRowStream:
        """Row stream in form of a generator of Row objects

        Yields:
            gen<Row[]>?: row stream
        """
        pass

    @property
    def closed(self) -> bool:
        """Whether the table is closed

        Returns:
            bool: if closed
        """
        pass

    def close(self) -> None:
        """Close the resource as "filelike.close" does"""
        if self.__parser:
            self.__parser.close()
            self.__parser = None
        if self.__loader:
            self.__loader.close()
            self.__loader = None

    def open(self):
        """Open the resource as "io.open" does"""
        pass

    def __open_parser(self):
        pass

    def __open_buffer(self):
        pass

    def __open_sample(self):
        pass

    def __open_dialect(self):
        pass

    def __open_labels(self):
        pass

    def __open_fragment(self):
        pass

    def __open_schema(self):
        pass

    def __open_header(self):
        pass

    def __open_lookup(self):
        pass

    def __open_row_stream(self):
        # TODO: we need to rework this field_info / row code
        # During row streaming we create a field info structure
        # This structure is optimized and detached version of schema.fields
        # We create all data structures in-advance to share them between rows

        # Create field info
        pass

    def remove_missing_required_label_from_field_info(
        self, field: Field, field_info: Dict[str, Any]
    ):
        pass

    @staticmethod
    def label_is_missing(
        field_name: str,
        expected_field_names: List[str],
        table_labels: types.ILabels,
        case_sensitive: bool,
    ) -> bool:
        """Check if a schema field name is missing from the TableResource
        labels.
        """
        pass

    @staticmethod
    def remove_field_from_field_info(field_name: str, field_info: Dict[str, Any]):
        pass

    def primary_key_cells(self, row: Row, case_sensitive: bool) -> Tuple[Any, ...]:
        """Create a tuple containg all cells from a given row associated to primary
        keys"""
        pass

    def primary_key_labels(
        self,
        row: Row,
        case_sensitive: bool,
    ) -> List[str]:
        """Create a list of TableResource labels that are primary keys"""
        pass

    # Read
    def read_cells(self, *, size: Optional[int] = None) -> List[List[Any]]:
        """Read lists into memory

        Returns:
            any[][]: table lists
        """
        pass

    def read_rows(self, *, size: Optional[int] = None) -> List[Row]:
        """Read rows into memory

        Returns:
            Row[]: table rows
        """
        with helpers.ensure_open(self):
            rows: List[Row] = []
            for row in self.row_stream:
                rows.append(row)
                if size and len(rows) >= size:
                    break
            return rows

    # TODO: implement
    def read_table(self) -> Table:
        pass

    # Write

    def write_table(
        self, target: Optional[Union[Resource, Any]] = None, **options: Any
    ) -> TableResource:
        """Write this resource to the target resource

        You can pass:
        - a target resource instance (no extra options are allowed) OR
        - path and options to create a new resource.

        Parameters:
            target (Resource|Any): target path or target resource instance
            **options (dict): resource constructor options
        """
        resource = target
        if not isinstance(resource, Resource):
            resource = Resource(target, **options)
        if not isinstance(resource, TableResource):
            raise FrictionlessException("target must be a table resource")
        parser = system.create_parser(resource)
        parser.write_row_stream(self)
        return resource

    # Infer

    # TODO: allow cherry-picking stats for adding to a descriptor
    def infer(self, *, stats: bool = False) -> None:
        """Infer metadata

        Parameters:
            stats: stream file completely and infer stats
        """
        if not self.closed:
            note = "Resource.infer cannot be used on a open resource"
            raise FrictionlessException(errors.ResourceError(note=note))
        with self:
            if not stats:
                return
            helpers.pass_through(self.row_stream)
            self.hash = f"sha256:{self.stats.sha256}"
            self.bytes = self.stats.bytes
            self.fields = self.stats.fields
            self.rows = self.stats.rows

    # Analyze

    def analyze(self, *, detailed: bool = False):
        """Analyze the resource

        This feature is currently experimental, and its API may change
        without warning.

        Parameters:
            detailed: do detailed analysis

        Returns:
            dict: resource analysis

        """
        pass

    # Convert

    def convert(
        self,
        to_path: str,
        to_format: Optional[str] = None,
        to_dialect: Optional[Union[Dialect, str]] = None,
    ) -> str:
        dialect = to_dialect or Dialect()
        target = TableResource(path=to_path, format=to_format, dialect=dialect)
        if os.path.exists(to_path):
            note = f'Cannot convert to the existent path "{to_path}"'
            raise FrictionlessException(note)
        self.write(target)
        return to_path

    # Extract

    def extract(
        self,
        *,
        name: Optional[str] = None,
        filter: Optional[types.IFilterFunction] = None,
        process: Optional[types.IProcessFunction] = None,
        limit_rows: Optional[int] = None,
    ) -> types.ITabularData:
        if not process:
            process = lambda row: row.to_dict()
        data = self.read_rows(size=limit_rows)
        data = builtins.filter(filter, data) if filter else data
        data = (process(row) for row in data) if process else data
        return {name or self.name: list(data)}

    # Index

    def index(
        self,
        database_url: str,
        *,
        name: Optional[str] = None,
        fast: bool = False,
        with_metadata: bool = False,
        on_row: Optional[IOnRow] = None,
        on_progress: Optional[IOnProgress] = None,
        use_fallback: bool = False,
        qsv_path: Optional[str] = None,
    ) -> List[str]:
        name = name or self.name
        indexer = Indexer(
            resource=self,
            database=database_url,
            table_name=name,
            fast=fast,
            with_metadata=with_metadata,
            on_row=on_row,
            on_progress=on_progress,
            use_fallback=use_fallback,
            qsv_path=qsv_path,
        )
        indexer.index()
        return [name]

    # Transform

    def transform(self, pipeline: Pipeline):
        transformer = Transformer()
        return transformer.transform_table_resource(self, pipeline)

    # Export

    def to_view(self, type: str = "look", **options: Any):
        """Create a view from the resource

        See PETL's docs for more information:
        https://platform.petl.readthedocs.io/en/stable/util.html#visualising-tables

        Parameters:
            type (look|lookall|see|display|displayall): view's type
            **options (dict): options to be passed to PETL

        Returns
            str: resource's view
        """
        pass

    def to_inline(self, *, dialect: Optional[Dialect] = None):
        """Helper to export resource as an inline data"""
        pass

    def to_pandas(self, *, dialect: Optional[Dialect] = None):
        """Helper to export resource as an Pandas dataframe"""
        dialect = dialect or Dialect()
        target = self.write(Resource(format="pandas", dialect=dialect))  # type: ignore
        return target.data

    def to_snap(self, *, json: bool = False):
        """Create a snapshot from the resource

        Parameters:
            json (bool): make data types compatible with JSON format

        Returns
            list: resource's data
        """
        pass

    @staticmethod
    def from_petl(view: Any, **options: Any):
        """Create a resource from PETL view"""
        pass

    def to_petl(self, normalize: bool = False):
        """Export resource as a PETL table"""
        resource = self.to_copy()

        # Define view
        class ResourceView(platform.petl.Table):  # type: ignore
            def __iter__(self):  # type: ignore
                with resource:
                    if normalize:
                        yield resource.schema.field_names
                        yield from (row.to_list() for row in resource.row_stream)
                        return
                    if not resource.header.missing:
                        yield resource.header.labels
                    yield from (row.cells for row in resource.row_stream)

        return ResourceView()

    # Legacy

    def write(
        self, target: Optional[Union[Resource, Any]] = None, **options: Any
    ) -> TableResource:
        return self.write_table(target, **options)
