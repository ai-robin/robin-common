from unittest.mock import patch

from robin_common import StorageClient

ORIGINAL_DOCS_BUCKET = "original-bucket"
DOCX_BUCKET = "docx-bucket"
JSON_BUCKET = "json-bucket"


class TestStorageClient:
    @patch("robin_common.storage_client.storage")
    def test_gcloud_api_calls(self, mock_storage):
        client = StorageClient()
        mock_client = mock_storage.Client.return_value
        mock_bucket = mock_client.get_bucket.return_value
        mock_file = mock_bucket.blob.return_value

        # Getting a file
        json_filename = "just-a-file.json"
        file = client.get_file(json_filename, JSON_BUCKET)

        mock_client.get_bucket.assert_called_once_with(JSON_BUCKET)
        mock_bucket.blob.assert_called_once_with(json_filename)
        mock_file.download_as_string.assert_called_once()
        file_contents = mock_file.download_as_string.return_value
        assert file == file_contents

        # Saving a file
        docx_filename = "revised-file.docx"
        client.save_file(docx_filename, DOCX_BUCKET, b"hey")

        mock_client.get_bucket.assert_called_with(DOCX_BUCKET)
        mock_bucket.blob.assert_called_with(docx_filename)
        mock_file.upload_from_string.assert_called_once_with(b"hey")
