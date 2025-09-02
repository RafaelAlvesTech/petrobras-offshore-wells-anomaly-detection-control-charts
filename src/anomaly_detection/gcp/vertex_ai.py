"""
Vertex AI management for model training and deployment.
"""

import logging
from datetime import datetime, timedelta
from typing import Any

from google.cloud import aiplatform
from google.cloud.aiplatform import CustomJob, Endpoint, HyperparameterTuningJob, Model

logger = logging.getLogger(__name__)


class VertexAIManager:
    """
    Manages Vertex AI operations for the anomaly detection project.

    This class handles experiment management, model training, hyperparameter tuning,
    model deployment, and monitoring.
    """

    def __init__(self, config, authenticator):
        """
        Initialize Vertex AI manager.

        Args:
            config: GCPConfig instance
            authenticator: GCPAuthenticator instance
        """
        self.config = config
        self.authenticator = authenticator
        self.client = authenticator.get_aiplatform_client()
        self.location = config.vertex_ai.location
        self.project_id = authenticator.project_id

        # Initialize Vertex AI
        aiplatform.init(
            project=self.project_id,
            location=self.location,
            credentials=authenticator.credentials,
        )

        # Get or create experiment
        self.experiment = self._get_or_create_experiment()

        logger.info(f"Initialized Vertex AI manager for project {self.project_id}")

    def _get_or_create_experiment(self):
        """Get or create the main experiment."""
        try:
            # Try to get existing experiment
            experiments = aiplatform.Experiment.list(
                filter=f"display_name={self.config.vertex_ai.experiment_name}"
            )

            if experiments:
                experiment = experiments[0]
                logger.info(f"Using existing experiment: {experiment.display_name}")
            else:
                # Create new experiment
                experiment = aiplatform.Experiment.create(
                    display_name=self.config.vertex_ai.experiment_name,
                    description="Experimentos para detecção de anomalias em poços offshore",
                )
                logger.info(f"Created new experiment: {experiment.display_name}")

            return experiment

        except Exception as e:
            logger.error(f"Failed to get/create experiment: {e}")
            raise

    def create_custom_training_job(
        self,
        display_name: str,
        script_path: str,
        requirements: list[str],
        machine_type: str | None = None,
        accelerator_type: str | None = None,
        accelerator_count: int | None = None,
        **kwargs,
    ) -> CustomJob:
        """
        Create a custom training job.

        Args:
            display_name: Name for the training job
            script_path: GCS path to training script
            requirements: List of Python requirements
            machine_type: Machine type for training
            accelerator_type: GPU accelerator type
            accelerator_count: Number of accelerators
            **kwargs: Additional arguments for CustomJob

        Returns:
            CustomJob instance
        """
        # Use defaults from config if not specified
        machine_type = machine_type or self.config.vertex_ai.default_machine_type
        accelerator_type = (
            accelerator_type or self.config.vertex_ai.default_accelerator_type
        )
        accelerator_count = (
            accelerator_count or self.config.vertex_ai.default_accelerator_count
        )

        try:
            job = CustomJob(
                display_name=display_name,
                script_path=script_path,
                requirements=requirements,
                machine_type=machine_type,
                accelerator_type=accelerator_type,
                accelerator_count=accelerator_count,
                **kwargs,
            )

            logger.info(f"Created custom training job: {display_name}")
            return job

        except Exception as e:
            logger.error(f"Failed to create custom training job {display_name}: {e}")
            raise

    def start_training_job(self, job, **kwargs):
        """
        Start a training job.

        Args:
            job: TrainingJob instance
            **kwargs: Additional arguments for job.run()

        Returns:
            Running job instance
        """
        try:
            # Start the job
            running_job = job.run(**kwargs)

            logger.info(f"Started training job: {job.display_name}")
            logger.info(f"Job ID: {running_job.name}")

            return running_job

        except Exception as e:
            logger.error(f"Failed to start training job {job.display_name}: {e}")
            raise

    def create_hyperparameter_tuning_job(
        self,
        display_name: str,
        base_job: CustomJob,
        parameter_specs: dict[str, Any],
        max_trial_count: int | None = None,
        parallel_trial_count: int | None = None,
        **kwargs,
    ) -> HyperparameterTuningJob:
        """
        Create a hyperparameter tuning job.

        Args:
            display_name: Name for the tuning job
            base_job: Base CustomJob to tune
            parameter_specs: Hyperparameter specifications
            max_trial_count: Maximum number of trials
            parallel_trial_count: Number of parallel trials
            **kwargs: Additional arguments for HyperparameterTuningJob

        Returns:
            HyperparameterTuningJob instance
        """
        # Use defaults from config if not specified
        max_trial_count = (
            max_trial_count
            or self.config.vertex_ai.hyperparameter_tuning.max_trial_count
        )
        parallel_trial_count = (
            parallel_trial_count
            or self.config.vertex_ai.hyperparameter_tuning.parallel_trial_count
        )

        try:
            tuning_job = HyperparameterTuningJob(
                display_name=display_name,
                base_job=base_job,
                parameter_specs=parameter_specs,
                max_trial_count=max_trial_count,
                parallel_trial_count=parallel_trial_count,
                **kwargs,
            )

            logger.info(f"Created hyperparameter tuning job: {display_name}")
            return tuning_job

        except Exception as e:
            logger.error(
                f"Failed to create hyperparameter tuning job {display_name}: {e}"
            )
            raise

    def deploy_model(self, model: Model, endpoint_name: str, **kwargs):
        """
        Deploy a model to an endpoint.

        Args:
            model: Trained model to deploy
            endpoint_name: Name for the endpoint
            **kwargs: Additional arguments for model.deploy()

        Returns:
            Deployed endpoint
        """
        try:
            endpoint = model.deploy(endpoint_name=endpoint_name, **kwargs)

            logger.info(
                f"Deployed model {model.display_name} to endpoint {endpoint_name}"
            )
            return endpoint

        except Exception as e:
            logger.error(f"Failed to deploy model {model.display_name}: {e}")
            raise

    def list_models(self, filter_expr: str | None = None) -> list[Model]:
        """
        List models in the project.

        Args:
            filter_expr: Optional filter expression

        Returns:
            List of models
        """
        try:
            models = Model.list(filter=filter_expr)
            logger.info(f"Found {len(models)} models")
            return models

        except Exception as e:
            logger.error(f"Failed to list models: {e}")
            raise

    def get_model(self, model_id: str) -> Model:
        """
        Get a specific model by ID.

        Args:
            model_id: Model ID

        Returns:
            Model instance
        """
        try:
            model = Model(model_id)
            logger.info(f"Retrieved model: {model.display_name}")
            return model

        except Exception as e:
            logger.error(f"Failed to get model {model_id}: {e}")
            raise

    def list_endpoints(self, filter_expr: str | None = None) -> list[Endpoint]:
        """
        List endpoints in the project.

        Args:
            filter_expr: Optional filter expression

        Returns:
            List of endpoints
        """
        try:
            endpoints = Endpoint.list(filter=filter_expr)
            logger.info(f"Found {len(endpoints)} endpoints")
            return endpoints

        except Exception as e:
            logger.error(f"Failed to list endpoints: {e}")
            raise

    def get_endpoint(self, endpoint_id: str) -> Endpoint:
        """
        Get a specific endpoint by ID.

        Args:
            endpoint_id: Endpoint ID

        Returns:
            Endpoint instance
        """
        try:
            endpoint = Endpoint(endpoint_id)
            logger.info(f"Retrieved endpoint: {endpoint.display_name}")
            return endpoint

        except Exception as e:
            logger.error(f"Failed to get endpoint {endpoint_id}: {e}")
            raise

    def list_training_jobs(self, filter_expr: str | None = None) -> list[CustomJob]:
        """
        List training jobs in the project.

        Args:
            filter_expr: Optional filter expression

        Returns:
            List of training jobs
        """
        try:
            jobs = CustomJob.list(filter=filter_expr)
            logger.info(f"Found {len(jobs)} training jobs")
            return jobs

        except Exception as e:
            logger.error(f"Failed to list training jobs: {e}")
            raise

    def get_training_job(self, job_id: str) -> CustomJob:
        """
        Get a specific training job by ID.

        Args:
            job_id: Training job ID

        Returns:
            CustomJob instance
        """
        try:
            job = CustomJob(job_id)
            logger.info(f"Retrieved training job: {job.display_name}")
            return job

        except Exception as e:
            logger.error(f"Failed to get training job {job_id}: {e}")
            raise

    def create_experiment_run(self, run_name: str, **kwargs):
        """
        Create a new run in the experiment.

        Args:
            run_name: Name for the run
            **kwargs: Additional arguments for experiment.start_run()

        Returns:
            Experiment run instance
        """
        try:
            run = self.experiment.start_run(run_name, **kwargs)
            logger.info(f"Created experiment run: {run_name}")
            return run

        except Exception as e:
            logger.error(f"Failed to create experiment run {run_name}: {e}")
            raise

    def log_metrics(self, run, metrics: dict[str, float], step: int | None = None):
        """
        Log metrics to an experiment run.

        Args:
            run: Experiment run instance
            metrics: Dictionary of metric names and values
            step: Optional step number
        """
        try:
            for metric_name, metric_value in metrics.items():
                run.log_metric(metric_name, metric_value, step=step)

            logger.info(f"Logged {len(metrics)} metrics to run {run.display_name}")

        except Exception as e:
            logger.error(f"Failed to log metrics: {e}")
            raise

    def log_params(self, run, params: dict[str, Any]):
        """
        Log parameters to an experiment run.

        Args:
            run: Experiment run instance
            params: Dictionary of parameter names and values
        """
        try:
            for param_name, param_value in params.items():
                run.log_param(param_name, param_value)

            logger.info(f"Logged {len(params)} parameters to run {run.display_name}")

        except Exception as e:
            logger.error(f"Failed to log parameters: {e}")
            raise

    def get_experiment_info(self) -> dict[str, Any]:
        """Get information about the current experiment."""
        try:
            info = {
                "display_name": self.experiment.display_name,
                "name": self.experiment.name,
                "description": self.experiment.description,
                "create_time": self.experiment.create_time,
                "update_time": self.experiment.update_time,
                "state": (
                    self.experiment.state.name
                    if hasattr(self.experiment.state, "name")
                    else str(self.experiment.state)
                ),
            }

            # Get run count
            try:
                runs = list(self.experiment.list_runs())
                info["run_count"] = len(runs)
            except Exception:
                info["run_count"] = 0

            return info

        except Exception as e:
            logger.error(f"Failed to get experiment info: {e}")
            raise

    def cleanup_resources(self, older_than_days: int = 30):
        """
        Clean up old resources (models, endpoints, jobs).

        Args:
            older_than_days: Age threshold for cleanup
        """
        try:
            cutoff_date = datetime.now() - timedelta(days=older_than_days)

            # Clean up old models
            models = self.list_models()
            for model in models:
                if hasattr(model, "create_time") and model.create_time < cutoff_date:
                    try:
                        model.delete()
                        logger.info(f"Deleted old model: {model.display_name}")
                    except Exception as e:
                        logger.warning(
                            f"Failed to delete old model {model.display_name}: {e}"
                        )

            # Clean up old endpoints
            endpoints = self.list_endpoints()
            for endpoint in endpoints:
                if (
                    hasattr(endpoint, "create_time")
                    and endpoint.create_time < cutoff_date
                ):
                    try:
                        endpoint.delete()
                        logger.info(f"Deleted old endpoint: {endpoint.display_name}")
                    except Exception as e:
                        logger.warning(
                            f"Failed to delete old endpoint {endpoint.display_name}: {e}"
                        )

            logger.info("Resource cleanup completed")

        except Exception as e:
            logger.error(f"Failed to cleanup resources: {e}")
            raise

    def __repr__(self) -> str:
        """String representation of Vertex AI manager."""
        return f"VertexAIManager(project={self.project_id}, location={self.location})"
