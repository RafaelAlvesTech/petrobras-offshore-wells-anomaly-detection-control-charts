"""
Configuration management for Google Cloud Platform integration.
"""

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import yaml
from dotenv import load_dotenv


@dataclass
class GCPAuthConfig:
    """Configuration for GCP authentication."""

    service_account_key_path: Optional[str] = None
    application_default_credentials: bool = True
    project_id: Optional[str] = None
    region: str = "us-central1"
    zone: str = "us-central1-a"


@dataclass
class VertexAIConfig:
    """Configuration for Vertex AI."""

    location: str = "us-central1"
    experiment_name: str = "petrobras-anomaly-detection"
    model_registry_name: str = "anomaly-detection-models"
    default_machine_type: str = "n1-standard-4"
    default_accelerator_type: str = "NVIDIA_TESLA_T4"
    default_accelerator_count: int = 1


@dataclass
class AIPlatformConfig:
    """Configuration for AI Platform Training."""

    region: str = "us-central1"
    scale_tier: str = "BASIC_GPU"
    master_type: str = "n1-standard-4"
    worker_type: str = "n1-standard-4"
    worker_count: int = 2


@dataclass
class CloudStorageConfig:
    """Configuration for Cloud Storage."""

    bucket_name: str = "your-bucket-name"
    data_path: str = "gs://{bucket}/data"
    models_path: str = "gs://{bucket}/models"
    experiments_path: str = "gs://{bucket}/experiments"
    logs_path: str = "gs://{bucket}/logs"
    checkpoints_path: str = "gs://{bucket}/checkpoints"


@dataclass
class MLflowConfig:
    """Configuration for MLflow integration."""

    tracking_uri: str = "http://localhost:5000"
    experiment_name: str = "petrobras-anomaly-detection"
    artifacts_storage: str = "gcs"
    artifacts_bucket: str = "your-bucket-name"
    artifacts_path: str = "mlflow-artifacts"


@dataclass
class TrainingConfig:
    """Configuration for model training."""

    batch_size: int = 32
    learning_rate: float = 0.001
    epochs: int = 100
    validation_split: float = 0.2


