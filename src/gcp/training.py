"""
AI Platform Training management for distributed model training.
"""

import json
import logging
import os
import subprocess
from typing import Any

from google.cloud.aiplatform_v1 import CreateCustomJobRequest, JobServiceClient
from google.cloud.aiplatform_v1.types import (
    ContainerSpec,
    CustomJobSpec,
    MachineSpec,
    Scheduling,
    CustomJob,
    WorkerPoolSpec,
)

logger = logging.getLogger(__name__)


class AIPlatformTrainer:
    """
    Manages AI Platform Training jobs for distributed model training.

    This class handles job submission, monitoring, and management for
    training jobs on Google Cloud AI Platform.
    """

    def __init__(self, config, authenticator):
        """
        Initialize AI Platform trainer.

        Args:
            config: GCPConfig instance
            authenticator: GCPAuthenticator instance
        """
        self.config = config
        self.authenticator = authenticator
        self.project_id = authenticator.project_id
        self.region = config.ai_platform.region

        # Initialize AI Platform client
        self.client = JobServiceClient(credentials=authenticator.credentials)

        logger.info(f"Initialized AI Platform trainer for project {self.project_id}")

    def create_training_job(
        self,
        display_name: str,
        script_path: str,
        requirements: list[str],
        machine_type: str | None = None,
        accelerator_type: str | None = None,
        accelerator_count: int | None = None,
        worker_count: int | None = None,
        **kwargs,
    ) -> CustomJob:
        """
        Create a training job on AI Platform.

        Args:
            display_name: Name for the training job
            script_path: GCS path to training script
            requirements: List of Python requirements
            machine_type: Machine type for training
            accelerator_type: GPU accelerator type
            accelerator_count: Number of accelerators
            worker_count: Number of worker nodes
            **kwargs: Additional arguments

        Returns:
            CustomJob instance
        """
        # Use defaults from config if not specified
        machine_type = machine_type or self.config.ai_platform.master_type
        accelerator_type = accelerator_type or "NVIDIA_TESLA_T4"
        accelerator_count = accelerator_count or 1
        worker_count = worker_count or self.config.ai_platform.worker_count

        try:
            # Create container spec
            container_spec = ContainerSpec(
                image_uri=f"gcr.io/{self.project_id}/anomaly-detection-training:latest",
                command=["python"],
                args=[script_path],
                env=[
                    {"name": "GOOGLE_CLOUD_PROJECT", "value": self.project_id},
                    {"name": "GOOGLE_CLOUD_REGION", "value": self.region},
                ],
            )

            # Create machine spec
            machine_spec = MachineSpec(
                machine_type=machine_type,
                accelerator_type=accelerator_type,
                accelerator_count=accelerator_count,
            )

            # Create worker pool spec
            worker_pool_spec = WorkerPoolSpec(
                machine_spec=machine_spec,
                replica_count=worker_count,
                container_spec=container_spec,
            )

            # Create custom job spec
            custom_job_spec = CustomJobSpec(
                worker_pool_specs=[worker_pool_spec],
                scheduling=Scheduling(timeout="7200s"),  # 2 hours
            )

            # Create training job request
            request = CreateCustomJobRequest(
                parent=f"projects/{self.project_id}/locations/{self.region}",
                custom_job=CustomJob(
                    display_name=display_name, custom_job=custom_job_spec
                ),
            )

            # Submit job
            operation = self.client.create_custom_job(request=request)
            training_job = operation.result()

            logger.info(f"Created training job: {display_name}")
            logger.info(f"Job ID: {training_job.name}")

            return training_job

        except Exception as e:
            logger.error(f"Failed to create training job {display_name}: {e}")
            raise

    def submit_training_job(
        self, job_name: str, script_path: str, requirements: list[str], **kwargs
    ) -> str:
        """
        Submit a training job using gcloud CLI.

        Args:
            job_name: Name for the training job
            script_path: GCS path to training script
            requirements: List of Python requirements
            **kwargs: Additional arguments

        Returns:
            Job ID
        """
        try:
            # Build gcloud command
            cmd = [
                "gcloud",
                "ai",
                "custom-jobs",
                "create",
                f"--display-name={job_name}",
                f"--region={self.region}",
                f"--project={self.project_id}",
                "--worker-pool-spec=replica-count=1,machine-type=n1-standard-4,container-image-uri=gcr.io/cloud-aiplatform/training/pytorch-gpu.1-13:latest,exec=python,args=--help",
            ]

            # Add custom arguments
            if "machine_type" in kwargs:
                cmd.extend(
                    ["--worker-pool-spec", f"machine-type={kwargs['machine_type']}"]
                )

            if "accelerator_type" in kwargs:
                cmd.extend(
                    [
                        "--worker-pool-spec",
                        f"accelerator-type={kwargs['accelerator_type']}",
                    ]
                )

            if "accelerator_count" in kwargs:
                cmd.extend(
                    [
                        "--worker-pool-spec",
                        f"accelerator-count={kwargs['accelerator_count']}",
                    ]
                )

            # Execute command
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)

            # Extract job ID from output
            job_id = self._extract_job_id(result.stdout)

            logger.info(f"Submitted training job: {job_name}")
            logger.info(f"Job ID: {job_id}")

            return job_id

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to submit training job {job_name}: {e}")
            logger.error(f"stderr: {e.stderr}")
            raise
        except Exception as e:
            logger.error(f"Failed to submit training job {job_name}: {e}")
            raise

    def _extract_job_id(self, output: str) -> str:
        """Extract job ID from gcloud command output."""
        # This is a simple extraction - you might need to adjust based on actual output format
        lines = output.split("\n")
        for line in lines:
            if (
                "projects/" in line
                and "/locations/" in line
                and "/trainingJobs/" in line
            ):
                return line.strip()

        # Fallback: try to find any line with trainingJobs
        for line in lines:
            if "trainingJobs/" in line:
                parts = line.split("trainingJobs/")
                if len(parts) > 1:
                    return parts[1].strip()

        raise ValueError("Could not extract job ID from output")

    def get_training_job(self, job_id: str) -> dict[str, Any]:
        """
        Get information about a training job.

        Args:
            job_id: Training job ID

        Returns:
            Dictionary with job information
        """
        try:
            # Use gcloud to get job info
            cmd = [
                "gcloud",
                "ai",
                "custom-jobs",
                "describe",
                job_id,
                f"--region={self.region}",
                f"--project={self.project_id}",
                "--format=json",
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, check=True)

            job_info = json.loads(result.stdout)

            logger.info(f"Retrieved training job: {job_id}")
            return job_info

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to get training job {job_id}: {e}")
            logger.error(f"stderr: {e.stderr}")
            raise
        except Exception as e:
            logger.error(f"Failed to get training job {job_id}: {e}")
            raise

    def list_training_jobs(
        self, filter_expr: str | None = None
    ) -> list[dict[str, Any]]:
        """
        List training jobs in the project.

        Args:
            filter_expr: Optional filter expression

        Returns:
            List of training job information
        """
        try:
            # Use gcloud to list jobs
            cmd = [
                "gcloud",
                "ai",
                "custom-jobs",
                "list",
                f"--region={self.region}",
                f"--project={self.project_id}",
                "--format=json",
            ]

            if filter_expr:
                cmd.extend(["--filter", filter_expr])

            result = subprocess.run(cmd, capture_output=True, text=True, check=True)

            jobs = json.loads(result.stdout)

            logger.info(f"Found {len(jobs)} training jobs")
            return jobs

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to list training jobs: {e}")
            logger.error(f"stderr: {e.stderr}")
            raise
        except Exception as e:
            logger.error(f"Failed to list training jobs: {e}")
            raise

    def cancel_training_job(self, job_id: str) -> bool:
        """
        Cancel a running training job.

        Args:
            job_id: Training job ID

        Returns:
            True if cancelled successfully
        """
        try:
            # Use gcloud to cancel job
            cmd = [
                "gcloud",
                "ai",
                "custom-jobs",
                "cancel",
                job_id,
                f"--region={self.region}",
                f"--project={self.project_id}",
            ]

            subprocess.run(cmd, capture_output=True, text=True, check=True)

            logger.info(f"Cancelled training job: {job_id}")
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to cancel training job {job_id}: {e}")
            logger.error(f"stderr: {e.stderr}")
            return False
        except Exception as e:
            logger.error(f"Failed to cancel training job {job_id}: {e}")
            return False

    def get_job_logs(self, job_id: str, max_lines: int | None = None) -> str:
        """
        Get logs from a training job.

        Args:
            job_id: Training job ID
            max_lines: Maximum number of log lines to return

        Returns:
            Job logs as string
        """
        try:
            # Use gcloud to get logs
            cmd = [
                "gcloud",
                "ai",
                "custom-jobs",
                "stream-logs",
                job_id,
                f"--region={self.region}",
                f"--project={self.project_id}",
            ]

            if max_lines:
                cmd.extend(["--max-lines", str(max_lines)])

            result = subprocess.run(cmd, capture_output=True, text=True, check=True)

            logger.info(f"Retrieved logs for training job: {job_id}")
            return result.stdout

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to get logs for training job {job_id}: {e}")
            logger.error(f"stderr: {e.stderr}")
            raise
        except Exception as e:
            logger.error(f"Failed to get logs for training job {job_id}: {e}")
            raise

    def wait_for_job_completion(self, job_id: str, timeout_minutes: int = 120) -> str:
        """
        Wait for a training job to complete.

        Args:
            job_id: Training job ID
            timeout_minutes: Timeout in minutes

        Returns:
            Final job state
        """
        import time

        start_time = time.time()
        timeout_seconds = timeout_minutes * 60

        logger.info(f"Waiting for training job {job_id} to complete...")

        while True:
            # Check if timeout exceeded
            if time.time() - start_time > timeout_seconds:
                raise TimeoutError(
                    f"Training job {job_id} did not complete within {timeout_minutes} minutes"
                )

            try:
                # Get job status
                job_info = self.get_training_job(job_id)
                state = job_info.get("state", "UNKNOWN")

                logger.info(f"Job {job_id} state: {state}")

                # Check if job is complete
                if state in ["SUCCEEDED", "FAILED", "CANCELLED"]:
                    logger.info(f"Training job {job_id} completed with state: {state}")
                    return state

                # Wait before checking again
                time.sleep(30)

            except Exception as e:
                logger.warning(f"Error checking job status: {e}")
                time.sleep(30)

    def create_training_script(
        self, script_name: str, model_type: str, **kwargs
    ) -> str:
        """
        Create a training script for the specified model type.

        Args:
            script_name: Name for the training script
            model_type: Type of model (lstm_vae, tranad, usad, ecod)
            **kwargs: Additional parameters

        Returns:
            Path to created training script
        """
        try:
            # Get model-specific configuration
            model_config = self.config.training.models.get(model_type, {})

            # Create script content
            script_content = self._generate_training_script(
                model_type, model_config, **kwargs
            )

            # Save script to local file
            script_path = f"training_scripts/{script_name}.py"
            os.makedirs(os.path.dirname(script_path), exist_ok=True)

            with open(script_path, "w") as f:
                f.write(script_content)

            logger.info(f"Created training script: {script_path}")
            return script_path

        except Exception as e:
            logger.error(f"Failed to create training script {script_name}: {e}")
            raise

    def _generate_training_script(
        self, model_type: str, model_config: dict[str, Any], **kwargs
    ) -> str:
        """Generate training script content based on model type."""
        # This is a template - you would customize based on your actual model implementations
        script_template = f'''#!/usr/bin/env python3
# ruff: noqa
"""
Training script for {model_type.upper()} anomaly detection model.
Generated automatically by AIPlatformTrainer.
"""

import os
import sys
import logging
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, '/app/src')

from gcp.config import GCPConfig
from gcp.auth import GCPAuthenticator
from gcp.vertex_ai import VertexAIManager

def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def main():
    """Main training function."""
    parser = argparse.ArgumentParser(description='Train {model_type.upper()} model')
    parser.add_argument('--data-path', required=True, help='Path to training data')
    parser.add_argument('--model-dir', required=True, help='Path to save model')
    parser.add_argument('--epochs', type=int, default={model_config.get("epochs", 100)}, help='Number of epochs')
    parser.add_argument('--batch-size', type=int, default={model_config.get("batch_size", 32)}, help='Batch size')
    parser.add_argument('--learning-rate', type=float, default={model_config.get("learning_rate", 0.001)}, help='Learning rate')

    args = parser.parse_args()

    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info(f"Starting {model_type.upper()} model training")
    logger.info(f"Arguments: {{vars(args)}}")

    try:
        # Initialize GCP components
        config = GCPConfig()
        authenticator = GCPAuthenticator(config)
        vertex_ai = VertexAIManager(config, authenticator)

        # Create experiment run
        run = vertex_ai.create_experiment_run(f"{{model_type}}_training_{{datetime.now().strftime("%Y%m%d_%H%M%S")}}")

        # Log parameters
        vertex_ai.log_params(run, vars(args))

        # TODO: Implement actual model training logic here
        # This would include:
        # 1. Loading data
        # 2. Preprocessing
        # 3. Model initialization
        # 4. Training loop
        # 5. Validation
        # 6. Model saving

        logger.info("Training completed successfully")

        # Log final metrics
        vertex_ai.log_metrics(run, {{"final_loss": 0.0, "final_accuracy": 0.0}})

    except Exception as e:
        logger.error(f"Training failed: {{e}}")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''

        return script_template

    def __repr__(self) -> str:
        """String representation of AI Platform trainer."""
        return f"AIPlatformTrainer(project={self.project_id}, region={self.region})"
