"""
Módulo de dados para detecção de anomalias em poços offshore.

Este módulo contém funcionalidades para:
- Carregamento e processamento de dados do dataset 3W
- Pré-processamento de séries temporais multivariadas
- Engenharia de atributos para detecção de anomalias
- Validação e limpeza de dados
"""

from . import data_loader, preprocessing, threew_dataset

__all__ = ["threew_dataset", "data_loader", "preprocessing"]
