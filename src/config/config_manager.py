"""
Gerenciador de configurações para o projeto.

Este módulo fornece funcionalidades para:
- Carregamento de configurações de arquivos YAML
- Validação de configurações
- Configurações padrão
- Gerenciamento de diferentes ambientes
"""

import logging
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Optional, Union

import yaml


@dataclass
class DatasetConfig:
    """Configurações do dataset."""

    name: str
    version: str
    description: str
    paths: Dict[str, str]
    loading: Dict[str, Any]
    preprocessing: Dict[str, Any]
    rolling_window: Dict[str, Any]


@dataclass
class ExperimentConfig:
    """Configurações de experimentos."""

    n_folds: int
    cross_validation: bool
    hyperparameter_optimization: bool
    optimization_trials: int


@dataclass
class LoggingConfig:
    """Configurações de logging."""

    level: str
    format: str
    file: str


@dataclass
class CacheConfig:
    """Configurações de cache."""

    enabled: bool
    max_size: int
    ttl: int
    backend: str


@dataclass
class ValidationConfig:
    """Configurações de validação."""

    check_data_integrity: bool
    validate_schema: bool
    check_missing_values: bool
    outlier_detection: bool


@dataclass
class PerformanceConfig:
    """Configurações de performance."""

    use_multiprocessing: bool
    n_jobs: int
    batch_size: int
    memory_efficient: bool


@dataclass
class ExportConfig:
    """Configurações de exportação."""

    formats: list
    compression: str
    include_metadata: bool
    save_preprocessing_pipeline: bool


@dataclass
class ThreeWConfig:
    """Configuração completa do 3W."""

    dataset: DatasetConfig
    problems: list
    experiments: Dict[str, ExperimentConfig]
    logging: LoggingConfig
    cache: CacheConfig
    validation: ValidationConfig
    performance: PerformanceConfig
    export: ExportConfig


