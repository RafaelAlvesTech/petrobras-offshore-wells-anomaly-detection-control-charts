"""
Configurações específicas para o Dataset 3W da Petrobras.

Este módulo contém configurações e constantes específicas
para trabalhar com o dataset 3W.
"""

from typing import Any, Dict

from .config_manager import get_threew_setting

# Constantes do Dataset 3W
THREEW_DATASET_NAME = "3W"
THREEW_DATASET_VERSION = "1.1.0"
THREEW_DESCRIPTION = (
    "Dataset 3W da Petrobras para detecção de anomalias em poços offshore"
)

# Problemas disponíveis
THREEW_AVAILABLE_PROBLEMS = ["01_binary_classifier_of_spurious_closure_of_dhsv"]

# Configurações padrão de carregamento
DEFAULT_LOADING_CONFIG = {
    "use_cache": True,
    "cache_size": 1000,  # MB
    "normalize_data": True,
    "test_size": 0.2,
    "random_state": 42,
    "shuffle": True,
    "stratify": True,
}

# Configurações padrão de pré-processamento
DEFAULT_PREPROCESSING_CONFIG = {
    "imputation_strategy": "mean",  # mean, median, most_frequent
    "scaling_method": "robust",  # standard, minmax, robust
    "feature_selection_method": "mutual_info",  # mutual_info, f_classif, variance
    "n_features": None,  # None para usar todas, ou número específico
    "pca_components": None,  # None para não usar PCA, ou número específico
    "outlier_detection": True,
    "outlier_method": "isolation_forest",
}

# Configurações padrão de janelas deslizantes
DEFAULT_ROLLING_WINDOW_CONFIG = {
    "window_size": 100,
    "step_size": 1,
    "padding": "same",  # same, valid, full
    "overlap": True,
}

# Configurações padrão de experimentos
DEFAULT_EXPERIMENT_CONFIG = {
    "n_folds": 5,
    "cross_validation": True,
    "hyperparameter_optimization": True,
    "optimization_trials": 100,
    "optimization_method": "optuna",
    "metric": "f1_score",
    "scoring": "f1_weighted",
}

# Configurações padrão de validação
DEFAULT_VALIDATION_CONFIG = {
    "check_data_integrity": True,
    "validate_schema": True,
    "check_missing_values": True,
    "outlier_detection": True,
    "data_quality_threshold": 0.95,
    "max_missing_ratio": 0.1,
}

# Configurações padrão de performance
DEFAULT_PERFORMANCE_CONFIG = {
    "use_multiprocessing": True,
    "n_jobs": -1,  # -1 para usar todos os cores
    "batch_size": 1000,
    "memory_efficient": True,
    "chunk_size": 10000,
}

# Configurações padrão de cache
DEFAULT_CACHE_CONFIG = {
    "enabled": True,
    "max_size": 1000,  # MB
    "ttl": 3600,  # segundos
    "backend": "memory",  # memory, disk, redis
    "compression": True,
}

# Configurações padrão de exportação
DEFAULT_EXPORT_CONFIG = {
    "formats": ["parquet", "csv", "numpy"],
    "compression": "brotli",
    "include_metadata": True,
    "save_preprocessing_pipeline": True,
    "save_model": True,
    "save_predictions": True,
}

# Configurações padrão de logging
DEFAULT_LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "logs/3w_integration.log",
    "console": True,
    "rotation": "1 day",
    "retention": "30 days",
}


def get_threew_dataset_config() -> Dict[str, Any]:
    """
    Retorna a configuração completa do dataset 3W.

    Returns:
        Dicionário com todas as configurações
    """
    return {
        "dataset": {
            "name": THREEW_DATASET_NAME,
            "version": THREEW_DATASET_VERSION,
            "description": THREEW_DESCRIPTION,
            "paths": {
                "toolkit": "3W/toolkit",
                "dataset": "3W/dataset",
                "folds": "3W/dataset/folds",
                "problems": "3W/problems",
                "overviews": "3W/overviews",
            },
        },
        "problems": THREEW_AVAILABLE_PROBLEMS,
        "loading": DEFAULT_LOADING_CONFIG,
        "preprocessing": DEFAULT_PREPROCESSING_CONFIG,
        "rolling_window": DEFAULT_ROLLING_WINDOW_CONFIG,
        "experiments": {"default": DEFAULT_EXPERIMENT_CONFIG},
        "validation": DEFAULT_VALIDATION_CONFIG,
        "performance": DEFAULT_PERFORMANCE_CONFIG,
        "cache": DEFAULT_CACHE_CONFIG,
        "export": DEFAULT_EXPORT_CONFIG,
        "logging": DEFAULT_LOGGING_CONFIG,
    }


def get_threew_problem_config(problem_name: str) -> Dict[str, Any]:
    """
    Retorna a configuração específica de um problema.

    Args:
        problem_name: Nome do problema

    Returns:
        Configuração do problema
    """
    if problem_name == "01_binary_classifier_of_spurious_closure_of_dhsv":
        return {
            "name": problem_name,
            "type": "classification",
            "target_column": 0,  # Primeira coluna é o target
            "binary": True,
            "positive_class": 1,
            "negative_class": 0,
            "metrics": ["accuracy", "precision", "recall", "f1_score", "roc_auc"],
            "cv_strategy": "stratified_kfold",
            "n_splits": 5,
            "shuffle": True,
            "random_state": 42,
        }

    # Configuração padrão para problemas não reconhecidos
    return {
        "name": problem_name,
        "type": "unknown",
        "target_column": 0,
        "binary": False,
        "metrics": ["accuracy"],
        "cv_strategy": "kfold",
        "n_splits": 5,
        "shuffle": True,
        "random_state": 42,
    }


