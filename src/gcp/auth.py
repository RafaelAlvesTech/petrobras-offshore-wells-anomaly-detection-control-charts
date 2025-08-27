"""
Google Cloud Platform authentication management.
"""

import os
from typing import Any, Dict

from google.auth import default
from google.auth.exceptions import DefaultCredentialsError, GoogleAuthError
from google.auth.transport.requests import Request
from google.cloud import aiplatform, logging, monitoring, storage
from google.oauth2 import service_account


class GCPAuthenticator:
    """
    Manages Google Cloud Platform authentication and client initialization.

    This class handles authentication using either service account keys
    or application default credentials, and provides initialized clients
    for various Google Cloud services.
    """

    def __init__(self, config):
        """
        Initialize GCP authenticator.

        Args:
            config: GCPConfig instance containing authentication settings
        """
        self.config = config
        self.credentials = None
        self.project_id = None
        self.clients = {}

        # Initialize authentication
        self._authenticate()

    def _authenticate(self) -> None:
        """Authenticate with Google Cloud Platform."""
        try:
            if self.config.auth.service_account_key_path:
                self._authenticate_with_service_account()
            else:
                self._authenticate_with_default_credentials()

            # Set project ID
            if self.config.auth.project_id:
                self.project_id = self.config.auth.project_id
            elif self.credentials:
                self.project_id = self.credentials.project_id

            if not self.project_id:
                raise GoogleAuthError(
                    "No project ID found in credentials or configuration"
                )

        except Exception as e:
            raise GoogleAuthError(f"Authentication failed: {str(e)}")

    def _authenticate_with_service_account(self) -> None:
        """Authenticate using service account key file."""
        key_path = self.config.auth.service_account_key_path

        if not os.path.exists(key_path):
            raise FileNotFoundError(f"Service account key file not found: {key_path}")

        try:
            self.credentials = service_account.Credentials.from_service_account_file(
                key_path,
                scopes=[
                    "https://www.googleapis.com/auth/cloud-platform",
                    "https://www.googleapis.com/auth/cloud-platform.read-only",
                ],
            )

            # Refresh credentials
            self.credentials.refresh(Request())

        except Exception as e:
            raise GoogleAuthError(
                f"Failed to load service account credentials: {str(e)}"
            )

    def _authenticate_with_default_credentials(self) -> None:
        """Authenticate using application default credentials."""
        try:
            self.credentials, self.project_id = default(
                scopes=[
                    "https://www.googleapis.com/auth/cloud-platform",
                    "https://www.googleapis.com/auth/cloud-platform.read-only",
                ]
            )

        except DefaultCredentialsError:
            raise GoogleAuthError(
                "Application default credentials not found. "
                "Run 'gcloud auth application-default login' or set GOOGLE_APPLICATION_CREDENTIALS"
            )

    def get_client(self, service_name: str):
        """
        Get or create a Google Cloud client for the specified service.

        Args:
            service_name: Name of the service (storage, aiplatform, logging, monitoring)

        Returns:
            Initialized Google Cloud client
        """
        if service_name not in self.clients:
            self.clients[service_name] = self._create_client(service_name)

        return self.clients[service_name]

    def _create_client(self, service_name: str):
        """Create a new Google Cloud client."""
        if service_name == "storage":
            return storage.Client(project=self.project_id, credentials=self.credentials)
        elif service_name == "aiplatform":
            return aiplatform.Client(
                project=self.project_id,
                location=self.config.vertex_ai.location,
                credentials=self.credentials,
            )
        elif service_name == "logging":
            return logging.Client(project=self.project_id, credentials=self.credentials)
        elif service_name == "monitoring":
            return monitoring.MetricServiceClient(credentials=self.credentials)
        else:
            raise ValueError(f"Unknown service: {service_name}")

    def get_storage_client(self):
        """Get Cloud Storage client."""
        return self.get_client("storage")

    def get_aiplatform_client(self):
        """Get Vertex AI client."""
        return self.get_client("aiplatform")

    def get_logging_client(self):
        """Get Cloud Logging client."""
        return self.get_client("logging")

    def get_monitoring_client(self):
        """Get Cloud Monitoring client."""
        return self.get_client("monitoring")

    def test_authentication(self) -> Dict[str, Any]:
        """
        Test authentication with all services.

        Returns:
            Dictionary with authentication test results
        """
        results = {
            "authenticated": False,
            "project_id": self.project_id,
            "services": {},
            "errors": [],
        }

        try:
            # Test basic authentication
            if self.credentials and self.project_id:
                results["authenticated"] = True

                # Test each service
                services = ["storage", "aiplatform", "logging", "monitoring"]

                for service in services:
                    try:
                        client = self.get_client(service)
                        # Try to make a simple API call
                        if service == "storage":
                            # List buckets
                            list(client.list_buckets(max_results=1))
                        elif service == "aiplatform":
                            # List experiments
                            client.list_experiments()
                        elif service == "logging":
                            # List log entries
                            client.list_entries(max_results=1)
                        elif service == "monitoring":
                            # List metric descriptors
                            client.list_metric_descriptors(
                                name=f"projects/{self.project_id}"
                            )

                        results["services"][service] = "OK"

                    except Exception as e:
                        results["services"][service] = f"ERROR: {str(e)}"
                        results["errors"].append(f"{service}: {str(e)}")

        except Exception as e:
            results["errors"].append(f"Authentication test failed: {str(e)}")

        return results

    def get_credentials_info(self) -> Dict[str, Any]:
        """Get information about current credentials."""
        if not self.credentials:
            return {"error": "No credentials available"}

        info = {
            "type": type(self.credentials).__name__,
            "project_id": getattr(self.credentials, "project_id", None),
            "service_account_email": getattr(
                self.credentials, "service_account_email", None
            ),
            "expired": self.credentials.expired
            if hasattr(self.credentials, "expired")
            else None,
            "valid": not self.credentials.expired
            if hasattr(self.credentials, "expired")
            else None,
        }

        # Add scopes if available
        if hasattr(self.credentials, "scopes"):
            info["scopes"] = list(self.credentials.scopes)

        return info

    def refresh_credentials(self) -> None:
        """Refresh credentials if they're expired."""
        if self.credentials and hasattr(self.credentials, "refresh"):
            try:
                self.credentials.refresh(Request())
            except Exception as e:
                raise GoogleAuthError(f"Failed to refresh credentials: {str(e)}")

    def __repr__(self) -> str:
        """String representation of authenticator."""
        return f"GCPAuthenticator(project={self.project_id}, authenticated={self.credentials is not None})"
