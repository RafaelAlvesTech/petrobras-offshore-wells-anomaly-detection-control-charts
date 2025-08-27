"""
AWS Integration Module for Petrobras Offshore Wells Anomaly Detection

Este módulo fornece integração completa com Amazon Web Services para:
- Configuração e gerenciamento de recursos AWS
- Treinamento de modelos usando SageMaker
- Armazenamento de dados e modelos no S3
- Monitoramento com CloudWatch
- Gerenciamento de custos e segurança
"""

from .aws_config_manager import AWSConfigManager
from .aws_training import AWSTrainingManager, TrainingJobConfig

__version__ = "1.0.0"
__author__ = "Petrobras Anomaly Detection Team"

__all__ = ["AWSConfigManager", "AWSTrainingManager", "TrainingJobConfig"]
