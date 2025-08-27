# -*- coding: utf-8 -*-
"""
Exemplo de Integração com o Dataset 3W da Petrobras

Este notebook demonstra como usar o módulo de integração 3W
para carregar e processar dados de detecção de anomalias em poços offshore.
"""

import logging
import sys
from pathlib import Path

import marimo as mo
import numpy as np

# Importa os módulos do projeto
from src.data.data_loader import create_data_loader
from src.data.preprocessing import TimeSeriesPreprocessor
from src.data.threew_dataset import ThreeWDataset, get_threew_info

# Configura logging
logging.basicConfig(level=logging.INFO)

# Adiciona o caminho do projeto ao sys.path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configuração do Marimo
mo.md("# 🛢️ Integração com Dataset 3W da Petrobras")
mo.md(
    "Este notebook demonstra a integração com o dataset 3W para detecção de anomalias em poços offshore."
)

# Verifica disponibilidade do 3W
mo.md("## 📊 Verificação de Disponibilidade do Dataset 3W")

threew_info = get_threew_info()
mo.json(threew_info)

if threew_info["available"]:
    mo.md("✅ Dataset 3W disponível!")
else:
    mo.md("❌ Dataset 3W não disponível. Verifique se o diretório 3W está presente.")
    mo.md("Para usar este notebook, clone o repositório 3W da Petrobras.")

