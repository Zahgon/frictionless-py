from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from ...platform import platform
from ...system import Mapper

if TYPE_CHECKING:
    from ...metadata import Metadata


class MarkdownMapper(Mapper):
    """Markdown mapper"""

    def write_metadata(self, metadata: Metadata, *, table: bool = False):
        pass


# Internal


def render_markdown(path: str, data: Dict[str, Any]) -> str:
    """Render any JSON-like object as Markdown, using jinja2 template"""
    pass


def dict_to_markdown(
    x: Union[Dict[str, Any], List[Any], int, float, str, bool],
    level: int = 0,
    tab: int = 2,
    flatten_scalar_lists: bool = True,
) -> str:
    """Render any JSON-like object as Markdown, using nested bulleted lists"""
    pass


def dicts_to_markdown_table(dicts: List[Dict[str, Any]], **kwargs: Any) -> str:
    """Tabulate dictionaries and render as a Markdown table"""
    pass


def filter_dict(
    x: Dict[str, Any],
    include: Optional[List[Any]] = None,
    exclude: Optional[List[Any]] = None,
    order: Optional[List[Any]] = None,
) -> Dict[str, Any]:
    """Filter and order dictionary by key names"""
    pass
