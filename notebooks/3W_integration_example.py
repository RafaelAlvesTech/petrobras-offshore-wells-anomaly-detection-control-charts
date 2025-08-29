"""
Exemplo de Integração com o Dataset 3W da Petrobras

Este notebook demonstra como usar o módulo de integração 3W
para carregar e processar dados de detecção de anomalias em poços offshore.
"""

import marimo as mo
import logging
import sys
from pathlib import Path

# Importa os módulos do projeto
from src.data.data_loader import create_data_loader
from src.data.preprocessing import TimeSeriesPreprocessor
from src.data.threew_dataset import ThreeWDataset, get_threew_info

# Configura logging
logging.basicConfig(level=logging.INFO)

# Adiciona o caminho do projeto ao sys.path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# =============================================================================
# CÉLULAS MARIMO
# =============================================================================


@mo.cell
def title():
    mo.md("# 🛢️ Integração com Dataset 3W da Petrobras")
    mo.md(
        "Este notebook demonstra a integração com o dataset 3W para "
        "detecção de anomalias em poços offshore."
    )


@mo.cell
def check_availability():
    mo.md("## 📊 Verificação de Disponibilidade do Dataset 3W")

    try:
        threew_info = get_threew_info()
        mo.json(threew_info)

        if threew_info["available"]:
            mo.md("✅ Dataset 3W disponível!")
            return True
        else:
            mo.md(
                "❌ Dataset 3W não disponível. Verifique se o diretório 3W "
                "está presente."
            )
            mo.md("Para usar este notebook, clone o repositório 3W da Petrobras.")
            return False
    except Exception as e:
        mo.md(f"❌ Erro ao verificar disponibilidade: {e}")
        return False


@mo.cell
def initialize_dataset():
    mo.md("## 🔧 Inicialização do Dataset 3W")

    try:
        threew_dataset = ThreeWDataset()
        mo.md("✅ Dataset 3W inicializado com sucesso")

        dataset_info = threew_dataset.get_dataset_info()
        mo.json(dataset_info)

        return threew_dataset
    except Exception as e:
        mo.md(f"❌ Erro ao inicializar dataset 3W: {e}")
        return None


@mo.cell
def list_problems(threew_dataset):
    if not threew_dataset:
        mo.md("❌ Dataset 3W não disponível")
        return []

    mo.md("## 📋 Problemas Disponíveis")

    try:
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

        return problems
    except Exception as e:
        mo.md(f"❌ Erro ao listar problemas: {e}")
        return []


@mo.cell
def load_data(problems):
    if not problems:
        mo.md("❌ Nenhum problema disponível")
        return None

    mo.md("## 📊 Carregamento de Dados")

    try:
        data_loader = create_data_loader(use_threew=True, cache_data=True)
        mo.md("✅ Carregador de dados inicializado")

        loader_info = data_loader.get_data_info()
        mo.json(loader_info)

        # Tenta carregar dados do primeiro problema
        first_problem = problems[0]
        mo.md(f"Tentando carregar dados do problema: **{first_problem}**")

        # Verifica configurações de folds
        folds_dir = Path(project_root) / "3W" / "dataset" / "folds"
        if folds_dir.exists():
            fold_files = [f.stem for f in folds_dir.glob("*.csv")]
            mo.md(f"Configurações de folds disponíveis: {fold_files}")

            if fold_files:
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

                    # Resumo dos dados
                    data_summary = {
                        "Problema": data["problem_name"],
                        "Forma X_train": str(data["X_train"].shape),
                        "Forma y_train": str(data["y_train"].shape),
                        "Forma X_test": str(data["X_test"].shape),
                        "Forma y_test": str(data["y_test"].shape),
                        "Normalizado": data["normalized"],
                    }
                    mo.json(data_summary)

                    return data
                else:
                    mo.md("❌ Falha ao carregar dados")
            else:
                mo.md("❌ Nenhuma configuração de fold encontrada")
        else:
            mo.md("❌ Diretório de folds não encontrado")

    except Exception as e:
        mo.md(f"❌ Erro ao carregar dados: {e}")

    return None


