from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Dict, List, Union

from ...catalog import Catalog, Dataset
from ...exception import FrictionlessException
from ...package import Package
from ...platform import platform
from ...resource import Resource
from ...system import Adapter, PublishResult
from .control import GithubControl

if TYPE_CHECKING:
    from github.ContentFile import ContentFile
    from github.Repository import Repository


class GithubAdapter(Adapter):
    """Read and write data from/to Github"""

    def __init__(self, control: GithubControl):
        self.control = control

    # Read

    def read_package(self) -> Package:
        pass

    # Write

    # TODO: should return path: str
    def write_package(self, package: Package):
        assert self.control.repo
        assert self.control.apikey

        # Create repo
        repository = None
        user = None
        try:
            client = platform.github.Github(self.control.apikey)
            user = client.get_user()
            repository = user.create_repo(
                name=self.control.repo, auto_init=True, gitignore_template="Python"
            )
        except Exception as exception:
            note = "Github API error:" + repr(exception)
            raise FrictionlessException(note)

        # Write package file
        content = package.to_json()
        package_path = self.control.filename or "datapackage.json"
        if self.control.basepath:
            package_path = os.path.join(self.control.basepath, package_path)
        repository = user.get_repo(self.control.repo)
        username = self.control.name or user.name or self.control.user
        email = user.email or self.control.email or f"{username}@users.noreply.github.com"
        assert email
        assert username
        author = platform.github.InputGitAuthor(username, email)
        branch = repository.default_branch
        try:
            repository.create_file(
                path=package_path,
                message='Create "datapackage.json"',
                content=content,
                branch=repository.default_branch,
                committer=author,
                author=author,
            )
        except Exception as exception:
            note = "Github API error:" + repr(exception)
            raise FrictionlessException(note)

        # Write resource files
        try:
            for resource in package.resources:
                resource_path: str = resource.path or ""
                if self.control.basepath:
                    resource_path = os.path.join(self.control.basepath, resource_path)
                repository.create_file(
                    path=resource_path,
                    message='Create "resource_path"',
                    # It seeems to be it requires a string by a mistake
                    # https://stackoverflow.com/questions/72668275/how-to-upload-an-image-file-to-github-using-pygithub
                    content=resource.read_bytes(),  # type: ignore
                    branch=branch,
                    committer=author,
                    author=author,
                )
        except Exception as exception:
            note = "Github API error:" + repr(exception)
            raise FrictionlessException(note)

        # Get url
        url = repository.html_url

        # Enable pages
        if self.control.enable_pages:
            try:
                # TODO: rebase on public API when it's available
                # https://github.com/PyGithub/PyGithub/issues/2037
                repository._requester.requestJsonAndCheck(
                    "POST",
                    f"{repository.url}/pages",
                    input={"source": {"branch": "main"}},
                )
                url = f"https://{user.name}.github.io/{repository.name}"
            except Exception as exception:
                note = "Github API error:" + repr(exception)
                raise FrictionlessException(note)

        return PublishResult(url=url, context=dict(repository=repository))

    # Experimental

    def read_catalog(self) -> Catalog:
        pass


def get_resources(
    contents: Union[List[ContentFile], ContentFile], repository: Repository
) -> List[ContentFile]:
    pass


def get_package(
    paths: List[ContentFile],
    repository: Repository,
    base_path: str,
    formats: List[str],
    catalog: bool = False,
) -> Union[Package, List[Package]]:
    pass
