"""
Google Cloud Storage management for data and model storage.
"""

import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from google.cloud.exceptions import GoogleCloudError, NotFound

logger = logging.getLogger(__name__)


class GCSManager:
    """
    Manages Google Cloud Storage operations for the anomaly detection project.

    This class handles uploading/downloading data and models, managing bucket structure,
    and providing utilities for working with GCS paths.
    """

    def __init__(self, config, authenticator):
        """
        Initialize GCS manager.

        Args:
            config: GCPConfig instance
            authenticator: GCPAuthenticator instance
        """
        self.config = config
        self.authenticator = authenticator
        self.client = authenticator.get_storage_client()
        self.bucket_name = config.storage.bucket_name

        # Ensure bucket exists
        self._ensure_bucket_exists()

        # Create folder structure
        self._create_folder_structure()

    def _ensure_bucket_exists(self) -> None:
        """Ensure the configured bucket exists, create if it doesn't."""
        try:
            bucket = self.client.bucket(self.bucket_name)
            if not bucket.exists():
                logger.info(f"Creating bucket: {self.bucket_name}")
                bucket = self.client.create_bucket(
                    self.bucket_name, location=self.config.auth.region
                )
                logger.info(f"Bucket {self.bucket_name} created successfully")
            else:
                logger.info(f"Bucket {self.bucket_name} already exists")

        except GoogleCloudError as e:
            logger.error(f"Failed to create/access bucket {self.bucket_name}: {e}")
            raise

    def _create_folder_structure(self) -> None:
        """Create the standard folder structure in the bucket."""
        folders = [
            "data/",
            "models/",
            "experiments/",
            "logs/",
            "checkpoints/",
            "mlflow-artifacts/",
        ]

        bucket = self.client.bucket(self.bucket_name)

        for folder in folders:
            blob = bucket.blob(folder)
            if not blob.exists():
                blob.upload_from_string("", content_type="application/x-directory")
                logger.info(f"Created folder: {folder}")

    def upload_file(
        self, local_path: str, gcs_path: str, content_type: Optional[str] = None
    ) -> str:
        """
        Upload a local file to Google Cloud Storage.

        Args:
            local_path: Path to local file
            gcs_path: GCS path (e.g., 'data/dataset.csv')
            content_type: Optional content type

        Returns:
            Full GCS URI of uploaded file
        """
        if not os.path.exists(local_path):
            raise FileNotFoundError(f"Local file not found: {local_path}")

        try:
            bucket = self.client.bucket(self.bucket_name)
            blob = bucket.blob(gcs_path)

            # Set content type if provided
            if content_type:
                blob.content_type = content_type

            # Upload file
            blob.upload_from_filename(local_path)

            gcs_uri = f"gs://{self.bucket_name}/{gcs_path}"
            logger.info(f"Uploaded {local_path} to {gcs_uri}")

            return gcs_uri

        except GoogleCloudError as e:
            logger.error(f"Failed to upload {local_path}: {e}")
            raise

    def upload_directory(self, local_dir: str, gcs_prefix: str) -> List[str]:
        """
        Upload an entire directory to Google Cloud Storage.

        Args:
            local_dir: Path to local directory
            gcs_prefix: GCS prefix for uploaded files

        Returns:
            List of uploaded GCS URIs
        """
        if not os.path.isdir(local_dir):
            raise NotADirectoryError(f"Local directory not found: {local_dir}")

        uploaded_files = []
        local_path = Path(local_dir)

        for file_path in local_path.rglob("*"):
            if file_path.is_file():
                # Calculate relative path from local directory
                relative_path = file_path.relative_to(local_path)
                gcs_path = f"{gcs_prefix}/{relative_path}".replace("\\", "/")

                try:
                    gcs_uri = self.upload_file(str(file_path), gcs_path)
                    uploaded_files.append(gcs_uri)
                except Exception as e:
                    logger.warning(f"Failed to upload {file_path}: {e}")

        logger.info(f"Uploaded {len(uploaded_files)} files from {local_dir}")
        return uploaded_files

    def download_file(self, gcs_path: str, local_path: str) -> str:
        """
        Download a file from Google Cloud Storage.

        Args:
            gcs_path: GCS path (e.g., 'data/dataset.csv')
            local_path: Local path to save file

        Returns:
            Path to downloaded file
        """
        try:
            bucket = self.client.bucket(self.bucket_name)
            blob = bucket.blob(gcs_path)

            if not blob.exists():
                raise NotFound(f"GCS file not found: {gcs_path}")

            # Create local directory if it doesn't exist
            os.makedirs(os.path.dirname(local_path), exist_ok=True)

            # Download file
            blob.download_to_filename(local_path)

            logger.info(f"Downloaded {gcs_path} to {local_path}")
            return local_path

        except GoogleCloudError as e:
            logger.error(f"Failed to download {gcs_path}: {e}")
            raise

    def download_directory(self, gcs_prefix: str, local_dir: str) -> List[str]:
        """
        Download an entire directory from Google Cloud Storage.

        Args:
            gcs_prefix: GCS prefix to download
            local_dir: Local directory to save files

        Returns:
            List of downloaded local file paths
        """
        try:
            bucket = self.client.bucket(self.bucket_name)
            blobs = bucket.list_blobs(prefix=gcs_prefix)

            downloaded_files = []
            os.makedirs(local_dir, exist_ok=True)

            for blob in blobs:
                if not blob.name.endswith("/"):  # Skip directories
                    # Calculate local path
                    relative_path = blob.name[len(gcs_prefix) :].lstrip("/")
                    local_path = os.path.join(local_dir, relative_path)

                    # Create local directory if needed
                    os.makedirs(os.path.dirname(local_path), exist_ok=True)

                    # Download file
                    blob.download_to_filename(local_path)
                    downloaded_files.append(local_path)

            logger.info(f"Downloaded {len(downloaded_files)} files to {local_dir}")
            return downloaded_files

        except GoogleCloudError as e:
            logger.error(f"Failed to download directory {gcs_prefix}: {e}")
            raise

    def list_files(
        self, prefix: str = "", max_results: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        List files in Google Cloud Storage with given prefix.

        Args:
            prefix: GCS prefix to filter files
            max_results: Maximum number of results to return

        Returns:
            List of file information dictionaries
        """
        try:
            bucket = self.client.bucket(self.bucket_name)
            blobs = bucket.list_blobs(prefix=prefix, max_results=max_results)

            files = []
            for blob in blobs:
                if not blob.name.endswith("/"):  # Skip directories
                    file_info = {
                        "name": blob.name,
                        "size": blob.size,
                        "updated": blob.updated,
                        "content_type": blob.content_type,
                        "uri": f"gs://{self.bucket_name}/{blob.name}",
                    }
                    files.append(file_info)

            return files

        except GoogleCloudError as e:
            logger.error(f"Failed to list files with prefix {prefix}: {e}")
            raise

    def delete_file(self, gcs_path: str) -> bool:
        """
        Delete a file from Google Cloud Storage.

        Args:
            gcs_path: GCS path to delete

        Returns:
            True if deleted successfully
        """
        try:
            bucket = self.client.bucket(self.bucket_name)
            blob = bucket.blob(gcs_path)

            if blob.exists():
                blob.delete()
                logger.info(f"Deleted {gcs_path}")
                return True
            else:
                logger.warning(f"File {gcs_path} does not exist")
                return False

        except GoogleCloudError as e:
            logger.error(f"Failed to delete {gcs_path}: {e}")
            raise

    def copy_file(self, source_path: str, dest_path: str) -> str:
        """
        Copy a file within Google Cloud Storage.

        Args:
            source_path: Source GCS path
            dest_path: Destination GCS path

        Returns:
            Full GCS URI of copied file
        """
        try:
            bucket = self.client.bucket(self.bucket_name)
            source_blob = bucket.blob(source_path)
            dest_blob = bucket.blob(dest_path)

            if not source_blob.exists():
                raise NotFound(f"Source file not found: {source_path}")

            # Copy file
            bucket.copy_blob(source_blob, bucket, dest_blob)

            gcs_uri = f"gs://{self.bucket_name}/{dest_path}"
            logger.info(f"Copied {source_path} to {gcs_uri}")

            return gcs_uri

        except GoogleCloudError as e:
            logger.error(f"Failed to copy {source_path} to {dest_path}: {e}")
            raise

    def get_file_metadata(self, gcs_path: str) -> Dict[str, Any]:
        """
        Get metadata for a file in Google Cloud Storage.

        Args:
            gcs_path: GCS path to get metadata for

        Returns:
            Dictionary with file metadata
        """
        try:
            bucket = self.client.bucket(self.bucket_name)
            blob = bucket.blob(gcs_path)

            if not blob.exists():
                raise NotFound(f"File not found: {gcs_path}")

            # Reload blob to get latest metadata
            blob.reload()

            metadata = {
                "name": blob.name,
                "size": blob.size,
                "updated": blob.updated,
                "created": blob.time_created,
                "content_type": blob.content_type,
                "md5_hash": blob.md5_hash,
                "crc32c": blob.crc32c,
                "etag": blob.etag,
                "uri": f"gs://{self.bucket_name}/{blob.name}",
            }

            # Add custom metadata if any
            if blob.metadata:
                metadata["custom_metadata"] = blob.metadata

            return metadata

        except GoogleCloudError as e:
            logger.error(f"Failed to get metadata for {gcs_path}: {e}")
            raise

    def set_file_metadata(self, gcs_path: str, metadata: Dict[str, str]) -> None:
        """
        Set custom metadata for a file in Google Cloud Storage.

        Args:
            gcs_path: GCS path to set metadata for
            metadata: Dictionary of metadata key-value pairs
        """
        try:
            bucket = self.client.bucket(self.bucket_name)
            blob = bucket.blob(gcs_path)

            if not blob.exists():
                raise NotFound(f"File not found: {gcs_path}")

            # Set metadata
            blob.metadata = metadata
            blob.patch()

            logger.info(f"Set metadata for {gcs_path}: {metadata}")

        except GoogleCloudError as e:
            logger.error(f"Failed to set metadata for {gcs_path}: {e}")
            raise

    def get_bucket_info(self) -> Dict[str, Any]:
        """Get information about the configured bucket."""
        try:
            bucket = self.client.bucket(self.bucket_name)
            bucket.reload()

            info = {
                "name": bucket.name,
                "location": bucket.location,
                "storage_class": bucket.storage_class,
                "created": bucket.time_created,
                "updated": bucket.updated,
                "versioning_enabled": bucket.versioning_enabled,
                "labels": bucket.labels or {},
                "uri": f"gs://{bucket.name}",
            }

            return info

        except GoogleCloudError as e:
            logger.error(f"Failed to get bucket info: {e}")
            raise

    def __repr__(self) -> str:
        """String representation of GCS manager."""
        return f"GCSManager(bucket={self.bucket_name}, project={self.authenticator.project_id})"
