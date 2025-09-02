"""
Google Cloud Platform (GCP) integration module for Petrobras Offshore Wells Anomaly Detection.

This module provides integration with Google Cloud services including:
- Vertex AI for model training and deployment
- AI Platform for distributed training
- Cloud Storage for data and model storage
- Cloud Logging and Monitoring
- MLflow integration with GCS
"""

from .config import GCPConfig
from .auth import GCPAuthenticator
from .storage import GCSManager
from .vertex_ai import VertexAIManager
from .training import AIPlatformTrainer
from .mlflow_integration import MLflowGCSIntegration

__version__ = "1.0.0"
__all__ = [
    "GCPConfig",
    "GCPAuthenticator",
    "GCSManager",
    "VertexAIManager",
    "AIPlatformTrainer",
    "MLflowGCSIntegration",
]
