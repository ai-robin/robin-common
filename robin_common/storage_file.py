import re
import typing

from robin_common import StorageClient


class CloudFile:
    """
    Container that wraps a given file in a cloud storage bucket.
    The interface for fetching and saving files should be kept consistent,
    regardless of the cloud storage provider used (GCP, AWS, etc).
    """

    def __init__(
        self, name: str, bucket: str, contents: typing.Union[bytes, str] = None
    ):
        self.name = self._validate_name(name)
        self.bucket = bucket
        self._contents = contents
        self.storage = StorageClient()

    def _validate_name(self, name: str) -> str:
        if not re.match(r".+\.[A-Za-z]{1,4}$", name):
            err = f"File '{name}' missing extension."
            raise ValueError(err)
        return name

    @classmethod
    def from_gcp_event(cls, event: dict):
        """
        Construct CloudFile from a Google Cloud Storage object.
        See: https://cloud.google.com/storage/docs/json_api/v1/objects#resource
        """
        return cls(name=event["name"], bucket=event["bucket"])

    @property
    def extension(self) -> str:
        extension = self.name.split(".")[-1]
        return extension.lower()

    @property
    def basename(self) -> str:
        """Isolates the entire filepath and name, *without* extension."""
        return self.name.split(".")[-2]

    @property
    def contents(self):
        if not self._contents:
            self.fetch()
        return self._contents

    def fetch(self):
        self._contents = self.storage.get_file(self.name, self.bucket)

    def save(self):
        self.storage.save_file(self.name, self.bucket, self._contents)
