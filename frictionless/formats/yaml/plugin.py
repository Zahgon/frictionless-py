from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from ...detector import Detector
from ...system import Plugin
from .control import YamlControl
from .parser import YamlParser

if TYPE_CHECKING:
    from ...resource import Resource


class YamlPlugin(Plugin):
    """Plugin for Yaml"""

    # Hooks

    def create_parser(self, resource: Resource):
        if resource.format == "yaml":
            return YamlParser(resource)

    def detect_resource(self, resource: Resource):
        pass

    def select_control_class(self, type: Optional[str] = None):
        if type == "yaml":
            return YamlControl
