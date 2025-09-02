import unittest
from unittest.mock import patch, mock_open, MagicMock
import yaml
import sys

sys.path.insert(0, ".")

from src.anomaly_detection.aws.aws_config_manager import AWSConfigManager


class TestAWSConfigManager(unittest.TestCase):
    """Unit tests for the AWSConfigManager class."""

    def setUp(self):
        """Set up a mock environment for each test."""
        # Mock config and env files
        self.mock_config_content = {
            "aws": {"region": "us-west-2"},
            "s3": {"bucket_name": "test-bucket", "region": "us-west-2"},
            "sagemaker": {
                "domain": {"name": "test-domain"},
                "training": {"default_instance_type": "ml.t3.medium"},
            },
        }
        self.mock_env_content = "AWS_ACCESS_KEY_ID=TEST_KEY\nAWS_SECRET_ACCESS_KEY=TEST_SECRET\nSAGEMAKER_ROLE_ARN=arn:aws:iam::123456789012:role/test-role"

    @patch("pathlib.Path.exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_load_config_and_env_vars_successfully(self, mock_file, mock_exists):
        """Test that config and env files are loaded correctly."""
        mock_exists.return_value = True
        # Configure mock_open to handle both yaml and env files
        mock_file.side_effect = [
            mock_open(read_data=yaml.dump(self.mock_config_content)).return_value,
            mock_open(read_data=self.mock_env_content).return_value,
        ]

        with patch("boto3.client"):
            manager = AWSConfigManager()

        self.assertEqual(manager.config, self.mock_config_content)
        self.assertEqual(manager.env_vars["AWS_ACCESS_KEY_ID"], "TEST_KEY")
        self.assertEqual(manager.env_vars["AWS_SECRET_ACCESS_KEY"], "TEST_SECRET")

    @patch("boto3.client")
    def test_validate_aws_credentials_success(self, mock_boto_client):
        """Test successful AWS credential validation."""
        # Mock the S3 client and its list_buckets method
        mock_s3 = MagicMock()
        mock_boto_client.return_value = mock_s3

        manager = AWSConfigManager(
            config_path="nonexistent.yaml", env_path="nonexistent.env"
        )
        manager.s3_client = mock_s3  # Assign the mocked client

        result = manager.validate_aws_credentials()

        self.assertTrue(result)
        mock_s3.list_buckets.assert_called_once()

    @patch("boto3.client")
    def test_validate_aws_credentials_failure(self, mock_boto_client):
        """Test failed AWS credential validation."""
        from botocore.exceptions import ClientError

        mock_s3 = MagicMock()
        mock_s3.list_buckets.side_effect = ClientError(
            {
                "Error": {
                    "Code": "InvalidAccessKeyId",
                    "Message": "Invalid Access Key ID",
                }
            },
            "ListBuckets",
        )
        mock_boto_client.return_value = mock_s3

        manager = AWSConfigManager(
            config_path="nonexistent.yaml", env_path="nonexistent.env"
        )
        manager.s3_client = mock_s3

        result = manager.validate_aws_credentials()

        self.assertFalse(result)
        mock_s3.list_buckets.assert_called_once()

    @patch("boto3.client")
    def test_create_s3_bucket_already_exists(self, mock_boto_client):
        """Test S3 bucket creation when the bucket already exists."""
        mock_s3 = MagicMock()
        mock_boto_client.return_value = mock_s3

        # No exception means head_bucket found the bucket
        mock_s3.head_bucket.return_value = {}

        manager = AWSConfigManager(
            config_path="nonexistent.yaml", env_path="nonexistent.env"
        )
        manager.s3_client = mock_s3
        manager.config = self.mock_config_content  # Manually set config

        result = manager.create_s3_bucket()

        self.assertTrue(result)
        mock_s3.head_bucket.assert_called_once_with(Bucket="test-bucket")
        mock_s3.create_bucket.assert_not_called()

    @patch("boto3.client")
    def test_create_s3_bucket_new_creation(self, mock_boto_client):
        """Test new S3 bucket creation."""
        from botocore.exceptions import ClientError

        mock_s3 = MagicMock()
        mock_boto_client.return_value = mock_s3

        # Simulate bucket not found
        mock_s3.head_bucket.side_effect = ClientError(
            {"Error": {"Code": "404", "Message": "Not Found"}},
            "HeadBucket",
        )

        manager = AWSConfigManager(
            config_path="nonexistent.yaml", env_path="nonexistent.env"
        )
        manager.s3_client = mock_s3
        manager.config = self.mock_config_content

        result = manager.create_s3_bucket()

        self.assertTrue(result)
        mock_s3.head_bucket.assert_called_once_with(Bucket="test-bucket")
        mock_s3.create_bucket.assert_called_once()
        mock_s3.put_bucket_versioning.assert_called_once()
        mock_s3.put_bucket_encryption.assert_called_once()


if __name__ == "__main__":
    unittest.main()
