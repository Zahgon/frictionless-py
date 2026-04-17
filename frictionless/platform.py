import platform as python_platform
import sys
from functools import cached_property
from importlib import import_module
from typing import Any, Callable, ClassVar


def extras(*, name: str):
    """Extra dependency decorator"""

    def outer(func: Callable[..., Any]):
        pass

    return outer


class Platform:
    """Platform representation"""

    type: ClassVar[str] = python_platform.system().lower()
    """
    Type of the platform(OS) framework is running on. For example, windows,
    linux etc.
    """

    python: ClassVar[str] = f"{sys.version_info.major}.{sys.version_info.minor}"
    """
    Python version
    """

    # Core

    @cached_property
    def bz2(self):
        pass

    @cached_property
    def chardet(self):
        pass

    @cached_property
    def dateutil_parser(self):
        pass

    @cached_property
    def frictionless(self):
        pass

    @cached_property
    def frictionless_checks(self):
        pass

    @cached_property
    def frictionless_errors(self):
        pass

    @cached_property
    def frictionless_fields(self):
        pass

    @cached_property
    def frictionless_formats(self):
        pass

    @cached_property
    def frictionless_portals(self):
        pass

    @cached_property
    def frictionless_resources(self):
        pass

    @cached_property
    def frictionless_schemes(self):
        pass

    @cached_property
    def frictionless_steps(self):
        pass

    @cached_property
    def gzip(self):
        pass

    @cached_property
    def html_parser(self):
        pass

    @cached_property
    def isodate(self):
        pass

    @cached_property
    def jinja2(self):
        pass

    @cached_property
    def jinja2_filters(self):
        pass

    @cached_property
    def jsonschema(self):
        pass

    @cached_property
    def jsonschema_validators(self):
        pass

    @cached_property
    def lzma(self):
        pass

    @cached_property
    def marko(self):
        pass

    @cached_property
    def marko_ext_gfm(self):
        pass

    @cached_property
    def petl(self):
        pass

    @cached_property
    def psycopg(self):
        pass

    @cached_property
    def requests(self):
        pass

    @cached_property
    def requests_utils(self):
        pass

    @cached_property
    def rfc3986(self):
        pass

    @cached_property
    def validators(self):
        pass

    @cached_property
    def yaml(self):
        pass

    @cached_property
    def zipfile(self):
        pass

    # Extras

    @cached_property
    @extras(name="aws")
    def boto3(self):
        pass

    @cached_property
    @extras(name="ckan")
    def frictionless_ckan_mapper_ckan_to_frictionless(self):
        pass

    @cached_property
    @extras(name="ckan")
    def frictionless_ckan_mapper_frictionless_to_ckan(self):
        pass

    @cached_property
    @extras(name="excel")
    def xlrd(self):
        pass

    @cached_property
    @extras(name="excel")
    def xlwt(self):
        pass

    @cached_property
    @extras(name="excel")
    def openpyxl(self):
        pass

    @cached_property
    @extras(name="excel")
    def tableschema_to_template(self):
        pass

    @cached_property
    @extras(name="json")
    def ijson(self):
        pass

    @cached_property
    @extras(name="json")
    def jsonlines(self):
        pass

    @cached_property
    @extras(name="github")
    def github(self):
        pass

    @cached_property
    @extras(name="gsheets")
    def pygsheets(self):
        pass

    @cached_property
    @extras(name="html")
    def pyquery(self):
        pass

    @cached_property
    @extras(name="ods")
    def ezodf(self):
        pass

    @cached_property
    @extras(name="markdown")
    def livemark(self):
        pass

    @cached_property
    @extras(name="pandas")
    def pandas(self):
        pass

    @cached_property
    @extras(name="pandas")
    def pandas_core_dtypes_api(self):
        pass

    @cached_property
    @extras(name="pandas")
    def numpy(self):
        pass

    @cached_property
    @extras(name="parquet")
    def pyarrow_parquet(self):
        pass

    @cached_property
    @extras(name="spss")
    def sav_reader_writer(self):
        pass

    @cached_property
    @extras(name="sql")
    def sqlalchemy(self):
        pass

    @cached_property
    @extras(name="sql")
    def sqlalchemy_exc(self):
        pass

    @cached_property
    @extras(name="sql")
    def sqlalchemy_schema(self):
        pass

    @cached_property
    @extras(name="sql")
    def sqlalchemy_dialects(self):
        pass

    @cached_property
    @extras(name="sql")
    def sqlalchemy_dialects_postgresql(self):
        pass

    @cached_property
    @extras(name="sql")
    def sqlalchemy_dialects_mysql(self):
        pass

    @cached_property
    @extras(name="zenodo")
    def pyzenodo3(self):
        pass

    @cached_property
    @extras(name="zenodo")
    def pyzenodo3_upload(self):
        pass

    @cached_property
    @extras(name="wkt")
    def wkt(self):
        pass


platform = Platform()
