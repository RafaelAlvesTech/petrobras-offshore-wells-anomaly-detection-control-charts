"""
Pré-processamento de séries temporais multivariadas.

Este módulo fornece funcionalidades para:
- Limpeza e validação de dados
- Engenharia de atributos
- Redução de dimensionalidade
- Preparação para modelos de ML
"""

import logging
import warnings
from typing import Any

import numpy as np
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler, RobustScaler, StandardScaler

warnings.filterwarnings("ignore")


class TimeSeriesPreprocessor:
    """
    Pré-processador para séries temporais multivariadas.

    Implementa técnicas de limpeza, normalização e engenharia
    de atributos específicas para detecção de anomalias.
    """

    def __init__(
        self,
        imputation_strategy: str = "mean",
        scaling_method: str = "robust",
        feature_selection_method: str = "mutual_info",
        n_features: int | None = None,
        pca_components: int | None = None,
    ):
        """
        Inicializa o pré-processador.

        Args:
            imputation_strategy: Estratégia para valores faltantes
            scaling_method: Método de normalização
            feature_selection_method: Método de seleção de atributos
            n_features: Número de atributos a selecionar
            pca_components: Número de componentes PCA
        """
        self.imputation_strategy = imputation_strategy
        self.scaling_method = scaling_method
        self.feature_selection_method = feature_selection_method
        self.n_features = n_features
        self.pca_components = pca_components

        # Inicializa os transformadores
        self.imputer = None
        self.scaler = None
        self.feature_selector = None
        self.pca = None

        # Flags de ajuste
        self.is_fitted = False

        logging.info("TimeSeriesPreprocessor inicializado")

    def fit_transform(self, X: np.ndarray, y: np.ndarray | None = None) -> np.ndarray:
        """
        Ajusta o pré-processador e transforma os dados.

        Args:
            X: Dados de entrada
            y: Labels (opcional, usado para seleção de atributos)

        Returns:
            Dados pré-processados
        """
        return self.fit(X, y).transform(X)

    def fit(
        self, X: np.ndarray, y: np.ndarray | None = None
    ) -> "TimeSeriesPreprocessor":
        """
        Ajusta o pré-processador aos dados.

        Args:
            X: Dados de entrada
            y: Labels (opcional)

        Returns:
            Self para encadeamento
        """
        logging.info(f"Ajustando pré-processador para dados de forma {X.shape}")

        # 1. Imputação de valores faltantes
        self._fit_imputer(X)

        # 2. Normalização
        self._fit_scaler(X)

        # 3. Seleção de atributos (se especificado)
        if self.n_features and self.n_features < X.shape[1]:
            self._fit_feature_selector(X, y)

        # 4. PCA (se especificado)
        if self.pca_components and self.pca_components < X.shape[1]:
            self._fit_pca(X)

        self.is_fitted = True
        logging.info("Pré-processador ajustado com sucesso")

        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        """
        Transforma os dados usando o pré-processador ajustado.

        Args:
            X: Dados de entrada

        Returns:
            Dados transformados
        """
        if not self.is_fitted:
            raise ValueError("Pré-processador deve ser ajustado antes de transformar")

        X_transformed = X.copy()

        # 1. Imputação
        if self.imputer:
            X_transformed = self.imputer.transform(X_transformed)

        # 2. Normalização
        if self.scaler:
            X_transformed = self.scaler.transform(X_transformed)

        # 3. Seleção de atributos
        if self.feature_selector:
            X_transformed = self.feature_selector.transform(X_transformed)

        # 4. PCA
        if self.pca:
            X_transformed = self.pca.transform(X_transformed)

        logging.info(f"Dados transformados: {X.shape} -> {X_transformed.shape}")
        return X_transformed

    def _fit_imputer(self, X: np.ndarray) -> None:
        """Ajusta o imputer para valores faltantes."""
        if np.isnan(X).any():
            self.imputer = SimpleImputer(strategy=self.imputation_strategy)
            self.imputer.fit(X)
            logging.info(f"Imputer ajustado com estratégia: {self.imputation_strategy}")
        else:
            logging.info("Nenhum valor faltante encontrado, imputer não necessário")

    def _fit_scaler(self, X: np.ndarray) -> None:
        """Ajusta o scaler para normalização."""
        if self.scaling_method == "standard":
            self.scaler = StandardScaler()
        elif self.scaling_method == "minmax":
            self.scaler = MinMaxScaler()
        elif self.scaling_method == "robust":
            self.scaler = RobustScaler()
        else:
            raise ValueError(f"Método de normalização inválido: {self.scaling_method}")

        # Ajusta o scaler
        self.scaler.fit(X)
        logging.info(f"Scaler ajustado com método: {self.scaling_method}")

    def _fit_feature_selector(self, X: np.ndarray, y: np.ndarray | None) -> None:
        """Ajusta o seletor de atributos."""
        if y is None:
            logging.warning(
                "Labels não fornecidos, usando seleção baseada em variância"
            )
            # Seleção baseada em variância quando não há labels
            from sklearn.feature_selection import VarianceThreshold

            self.feature_selector = VarianceThreshold(threshold=0.01)
        else:
            if self.feature_selection_method == "mutual_info":
                self.feature_selector = SelectKBest(
                    score_func=mutual_info_classif, k=self.n_features
                )
            elif self.feature_selection_method == "f_classif":
                self.feature_selector = SelectKBest(
                    score_func=f_classif, k=self.n_features
                )
            else:
                raise ValueError(
                    f"Método de seleção inválido: {self.feature_selection_method}"
                )

        self.feature_selector.fit(X, y)
        logging.info(
            f"Seletor de atributos ajustado: {self.n_features} atributos selecionados"
        )

    def _fit_pca(self, X: np.ndarray) -> None:
        """Ajusta o PCA para redução de dimensionalidade."""
        self.pca = PCA(n_components=self.pca_components)
        self.pca.fit(X)

        explained_variance_ratio = self.pca.explained_variance_ratio_.sum()
        logging.info(
            f"PCA ajustado: {self.pca_components} componentes, "
            f"variância explicada: {explained_variance_ratio:.3f}"
        )

    def get_feature_names(
        self, original_features: list[str] | None = None
    ) -> list[str]:
        """
        Retorna os nomes dos atributos após o pré-processamento.

        Args:
            original_features: Lista original de nomes de atributos

        Returns:
            Lista de nomes de atributos finais
        """
        if not self.is_fitted:
            return []

        features = original_features or [f"feature_{i}" for i in range(1000)]

        # Aplica seleção de atributos
        if self.feature_selector:
            selected_indices = self.feature_selector.get_support()
            features = [
                features[i] for i, selected in enumerate(selected_indices) if selected
            ]

        # Aplica PCA
        if self.pca:
            features = [f"pca_component_{i}" for i in range(self.pca_components)]

        return features

    def get_preprocessing_info(self) -> dict[str, Any]:
        """
        Retorna informações sobre o pré-processamento aplicado.

        Returns:
            Dicionário com informações do pré-processamento
        """
        info = {
            "is_fitted": self.is_fitted,
            "imputation_strategy": self.imputation_strategy,
            "scaling_method": self.scaling_method,
            "feature_selection_method": self.feature_selection_method,
            "n_features": self.n_features,
            "pca_components": self.pca_components,
            "has_imputer": self.imputer is not None,
            "has_scaler": self.scaler is not None,
            "has_feature_selector": self.feature_selector is not None,
            "has_pca": self.pca is not None,
        }

        if self.pca and self.is_fitted:
            info["explained_variance_ratio"] = self.pca.explained_variance_ratio_.sum()

        return info

    def inverse_transform(self, X: np.ndarray) -> np.ndarray:
        """
        Aplica a transformação inversa (quando possível).

        Args:
            X: Dados transformados

        Returns:
            Dados com transformação inversa aplicada
        """
        if not self.is_fitted:
            raise ValueError("Pré-processador deve ser ajustado antes de transformar")

        X_inverse = X.copy()

        # PCA inverso
        if self.pca:
            X_inverse = self.pca.inverse_transform(X_inverse)

        # Seleção de atributos não tem inversa
        # Scaler inverso
        if self.scaler:
            X_inverse = self.scaler.inverse_transform(X_inverse)

        # Imputer não tem inversa

        return X_inverse


