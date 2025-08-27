"""
Integração com o Dataset 3W da Petrobras.

Este módulo fornece uma interface unificada para trabalhar com o dataset 3W,
incluindo carregamento de dados, configuração de folds e acesso aos problemas
implementados.
"""

import logging
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

# Adiciona o caminho do toolkit 3W ao sys.path
THREEW_PATH = Path(__file__).parent.parent.parent / "3W"
if THREEW_PATH.exists():
    sys.path.insert(0, str(THREEW_PATH))

try:
    from toolkit import (
        DATASET_VERSION,
        PATH_DATASET,
        PATH_FOLDS,
        EventFolds,
        EventType,
        Experiment,
    )

    THREEW_AVAILABLE = True
except ImportError as e:
    logging.warning(f"3W Toolkit não disponível: {e}")
    THREEW_AVAILABLE = False

    # Placeholder classes para quando o toolkit não estiver disponível
    class EventType:
        pass

    class EventFolds:
        pass

    class Experiment:
        pass


class ThreeWDataset:
    """
    Interface unificada para o Dataset 3W da Petrobras.

    Esta classe fornece métodos para:
    - Carregar instâncias do dataset
    - Configurar folds para validação cruzada
    - Acessar problemas implementados
    - Gerenciar metadados do dataset
    """

    def __init__(self, dataset_path: Optional[Union[str, Path]] = None):
        """
        Inicializa o acesso ao dataset 3W.

        Args:
            dataset_path: Caminho opcional para o dataset. Se None, usa o padrão.
        """
        if not THREEW_AVAILABLE:
            raise ImportError(
                "3W Toolkit não está disponível. "
                "Certifique-se de que o diretório 3W está presente."
            )

        self.dataset_path = Path(dataset_path) if dataset_path else PATH_DATASET
        self.folds_path = PATH_FOLDS
        self.version = DATASET_VERSION

        # Verifica se os diretórios existem
        if not self.dataset_path.exists():
            raise FileNotFoundError(f"Dataset não encontrado em: {self.dataset_path}")

        if not self.folds_path.exists():
            raise FileNotFoundError(
                f"Diretório de folds não encontrado em: {self.folds_path}"
            )

        logging.info(f"3W Dataset inicializado - Versão: {self.version}")
        logging.info(f"Dataset path: {self.dataset_path}")
        logging.info(f"Folds path: {self.folds_path}")

    def get_dataset_info(self) -> Dict[str, str]:
        """
        Retorna informações sobre o dataset.

        Returns:
            Dicionário com informações do dataset
        """
        return {
            "version": self.version,
            "dataset_path": str(self.dataset_path),
            "folds_path": str(self.folds_path),
            "available": THREEW_AVAILABLE,
        }

    def list_available_problems(self) -> List[str]:
        """
        Lista os problemas disponíveis no toolkit 3W.

        Returns:
            Lista de problemas disponíveis
        """
        problems_dir = Path(__file__).parent.parent.parent / "3W" / "problems"
        if not problems_dir.exists():
            return []

        problems = []
        for item in problems_dir.iterdir():
            if item.is_dir() and not item.name.startswith("_"):
                problems.append(item.name)

        return problems

    def load_problem_config(self, problem_name: str) -> Optional[Dict]:
        """
        Carrega a configuração de um problema específico.

        Args:
            problem_name: Nome do problema

        Returns:
            Configuração do problema ou None se não encontrado
        """
        problem_dir = (
            Path(__file__).parent.parent.parent / "3W" / "problems" / problem_name
        )
        if not problem_dir.exists():
            logging.warning(f"Problema '{problem_name}' não encontrado")
            return None

        config_file = problem_dir / "README.md"
        if config_file.exists():
            with open(config_file, "r", encoding="utf-8") as f:
                content = f.read()
                return {
                    "name": problem_name,
                    "description": content,
                    "path": str(problem_dir),
                }

        return None

    def get_event_folds(
        self, problem_name: str, fold_config: str
    ) -> Optional[EventFolds]:
        """
        Carrega os folds para um problema específico.

        Args:
            problem_name: Nome do problema
            fold_config: Nome do arquivo de configuração dos folds

        Returns:
            Objeto EventFolds ou None se não encontrado
        """
        try:
            # Constrói o caminho para o arquivo de configuração dos folds
            fold_file = self.folds_path / f"{fold_config}.csv"
            if not fold_file.exists():
                logging.warning(f"Arquivo de folds não encontrado: {fold_file}")
                return None

            # Carrega os folds usando o toolkit 3W
            folds = EventFolds(fold_file)
            logging.info(f"Folds carregados para {problem_name}: {len(folds)} folds")
            return folds

        except Exception as e:
            logging.error(f"Erro ao carregar folds: {e}")
            return None

    def load_instances_for_problem(
        self, problem_name: str, fold_config: str, fold_index: int = 0
    ) -> Optional[Tuple]:
        """
        Carrega as instâncias de treino e teste para um problema específico.

        Args:
            problem_name: Nome do problema
            fold_config: Nome do arquivo de configuração dos folds
            fold_index: Índice do fold (padrão: 0)

        Returns:
            Tupla (X_train, y_train, X_test, y_test) ou None se erro
        """
        try:
            # Carrega os folds
            folds = self.get_event_folds(problem_name, fold_config)
            if folds is None:
                return None

            # Obtém o fold específico
            if fold_index >= len(folds):
                logging.error(f"Índice de fold inválido: {fold_index}")
                return None

            fold = folds[fold_index]

            # Carrega as instâncias de treino
            train_instances = load_instances(fold.train_instances)
            X_train = []
            y_train = []

            for instance in train_instances:
                # Assumindo que a primeira coluna é o target
                X_train.append(instance.iloc[:, 1:].values)  # Features
                y_train.append(instance.iloc[:, 0].values)  # Target

            # Carrega as instâncias de teste
            test_instances = load_instances(fold.test_instances)
            X_test = []
            y_test = []

            for instance in test_instances:
                X_test.append(instance.iloc[:, 1:].values)  # Features
                y_test.append(instance.iloc[:, 0].values)  # Target

            logging.info(
                f"Instâncias carregadas - Treino: {len(X_train)}, Teste: {len(X_test)}"
            )

            return X_train, y_train, X_test, y_test

        except Exception as e:
            logging.error(f"Erro ao carregar instâncias: {e}")
            return None

    def get_problem_experiment(self, problem_name: str) -> Optional[Experiment]:
        """
        Cria um experimento para um problema específico.

        Args:
            problem_name: Nome do problema

        Returns:
            Objeto Experiment ou None se erro
        """
        try:
            # Carrega a configuração do problema
            config = self.load_problem_config(problem_name)
            if config is None:
                return None

            # Cria o experimento
            experiment = Experiment(
                name=problem_name,
                description=config.get("description", ""),
                path=config.get("path", ""),
            )

            logging.info(f"Experimento criado para {problem_name}")
            return experiment

        except Exception as e:
            logging.error(f"Erro ao criar experimento: {e}")
            return None


