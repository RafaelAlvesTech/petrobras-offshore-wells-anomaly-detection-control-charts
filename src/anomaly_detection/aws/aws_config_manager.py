#!/usr/bin/env python3
"""
AWS Configuration Manager for Petrobras Offshore Wells Anomaly Detection

Este módulo gerencia todas as configurações relacionadas à AWS para treinamento
de modelos de detecção de anomalias na cloud.
"""

import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import boto3
import yaml
from botocore.exceptions import ClientError, NoCredentialsError

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class AWSConfig:
    """Classe para armazenar configurações AWS."""

    region: str
    access_key_id: str | None = None
    secret_access_key: str | None = None
    session_token: str | None = None
    profile_name: str | None = None


@dataclass
class SageMakerConfig:
    """Classe para armazenar configurações do SageMaker."""

    domain_name: str
    user_profile_name: str
    default_instance_type: str
    role_arn: str


@dataclass
class S3Config:
    """Classe para armazenar configurações do S3."""

    bucket_name: str
    region: str
    data_path: str
    models_path: str
    experiments_path: str


class AWSConfigManager:
    """Gerenciador de configurações AWS para o projeto."""

    def __init__(
        self, config_path: str = "aws-config.yaml", env_path: str = ".env.aws"
    ):
        """
        Inicializa o gerenciador de configurações AWS.

        Args:
            config_path: Caminho para o arquivo de configuração YAML
            env_path: Caminho para o arquivo de variáveis de ambiente
        """
        self.config_path = Path(config_path)
        self.env_path = Path(env_path)
        self.config = {}
        self.env_vars = {}

        # Carrega configurações
        self._load_config()
        self._load_env_vars()

        # Inicializa clientes AWS
        self._init_aws_clients()

    def _load_config(self) -> None:
        """Carrega configurações do arquivo YAML."""
        try:
            if self.config_path.exists():
                with open(self.config_path, encoding="utf-8") as f:
                    self.config = yaml.safe_load(f)
                logger.info(f"Configuração carregada de {self.config_path}")
            else:
                logger.warning(
                    f"Arquivo de configuração {self.config_path} não encontrado"
                )
                self.config = {}
        except Exception as e:
            logger.error(f"Erro ao carregar configuração: {e}")
            self.config = {}

    def _load_env_vars(self) -> None:
        """Carrega variáveis de ambiente."""
        try:
            if self.env_path.exists():
                with open(self.env_path, encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            key, value = line.split("=", 1)
                            self.env_vars[key.strip()] = value.strip()
                logger.info(f"Variáveis de ambiente carregadas de {self.env_path}")
            else:
                logger.warning(
                    f"Arquivo de variáveis de ambiente {self.env_path} não encontrado"
                )
                self.env_vars = {}
        except Exception as e:
            logger.error(f"Erro ao carregar variáveis de ambiente: {e}")
            self.env_vars = {}

    def _init_aws_clients(self) -> None:
        """Inicializa clientes AWS."""
        try:
            # Configura credenciais
            if self.env_vars.get("AWS_ACCESS_KEY_ID") and self.env_vars.get(
                "AWS_SECRET_ACCESS_KEY"
            ):
                boto3.setup_default_session(
                    aws_access_key_id=self.env_vars["AWS_ACCESS_KEY_ID"],
                    aws_secret_access_key=self.env_vars["AWS_SECRET_ACCESS_KEY"],
                    region_name=self.env_vars.get("AWS_REGION", "us-east-1"),
                )
            elif self.env_vars.get("AWS_PROFILE"):
                boto3.setup_default_session(profile_name=self.env_vars["AWS_PROFILE"])

            # Inicializa clientes
            self.s3_client = boto3.client("s3")
            self.sagemaker_client = boto3.client("sagemaker")
            self.ec2_client = boto3.client("ec2")
            self.cloudwatch_client = boto3.client("cloudwatch")
            self.iam_client = boto3.client("iam")

            logger.info("Clientes AWS inicializados com sucesso")

        except NoCredentialsError:
            logger.error("Credenciais AWS não encontradas")
            self.s3_client = None
            self.sagemaker_client = None
            self.ec2_client = None
            self.cloudwatch_client = None
            self.iam_client = None
        except Exception as e:
            logger.error(f"Erro ao inicializar clientes AWS: {e}")
            self.s3_client = None
            self.sagemaker_client = None
            self.ec2_client = None
            self.cloudwatch_client = None
            self.iam_client = None

    def validate_aws_credentials(self) -> bool:
        """
        Valida as credenciais AWS.

        Returns:
            True se as credenciais são válidas, False caso contrário
        """
        try:
            if not self.s3_client:
                return False

            # Tenta listar buckets para validar credenciais
            self.s3_client.list_buckets()
            logger.info("Credenciais AWS validadas com sucesso")
            return True

        except ClientError as e:
            if e.response["Error"]["Code"] == "InvalidAccessKeyId":
                logger.error("Access Key ID inválida")
            elif e.response["Error"]["Code"] == "SignatureDoesNotMatch":
                logger.error("Secret Access Key inválida")
            else:
                logger.error(f"Erro de credenciais: {e}")
            return False
        except Exception as e:
            logger.error(f"Erro ao validar credenciais: {e}")
            return False

    def create_s3_bucket(self, bucket_name: str | None = None) -> bool:
        """
        Cria bucket S3 se não existir.

        Args:
            bucket_name: Nome do bucket (usa configuração padrão se None)

        Returns:
            True se o bucket foi criado ou já existe, False caso contrário
        """
        try:
            if not self.s3_client:
                logger.error("Cliente S3 não inicializado")
                return False

            bucket_name = bucket_name or self.config.get("s3", {}).get("bucket_name")
            if not bucket_name:
                logger.error("Nome do bucket não especificado")
                return False

            region = self.config.get("s3", {}).get("region", "us-east-1")

            # Verifica se o bucket já existe
            try:
                self.s3_client.head_bucket(Bucket=bucket_name)
                logger.info(f"Bucket S3 {bucket_name} já existe")
                return True
            except ClientError as e:
                if e.response["Error"]["Code"] == "404":
                    pass  # Bucket não existe, continua para criar
                else:
                    raise

            # Cria o bucket
            if region == "us-east-1":
                self.s3_client.create_bucket(Bucket=bucket_name)
            else:
                self.s3_client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={"LocationConstraint": region},
                )

            # Configura versionamento
            self.s3_client.put_bucket_versioning(
                Bucket=bucket_name, VersioningConfiguration={"Status": "Enabled"}
            )

            # Configura criptografia
            self.s3_client.put_bucket_encryption(
                Bucket=bucket_name,
                ServerSideEncryptionConfiguration={
                    "Rules": [
                        {
                            "ApplyServerSideEncryptionByDefault": {
                                "SSEAlgorithm": "AES256"
                            }
                        }
                    ]
                },
            )

            logger.info(
                f"Bucket S3 {bucket_name} criado com sucesso na região {region}"
            )
            return True

        except Exception as e:
            logger.error(f"Erro ao criar bucket S3: {e}")
            return False

    def setup_s3_structure(self, bucket_name: str | None = None) -> bool:
        """
        Configura estrutura de pastas no S3.

        Args:
            bucket_name: Nome do bucket (usa configuração padrão se None)

        Returns:
            True se a estrutura foi configurada, False caso contrário
        """
        try:
            bucket_name = bucket_name or self.config.get("s3", {}).get("bucket_name")
            if not bucket_name:
                logger.error("Nome do bucket não especificado")
                return False

            # Pastas padrão
            folders = [
                "data/",
                "models/",
                "experiments/",
                "logs/",
                "checkpoints/",
                "datasets/",
                "mlflow-artifacts/",
                "tensorboard-logs/",
            ]

            for folder in folders:
                try:
                    self.s3_client.put_object(Bucket=bucket_name, Key=folder, Body="")
                    logger.info(f"Pasta {folder} criada no bucket {bucket_name}")
                except Exception as e:
                    logger.warning(f"Erro ao criar pasta {folder}: {e}")

            logger.info(f"Estrutura S3 configurada no bucket {bucket_name}")
            return True

        except Exception as e:
            logger.error(f"Erro ao configurar estrutura S3: {e}")
            return False

    def validate_sagemaker_setup(self) -> dict[str, Any]:
        """
        Valida configuração do SageMaker.

        Returns:
            Dicionário com status de validação
        """
        result = {
            "domain_exists": False,
            "user_profile_exists": False,
            "role_exists": False,
            "valid": False,
        }

        try:
            if not self.sagemaker_client:
                logger.error("Cliente SageMaker não inicializado")
                return result

            domain_name = self.config.get("sagemaker", {}).get("domain", {}).get("name")
            user_profile_name = (
                self.config.get("sagemaker", {})
                .get("notebook", {})
                .get("instance_type")
            )
            role_arn = self.env_vars.get("SAGEMAKER_ROLE_ARN")

            # Valida domínio
            if domain_name:
                try:
                    self.sagemaker_client.describe_domain(DomainName=domain_name)
                    result["domain_exists"] = True
                    logger.info(f"Domínio SageMaker {domain_name} encontrado")
                except ClientError as e:
                    if e.response["Error"]["Code"] == "ValidationException":
                        logger.warning(
                            f"Domínio SageMaker {domain_name} não encontrado"
                        )
                    else:
                        logger.error(f"Erro ao verificar domínio: {e}")

            # Valida perfil de usuário
            if user_profile_name:
                try:
                    self.sagemaker_client.describe_user_profile(
                        DomainName=domain_name, UserProfileName=user_profile_name
                    )
                    result["user_profile_exists"] = True
                    logger.info(f"Perfil de usuário {user_profile_name} encontrado")
                except ClientError as e:
                    if e.response["Error"]["Code"] == "ValidationException":
                        logger.warning(
                            f"Perfil de usuário {user_profile_name} não encontrado"
                        )
                    else:
                        logger.error(f"Erro ao verificar perfil de usuário: {e}")

            # Valida role IAM
            if role_arn:
                try:
                    role_name = role_arn.split("/")[-1]
                    self.iam_client.get_role(RoleName=role_name)
                    result["role_exists"] = True
                    logger.info(f"Role IAM {role_name} encontrada")
                except ClientError as e:
                    if e.response["Error"]["Code"] == "NoSuchEntity":
                        logger.warning(f"Role IAM {role_name} não encontrada")
                    else:
                        logger.error(f"Erro ao verificar role IAM: {e}")

            # Determina se tudo está válido
            result["valid"] = all(
                [
                    result["domain_exists"],
                    result["user_profile_exists"],
                    result["role_exists"],
                ]
            )

            return result

        except Exception as e:
            logger.error(f"Erro ao validar SageMaker: {e}")
            return result

    def get_training_config(self, model_name: str) -> dict[str, Any]:
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

            # Adiciona configurações de instância
            training_config["instance_type"] = (
                self.config.get("sagemaker", {})
                .get("training", {})
                .get("default_instance_type", "ml.p3.2xlarge")
            )

            return training_config

        except Exception as e:
            logger.error(f"Erro ao obter configuração de treinamento: {e}")
            return {}

    def get_hyperparameter_search_space(self, model_name: str) -> dict[str, Any]:
        """
        Obtém espaço de busca de hiperparâmetros para um modelo.

        Args:
            model_name: Nome do modelo

        Returns:
            Espaço de busca de hiperparâmetros
        """
        try:
            search_spaces = self.config.get("hyperparameter_tuning", {}).get(
                "search_spaces", {}
            )
            return search_spaces.get(model_name, {})
        except Exception as e:
            logger.error(f"Erro ao obter espaço de busca: {e}")
            return {}

    def create_cost_alarm(
        self, budget_amount: float, budget_period: str = "MONTHLY"
    ) -> bool:
        """
        Cria alarme de custo no CloudWatch.

        Args:
            budget_amount: Valor do orçamento
            budget_period: Período do orçamento (MONTHLY, DAILY)

        Returns:
            True se o alarme foi criado, False caso contrário
        """
        try:
            if not self.cloudwatch_client:
                logger.error("Cliente CloudWatch não inicializado")
                return False

            alarm_name = f"petrobras-cost-alarm-{budget_period.lower()}"

            # Cria alarme de custo
            self.cloudwatch_client.put_metric_alarm(
                AlarmName=alarm_name,
                ComparisonOperator="GreaterThanThreshold",
                EvaluationPeriods=1,
                MetricName="EstimatedCharges",
                Namespace="AWS/Billing",
                Period=86400,  # 24 horas
                Statistic="Maximum",
                Threshold=budget_amount,
                ActionsEnabled=True,
                AlarmDescription=f"Alarme de custo para {budget_period.lower()}",
            )

            logger.info(f"Alarme de custo {alarm_name} criado com sucesso")
            return True

        except Exception as e:
            logger.error(f"Erro ao criar alarme de custo: {e}")
            return False

    def generate_setup_script(self, output_path: str = "setup_aws.sh") -> bool:
        """
        Gera script de setup para AWS.

        Args:
            output_path: Caminho para o script de saída

        Returns:
            True se o script foi gerado, False caso contrário
        """
        try:
            script_content = f"""#!/bin/bash
# Script de Setup AWS para Petrobras Offshore Wells Anomaly Detection
# Gerado automaticamente pelo AWSConfigManager

set -e

echo "🚀 Iniciando setup AWS para Petrobras Anomaly Detection..."

# Verifica se AWS CLI está instalado
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI não encontrado. Instalando..."
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    sudo ./aws/install
    rm -rf aws awscliv2.zip
fi

# Configura credenciais AWS
echo "🔐 Configurando credenciais AWS..."
aws configure set aws_access_key_id ${{AWS_ACCESS_KEY_ID}}
aws configure set aws_secret_access_key ${{AWS_SECRET_ACCESS_KEY}}
aws configure set region {self.config.get("aws", {}).get("region", "us-east-1")}

# Cria bucket S3
echo "🪣 Criando bucket S3..."
aws s3 mb s3://{self.config.get("s3", {}).get("bucket_name", "petrobras-anomaly-detection")} --region {self.config.get("s3", {}).get("region", "us-east-1")}

# Configura versionamento do bucket
echo "📝 Configurando versionamento do bucket..."
aws s3api put-bucket-versioning --bucket {self.config.get("s3", {}).get("bucket_name", "petrobras-anomaly-detection")} --versioning-configuration Status=Enabled

# Cria estrutura de pastas
echo "📁 Criando estrutura de pastas..."
aws s3api put-object --bucket {self.config.get("s3", {}).get("bucket_name", "petrobras-anomaly-detection")} --key data/
aws s3api put-object --bucket {self.config.get("s3", {}).get("bucket_name", "petrobras-anomaly-detection")} --key models/
aws s3api put-object --bucket {self.config.get("s3", {}).get("bucket_name", "petrobras-anomaly-detection")} --key experiments/
aws s3api put-object --bucket {self.config.get("s3", {}).get("bucket_name", "petrobras-anomaly-detection")} --key logs/
aws s3api put-object --bucket {self.config.get("s3", {}).get("bucket_name", "petrobras-anomaly-detection")} --key checkpoints/
aws s3api put-object --bucket {self.config.get("s3", {}).get("bucket_name", "petrobras-anomaly-detection")} --key datasets/

echo "✅ Setup AWS concluído com sucesso!"
echo "📋 Próximos passos:"
echo "   1. Configure o SageMaker Domain"
echo "   2. Crie o User Profile"
echo "   3. Configure as permissões IAM"
echo "   4. Teste a conectividade"
"""

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(script_content)

            # Torna o script executável
            os.chmod(output_path, 0o755)

            logger.info(f"Script de setup gerado em {output_path}")
            return True

        except Exception as e:
            logger.error(f"Erro ao gerar script de setup: {e}")
            return False

    def print_status(self) -> None:
        """Imprime status atual da configuração AWS."""
        print("\n" + "=" * 60)
        print("🔍 STATUS DA CONFIGURAÇÃO AWS")
        print("=" * 60)

        # Status das credenciais
        print(
            f"🔐 Credenciais AWS: {'✅ Válidas' if self.validate_aws_credentials() else '❌ Inválidas'}"
        )

        # Status do S3
        bucket_name = self.config.get("s3", {}).get("bucket_name")
        if bucket_name:
            print(f"🪣 Bucket S3: {bucket_name}")

        # Status do SageMaker
        sagemaker_status = self.validate_sagemaker_setup()
        print(
            f"🤖 SageMaker Domain: {'✅ Configurado' if sagemaker_status['domain_exists'] else '❌ Não configurado'}"
        )
        print(
            f"👤 User Profile: {'✅ Configurado' if sagemaker_status['user_profile_exists'] else '❌ Não configurado'}"
        )
        print(
            f"🔑 IAM Role: {'✅ Configurado' if sagemaker_status['role_exists'] else '❌ Não configurado'}"
        )

        # Configurações de treinamento
        print("\n📊 Configurações de Treinamento:")
        training_config = self.get_training_config("lstm_vae")
        if training_config:
            print(f"   • Instance Type: {training_config.get('instance_type', 'N/A')}")
            print(f"   • Batch Size: {training_config.get('batch_size', 'N/A')}")
            print(f"   • Learning Rate: {training_config.get('learning_rate', 'N/A')}")
            print(f"   • Epochs: {training_config.get('epochs', 'N/A')}")

        print("=" * 60)


def main():
    """Função principal para teste do gerenciador."""
    try:
        # Inicializa gerenciador
        manager = AWSConfigManager()

        # Imprime status
        manager.print_status()

        # Gera script de setup
        if manager.generate_setup_script():
            print("\n📜 Script de setup gerado: setup_aws.sh")
            print("💡 Execute: chmod +x setup_aws.sh && ./setup_aws.sh")

    except Exception as e:
        logger.error(f"Erro na execução principal: {e}")


if __name__ == "__main__":
    main()
