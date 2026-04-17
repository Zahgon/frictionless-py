from __future__ import annotations

import datetime
import json
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Union, cast

from ...catalog import Catalog, Dataset
from ...exception import FrictionlessException
from ...package import Package
from ...platform import platform
from ...resource import Resource
from ...system import Adapter, PublishResult
from .control import ZenodoControl
from .models import ZenodoCreator, ZenodoMetadata

if TYPE_CHECKING:
    from pyzenodo3 import Record  # type: ignore


class ZenodoAdapter(Adapter):
    """Read and write data from/to Zenodo"""

    def __init__(self, control: ZenodoControl):
        self.control = control

    # Read

    def read_package(self) -> Package:
        pass

    # Write

    def write_package(self, package: Package):
        client = platform.pyzenodo3_upload
        client.BASE_URL = self.control.base_url

        # Ensure api key
        if not self.control.apikey:
            raise FrictionlessException("Api key is required for zenodo publishing")

        try:
            # Ensure deposition
            deposition_id = self.control.deposition_id
            if not deposition_id:
                deposition_id = cast(
                    int,
                    client.create(
                        token=self.control.apikey,
                        base_url=self.control.base_url,
                    ),
                )

            # Generate metadata
            if self.control.metafn:
                descriptor = json.loads(Path(self.control.metafn).read_text())
                meta = descriptor.get("metadata", {})
                meta.setdefault("publication_date", str(datetime.date.today()))
                meta.setdefault("access_right", "open")
                metadata = ZenodoMetadata(**meta)
            else:
                description = self.control.description or package.description or "About"
                license = "CC-BY-4.0"
                if package.licenses:
                    license = package.licenses[0].get("name", license)
                metadata = ZenodoMetadata(
                    title=self.control.title or package.title or "Title",
                    description=description,
                    license=license,
                    publication_date=str(datetime.date.today()),
                )
                if self.control.author:
                    metadata.creators.append(
                        ZenodoCreator(
                            name=self.control.author,
                            affiliation=self.control.company,
                        )
                    )
                for contributor in package.contributors:
                    metadata.creators.append(
                        ZenodoCreator(
                            name=contributor.get("title", "Title"),
                            affiliation=contributor.get("organization"),
                        )
                    )

            # Upload metadata
            with tempfile.NamedTemporaryFile("wt") as file:
                data = dict(metadata=metadata.model_dump(exclude_none=True))
                json.dump(data, file, indent=2)
                file.flush()
                client.upload_meta(
                    token=self.control.apikey,
                    metafn=file.name,
                    depid=deposition_id,
                )

            # Upload package
            with tempfile.TemporaryDirectory() as dir:
                path = Path(dir) / "datapackage.json"
                package.to_json(str(path))
                client.upload_data(
                    token=self.control.apikey,
                    datafn=path,
                    depid=deposition_id,
                    base_url=self.control.base_url,
                )

            # Upload resource
            for resource in package.resources:
                if resource.normpath and not resource.remote:
                    client.upload_data(
                        token=self.control.apikey,
                        datafn=Path(resource.normpath),
                        depid=deposition_id,
                        base_url=self.control.base_url,
                    )

            # Return result
            return PublishResult(
                url=f"https://zenodo.org/deposit/{deposition_id}",
                context=dict(deposition_id=deposition_id),
            )

        except Exception as exception:
            note = "Zenodo API error" + repr(exception)
            raise FrictionlessException(note)

    # Experimental

    def read_catalog(self) -> Catalog:
        pass


def get_package(record: Record, title: str, formats: List[str]) -> Package:  # type: ignore
    pass