class ConfigManager:
    """
    Gerenciador de configurações para o projeto.

    Permite carregar e gerenciar configurações de diferentes
    arquivos e ambientes.
    """

    def __init__(self, config_dir: Optional[Union[str, Path]] = None):
        """
        Inicializa o gerenciador de configurações.

        Args:
            config_dir: Diretório de configurações (padrão: config/)
        """
        self.config_dir = (
            Path(config_dir)
            if config_dir
            else Path(__file__).parent.parent.parent / "config"
        )
        self.configs = {}
        self.logger = logging.getLogger(__name__)

        # Verifica se o diretório existe
        if not self.config_dir.exists():
            self.logger.warning(
                f"Diretório de configurações não encontrado: {self.config_dir}"
            )
            self.config_dir.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Diretório de configurações criado: {self.config_dir}")

    def load_config(self, config_name: str) -> Dict[str, Any]:
        """
        Carrega uma configuração específica.

        Args:
            config_name: Nome do arquivo de configuração (sem extensão)

        Returns:
            Dicionário com as configurações
        """
        config_file = self.config_dir / f"{config_name}.yaml"

        if not config_file.exists():
            self.logger.warning(
                f"Arquivo de configuração não encontrado: {config_file}"
            )
            return {}

        try:
            with open(config_file, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
                self.configs[config_name] = config
                self.logger.info(f"Configuração carregada: {config_name}")
                return config
        except Exception as e:
            self.logger.error(f"Erro ao carregar configuração {config_name}: {e}")
            return {}

    def get_config(self, config_name: str) -> Dict[str, Any]:
        """
        Obtém uma configuração (carrega se necessário).

        Args:
            config_name: Nome da configuração

        Returns:
            Dicionário com as configurações
        """
        if config_name not in self.configs:
            return self.load_config(config_name)
        return self.configs[config_name]

    def save_config(self, config_name: str, config: Dict[str, Any]) -> bool:
        """
        Salva uma configuração em arquivo.

        Args:
            config_name: Nome da configuração
            config: Dados da configuração

        Returns:
            True se salvo com sucesso, False caso contrário
        """
        try:
            config_file = self.config_dir / f"{config_name}.yaml"

            with open(config_file, "w", encoding="utf-8") as f:
                yaml.dump(
                    config, f, default_flow_style=False, allow_unicode=True, indent=2
                )

            self.configs[config_name] = config
            self.logger.info(f"Configuração salva: {config_name}")
            return True

        except Exception as e:
            self.logger.error(f"Erro ao salvar configuração {config_name}: {e}")
            return False

    def update_config(self, config_name: str, updates: Dict[str, Any]) -> bool:
        """
        Atualiza uma configuração existente.

        Args:
            config_name: Nome da configuração
            updates: Atualizações a aplicar

        Returns:
            True se atualizado com sucesso, False caso contrário
        """
        current_config = self.get_config(config_name)
        if not current_config:
            return False

        # Aplica as atualizações recursivamente
        updated_config = self._deep_update(current_config, updates)

        return self.save_config(config_name, updated_config)

    def _deep_update(
        self, base: Dict[str, Any], updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Atualiza recursivamente um dicionário.

        Args:
            base: Dicionário base
            updates: Atualizações a aplicar

        Returns:
            Dicionário atualizado
        """
        result = base.copy()

        for key, value in updates.items():
            if (
                key in result
                and isinstance(result[key], dict)
                and isinstance(value, dict)
            ):
                result[key] = self._deep_update(result[key], value)
            else:
                result[key] = value

        return result

    def validate_config(self, config_name: str) -> bool:
        """
        Valida uma configuração.

        Args:
            config_name: Nome da configuração

        Returns:
            True se válida, False caso contrário
        """
        config = self.get_config(config_name)
        if not config:
            return False

        # Implementa validações específicas aqui
        required_keys = ["dataset", "problems", "experiments"]

        for key in required_keys:
            if key not in config:
                self.logger.error(f"Chave obrigatória não encontrada: {key}")
                return False

        self.logger.info(f"Configuração {config_name} validada com sucesso")
        return True

    def get_default_config(self, config_name: str) -> Dict[str, Any]:
        """
        Retorna a configuração padrão para um tipo específico.

        Args:
            config_name: Nome do tipo de configuração

        Returns:
            Configuração padrão
        """
        defaults = {
            "3w": {
                "dataset": {
                    "name": "3W",
                    "version": "1.1.0",
                    "description": "Dataset 3W da Petrobras",
                    "paths": {
                        "toolkit": "3W/toolkit",
                        "dataset": "3W/dataset",
                        "folds": "3W/dataset/folds",
                        "problems": "3W/problems",
                    },
                    "loading": {
                        "use_cache": True,
                        "normalize_data": True,
                        "test_size": 0.2,
                    },
                    "preprocessing": {
                        "imputation_strategy": "mean",
                        "scaling_method": "robust",
                    },
                },
                "experiments": {"default": {"n_folds": 5, "cross_validation": True}},
            }
        }

        return defaults.get(config_name, {})

    def create_config_from_default(self, config_name: str) -> bool:
        """
        Cria uma configuração a partir dos padrões.

        Args:
            config_name: Nome da configuração

        Returns:
            True se criada com sucesso, False caso contrário
        """
        default_config = self.get_default_config(config_name)
        if not default_config:
            self.logger.error(f"Configuração padrão não encontrada para: {config_name}")
            return False

        return self.save_config(config_name, default_config)

    def list_configs(self) -> list:
        """
        Lista todas as configurações disponíveis.

        Returns:
            Lista de nomes de configurações
        """
        configs = []
        for config_file in self.config_dir.glob("*.yaml"):
            configs.append(config_file.stem)

        return configs


# Instância global do gerenciador de configurações
@lru_cache()
def get_config_manager() -> ConfigManager:
    """
    Retorna uma instância global do gerenciador de configurações.

    Returns:
        Instância do ConfigManager
    """
    return ConfigManager()


# Funções de conveniência
def load_threew_config() -> Dict[str, Any]:
    """
    Carrega a configuração do 3W.

    Returns:
        Configuração do 3W
    """
    config_manager = get_config_manager()
    return config_manager.get_config("3w")


def save_threew_config(config: Dict[str, Any]) -> bool:
    """
    Salva a configuração do 3W.

    Args:
        config: Configuração a salvar

    Returns:
        True se salvo com sucesso, False caso contrário
    """
    config_manager = get_config_manager()
    return config_manager.save_config("3w", config)


def get_threew_setting(setting_path: str, default: Any = None) -> Any:
    """
    Obtém uma configuração específica do 3W.

    Args:
        setting_path: Caminho da configuração (ex: 'dataset.loading.normalize_data')
        default: Valor padrão se não encontrado

    Returns:
        Valor da configuração ou padrão
    """
    config = load_threew_config()

    # Navega pela estrutura da configuração
    keys = setting_path.split(".")
    current = config

    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default

    return current