class RollingWindowPreprocessor:
    """
    Pré-processador específico para janelas deslizantes em séries temporais.

    Útil para modelos que trabalham com janelas de tempo fixas.
    """

    def __init__(
        self, window_size: int = 100, step_size: int = 1, padding: str = "same"
    ):
        """
        Inicializa o pré-processador de janelas deslizantes.

        Args:
            window_size: Tamanho da janela
            step_size: Tamanho do passo
            padding: Tipo de padding ('same', 'valid', 'full')
        """
        self.window_size = window_size
        self.step_size = step_size
        self.padding = padding

        logging.info(
            f"RollingWindowPreprocessor inicializado: "
            f"window_size={window_size}, step_size={step_size}"
        )

    def create_windows(
        self, X: np.ndarray, y: np.ndarray | None = None
    ) -> tuple[np.ndarray, np.ndarray | None]:
        """
        Cria janelas deslizantes dos dados.

        Args:
            X: Dados de entrada (n_samples, n_features)
            y: Labels (opcional)

        Returns:
            Tupla com janelas de dados e labels correspondentes
        """
        n_samples, n_features = X.shape

        if self.padding == "same":
            # Padding para manter o mesmo número de amostras
            pad_size = self.window_size // 2
            X_padded = np.pad(X, ((pad_size, pad_size), (0, 0)), mode="edge")
        elif self.padding == "valid":
            # Sem padding
            X_padded = X
            pad_size = 0
        else:  # "full"
            # Padding completo
            pad_size = self.window_size - 1
            X_padded = np.pad(X, ((pad_size, pad_size), (0, 0)), mode="edge")

        # Calcula o número de janelas
        n_windows = (n_samples + 2 * pad_size - self.window_size) // self.step_size + 1

        # Cria as janelas
        windows = np.zeros((n_windows, self.window_size, n_features))
        for i in range(n_windows):
            start_idx = i * self.step_size
            end_idx = start_idx + self.window_size
            windows[i] = X_padded[start_idx:end_idx]

        # Cria labels correspondentes
        if y is not None:
            if self.padding == "same":
                y_windows = y
            else:
                y_windows = y[
                    pad_size : pad_size + n_windows * self.step_size : self.step_size
                ]
        else:
            y_windows = None

        logging.info(f"Janelas criadas: {X.shape} -> {windows.shape}")
        return windows, y_windows

    def flatten_windows(self, windows: np.ndarray) -> np.ndarray:
        """
        Achatas as janelas para formato 2D.

        Args:
            windows: Janelas de dados (n_windows, window_size, n_features)

        Returns:
            Dados achatados (n_windows, window_size * n_features)
        """
        n_windows, window_size, n_features = windows.shape
        flattened = windows.reshape(n_windows, window_size * n_features)

        logging.info(f"Janelas achatadas: {windows.shape} -> {flattened.shape}")
        return flattened


