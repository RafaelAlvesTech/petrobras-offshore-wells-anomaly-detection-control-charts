#!/usr/bin/env python3
"""
MLflow Server for Google Cloud Run
This server provides experiment tracking for the anomaly detection project.
"""

import logging
import os
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """Start MLflow server."""
    try:
        import mlflow
        from mlflow.server import app

        # Get configuration from environment
        tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "sqlite:///mlflow.db")
        backend_store_uri = os.getenv("MLFLOW_BACKEND_STORE_URI", tracking_uri)
        default_artifact_root = os.getenv("MLFLOW_DEFAULT_ARTIFACT_ROOT", "/mlflow")

        # Set MLflow configuration
        mlflow.set_tracking_uri(tracking_uri)

        # Create MLflow directories
        Path("/mlflow").mkdir(exist_ok=True)

        logger.info("Starting MLflow server...")
        logger.info(f"Tracking URI: {tracking_uri}")
        logger.info(f"Backend Store URI: {backend_store_uri}")
        logger.info(f"Default Artifact Root: {default_artifact_root}")

        # Start server
        app.run(host="0.0.0.0", port=5000, debug=False)

    except ImportError as e:
        logger.error(f"Failed to import MLflow: {e}")
        logger.error("Please install MLflow: pip install mlflow")
        exit(1)
    except Exception as e:
        logger.error(f"Failed to start MLflow server: {e}")
        exit(1)


if __name__ == "__main__":
    main()
