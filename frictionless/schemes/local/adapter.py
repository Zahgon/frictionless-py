from __future__ import annotations

import os
from typing import Any, Optional

from ... import helpers
from ...exception import FrictionlessException
from ...package import Package
from ...resource import Resource
from ...system import Adapter


class LocalAdapter(Adapter):
    def __init__(self, source: Any, *, basepath: Optional[str] = None):
        self.source = source
        self.basepath = basepath

    def read_package(self):
        # Directory
        pass