@mo.cell
def preprocessing(data):
    if not data:
        mo.md("❌ Nenhum dado disponível para pré-processamento")
        return None

    mo.md("## 🧹 Pré-processamento de Dados")

    try:
        preprocessor = TimeSeriesPreprocessor(
            imputation_strategy="mean",
            scaling_method="robust",
            feature_selection_method="mutual_info",
            n_features=10,
            pca_components=5,
        )

        mo.md("✅ Pré-processador criado")

        # Aplica pré-processamento
        X_train_processed = preprocessor.fit_transform(data["X_train"], data["y_train"])
        X_test_processed = preprocessor.transform(data["X_test"])

        mo.md("✅ Pré-processamento aplicado com sucesso!")

        # Compara formas
        comparison = {
            "Original": {
                "X_train": str(data["X_train"].shape),
                "X_test": str(data["X_test"].shape),
            },
            "Processado": {
                "X_train": str(X_train_processed.shape),
                "X_test": str(X_test_processed.shape),
            },
        }
        mo.json(comparison)

        return {
            "preprocessor": preprocessor,
            "X_train_processed": X_train_processed,
            "X_test_processed": X_test_processed,
        }

    except Exception as e:
        mo.md(f"❌ Erro no pré-processamento: {e}")
        return None


@mo.cell
def summary(problems, data, preprocessing_result):
    mo.md("## 📝 Resumo da Integração")

    summary_data = {
        "Dataset 3W": "✅ Integrado com sucesso",
        "Problemas Disponíveis": len(problems) if problems else 0,
        "Dados Carregados": "✅ Sim" if data else "❌ Não",
        "Pré-processamento": (
            "✅ Aplicado" if preprocessing_result else "❌ Não aplicado"
        ),
    }

    mo.json(summary_data)


@mo.cell
def next_steps():
    mo.md("## 🎯 Próximos Passos")
    mo.md(
        """
    Com a integração funcionando, você pode:

    1. **Treinar modelos de ML**: Use os dados carregados para treinar modelos de detecção de anomalias
    2. **Experimentar com diferentes problemas**: Teste diferentes configurações de folds e problemas
    3. **Implementar novos modelos**: Adicione novos algoritmos ao projeto
    4. **Otimizar hiperparâmetros**: Use técnicas como Optuna para otimização
    5. **Avaliar performance**: Compare diferentes abordagens usando métricas apropriadas
    """
    )


@mo.cell
def configuration_help():
    mo.md("## ⚠️ Configuração Necessária")
    mo.md(
        """
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
    """
    )


@mo.cell
def documentation():
    mo.md("## 📚 Documentação Adicional")
    mo.md(
        """
    ### 🔗 Recursos Oficiais 3W
    - [**Repositório Principal 3W**](https://github.com/petrobras/3W) - Primeiro repositório público da Petrobras
    - [**Estrutura do Dataset**](https://github.com/petrobras/3W/blob/main/3W_DATASET_STRUCTURE.md) - Organização dos dados
    - [**Estrutura do Toolkit**](https://github.com/petrobras/3W/blob/main/3W_TOOLKIT_STRUCTURE.md) - Ferramentas disponíveis
    - [**Guia de Contribuição**](https://github.com/petrobras/3W/blob/main/CONTRIBUTING.md) - Como contribuir
    - [**Código de Conduta**](https://github.com/petrobras/3W/blob/main/CODE_OF_CONDUCT.md) - Padrões da comunidade

    ### 🌍 Comunidade e Eventos
    - [**Discussões no GitHub**](https://github.com/petrobras/3W/discussions) - Fórum da comunidade
    - [**Workshop 3W 2025**](https://forms.gle/cmLa2u4VaXd1T7qp8) - 4ª edição anual
    - [**Paper Acadêmico**](https://www.sciencedirect.com/science/article/abs/pii/S0920410522001234) - Journal of Petroleum Science and Engineering

    ### 📊 Características do Dataset
    - **Primeiro dataset público realista** com eventos raros reais em poços offshore
    - **Licença Creative Commons 4.0** para dados
    - **Licença Apache 2.0** para código
    - **Compressão Brotli** para eficiência de armazenamento
    """
    )


# =============================================================================
# APLICAÇÃO MARIMO
# =============================================================================

app = mo.App(
    title="3W Integration Example",
    cells=[
        title,
        check_availability,
        initialize_dataset,
        list_problems,
        load_data,
        preprocessing,
        summary,
        next_steps,
        configuration_help,
        documentation,
    ],
)

if __name__ == "__main__":
    app.run()
