from typing import Any, List, Optional

from ..resource import Resource


def list(
    source: Optional[Any] = None,
    *,
    name: Optional[str] = None,
    type: Optional[str] = None,
    **options: Any,
) -> List[Resource]:
    """List resources

    Parameters:
        source: a data source
        type: data type
        **options: Resource options

    Returns:
        data resources
    """
    pass
