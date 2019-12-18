from unittest.mock import call, patch

import pytest
from robin_common import CloudFile


@patch("robin_common.storage_file.StorageClient")
class TestCloudFile:
    def test_from_gcp_event(self, *args):
        event = {"name": "dir/something.json", "bucket": "json-files"}
        file = CloudFile.from_gcp_event(event)

        assert file.name == "dir/something.json"
        assert file.bucket == "json-files"

    @pytest.mark.parametrize(
        "name,extension",
        [
            ("DIR/dolor/lorem-ipsum_sit.docX", "docx"),
            ("a_file.txt", "txt"),
            ("some_dir/a.JSON", "json"),
            ("A_FOLDER/blob.DoC", "doc"),
        ],
    )
    def test_extension_isolation(self, storage_client, name, extension):
        file = CloudFile(name=name, bucket="a_Bucket")
        assert file.extension == extension

    @pytest.mark.parametrize(
        "name,basename",
        [
            ("a_very/long-dir/with/file.HTmL", "a_very/long-dir/with/file"),
            ("just_A_file.JSON", "just_A_file"),
        ],
    )
    def test_basename_isolation(self, storage_client, name, basename):
        file = CloudFile(name=name, bucket="something")
        assert file.basename == basename

    @pytest.mark.parametrize(
        "name",
        [
            "just_a-dir/",
            "dir/file-without-extension",
            "dir.with.dots/somefile",
            "ends-with-dot.",
            "ends-with.1234",  # numeric extension
            "ends-with.xxxxx",  # extension > 4 chars
            ".doc",  # extension only
        ],
    )
    def test_error_for_files_without_extension(self, storage_client, name):
        with pytest.raises(ValueError, match=f"File '{name}' missing extension."):
            CloudFile(name=name, bucket="bucket")

    def test_cloud_storage_called_on_fetch(self, storage_client):
        mock_storage = storage_client.return_value
        file = CloudFile(name="something.json", bucket="pipeline-bucket")
        file.fetch()
        assert mock_storage.get_file.mock_calls == [
            call("something.json", "pipeline-bucket")
        ]

    def test_cloud_storage_called_on_save(self, storage_client):
        mock_storage = storage_client.return_value
        file = CloudFile(name="else.docx", bucket="some-bucket", contents=b"something")
        file.save()
        assert mock_storage.save_file.mock_calls == [
            call("else.docx", "some-bucket", b"something")
        ]

    def test_cloud_storage_called_when_needed_on_contents(self, storage_client):
        mock_storage = storage_client.return_value
        mock_storage.get_file.return_value = b"loaded"

        file = CloudFile(name="else.docx", bucket="some-bucket")

        assert not file.storage.get_file.called
        assert file.contents == b"loaded"  # Contents are fetched
        assert file.storage.get_file.called

        assert file.contents == b"loaded"
        assert len(file.storage.get_file.mock_calls) == 1  # Existing contents used
