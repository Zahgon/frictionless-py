from __future__ import annotations

from typing import TYPE_CHECKING

from ...system import Plugin
from . import settings

if TYPE_CHECKING:
    from ...resource import Resource


class ImagePlugin(Plugin):
    """Plugin for Image"""

    # Hooks

    def detect_resource(self, resource: Resource):
        pass
