#!/usr/bin/env python3
"""
Example script for training LSTM-VAE anomaly detection model on Google Cloud Platform.

This script demonstrates how to use the GCP integration modules to:
1. Configure and authenticate with Google Cloud
2. Upload training data to Cloud Storage
3. Create and submit training jobs
4. Track experiments with MLflow
5. Deploy trained models
"""

import argparse
import logging
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gcp.auth import GCPAuthenticator
from gcp.config import GCPConfig
from gcp.mlflow_integration import MLflowGCSIntegration
from gcp.storage import GCSManager
from gcp.training import AIPlatformTrainer
from gcp.vertex_ai import VertexAIManager


def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def main():
    """Main training function."""
    parser = argparse.ArgumentParser(description="Train LSTM-VAE model on GCP")
    parser.add_argument(
        "--config", default="gcp-config.yaml", help="Path to GCP config file"
    )
    parser.add_argument("--data-path", required=True, help="Path to training data")
    parser.add_argument(
        "--model-name", default="lstm-vae-anomaly-detection", help="Name for the model"
    )
    parser.add_argument(
        "--epochs", type=int, default=150, help="Number of training epochs"
    )
    parser.add_argument(
        "--batch-size", type=int, default=64, help="Training batch size"
    )
    parser.add_argument(
        "--learning-rate", type=float, default=0.0001, help="Learning rate"
    )
    parser.add_argument(
        "--use-vertex-ai",
        action="store_true",
        help="Use Vertex AI instead of AI Platform",
    )

    args = parser.parse_args()

    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("Starting LSTM-VAE model training on Google Cloud Platform")
    logger.info(f"Arguments: {vars(args)}")

    try:
        # Initialize GCP configuration
        logger.info("Initializing GCP configuration...")
        config = GCPConfig(config_path=args.config)

        # Initialize authentication
        logger.info("Authenticating with Google Cloud...")
        authenticator = GCPAuthenticator(config)

        # Test authentication
        auth_test = authenticator.test_authentication()
        if not auth_test["authenticated"]:
            logger.error("Authentication failed!")
            logger.error(f"Errors: {auth_test['errors']}")
            sys.exit(1)

        logger.info("Authentication successful!")
        logger.info(f"Project ID: {authenticator.project_id}")

        # Initialize GCS manager
        logger.info("Initializing Cloud Storage manager...")
        gcs_manager = GCSManager(config, authenticator)

        # Upload training data
        logger.info("Uploading training data to Cloud Storage...")
        data_gcs_uri = gcs_manager.upload_file(
            args.data_path, f"data/lstm_vae_training_data_{Path(args.data_path).name}"
        )
        logger.info(f"Training data uploaded to: {data_gcs_uri}")

        # Initialize MLflow integration
        logger.info("Initializing MLflow integration...")
        mlflow_integration = MLflowGCSIntegration(config, authenticator)

        # Start MLflow run
        run_name = f"lstm_vae_training_{args.model_name}_{args.epochs}epochs"
        with mlflow_integration.start_run(run_name=run_name):
            # Log parameters
            params = {
                "model_type": "lstm_vae",
                "epochs": args.epochs,
                "batch_size": args.batch_size,
                "learning_rate": args.learning_rate,
                "data_path": data_gcs_uri,
                "model_name": args.model_name,
            }
            mlflow_integration.log_params(params)

            if args.use_vertex_ai:
                # Use Vertex AI for training
                logger.info("Using Vertex AI for training...")
                vertex_ai = VertexAIManager(config, authenticator)

                # Create training job
                training_job = vertex_ai.create_custom_training_job(
                    display_name=f"lstm-vae-training-{args.model_name}",
                    script_path="gs://your-bucket/training_scripts/train_lstm_vae.py",
                    requirements=[
                        "torch>=2.0.1",
                        "polars>=1.32.3",
                        "scikit-learn>=1.7.1",
                        "numpy>=1.24.0",
                    ],
                    machine_type="n1-standard-4",
                    accelerator_type="NVIDIA_TESLA_T4",
                    accelerator_count=1,
                )

                # Start training
                running_job = vertex_ai.start_training_job(training_job)

                # Log job information
                mlflow_integration.log_artifact(
                    f"Job ID: {running_job.name}", "training_job_info.txt"
                )

                logger.info(f"Training job started: {running_job.name}")

            else:
                # Use AI Platform for training
                logger.info("Using AI Platform for training...")
                ai_trainer = AIPlatformTrainer(config, authenticator)

                # Create training script
                script_path = ai_trainer.create_training_script(
                    script_name=f"train_lstm_vae_{args.model_name}",
                    model_type="lstm_vae",
                    epochs=args.epochs,
                    batch_size=args.batch_size,
                    learning_rate=args.learning_rate,
                )

                # Upload training script
                script_gcs_uri = gcs_manager.upload_file(
                    script_path, f"training_scripts/train_lstm_vae_{args.model_name}.py"
                )

                # Submit training job
                job_id = ai_trainer.submit_training_job(
                    job_name=f"lstm-vae-training-{args.model_name}",
                    script_path=script_gcs_uri,
                    requirements=[
                        "torch>=2.0.1",
                        "polars>=1.32.3",
                        "scikit-learn>=1.7.1",
                        "numpy>=1.24.0",
                    ],
                    machine_type="n1-standard-4",
                    accelerator_type="NVIDIA_TESLA_T4",
                    accelerator_count=1,
                )

                # Log job information
                mlflow_integration.log_artifact(
                    f"Job ID: {job_id}", "training_job_info.txt"
                )

                logger.info(f"Training job submitted: {job_id}")

                # Wait for job completion (optional)
                try:
                    final_state = ai_trainer.wait_for_job_completion(
                        job_id, timeout_minutes=180
                    )
                    logger.info(f"Training job completed with state: {final_state}")

                    # Log final metrics
                    if final_state == "SUCCEEDED":
                        # Get job logs
                        logs = ai_trainer.get_job_logs(job_id)
                        mlflow_integration.log_artifact(logs, "training_logs.txt")

                        # Log success metrics
                        mlflow_integration.log_metrics(
                            {
                                "training_status": 1.0,
                                "job_completion_time": 180.0,  # minutes
                            }
                        )
                    else:
                        mlflow_integration.log_metrics(
                            {"training_status": 0.0, "job_final_state": 0.0}
                        )

                except TimeoutError:
                    logger.warning("Training job did not complete within timeout")
                    mlflow_integration.log_metrics(
                        {"training_status": 0.5, "timeout": 1.0}
                    )

            # Log completion
            mlflow_integration.log_metrics(
                {"training_initiated": 1.0, "data_uploaded": 1.0}
            )

            logger.info("Training setup completed successfully!")

    except Exception as e:
        logger.error(f"Training setup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
