"""
Carregador de dados para séries temporais multivariadas.

Este módulo fornece funcionalidades para:
- Carregamento de dados de diferentes formatos
- Conversão para formatos adequados para ML
- Validação de dados
- Cache de dados para performance
"""

import logging
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import polars as pl
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler

from .threew_dataset import ThreeWDataset, is_threew_available


class TimeSeriesDataLoader:
    """
    Carregador de dados para séries temporais multivariadas.

    Suporta múltiplos formatos de entrada e prepara os dados
    para modelos de detecção de anomalias.
    """

    def __init__(
        self,
        data_path: str | Path | None = None,
        use_threew: bool = True,
        cache_data: bool = True,
    ):
        """
        Inicializa o carregador de dados.

        Args:
            data_path: Caminho para os dados
            use_threew: Se deve usar o dataset 3W quando disponível
            cache_data: Se deve fazer cache dos dados carregados
        """
        self.data_path = Path(data_path) if data_path else None
        self.use_threew = use_threew and is_threew_available()
        self.cache_data = cache_data

        # Cache para dados carregados
        self._data_cache = {}

        # Inicializa o dataset 3W se disponível
        if self.use_threew:
            try:
                self.threew_dataset = ThreeWDataset()
                logging.info("Dataset 3W inicializado com sucesso")
            except Exception as e:
                logging.warning(f"Erro ao inicializar dataset 3W: {e}")
                self.use_threew = False
        else:
            self.threew_dataset = None

        # Scaler para normalização
        self.scaler = None
        self.scaler_fitted = False

        logging.info(f"TimeSeriesDataLoader inicializado - 3W: {self.use_threew}")

    def load_from_parquet(
        self, file_path: str | Path, columns: list[str] | None = None
    ) -> pd.DataFrame | None:
        """
        Carrega dados de um arquivo Parquet.

        Args:
            file_path: Caminho para o arquivo Parquet
            columns: Lista de colunas para carregar (None para todas)

        Returns:
            DataFrame com os dados ou None se erro
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                logging.error(f"Arquivo não encontrado: {file_path}")
                return None

            # Usa Polars para carregamento rápido
            df_pl = pl.read_parquet(file_path, columns=columns)

            # Converte para Pandas se necessário
            df = df_pl.to_pandas()

            logging.info(f"Dados carregados de {file_path}: {df.shape}")
            return df

        except Exception as e:
            logging.error(f"Erro ao carregar arquivo Parquet: {e}")
            return None

    def load_from_csv(
        self,
        file_path: str | Path,
        separator: str = ",",
        columns: list[str] | None = None,
    ) -> pd.DataFrame | None:
        """
        Carrega dados de um arquivo CSV.

        Args:
            file_path: Caminho para o arquivo CSV
            separator: Separador de campos
            columns: Lista de colunas para carregar

        Returns:
            DataFrame com os dados ou None se erro
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                logging.error(f"Arquivo não encontrado: {file_path}")
                return None

            # Usa Polars para carregamento rápido
            df_pl = pl.read_csv(file_path, separator=separator, columns=columns)
            df = df_pl.to_pandas()

            logging.info(f"Dados carregados de {file_path}: {df.shape}")
            return df

        except Exception as e:
            logging.error(f"Erro ao carregar arquivo CSV: {e}")
            return None

    def load_threew_problem(
        self,
        problem_name: str,
        fold_config: str,
        fold_index: int = 0,
        normalize: bool = True,
        test_size: float = 0.2,
    ) -> dict[str, Any] | None:
        """
        Carrega dados de um problema específico do dataset 3W.

        Args:
            problem_name: Nome do problema
            fold_config: Configuração dos folds
            fold_index: Índice do fold
            normalize: Se deve normalizar os dados
            test_size: Proporção de dados para teste

        Returns:
            Dicionário com dados de treino e teste ou None se erro
        """
        if not self.use_threew or self.threew_dataset is None:
            logging.error("Dataset 3W não disponível")
            return None

        try:
            # Carrega as instâncias
            result = self.threew_dataset.load_instances_for_problem(
                problem_name, fold_config, fold_index
            )

            if result is None:
                return None

            X_train, y_train, X_test, y_test = result

            # Concatena todas as instâncias
            X_train_combined = np.concatenate(X_train, axis=0)
            y_train_combined = np.concatenate(y_train, axis=0)
            X_test_combined = np.concatenate(X_test, axis=0)
            y_test_combined = np.concatenate(y_test, axis=0)

            # Normaliza se solicitado
            if normalize:
                X_train_combined, X_test_combined = self._normalize_data(
                    X_train_combined, X_test_combined
                )

            # Divide em treino e validação
            X_train_final, X_val, y_train_final, y_val = train_test_split(
                X_train_combined,
                y_train_combined,
                test_size=test_size,
                random_state=42,
                stratify=y_train_combined,
            )

            data_dict = {
                "X_train": X_train_final,
                "y_train": y_train_final,
                "X_val": X_val,
                "y_val": y_val,
                "X_test": X_test_combined,
                "y_test": y_test_combined,
                "problem_name": problem_name,
                "fold_config": fold_config,
                "fold_index": fold_index,
                "normalized": normalize,
            }

            # Cache dos dados se habilitado
            if self.cache_data:
                cache_key = f"{problem_name}_{fold_config}_{fold_index}"
                self._data_cache[cache_key] = data_dict

            logging.info(f"Dados do problema {problem_name} carregados com sucesso")
            logging.info(
                f"Treino: {X_train_final.shape}, Val: {X_val.shape}, Teste: {X_test_combined.shape}"
            )

            return data_dict

        except Exception as e:
            logging.error(f"Erro ao carregar problema 3W: {e}")
            return None

    def _normalize_data(
        self, X_train: np.ndarray, X_test: np.ndarray, method: str = "standard"
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Normaliza os dados de treino e teste.

        Args:
            X_train: Dados de treino
            X_test: Dados de teste
            method: Método de normalização ('standard' ou 'minmax')

        Returns:
            Tupla com dados normalizados
        """
        if method == "standard":
            self.scaler = StandardScaler()
        elif method == "minmax":
            self.scaler = MinMaxScaler()
        else:
            raise ValueError(f"Método de normalização inválido: {method}")

        # Ajusta o scaler apenas nos dados de treino
        X_train_normalized = self.scaler.fit_transform(X_train)
        X_test_normalized = self.scaler.transform(X_test)

        self.scaler_fitted = True

        logging.info(f"Dados normalizados usando {method}")
        return X_train_normalized, X_test_normalized

    def get_cached_data(self, cache_key: str) -> dict[str, Any] | None:
        """
        Obtém dados do cache.

        Args:
            cache_key: Chave do cache

        Returns:
            Dados em cache ou None se não encontrado
        """
        return self._data_cache.get(cache_key)

    def clear_cache(self) -> None:
        """Limpa o cache de dados."""
        self._data_cache.clear()
        logging.info("Cache de dados limpo")

    def get_data_info(self) -> dict[str, Any]:
        """
        Retorna informações sobre o carregador de dados.

        Returns:
            Dicionário com informações
        """
        return {
            "use_threew": self.use_threew,
            "cache_enabled": self.cache_data,
            "cache_size": len(self._data_cache),
            "scaler_fitted": self.scaler_fitted,
            "data_path": str(self.data_path) if self.data_path else None,
        }

    def list_available_problems(self) -> list[str]:
        """
        Lista os problemas disponíveis no dataset 3W.

        Returns:
            Lista de problemas disponíveis
        """
        if self.threew_dataset:
            return self.threew_dataset.list_available_problems()
        return []

    def get_problem_info(self, problem_name: str) -> dict[str, Any] | None:
        """
        Obtém informações sobre um problema específico.

        Args:
            problem_name: Nome do problema

        Returns:
            Informações do problema ou None se não encontrado
        """
        if self.threew_dataset:
            return self.threew_dataset.load_problem_config(problem_name)
        return None


# Função de conveniência para criar um carregador
def create_data_loader(
    data_path: str | Path | None = None,
    use_threew: bool = True,
    cache_data: bool = True,
) -> TimeSeriesDataLoader:
    """
    Cria um carregador de dados configurado.

    Args:
        data_path: Caminho para os dados
        use_threew: Se deve usar o dataset 3W
        cache_data: Se deve fazer cache dos dados

    Returns:
        TimeSeriesDataLoader configurado
    """
    return TimeSeriesDataLoader(
        data_path=data_path, use_threew=use_threew, cache_data=cache_data
    )
