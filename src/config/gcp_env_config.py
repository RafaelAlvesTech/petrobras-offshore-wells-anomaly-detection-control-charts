"""
GCP Configuration with Environment Variables
Secure configuration loading for Google Cloud Platform credentials.
"""

import os
from pathlib import Path


class GCPEnvConfig:
    """Secure GCP configuration using environment variables."""

    def __init__(self):
        """Initialize GCP configuration from environment variables."""
        self.project_id = self._get_required_env("GCP_PROJECT_ID")
        self.region = self._get_env("GCP_REGION", "us-central1")
        self.zone = self._get_env("GCP_ZONE", "us-central1-a")
        self.bucket_name = self._get_required_env("GCP_BUCKET_NAME")
        self.vertex_ai_location = self._get_env("VERTEX_AI_LOCATION", "us-central1")

        # Authentication
        self.service_account_path = self._get_env("GOOGLE_APPLICATION_CREDENTIALS")

        # Validate configuration
        self._validate_config()

    def _get_required_env(self, key: str) -> str:
        """Get required environment variable."""
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Required environment variable {key} not found")
        return value

    def _get_env(self, key: str, default: str = "") -> str:
        """Get environment variable with default."""
        return os.getenv(key, default)

    def _validate_config(self) -> None:
        """Validate GCP configuration."""
        if self.service_account_path:
            if not Path(self.service_account_path).exists():
                raise FileNotFoundError(
                    f"Service account key file not found: {self.service_account_path}"
                )

    def get_storage_paths(self) -> dict[str, str]:
        """Get GCS storage paths."""
        base_path = f"gs://{self.bucket_name}"
        return {
            "data": f"{base_path}/data",
            "models": f"{base_path}/models",
            "experiments": f"{base_path}/experiments",
            "logs": f"{base_path}/logs",
            "checkpoints": f"{base_path}/checkpoints",
            "tensorboard": f"{base_path}/tensorboard-logs",
            "mlflow_artifacts": f"{base_path}/mlflow-artifacts",
        }

    def get_vertex_ai_config(self) -> dict[str, str]:
        """Get Vertex AI configuration."""
        return {
            "project_id": self.project_id,
            "location": self.vertex_ai_location,
            "experiment_name": "petrobras-anomaly-detection",
            "model_registry_name": "anomaly-detection-models",
        }

    def is_configured(self) -> bool:
        """Check if GCP is properly configured."""
        try:
            return bool(self.project_id and self.bucket_name)
        except ValueError:
            return False


# Global instance
def get_gcp_config():
    """Get GCP config instance if properly configured."""
    try:
        return GCPEnvConfig()
    except ValueError:
        return None


gcp_config = get_gcp_config()
