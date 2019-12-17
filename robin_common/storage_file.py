import re

from robin_common import StorageClient


class CloudFile:
    """
    Container that wraps a given file in a cloud storage bucket.
    This interface should be kept consistent, regardless of the
    cloud storage provider used (GCP, AWS, etc).
    """

    def __init__(self, name: str, bucket: str, contents: bytes = None):
        self.name = self._validate_name(name)
        self.bucket = bucket
        self.contents = contents
        self.storage = StorageClient()

    def fetch(self):
        self.contents = self.storage.get_file(self.name, self.bucket)

    def save(self):
        self.storage.save_file(self.name, self.bucket, self.contents)

    @classmethod
    def from_gcp_event(cls, event: dict):
        """
        Populate CloudFile from a Google Cloud Storage object.
        See: https://cloud.google.com/storage/docs/json_api/v1/objects#resource
        """
        return cls(name=event["name"], bucket=event["bucket"])

    @property
    def extension(self) -> str:
        extension = self.name.split(".")[-1]
        return extension.lower()

    def _validate_name(self, name: str) -> str:
        """Ensure file has extension."""
        if not re.match(r".+\.[A-Za-z]", name):
            err = f"File '{name}' missing extension."
            raise ValueError(err)
        return name