def get_threew_preprocessing_config() -> Dict[str, Any]:
    """
    Retorna a configuração de pré-processamento.

    Returns:
        Configuração de pré-processamento
    """
    return DEFAULT_PREPROCESSING_CONFIG.copy()


def get_threew_experiment_config(experiment_name: str = "default") -> Dict[str, Any]:
    """
    Retorna a configuração de experimentos.

    Args:
        experiment_name: Nome do experimento

    Returns:
        Configuração do experimento
    """
    if experiment_name == "default":
        return DEFAULT_EXPERIMENT_CONFIG.copy()

    # Pode ser expandido para outros tipos de experimentos
    return DEFAULT_EXPERIMENT_CONFIG.copy()


def get_threew_validation_config() -> Dict[str, Any]:
    """
    Retorna a configuração de validação.

    Returns:
        Configuração de validação
    """
    return DEFAULT_VALIDATION_CONFIG.copy()


def get_threew_performance_config() -> Dict[str, Any]:
    """
    Retorna a configuração de performance.

    Returns:
        Configuração de performance
    """
    return DEFAULT_PERFORMANCE_CONFIG.copy()


def get_threew_cache_config() -> Dict[str, Any]:
    """
    Retorna a configuração de cache.

    Returns:
        Configuração de cache
    """
    return DEFAULT_CACHE_CONFIG.copy()


def get_threew_export_config() -> Dict[str, Any]:
    """
    Retorna a configuração de exportação.

    Returns:
        Configuração de exportação
    """
    return DEFAULT_EXPORT_CONFIG.copy()


def get_threew_logging_config() -> Dict[str, Any]:
    """
    Retorna a configuração de logging.

    Returns:
        Configuração de logging
    """
    return DEFAULT_LOGGING_CONFIG.copy()


# Funções de conveniência para configurações específicas
def get_threew_window_size() -> int:
    """Retorna o tamanho da janela padrão."""
    return get_threew_setting(
        "rolling_window.window_size", DEFAULT_ROLLING_WINDOW_CONFIG["window_size"]
    )


def get_threew_step_size() -> int:
    """Retorna o tamanho do passo padrão."""
    return get_threew_setting(
        "rolling_window.step_size", DEFAULT_ROLLING_WINDOW_CONFIG["step_size"]
    )


def get_threew_padding() -> str:
    """Retorna o tipo de padding padrão."""
    return get_threew_setting(
        "rolling_window.padding", DEFAULT_ROLLING_WINDOW_CONFIG["padding"]
    )


def get_threew_scaling_method() -> str:
    """Retorna o método de normalização padrão."""
    return get_threew_setting(
        "preprocessing.scaling_method", DEFAULT_PREPROCESSING_CONFIG["scaling_method"]
    )


def get_threew_imputation_strategy() -> str:
    """Retorna a estratégia de imputação padrão."""
    return get_threew_setting(
        "preprocessing.imputation_strategy",
        DEFAULT_PREPROCESSING_CONFIG["imputation_strategy"],
    )


def get_threew_feature_selection_method() -> str:
    """Retorna o método de seleção de atributos padrão."""
    return get_threew_setting(
        "preprocessing.feature_selection_method",
        DEFAULT_PREPROCESSING_CONFIG["feature_selection_method"],
    )


def get_threew_n_features() -> int:
    """Retorna o número de atributos a selecionar."""
    return get_threew_setting(
        "preprocessing.n_features", DEFAULT_PREPROCESSING_CONFIG["n_features"]
    )


def get_threew_pca_components() -> int:
    """Retorna o número de componentes PCA."""
    return get_threew_setting(
        "preprocessing.pca_components", DEFAULT_PREPROCESSING_CONFIG["pca_components"]
    )


def get_threew_test_size() -> float:
    """Retorna o tamanho do conjunto de teste."""
    return get_threew_setting("loading.test_size", DEFAULT_LOADING_CONFIG["test_size"])


def get_threew_random_state() -> int:
    """Retorna o estado aleatório padrão."""
    return get_threew_setting(
        "loading.random_state", DEFAULT_LOADING_CONFIG["random_state"]
    )


def get_threew_n_folds() -> int:
    """Retorna o número de folds para validação cruzada."""
    return get_threew_setting(
        "experiments.default.n_folds", DEFAULT_EXPERIMENT_CONFIG["n_folds"]
    )


def get_threew_optimization_trials() -> int:
    """Retorna o número de tentativas para otimização de hiperparâmetros."""
    return get_threew_setting(
        "experiments.default.optimization_trials",
        DEFAULT_EXPERIMENT_CONFIG["optimization_trials"],
    )


def get_threew_metric() -> str:
    """Retorna a métrica padrão para avaliação."""
    return get_threew_setting(
        "experiments.default.metric", DEFAULT_EXPERIMENT_CONFIG["metric"]
    )


def get_threew_use_cache() -> bool:
    """Retorna se o cache está habilitado."""
    return get_threew_setting("cache.enabled", DEFAULT_CACHE_CONFIG["enabled"])


def get_threew_cache_size() -> int:
    """Retorna o tamanho máximo do cache."""
    return get_threew_setting("cache.max_size", DEFAULT_CACHE_CONFIG["max_size"])


def get_threew_n_jobs() -> int:
    """Retorna o número de jobs para processamento paralelo."""
    return get_threew_setting(
        "performance.n_jobs", DEFAULT_PERFORMANCE_CONFIG["n_jobs"]
    )


def get_threew_batch_size() -> int:
    """Retorna o tamanho do lote para processamento."""
    return get_threew_setting(
        "performance.batch_size", DEFAULT_PERFORMANCE_CONFIG["batch_size"]
    )