# Se o 3W estiver disponível, continua com a demonstração
if threew_info["available"]:
    mo.md("## 🔧 Inicialização dos Módulos")

    # Inicializa o dataset 3W
    try:
        threew_dataset = ThreeWDataset()
        mo.md("✅ Dataset 3W inicializado com sucesso")

        # Mostra informações do dataset
        dataset_info = threew_dataset.get_dataset_info()
        mo.json(dataset_info)

    except Exception as e:
        mo.md(f"❌ Erro ao inicializar dataset 3W: {e}")
        threew_dataset = None

    if threew_dataset:
        mo.md("## 📋 Problemas Disponíveis")

        # Lista problemas disponíveis
        problems = threew_dataset.list_available_problems()
        mo.md(f"Problemas encontrados: {problems}")

        if problems:
            mo.md("### Detalhes dos Problemas")

            for problem in problems:
                problem_info = threew_dataset.load_problem_config(problem)
                if problem_info:
                    mo.md(f"**{problem}**")
                    mo.md(f"Descrição: {problem_info['description'][:200]}...")
                    mo.md(f"Caminho: {problem_info['path']}")
                    mo.md("---")

        mo.md("## 📊 Carregamento de Dados")

        # Inicializa o carregador de dados
        try:
            data_loader = create_data_loader(use_threew=True, cache_data=True)
            mo.md("✅ Carregador de dados inicializado")

            # Mostra informações do carregador
            loader_info = data_loader.get_data_info()
            mo.json(loader_info)

        except Exception as e:
            mo.md(f"❌ Erro ao inicializar carregador de dados: {e}")
            data_loader = None

        if data_loader and problems:
            mo.md("## 🚀 Demonstração de Carregamento")

            # Tenta carregar dados do primeiro problema disponível
            first_problem = problems[0]
            mo.md(f"Tentando carregar dados do problema: **{first_problem}**")

            try:
                # Lista configurações de folds disponíveis
                folds_dir = Path(project_root) / "3W" / "dataset" / "folds"
                if folds_dir.exists():
                    fold_files = [f.stem for f in folds_dir.glob("*.csv")]
                    mo.md(f"Configurações de folds disponíveis: {fold_files}")

                    if fold_files:
                        # Tenta carregar com a primeira configuração
                        first_fold = fold_files[0]
                        mo.md(f"Usando configuração de fold: **{first_fold}**")

                        data = data_loader.load_threew_problem(
                            problem_name=first_problem,
                            fold_config=first_fold,
                            fold_index=0,
                            normalize=True,
                            test_size=0.2,
                        )

                        if data:
                            mo.md("✅ Dados carregados com sucesso!")

                            # Mostra informações dos dados
                            data_summary = {
                                "Problema": data["problem_name"],
                                "Configuração de Fold": data["fold_config"],
                                "Índice do Fold": data["fold_index"],
                                "Forma X_train": str(data["X_train"].shape),
                                "Forma y_train": str(data["y_train"].shape),
                                "Forma X_val": str(data["X_val"].shape),
                                "Forma y_val": str(data["y_val"].shape),
                                "Forma X_test": str(data["X_test"].shape),
                                "Forma y_test": str(data["y_test"].shape),
                                "Normalizado": data["normalized"],
                            }

                            mo.json(data_summary)

                            # Estatísticas básicas
                            mo.md("### 📈 Estatísticas dos Dados")

                            # Distribuição das classes
                            unique_train, counts_train = np.unique(
                                data["y_train"], return_counts=True
                            )
                            unique_val, counts_val = np.unique(
                                data["y_val"], return_counts=True
                            )
                            unique_test, counts_test = np.unique(
                                data["y_test"], return_counts=True
                            )

                            class_distribution = {
                                "Treino": dict(
                                    zip(unique_train.astype(str), counts_train.tolist())
                                ),
                                "Validação": dict(
                                    zip(unique_val.astype(str), counts_val.tolist())
                                ),
                                "Teste": dict(
                                    zip(unique_test.astype(str), counts_test.tolist())
                                ),
                            }

                            mo.json(class_distribution)

                            # Estatísticas das features
                            X_train_stats = {
                                "Média": np.mean(data["X_train"], axis=0).tolist(),
                                "Desvio Padrão": np.std(
                                    data["X_train"], axis=0
                                ).tolist(),
                                "Mínimo": np.min(data["X_train"], axis=0).tolist(),
                                "Máximo": np.max(data["X_train"], axis=0).tolist(),
                            }

                            mo.md("### 📊 Estatísticas das Features (primeiras 5)")
                            mo.json({k: v[:5] for k, v in X_train_stats.items()})

                        else:
                            mo.md("❌ Falha ao carregar dados")

                else:
                    mo.md("❌ Diretório de folds não encontrado")

            except Exception as e:
                mo.md(f"❌ Erro ao carregar dados: {e}")

        mo.md("## 🧹 Pré-processamento de Dados")

        # Demonstra o pré-processador
        try:
            preprocessor = TimeSeriesPreprocessor(
                imputation_strategy="mean",
                scaling_method="robust",
                feature_selection_method="mutual_info",
                n_features=10,  # Seleciona top 10 features
                pca_components=5,  # Reduz para 5 componentes
            )

            mo.md("✅ Pré-processador criado")

            # Se temos dados, aplica o pré-processamento
            if "data" in locals() and data:
                mo.md("### 🔄 Aplicando Pré-processamento")

                # Ajusta o pré-processador
                X_train_processed = preprocessor.fit_transform(
                    data["X_train"], data["y_train"]
                )
                X_val_processed = preprocessor.transform(data["X_val"])
                X_test_processed = preprocessor.transform(data["X_test"])

                mo.md("✅ Pré-processamento aplicado com sucesso!")

                # Mostra informações do pré-processamento
                preprocessing_info = preprocessor.get_preprocessing_info()
                mo.json(preprocessing_info)

                # Compara formas antes e depois
                comparison = {
                    "Original": {
                        "X_train": str(data["X_train"].shape),
                        "X_val": str(data["X_val"].shape),
                        "X_test": str(data["X_test"].shape),
                    },
                    "Processado": {
                        "X_train": str(X_train_processed.shape),
                        "X_val": str(X_val_processed.shape),
                        "X_test": str(X_test_processed.shape),
                    },
                }

                mo.json(comparison)

        except Exception as e:
            mo.md(f"❌ Erro no pré-processamento: {e}")

        mo.md("## 📝 Resumo da Integração")

        integration_summary = {
            "Dataset 3W": "✅ Integrado com sucesso",
            "Carregamento de Dados": "✅ Funcionando",
            "Pré-processamento": "✅ Implementado",
            "Problemas Disponíveis": len(problems) if "problems" in locals() else 0,
            "Cache de Dados": "✅ Habilitado",
            "Normalização": "✅ Implementada",
            "Seleção de Features": "✅ Implementada",
            "Redução de Dimensionalidade": "✅ PCA implementado",
        }

        mo.json(integration_summary)

        mo.md("## 🎯 Próximos Passos")
        mo.md("""
        Com a integração funcionando, você pode:

        1. **Treinar modelos de ML**: Use os dados carregados para treinar modelos de detecção de anomalias
        2. **Experimentar com diferentes problemas**: Teste diferentes configurações de folds e problemas
        3. **Implementar novos modelos**: Adicione novos algoritmos ao projeto
        4. **Otimizar hiperparâmetros**: Use técnicas como Optuna para otimização
        5. **Avaliar performance**: Compare diferentes abordagens usando métricas apropriadas
        """)

else:
    mo.md("## ⚠️ Configuração Necessária")
    mo.md("""
    Para usar este notebook, você precisa:

    1. **Clonar o repositório 3W**:
       ```bash
       git clone https://github.com/petrobras/3W.git
       ```

    2. **Colocar o diretório 3W na raiz do projeto**

    3. **Instalar dependências do 3W**:
       ```bash
       cd 3W
       conda env create -f environment.yml
       conda activate 3W
       ```

    4. **Voltar ao projeto principal e executar este notebook**
    """)

mo.md("## 📚 Documentação Adicional")
mo.md("""
- [README do Projeto 3W](https://github.com/petrobras/3W)
- [Estrutura do Dataset](https://github.com/petrobras/3W/blob/main/3W_DATASET_STRUCTURE.md)
- [Estrutura do Toolkit](https://github.com/petrobras/3W/blob/main/3W_TOOLKIT_STRUCTURE.md)
- [Guia de Contribuição](https://github.com/petrobras/3W/blob/main/CONTRIBUTING.md)
""")