class GCPConfig:
    """
    Main configuration class for Google Cloud Platform integration.

    This class manages all GCP-related configurations including authentication,
    Vertex AI, AI Platform Training, Cloud Storage, and MLflow integration.
    """

    def __init__(
        self, config_path: Optional[str] = None, env_file: Optional[str] = None
    ):
        """
        Initialize GCP configuration.

        Args:
            config_path: Path to YAML configuration file
            env_file: Path to environment file (.env)
        """
        # Load environment variables first
        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv()

        # Load YAML configuration if provided
        self._yaml_config = {}
        if config_path:
            self._load_yaml_config(config_path)

        # Initialize configuration sections
        self.auth = self._init_auth_config()
        self.vertex_ai = self._init_vertex_ai_config()
        self.ai_platform = self._init_ai_platform_config()
        self.storage = self._init_storage_config()
        self.mlflow = self._init_mlflow_config()
        self.training = self._init_training_config()

        # Validate configuration
        self._validate_config()

    def _load_yaml_config(self, config_path: str) -> None:
        """Load configuration from YAML file."""
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                self._yaml_config = yaml.safe_load(f)
        except FileNotFoundError:
            print(
                f"Warning: Configuration file {config_path} not found. Using defaults."
            )
        except yaml.YAMLError as e:
            print(
                f"Warning: Error parsing YAML file {config_path}: {e}. Using defaults."
            )

    def _get_config_value(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value from YAML or environment variables.

        Args:
            key_path: Dot-separated path to configuration key
            default: Default value if not found

        Returns:
            Configuration value or default
        """
        # Try YAML first
        keys = key_path.split(".")
        value = self._yaml_config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                value = None
                break

        if value is not None:
            return value

        # Try environment variable
        env_key = key_path.upper().replace(".", "_")
        return os.getenv(env_key, default)

    def _init_auth_config(self) -> GCPAuthConfig:
        """Initialize authentication configuration."""
        return GCPAuthConfig(
            service_account_key_path=self._get_config_value(
                "google_cloud.authentication.service_account_key_path",
                os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
            ),
            application_default_credentials=self._get_config_value(
                "google_cloud.authentication.application_default_credentials", True
            ),
            project_id=self._get_config_value(
                "google_cloud.project_id", os.getenv("GOOGLE_CLOUD_PROJECT")
            ),
            region=self._get_config_value(
                "google_cloud.region", os.getenv("GOOGLE_CLOUD_REGION", "us-central1")
            ),
            zone=self._get_config_value(
                "google_cloud.zone", os.getenv("GOOGLE_CLOUD_ZONE", "us-central1-a")
            ),
        )

    def _init_vertex_ai_config(self) -> VertexAIConfig:
        """Initialize Vertex AI configuration."""
        return VertexAIConfig(
            location=self._get_config_value(
                "vertex_ai.location", os.getenv("VERTEX_AI_LOCATION", "us-central1")
            ),
            experiment_name=self._get_config_value(
                "vertex_ai.experiment.name",
                os.getenv("VERTEX_AI_EXPERIMENT_NAME", "petrobras-anomaly-detection"),
            ),
            model_registry_name=self._get_config_value(
                "vertex_ai.model_registry.name", "anomaly-detection-models"
            ),
            default_machine_type=self._get_config_value(
                "vertex_ai.training_jobs.default_machine_type", "n1-standard-4"
            ),
            default_accelerator_type=self._get_config_value(
                "vertex_ai.training_jobs.default_accelerator_type", "NVIDIA_TESLA_T4"
            ),
            default_accelerator_count=self._get_config_value(
                "vertex_ai.training_jobs.default_accelerator_count", 1
            ),
        )

    def _init_ai_platform_config(self) -> AIPlatformConfig:
        """Initialize AI Platform configuration."""
        return AIPlatformConfig(
            region=self._get_config_value(
                "ai_platform_training.region",
                os.getenv("AI_PLATFORM_TRAINING_REGION", "us-central1"),
            ),
            scale_tier=self._get_config_value(
                "ai_platform_training.scale_tiers.basic_gpu",
                os.getenv("AI_PLATFORM_TRAINING_SCALE_TIER", "BASIC_GPU"),
            ),
            master_type=self._get_config_value(
                "ai_platform_training.machine_types.master.0",
                os.getenv("AI_PLATFORM_TRAINING_MASTER_TYPE", "n1-standard-4"),
            ),
            worker_type=self._get_config_value(
                "ai_platform_training.machine_types.worker.0",
                os.getenv("AI_PLATFORM_TRAINING_WORKER_TYPE", "n1-standard-4"),
            ),
            worker_count=self._get_config_value(
                "ai_platform_training.worker_count",
                int(os.getenv("AI_PLATFORM_TRAINING_WORKER_COUNT", "2")),
            ),
        )

    def _init_storage_config(self) -> CloudStorageConfig:
        """Initialize Cloud Storage configuration."""
        bucket_name = self._get_config_value(
            "cloud_storage.bucket_name",
            os.getenv("GCS_BUCKET_NAME", "your-bucket-name"),
        )

        return CloudStorageConfig(
            bucket_name=bucket_name,
            data_path=self._get_config_value(
                "cloud_storage.paths.data", f"gs://{bucket_name}/data"
            ),
            models_path=self._get_config_value(
                "cloud_storage.paths.models", f"gs://{bucket_name}/models"
            ),
            experiments_path=self._get_config_value(
                "cloud_storage.paths.experiments", f"gs://{bucket_name}/experiments"
            ),
            logs_path=self._get_config_value(
                "cloud_storage.paths.logs", f"gs://{bucket_name}/logs"
            ),
            checkpoints_path=self._get_config_value(
                "cloud_storage.paths.checkpoints", f"gs://{bucket_name}/checkpoints"
            ),
        )

    def _init_mlflow_config(self) -> MLflowConfig:
        """Initialize MLflow configuration."""
        return MLflowConfig(
            tracking_uri=self._get_config_value(
                "mlflow.tracking_uri",
                os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000"),
            ),
            experiment_name=self._get_config_value(
                "mlflow.experiment_name",
                os.getenv("MLFLOW_EXPERIMENT_NAME", "petrobras-anomaly-detection"),
            ),
            artifacts_storage=self._get_config_value("mlflow.artifacts.storage", "gcs"),
            artifacts_bucket=self._get_config_value(
                "mlflow.artifacts.bucket",
                os.getenv("GCS_BUCKET_NAME", "your-bucket-name"),
            ),
            artifacts_path=self._get_config_value(
                "mlflow.artifacts.path", "mlflow-artifacts"
            ),
        )

    def _init_training_config(self) -> TrainingConfig:
        """Initialize training configuration."""
        return TrainingConfig(
            batch_size=int(
                self._get_config_value(
                    "training.default.batch_size", os.getenv("MODEL_BATCH_SIZE", "32")
                )
            ),
            learning_rate=float(
                self._get_config_value(
                    "training.default.learning_rate",
                    os.getenv("MODEL_LEARNING_RATE", "0.001"),
                )
            ),
            epochs=int(
                self._get_config_value(
                    "training.default.epochs", os.getenv("MODEL_EPOCHS", "100")
                )
            ),
            validation_split=float(
                self._get_config_value(
                    "training.default.validation_split",
                    os.getenv("MODEL_VALIDATION_SPLIT", "0.2"),
                )
            ),
        )

    def _validate_config(self) -> None:
        """Validate configuration and print warnings for missing values."""
        warnings = []

        if not self.auth.project_id:
            warnings.append("GOOGLE_CLOUD_PROJECT not set")

        if (
            not self.auth.service_account_key_path
            and not self.auth.application_default_credentials
        ):
            warnings.append("No authentication method configured")

        if self.storage.bucket_name == "your-bucket-name":
            warnings.append("GCS_BUCKET_NAME not configured")

        if warnings:
            print("Configuration warnings:")
            for warning in warnings:
                print(f"  - {warning}")

    def get_required_apis(self) -> list:
        """Get list of required Google Cloud APIs."""
        return self._get_config_value(
            "google_cloud.required_apis",
            [
                "aiplatform.googleapis.com",
                "ml.googleapis.com",
                "storage.googleapis.com",
                "logging.googleapis.com",
                "monitoring.googleapis.com",
                "compute.googleapis.com",
                "cloudbuild.googleapis.com",
            ],
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "auth": self.auth.__dict__,
            "vertex_ai": self.vertex_ai.__dict__,
            "ai_platform": self.ai_platform.__dict__,
            "storage": self.storage.__dict__,
            "mlflow": self.mlflow.__dict__,
            "training": self.training.__dict__,
            "required_apis": self.get_required_apis(),
        }

    def __repr__(self) -> str:
        """String representation of configuration."""
        return f"GCPConfig(project={self.auth.project_id}, region={self.auth.region})"
