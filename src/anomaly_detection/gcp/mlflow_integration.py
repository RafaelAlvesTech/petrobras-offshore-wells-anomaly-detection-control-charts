"""
MLflow integration with Google Cloud Storage for experiment tracking.
"""

import logging
import os
from typing import Any

import mlflow
import mlflow.pytorch
import mlflow.sklearn
from mlflow.entities import Experiment, Run
from mlflow.tracking import MlflowClient

logger = logging.getLogger(__name__)


class MLflowGCSIntegration:
    """
    Integrates MLflow with Google Cloud Storage for experiment tracking.

    This class provides seamless integration between MLflow tracking and GCS storage,
    allowing for distributed experiment tracking and model artifact storage.
    """

    def __init__(self, config, authenticator):
        """
        Initialize MLflow GCS integration.

        Args:
            config: GCPConfig instance
            authenticator: GCPAuthenticator instance
        """
        self.config = config
        self.authenticator = authenticator
        self.project_id = authenticator.project_id

        # Setup MLflow tracking
        self._setup_mlflow()

        # Initialize MLflow client
        self.client = MlflowClient()

        # Get or create experiment
        self.experiment = self._get_or_create_experiment()

        logger.info(f"Initialized MLflow GCS integration for project {self.project_id}")

    def _setup_mlflow(self) -> None:
        """Setup MLflow configuration."""
        try:
            # Set tracking URI
            mlflow.set_tracking_uri(self.config.mlflow.tracking_uri)

            # Set experiment name
            mlflow.set_experiment(self.config.mlflow.experiment_name)

            # Set GCS as artifact store if using GCS
            if self.config.mlflow.artifacts_storage == "gcs":
                mlflow.set_experiment(self.config.mlflow.experiment_name)

                # Set artifact location for the experiment
                experiment = mlflow.get_experiment_by_name(
                    self.config.mlflow.experiment_name
                )
                if experiment:
                    mlflow.set_experiment(experiment.name)
                    mlflow.set_tracking_uri(self.config.mlflow.tracking_uri)

            logger.info(f"MLflow tracking URI: {self.config.mlflow.tracking_uri}")
            logger.info(f"MLflow experiment: {self.config.mlflow.experiment_name}")

        except Exception as e:
            logger.error(f"Failed to setup MLflow: {e}")
            raise

    def _get_or_create_experiment(self) -> Experiment:
        """Get or create the MLflow experiment."""
        try:
            # Try to get existing experiment
            experiment = self.client.get_experiment_by_name(
                self.config.mlflow.experiment_name
            )

            if experiment:
                logger.info(f"Using existing MLflow experiment: {experiment.name}")
            else:
                # Create new experiment
                experiment_id = self.client.create_experiment(
                    name=self.config.mlflow.experiment_name,
                    artifact_location=f"gs://{self.config.mlflow.artifacts_bucket}/{self.config.mlflow.artifacts_path}",
                )
                experiment = self.client.get_experiment(experiment_id)
                logger.info(f"Created new MLflow experiment: {experiment.name}")

            return experiment

        except Exception as e:
            logger.error(f"Failed to get/create MLflow experiment: {e}")
            raise

    def start_run(self, run_name: str, tags: dict[str, str] | None = None) -> Run:
        """
        Start a new MLflow run.

        Args:
            run_name: Name for the run
            tags: Optional tags for the run

        Returns:
            MLflow run instance
        """
        try:
            # Start run
            run = mlflow.start_run(run_name=run_name, tags=tags)

            logger.info(f"Started MLflow run: {run_name}")
            return run

        except Exception as e:
            logger.error(f"Failed to start MLflow run {run_name}: {e}")
            raise

    def end_run(self) -> None:
        """End the current MLflow run."""
        try:
            mlflow.end_run()
            logger.info("Ended MLflow run")

        except Exception as e:
            logger.error(f"Failed to end MLflow run: {e}")
            raise

    def log_params(self, params: dict[str, Any]) -> None:
        """
        Log parameters to the current run.

        Args:
            params: Dictionary of parameter names and values
        """
        try:
            for param_name, param_value in params.items():
                mlflow.log_param(param_name, param_value)

            logger.info(f"Logged {len(params)} parameters")

        except Exception as e:
            logger.error(f"Failed to log parameters: {e}")
            raise

    def log_metrics(self, metrics: dict[str, float], step: int | None = None) -> None:
        """
        Log metrics to the current run.

        Args:
            metrics: Dictionary of metric names and values
            step: Optional step number
        """
        try:
            for metric_name, metric_value in metrics.items():
                mlflow.log_metric(metric_name, metric_value, step=step)

            logger.info(f"Logged {len(metrics)} metrics")

        except Exception as e:
            logger.error(f"Failed to log metrics: {e}")
            raise

    def log_artifact(self, local_path: str, artifact_path: str | None = None) -> None:
        """
        Log an artifact to the current run.

        Args:
            local_path: Path to local file/directory
            artifact_path: Optional path within artifacts
        """
        try:
            mlflow.log_artifact(local_path, artifact_path)
            logger.info(f"Logged artifact: {local_path}")

        except Exception as e:
            logger.error(f"Failed to log artifact {local_path}: {e}")
            raise

    def log_model(self, model, artifact_path: str, **kwargs) -> None:
        """
        Log a model to the current run.

        Args:
            model: Model to log
            artifact_path: Path for the model
            **kwargs: Additional arguments for model logging
        """
        try:
            # Determine model type and log accordingly
            if hasattr(model, "state_dict"):  # PyTorch model
                mlflow.pytorch.log_model(model, artifact_path, **kwargs)
            elif hasattr(model, "predict"):  # Scikit-learn model
                mlflow.sklearn.log_model(model, artifact_path, **kwargs)
            else:
                # Generic model logging
                mlflow.log_artifact(model, artifact_path)

            logger.info(f"Logged model to: {artifact_path}")

        except Exception as e:
            logger.error(f"Failed to log model to {artifact_path}: {e}")
            raise

    def load_model(self, model_uri: str, **kwargs):
        """
        Load a model from MLflow.

        Args:
            model_uri: URI of the model to load
            **kwargs: Additional arguments for model loading

        Returns:
            Loaded model
        """
        try:
            # Try to load as PyTorch model first
            try:
                model = mlflow.pytorch.load_model(model_uri, **kwargs)
                logger.info(f"Loaded PyTorch model from: {model_uri}")
                return model
            except Exception:
                pass

            # Try to load as scikit-learn model
            try:
                model = mlflow.sklearn.load_model(model_uri, **kwargs)
                logger.info(f"Loaded scikit-learn model from: {model_uri}")
                return model
            except Exception:
                pass

            # Generic artifact loading
            model = mlflow.artifacts.load_text(model_uri)
            logger.info(f"Loaded generic model from: {model_uri}")
            return model

        except Exception as e:
            logger.error(f"Failed to load model from {model_uri}: {e}")
            raise

    def search_runs(self, filter_string: str = "", max_results: int = 100) -> list[Run]:
        """
        Search for runs in the experiment.

        Args:
            filter_string: MLflow filter string
            max_results: Maximum number of results

        Returns:
            List of runs
        """
        try:
            runs = self.client.search_runs(
                experiment_ids=[self.experiment.experiment_id],
                filter_string=filter_string,
                max_results=max_results,
            )

            logger.info(f"Found {len(runs)} runs matching filter: {filter_string}")
            return runs

        except Exception as e:
            logger.error(f"Failed to search runs: {e}")
            raise

    def get_run(self, run_id: str) -> Run:
        """
        Get a specific run by ID.

        Args:
            run_id: Run ID

        Returns:
            MLflow run instance
        """
        try:
            run = self.client.get_run(run_id)
            logger.info(f"Retrieved run: {run.info.run_name}")
            return run

        except Exception as e:
            logger.error(f"Failed to get run {run_id}: {e}")
            raise

    def list_artifacts(self, run_id: str, path: str | None = None) -> list[str]:
        """
        List artifacts for a specific run.

        Args:
            run_id: Run ID
            path: Optional path within artifacts

        Returns:
            List of artifact paths
        """
        try:
            artifacts = self.client.list_artifacts(run_id, path)
            artifact_paths = [artifact.path for artifact in artifacts]

            logger.info(f"Found {len(artifact_paths)} artifacts for run {run_id}")
            return artifact_paths

        except Exception as e:
            logger.error(f"Failed to list artifacts for run {run_id}: {e}")
            raise

    def download_artifacts(self, run_id: str, path: str, local_path: str) -> str:
        """
        Download artifacts from a run.

        Args:
            run_id: Run ID
            path: Path within artifacts
            local_path: Local path to save artifacts

        Returns:
            Path to downloaded artifacts
        """
        try:
            # Ensure local directory exists
            os.makedirs(os.path.dirname(local_path), exist_ok=True)

            # Download artifacts
            downloaded_path = mlflow.artifacts.download_artifacts(
                run_id=run_id, artifact_path=path, dst_path=local_path
            )

            logger.info(f"Downloaded artifacts from {path} to {downloaded_path}")
            return downloaded_path

        except Exception as e:
            logger.error(f"Failed to download artifacts from {path}: {e}")
            raise

    def register_model(self, model_uri: str, name: str, **kwargs) -> str:
        """
        Register a model in the MLflow model registry.

        Args:
            model_uri: URI of the model to register
            name: Name for the registered model
            **kwargs: Additional arguments for model registration

        Returns:
            Model version URI
        """
        try:
            # Register model
            model_version = mlflow.register_model(model_uri, name, **kwargs)

            logger.info(f"Registered model {name} with version {model_version.version}")
            return model_version.model_uri

        except Exception as e:
            logger.error(f"Failed to register model {name}: {e}")
            raise

    def list_registered_models(self) -> list[str]:
        """
        List all registered models.

        Returns:
            List of registered model names
        """
        try:
            models = self.client.list_registered_models()
            model_names = [model.name for model in models]

            logger.info(f"Found {len(model_names)} registered models")
            return model_names

        except Exception as e:
            logger.error(f"Failed to list registered models: {e}")
            raise

    def get_experiment_info(self) -> dict[str, Any]:
        """Get information about the current experiment."""
        try:
            info = {
                "name": self.experiment.name,
                "experiment_id": self.experiment.experiment_id,
                "artifact_location": self.experiment.artifact_location,
                "lifecycle_stage": self.experiment.lifecycle_stage,
                "creation_time": self.experiment.creation_time,
                "last_update_time": self.experiment.last_update_time,
            }

            # Get run count
            try:
                runs = self.search_runs(max_results=1000)
                info["run_count"] = len(runs)
            except Exception:
                info["run_count"] = 0

            return info

        except Exception as e:
            logger.error(f"Failed to get experiment info: {e}")
            raise

    def cleanup_old_runs(self, older_than_days: int = 30) -> int:
        """
        Clean up old runs from the experiment.

        Args:
            older_than_days: Age threshold for cleanup

        Returns:
            Number of runs cleaned up
        """
        try:
            from datetime import datetime, timedelta

            cutoff_date = datetime.now() - timedelta(days=older_than_days)
            cutoff_timestamp = cutoff_date.timestamp() * 1000  # Convert to milliseconds

            # Search for old runs
            old_runs = self.search_runs(
                filter_string=f"attributes.start_time < {cutoff_timestamp}",
                max_results=1000,
            )

            cleaned_count = 0
            for run in old_runs:
                try:
                    # Delete run
                    self.client.delete_run(run.info.run_id)
                    cleaned_count += 1
                    logger.info(f"Deleted old run: {run.info.run_name}")
                except Exception as e:
                    logger.warning(f"Failed to delete old run {run.info.run_name}: {e}")

            logger.info(f"Cleaned up {cleaned_count} old runs")
            return cleaned_count

        except Exception as e:
            logger.error(f"Failed to cleanup old runs: {e}")
            raise

    def export_experiment(self, export_path: str) -> str:
        """
        Export the experiment data.

        Args:
            export_path: Path to save exported data

        Returns:
            Path to exported data
        """
        try:
            # Ensure export directory exists
            os.makedirs(os.path.dirname(export_path), exist_ok=True)

            # Export experiment
            mlflow.export_import.export_experiment(
                experiment_id=self.experiment.experiment_id, output_dir=export_path
            )

            logger.info(f"Exported experiment to: {export_path}")
            return export_path

        except Exception as e:
            logger.error(f"Failed to export experiment: {e}")
            raise

    def __repr__(self) -> str:
        """String representation of MLflow GCS integration."""
        return f"MLflowGCSIntegration(project={self.project_id}, experiment={self.config.mlflow.experiment_name})"