def load_instances(instances_path: str) -> List:
    """
    Carrega instâncias de dados do caminho especificado.

    Args:
        instances_path: Caminho para as instâncias

    Returns:
        Lista de instâncias carregadas
    """
    try:
        # Por enquanto, retorna uma lista vazia
        # Esta função deve ser implementada de acordo com o formato dos dados 3W
        logging.warning("Função load_instances não implementada completamente")
        return []
    except Exception as e:
        logging.error(f"Erro ao carregar instâncias: {e}")
        return []


# Função de conveniência para verificar disponibilidade
def is_threew_available() -> bool:
    """
    Verifica se o toolkit 3W está disponível.

    Returns:
        True se disponível, False caso contrário
    """
    return THREEW_AVAILABLE


# Função para obter informações do dataset
def get_threew_info() -> Dict[str, str]:
    """
    Retorna informações básicas sobre o dataset 3W.

    Returns:
        Dicionário com informações do dataset
    """
    if not THREEW_AVAILABLE:
        return {"available": False, "error": "3W Toolkit não disponível"}

    try:
        return {
            "available": True,
            "version": DATASET_VERSION,
            "dataset_path": str(PATH_DATASET),
            "folds_path": str(PATH_FOLDS),
        }
    except Exception as e:
        return {"available": False, "error": str(e)}
