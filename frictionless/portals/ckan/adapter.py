import json
import os
from pathlib import PurePosixPath
from typing import Any, Dict, Optional
from urllib.parse import urljoin

from ... import helpers
from ...catalog import Catalog, Dataset
from ...exception import FrictionlessException
from ...package import Package
from ...platform import platform
from ...resource import Resource
from ...system import Adapter, PublishResult, system
from .control import CkanControl


class CkanAdapter(Adapter):
    """Read and write data from/to Ckan"""

    def __init__(self, control: CkanControl):
        self.control = control
        self.mapper = {
            "ckan_to_fric": platform.frictionless_ckan_mapper_ckan_to_frictionless,
            "fric_to_ckan": platform.frictionless_ckan_mapper_frictionless_to_ckan,
        }

    # Read

    def read_package(self) -> Package:
        pass

    # Write

    def write_package(self, package: Package):
        baseurl = self.control.baseurl
        endpoint = f"{baseurl}/api/action/package_create"
        headers = set_headers(self)
        package_descriptor = package.to_descriptor()
        package_data = self.mapper["fric_to_ckan"].package(package_descriptor)  # type: ignore
        package_data["owner_org"] = self.control.organization_name

        # Assure that the package has a name
        if "name" not in package_data:
            if not self.control.dataset:
                note = (
                    "Your package has no name. CKAN requires a name to publish a package"
                )
                raise FrictionlessException(note)
            else:
                package_data["name"] = self.control.dataset

        # if "id" exist and control is set to allow updates, try to update dataset
        if self.control.allow_update:
            endpoint = f"{baseurl}/api/action/package_update"

        if "resources" in package_data:
            del package_data["resources"]

        try:
            # Make request
            response = system.http_session.request(
                method="POST",
                url=endpoint,
                headers=headers,
                allow_redirects=True,
                json=package_data,
            )

            if response.status_code == 200:
                response_dict = json.loads(response.content)
                dataset_id = response_dict["result"]["id"]
                dataset_name = response_dict["result"]["name"]
                package_descriptor = package.to_descriptor(validate=True)

                # upload resources
                # TODO: See if it's possible to upload only the resources that need to be uploaded
                for index, resource in enumerate(package.resources):
                    if resource.path:
                        _, resource_filename = os.path.split(resource.path)
                        resource_filename = (
                            f"{resource.name}.{resource_filename.split('.')[1]}"
                        )
                        package_descriptor["resources"][index]["path"] = resource_filename
                    self.write_resource(dataset_id, resource)

                # upload package
                package_resource_data = {
                    "name": "datapackage",
                    "type": "json",
                    "package_id": dataset_id,
                }
                endpoint = f"{baseurl}/api/action/resource_create"
                make_ckan_request(
                    endpoint,
                    method="POST",
                    headers=headers,
                    data=package_resource_data,
                    files={
                        "upload": (
                            "datapackage.json",
                            json.dumps(package_descriptor, indent=2).encode("utf-8"),
                            "application/octet-stream",
                        )
                    },
                )
                return PublishResult(
                    url=urljoin(
                        self.control.baseurl or "",
                        str(PurePosixPath("dataset").joinpath(dataset_name)),
                    ),
                    context=dict(dataset_id=dataset_id),
                )
            else:
                note = response.text
                raise FrictionlessException(note)

        except Exception as exception:
            note = "CKAN API error:" + repr(exception)
            raise FrictionlessException(note)

    def write_resource(self, dataset_id: str, resource: Resource):
        baseurl = self.control.baseurl
        endpoint = f"{baseurl}/api/action/resource_create"
        headers = set_headers(self)
        resource_descriptor = resource.to_descriptor()
        resource_data = self.mapper["fric_to_ckan"].resource(resource_descriptor)  # type: ignore
        resource_data["package_id"] = dataset_id
        _, resource_filename = os.path.split(resource_data["url"])
        resource_data["owner_org"] = self.control.organization_name

        del resource_data["url"]

        try:
            response = system.http_session.request(
                method="POST",
                url=endpoint,
                headers=headers,
                allow_redirects=True,
                data=resource_data,
                files={
                    "upload": (
                        resource_filename,
                        resource.read_bytes(),
                        "application/octet-stream",
                    )
                },
            )

            if response.status_code != 200:
                note = response.text
                raise FrictionlessException(note)
        except Exception as exception:
            note = "CKAN API error:" + repr(exception)
            raise FrictionlessException(note)

    # Experimental

    def read_catalog(self) -> Catalog:
        pass


def set_headers(adapter: CkanAdapter) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    if adapter.control.apikey:
        if adapter.control.apikey.startswith("env:"):
            apikey = os.environ.get(adapter.control.apikey[4:])
        else:
            apikey = adapter.control.apikey

        headers.update({"Authorization": apikey})

    return headers


def make_ckan_request(
    endpoint: str,
    *,
    method: str = "GET",
    headers: Optional[Dict[str, str]] = None,
    apikey: Optional[str] = None,
    **options: Any,
) -> Dict[str, Any]:
    response_json: Dict[str, Any] = {}
    # Handle headers
    if headers is None:
        headers = {}

    # Handle API key
    if apikey:
        if apikey.startswith("env:"):
            apikey = os.environ.get(apikey[4:])
        headers.update({"Authorization": apikey})  # type: ignore

    # Make request
    response = system.http_session.request(
        method=method, url=endpoint, headers=headers, allow_redirects=True, **options
    )

    if response is not None:
        response_json = response.json()

    # Handle error
    try:
        ckan_error = None
        if not response_json.get("success") and response_json["error"]:
            ckan_error = response_json["error"]
    except TypeError:
        ckan_error = response
    if ckan_error:
        note = "CKAN returned an error: " + json.dumps(ckan_error)
        raise FrictionlessException(note)

    return response_json
