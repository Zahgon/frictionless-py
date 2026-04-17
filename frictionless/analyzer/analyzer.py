from __future__ import annotations

import statistics
from collections import Counter
from decimal import Decimal
from math import nan
from typing import TYPE_CHECKING, Any, Dict, List, Union

import attrs

from .. import helpers
from . import types

if TYPE_CHECKING:
    from ..resources import TableResource


class Analyzer:
    # Resource

    def analyze_table_resource(
        self, resource: TableResource, *, detailed: bool = False
    ) -> types.IAnalysisReport:
        # Create state
        pass


# Internal


def _common_values(data: Union[float, int]) -> Union[float, int]:
    """Finds highly common data with frequency

    Args:
        data (float|int): data

    Returns:
        (float|int): highly common element and its count
    """
    pass


def _statistics(data: Union[float, int]) -> Dict[str, Any]:
    """Calculate the descriptive statistics of the data

    Args:
        data (float|int): data

    Returns:
        dict : statistics of the data
    """
    pass


def _find_bounds(quartiles: List[Any]):
    """Calculate the higher and lower bound of distribution

    Args:
        quantiles (List): list of quartiles of distribution

    Returns:
        List: upper and lower bound
    """
    pass
