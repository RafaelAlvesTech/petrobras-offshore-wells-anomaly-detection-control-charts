#!/usr/bin/env python3
"""
AWS Training Script for Petrobras Offshore Wells Anomaly Detection

Este módulo implementa o treinamento de modelos de detecção de anomalias
usando Amazon SageMaker e EC2 para treinamento distribuído.
"""

import logging
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import boto3
import sagemaker
from sagemaker import get_execution_role
from sagemaker.pytorch import PyTorch
from sagemaker.tuner import (
    CategoricalParameter,
    ContinuousParameter,
    HyperparameterTuner,
    IntegerParameter,
)

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class TrainingJobConfig:
    """Configuração para job de treinamento."""

    model_name: str
    instance_type: str
    instance_count: int
    volume_size_gb: int
    max_run_seconds: int
    hyperparameters: Dict[str, Any]
    input_data_config: Dict[str, Any]
    output_data_config: Dict[str, Any]


class AWSTrainingManager:
    """Gerenciador de treinamento AWS para modelos de detecção de anomalias."""

    def __init__(self, config_path: str = "aws-config.yaml"):
        """
        Inicializa o gerenciador de treinamento AWS.

        Args:
            config_path: Caminho para o arquivo de configuração
        """
        self.config_path = Path(config_path)
        self.config = self._load_config()

        # Inicializa sessão SageMaker
        self.session = sagemaker.Session()
        self.role = get_execution_role()

        # Inicializa clientes
        self.sagemaker_client = boto3.client("sagemaker")
        self.s3_client = boto3.client("s3")

        logger.info("AWS Training Manager inicializado com sucesso")

    def _load_config(self) -> Dict[str, Any]:
        """Carrega configuração do arquivo YAML."""
        try:
            import yaml

            if self.config_path.exists():
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return yaml.safe_load(f)
            else:
                logger.warning(
                    f"Arquivo de configuração {self.config_path} não encontrado"
                )
                return {}
        except Exception as e:
            logger.error(f"Erro ao carregar configuração: {e}")
            return {}

    def get_training_config(self, model_name: str) -> TrainingJobConfig:
        """
        Obtém configuração de treinamento para um modelo específico.

        Args:
            model_name: Nome do modelo (lstm_vae, tranad, usad, ecod)

        Returns:
            Configuração de treinamento
        """
        try:
            # Configuração padrão
            default_config = self.config.get("training", {}).get("default", {})

            # Configuração específica do modelo
            model_config = (
                self.config.get("training", {}).get("models", {}).get(model_name, {})
            )

            # Combina configurações
            training_config = {**default_config, **model_config}

            # Configuração de instância
            instance_type = (
                self.config.get("sagemaker", {})
                .get("training", {})
                .get("default_instance_type", "ml.p3.2xlarge")
            )

            # Configuração de entrada
            input_data_config = {
                "train": self.session.upload_data(
                    path="data/train",
                    bucket=self.config.get("s3", {}).get(
                        "bucket_name", "petrobras-anomaly-detection"
                    ),
                    key_prefix=f"data/{model_name}/train",
                ),
                "validation": self.session.upload_data(
                    path="data/validation",
                    bucket=self.config.get("s3", {}).get(
                        "bucket_name", "petrobras-anomaly-detection"
                    ),
                    key_prefix=f"data/{model_name}/validation",
                ),
            }

            # Configuração de saída
            output_data_config = {
                "bucket": self.config.get("s3", {}).get(
                    "bucket_name", "petrobras-anomaly-detection"
                ),
                "key_prefix": f"models/{model_name}/output",
            }

            return TrainingJobConfig(
                model_name=model_name,
                instance_type=instance_type,
                instance_count=1,
                volume_size_gb=100,
                max_run_seconds=3600 * 24,  # 24 horas
                hyperparameters=training_config,
                input_data_config=input_data_config,
                output_data_config=output_data_config,
            )

        except Exception as e:
            logger.error(f"Erro ao obter configuração de treinamento: {e}")
            raise

    def create_training_job(self, config: TrainingJobConfig) -> str:
        """
        Cria job de treinamento no SageMaker.

        Args:
            config: Configuração do job de treinamento

        Returns:
            Nome do job de treinamento
        """
        try:
            # Cria estimador PyTorch
            estimator = PyTorch(
                entry_point="train.py",
                source_dir="src",
                role=self.role,
                instance_count=config.instance_count,
                instance_type=config.instance_type,
                volume_size=config.volume_size_gb,
                max_run=config.max_run_seconds,
                framework_version="2.0.1",
                py_version="py310",
                hyperparameters=config.hyperparameters,
                output_path=f"s3://{config.output_data_config['bucket']}/{config.output_data_config['key_prefix']}",
                code_location=f"s3://{config.output_data_config['bucket']}/code/{config.model_name}",
                use_spot_instances=True,
                max_wait_time=3600,
                checkpoint_s3_uri=f"s3://{config.output_data_config['bucket']}/checkpoints/{config.model_name}",
                checkpoint_local_path="/opt/ml/checkpoints",
            )

            # Inicia treinamento
            estimator.fit(
                inputs=config.input_data_config,
                job_name=f"petrobras-{config.model_name}-{int(time.time())}",
            )

            logger.info(f"Job de treinamento iniciado para {config.model_name}")
            return estimator.latest_training_job.name

        except Exception as e:
            logger.error(f"Erro ao criar job de treinamento: {e}")
            raise

    def create_hyperparameter_tuning_job(self, config: TrainingJobConfig) -> str:
        """
        Cria job de tuning de hiperparâmetros.

        Args:
            config: Configuração do job de treinamento

        Returns:
            Nome do job de tuning
        """
        try:
            # Obtém espaço de busca
            search_space = (
                self.config.get("hyperparameter_tuning", {})
                .get("search_spaces", {})
                .get(config.model_name, {})
            )

            if not search_space:
                logger.warning(
                    f"Espaço de busca não encontrado para {config.model_name}"
                )
                return self.create_training_job(config)

            # Cria estimador base
            estimator = PyTorch(
                entry_point="train.py",
                source_dir="src",
                role=self.role,
                instance_count=config.instance_count,
                instance_type=config.instance_type,
                volume_size=config.volume_size_gb,
                max_run=config.max_run_seconds,
                framework_version="2.0.1",
                py_version="py310",
                hyperparameters=config.hyperparameters,
                output_path=f"s3://{config.output_data_config['bucket']}/{config.output_data_config['key_prefix']}",
                code_location=f"s3://{config.output_data_config['bucket']}/code/{config.model_name}",
                use_spot_instances=True,
                max_wait_time=3600,
            )

            # Define parâmetros de busca
            hyperparameter_ranges = {}

            for param_name, param_config in search_space.items():
                if param_config.get("type") == "Continuous":
                    hyperparameter_ranges[param_name] = ContinuousParameter(
                        param_config["min_value"], param_config["max_value"]
                    )
                elif param_config.get("type") == "Integer":
                    hyperparameter_ranges[param_name] = IntegerParameter(
                        param_config["min_value"], param_config["max_value"]
                    )
                elif param_config.get("type") == "Categorical":
                    hyperparameter_ranges[param_name] = CategoricalParameter(
                        param_config["values"]
                    )

            # Cria tuner
            tuner = HyperparameterTuner(
                estimator=estimator,
                objective_metric_name="validation_loss",
                objective_type="Minimize",
                hyperparameter_ranges=hyperparameter_ranges,
                max_jobs=self.config.get("hyperparameter_tuning", {}).get(
                    "max_jobs", 20
                ),
                max_parallel_jobs=self.config.get("hyperparameter_tuning", {}).get(
                    "max_parallel_jobs", 5
                ),
                strategy=self.config.get("hyperparameter_tuning", {}).get(
                    "strategy", "Bayesian"
                ),
            )

            # Inicia tuning
            tuner.fit(
                inputs=config.input_data_config,
                job_name=f"petrobras-{config.model_name}-tuning-{int(time.time())}",
            )

            logger.info(f"Job de tuning iniciado para {config.model_name}")
            return tuner.latest_tuning_job.name

        except Exception as e:
            logger.error(f"Erro ao criar job de tuning: {e}")
            raise

    def deploy_model(self, model_name: str, training_job_name: str) -> str:
        """
        Faz deploy do modelo treinado.

        Args:
            model_name: Nome do modelo
            training_job_name: Nome do job de treinamento

        Returns:
            Nome do endpoint
        """
        try:
            # Obtém informações do job de treinamento
            training_job = self.sagemaker_client.describe_training_job(
                TrainingJobName=training_job_name
            )

            # Cria modelo
            model = sagemaker.pytorch.PyTorchModel(
                model_data=training_job["ModelArtifacts"]["S3ModelArtifacts"],
                role=self.role,
                entry_point="inference.py",
                source_dir="src",
                framework_version="2.0.1",
                py_version="py310",
            )

            # Faz deploy
            predictor = model.deploy(
                initial_instance_count=1,
                instance_type=self.config.get("deployment", {})
                .get("model_serving", {})
                .get("instance_type", "ml.m5.large"),
                endpoint_name=f"petrobras-{model_name}-endpoint",
            )

            logger.info(f"Modelo {model_name} deployado com sucesso")
            return predictor.endpoint_name

        except Exception as e:
            logger.error(f"Erro ao fazer deploy do modelo: {e}")
            raise

    def monitor_training_job(self, job_name: str) -> Dict[str, Any]:
        """
        Monitora job de treinamento.

        Args:
            job_name: Nome do job de treinamento

        Returns:
            Status do job
        """
        try:
            response = self.sagemaker_client.describe_training_job(
                TrainingJobName=job_name
            )

            status = {
                "job_name": job_name,
                "status": response["TrainingJobStatus"],
                "start_time": response.get("TrainingStartTime"),
                "end_time": response.get("TrainingEndTime"),
                "instance_type": response["ResourceConfig"]["InstanceType"],
                "instance_count": response["ResourceConfig"]["InstanceCount"],
                "output_location": response["OutputDataConfig"]["S3OutputPath"],
                "metrics": {},
            }

            # Obtém métricas se disponíveis
            if response["TrainingJobStatus"] == "Completed":
                try:
                    metrics = self.sagemaker_client.describe_training_job(
                        TrainingJobName=job_name
                    )
                    if "FinalMetricDataList" in metrics:
                        for metric in metrics["FinalMetricDataList"]:
                            status["metrics"][metric["MetricName"]] = metric["Value"]
                except Exception as e:
                    logger.warning(f"Erro ao obter métricas: {e}")

            return status

        except Exception as e:
            logger.error(f"Erro ao monitorar job: {e}")
            raise

    def list_training_jobs(
        self, model_name: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Lista jobs de treinamento.

        Args:
            model_name: Filtra por nome do modelo

        Returns:
            Lista de jobs de treinamento
        """
        try:
            jobs = []

            # Lista jobs
            paginator = self.sagemaker_client.get_paginator("list_training_jobs")
            page_iterator = paginator.paginate(
                NameContains="petrobras", SortBy="CreationTime", SortOrder="Descending"
            )

            for page in page_iterator:
                for job in page["TrainingJobSummaries"]:
                    if not model_name or model_name in job["TrainingJobName"]:
                        jobs.append(
                            {
                                "job_name": job["TrainingJobName"],
                                "status": job["TrainingJobStatus"],
                                "creation_time": job["CreationTime"],
                                "end_time": job.get("EndTime"),
                                "instance_type": job.get("TrainingJobStatus")
                                == "InProgress"
                                and job.get("InstanceType"),
                                "instance_count": job.get("TrainingJobStatus")
                                == "InProgress"
                                and job.get("InstanceCount"),
                            }
                        )

            return jobs

        except Exception as e:
            logger.error(f"Erro ao listar jobs: {e}")
            raise

    def stop_training_job(self, job_name: str) -> bool:
        """
        Para job de treinamento.

        Args:
            job_name: Nome do job de treinamento

        Returns:
            True se o job foi parado, False caso contrário
        """
        try:
            self.sagemaker_client.stop_training_job(TrainingJobName=job_name)

            logger.info(f"Job de treinamento {job_name} parado com sucesso")
            return True

        except Exception as e:
            logger.error(f"Erro ao parar job: {e}")
            return False

    def cleanup_resources(self, model_name: str) -> bool:
        """
        Limpa recursos AWS para um modelo específico.

        Args:
            model_name: Nome do modelo

        Returns:
            True se a limpeza foi bem-sucedida, False caso contrário
        """
        try:
            # Lista endpoints
            endpoints = self.sagemaker_client.list_endpoints(
                NameContains=f"petrobras-{model_name}-endpoint"
            )

            # Remove endpoints
            for endpoint in endpoints["Endpoints"]:
                try:
                    self.sagemaker_client.delete_endpoint(
                        EndpointName=endpoint["EndpointName"]
                    )
                    logger.info(f"Endpoint {endpoint['EndpointName']} removido")
                except Exception as e:
                    logger.warning(
                        f"Erro ao remover endpoint {endpoint['EndpointName']}: {e}"
                    )

            # Lista modelos
            models = self.sagemaker_client.list_models(
                NameContains=f"petrobras-{model_name}"
            )

            # Remove modelos
            for model in models["Models"]:
                try:
                    self.sagemaker_client.delete_model(ModelName=model["ModelName"])
                    logger.info(f"Modelo {model['ModelName']} removido")
                except Exception as e:
                    logger.warning(f"Erro ao remover modelo {model['ModelName']}: {e}")

            logger.info(f"Recursos limpos para modelo {model_name}")
            return True

        except Exception as e:
            logger.error(f"Erro ao limpar recursos: {e}")
            return False

    def get_cost_estimate(self, config: TrainingJobConfig) -> Dict[str, float]:
        """
        Estima custo do treinamento.

        Args:
            config: Configuração do job de treinamento

        Returns:
            Estimativa de custo
        """
        try:
            # Preços por hora (aproximados, podem variar)
            pricing = {
                "ml.p3.2xlarge": 3.06,  # 1x V100
                "ml.p3.8xlarge": 12.24,  # 4x V100
                "ml.p3.16xlarge": 24.48,  # 8x V100
                "ml.g4dn.xlarge": 0.526,  # 1x T4
                "ml.g4dn.2xlarge": 0.736,  # 1x T4
                "ml.g4dn.4xlarge": 1.178,  # 1x T4
                "ml.g4dn.8xlarge": 2.36,  # 1x T4
                "ml.g5.xlarge": 0.526,  # 1x A10G
                "ml.g5.2xlarge": 0.736,  # 1x A10G
                "ml.g5.4xlarge": 1.178,  # 1x A10G
                "ml.g5.8xlarge": 2.36,  # 1x A10G
                "ml.g5.12xlarge": 3.912,  # 4x A10G
                "ml.g5.16xlarge": 4.712,  # 1x A10G
                "ml.g5.24xlarge": 7.824,  # 4x A10G
                "ml.g5.48xlarge": 15.648,  # 8x A10G
            }

            # Calcula custo estimado
            hourly_cost = pricing.get(
                config.instance_type, 3.06
            )  # Default para p3.2xlarge
            estimated_hours = config.max_run_seconds / 3600
            total_cost = hourly_cost * estimated_hours * config.instance_count

            # Adiciona custo de dados (aproximado)
            data_cost = 0.023 * 100  # $0.023 por GB, estimando 100GB

            return {
                "instance_cost": total_cost,
                "data_cost": data_cost,
                "total_cost": total_cost + data_cost,
                "hourly_rate": hourly_cost,
                "estimated_hours": estimated_hours,
            }

        except Exception as e:
            logger.error(f"Erro ao estimar custo: {e}")
            return {}


def main():
    """Função principal para teste do gerenciador de treinamento."""
    try:
        # Inicializa gerenciador
        manager = AWSTrainingManager()

        # Exemplo de uso
        print("🚀 AWS Training Manager para Petrobras Anomaly Detection")
        print("=" * 60)

        # Lista jobs existentes
        print("\n📋 Jobs de treinamento existentes:")
        jobs = manager.list_training_jobs()
        for job in jobs[:5]:  # Mostra apenas os 5 mais recentes
            print(f"   • {job['job_name']} - {job['status']}")

        # Exemplo de configuração para LSTM-VAE
        print("\n⚙️ Configuração para LSTM-VAE:")
        config = manager.get_training_config("lstm_vae")
        print(f"   • Instance Type: {config.instance_type}")
        print(f"   • Batch Size: {config.hyperparameters.get('batch_size')}")
        print(f"   • Learning Rate: {config.hyperparameters.get('learning_rate')}")
        print(f"   • Epochs: {config.hyperparameters.get('epochs')}")

        # Estimativa de custo
        cost_estimate = manager.get_cost_estimate(config)
        print("\n💰 Estimativa de custo:")
        print(f"   • Custo por hora: ${cost_estimate.get('hourly_rate', 0):.2f}")
        print(f"   • Horas estimadas: {cost_estimate.get('estimated_hours', 0):.1f}")
        print(f"   • Custo total estimado: ${cost_estimate.get('total_cost', 0):.2f}")

        print("\n💡 Para iniciar treinamento:")
        print("   manager.create_training_job(config)")
        print("   manager.create_hyperparameter_tuning_job(config)")

    except Exception as e:
        logger.error(f"Erro na execução principal: {e}")


if __name__ == "__main__":
    main()