# Funções de conveniência
def create_preprocessor(
    imputation_strategy: str = "mean",
    scaling_method: str = "robust",
    feature_selection_method: str = "mutual_info",
    n_features: int | None = None,
    pca_components: int | None = None,
) -> TimeSeriesPreprocessor:
    """
    Cria um pré-processador configurado.

    Args:
        imputation_strategy: Estratégia para valores faltantes
        scaling_method: Método de normalização
        feature_selection_method: Método de seleção de atributos
        n_features: Número de atributos a selecionar
        pca_components: Número de componentes PCA

    Returns:
        TimeSeriesPreprocessor configurado
    """
    return TimeSeriesPreprocessor(
        imputation_strategy=imputation_strategy,
        scaling_method=scaling_method,
        feature_selection_method=feature_selection_method,
        n_features=n_features,
        pca_components=pca_components,
    )


def create_rolling_window_preprocessor(
    window_size: int = 100, step_size: int = 1, padding: str = "same"
) -> RollingWindowPreprocessor:
    """
    Cria um pré-processador de janelas deslizantes.

    Args:
        window_size: Tamanho da janela
        step_size: Tamanho do passo
        padding: Tipo de padding

    Returns:
        RollingWindowPreprocessor configurado
    """
    return RollingWindowPreprocessor(
        window_size=window_size, step_size=step_size, padding=padding
    )
