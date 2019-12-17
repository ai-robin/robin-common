from google.cloud import storage


class Singleton(type):
    _instance = None

    def __call__(self):
        if self._instance is None:
            self.client = storage.Client()
            self._instance = super().__call__()
        return self._instance


class StorageClient(metaclass=Singleton):
    """
    A Singleton wrapper for the GCP `storage` API. Multiple instances
    of this class can be created without needing to wait for
    `storage.Client` to initialise and authenticate against GCP each time.
    """

    def get_file(self, filename: str, bucket: str) -> bytes:
        bucket = self.client.get_bucket(bucket)
        file = bucket.blob(filename)
        return file.download_as_string()

    def save_file(self, filename: str, bucket: str, contents: bytes):
        bucket = self.client.get_bucket(bucket)
        file = bucket.blob(filename)
        file.upload_from_string(contents)
