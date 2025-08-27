# 🛢️ Integração com Dataset 3W da Petrobras

## 📋 Visão Geral

Este documento descreve a integração completa do projeto com o **Dataset 3W da Petrobras**, um dataset público para detecção de anomalias em poços offshore. A integração permite usar dados reais da indústria petrolífera para treinar e avaliar modelos de machine learning.

## 🎯 Sobre o Dataset 3W

### Características Principais
- **Fonte**: Petrobras (primeiro repositório público da empresa)
- **Tipo**: Séries temporais multivariadas de poços offshore
- **Eventos**: Detecção de eventos indesejáveis em poços
- **Formato**: Arquivos Parquet com compressão Brotli
- **Licença**: Creative Commons Attribution 4.0 International

### Estrutura dos Dados
- **Instâncias**: Cada arquivo representa uma instância de evento
- **Variáveis**: Pressão, temperatura, vazão, vibração, etc.
- **Labels**: Classificação binária (normal vs. anômalo)
- **Timestamps**: Índice temporal para cada observação

### Problemas Disponíveis
1. **Classificador Binário de Fechamento Espúrio de DHSV**
   - Tipo: Classificação binária
   - Objetivo: Identificar fechamentos não intencionais de válvulas
   - Aplicação: Segurança e integridade de poços

## 🏗️ Arquitetura da Integração

### Módulos Principais

#### 1. `src/data/threew_dataset.py`
Interface principal com o dataset 3W:
- Carregamento de instâncias
- Configuração de folds
- Metadados do dataset
- Gerenciamento de problemas

#### 2. `src/data/data_loader.py`
Carregador de dados unificado:
- Suporte a múltiplos formatos (Parquet, CSV)
- Cache inteligente de dados
- Normalização automática
- Divisão treino/validação/teste

#### 3. `src/data/preprocessing.py`
Pré-processamento avançado:
- Imputação de valores faltantes
- Normalização robusta
- Seleção de atributos
- Redução de dimensionalidade (PCA)
- Janelas deslizantes para séries temporais

#### 4. `src/config/`
Sistema de configuração:
- Configurações YAML
- Valores padrão otimizados
- Validação de configurações
- Gerenciamento de ambientes

## 🚀 Como Usar

### 1. Pré-requisitos

#### Clonar o Repositório 3W
```bash
# Na raiz do projeto
git clone https://github.com/petrobras/3W.git
```

#### Instalar Dependências
```bash
# Atualizar dependências do projeto principal
uv sync

# Ou instalar manualmente as dependências do 3W
cd 3W
conda env create -f environment.yml
conda activate 3W
```

### 2. Uso Básico

#### Verificar Disponibilidade
```python
from src.data.threew_dataset import is_threew_available, get_threew_info

# Verifica se o 3W está disponível
if is_threew_available():
    info = get_threew_info()
    print(f"Dataset 3W disponível - Versão: {info['version']}")
```

#### Carregar Dados
```python
from src.data.data_loader import create_data_loader

# Cria carregador de dados
loader = create_data_loader(use_threew=True, cache_data=True)

# Lista problemas disponíveis
problems = loader.list_available_problems()
print(f"Problemas: {problems}")

# Carrega dados de um problema específico
data = loader.load_threew_problem(
    problem_name="01_binary_classifier_of_spurious_closure_of_dhsv",
    fold_config="folds_clf_01",  # Configuração de folds
    fold_index=0,
    normalize=True,
    test_size=0.2
)

# Dados carregados
X_train, y_train = data["X_train"], data["y_train"]
X_val, y_val = data["X_val"], data["y_val"]
X_test, y_test = data["X_test"], data["y_test"]
```

#### Pré-processamento
```python
from src.data.preprocessing import create_preprocessor

# Cria pré-processador
preprocessor = create_preprocessor(
    imputation_strategy="mean",
    scaling_method="robust",
    feature_selection_method="mutual_info",
    n_features=10,
    pca_components=5
)

# Aplica pré-processamento
X_train_processed = preprocessor.fit_transform(X_train, y_train)
X_val_processed = preprocessor.transform(X_val)
X_test_processed = preprocessor.transform(X_test)
```

### 3. Uso Avançado

#### Configurações Personalizadas
```python
from src.config.threew_config import (
    get_threew_dataset_config,
    get_threew_problem_config
)

# Configuração completa do dataset
dataset_config = get_threew_dataset_config()

# Configuração específica de um problema
problem_config = get_threew_problem_config("01_binary_classifier_of_spurious_closure_of_dhsv")
```

#### Janelas Deslizantes
```python
from src.data.preprocessing import create_rolling_window_preprocessor

# Cria pré-processador de janelas
window_preprocessor = create_rolling_window_preprocessor(
    window_size=100,
    step_size=1,
    padding="same"
)

# Cria janelas deslizantes
X_windows, y_windows = window_preprocessor.create_windows(X_train, y_train)

# Achatas para formato 2D
X_flat = window_preprocessor.flatten_windows(X_windows)
```

## ⚙️ Configurações

### Arquivo de Configuração Principal
```yaml
# config/3w_config.yaml
dataset:
  name: "3W"
  version: "1.1.0"
  paths:
    toolkit: "3W/toolkit"
    dataset: "3W/dataset"
    folds: "3W/dataset/folds"

loading:
  use_cache: true
  normalize_data: true
  test_size: 0.2

preprocessing:
  imputation_strategy: "mean"
  scaling_method: "robust"
  feature_selection_method: "mutual_info"
  n_features: null
  pca_components: null

rolling_window:
  window_size: 100
  step_size: 1
  padding: "same"
```

### Configurações por Problema
```python
# Configurações específicas para cada problema
problem_configs = {
    "01_binary_classifier_of_spurious_closure_of_dhsv": {
        "type": "classification",
        "binary": True,
        "metrics": ["accuracy", "precision", "recall", "f1_score"],
        "cv_strategy": "stratified_kfold",
        "n_splits": 5
    }
}
```

## 📊 Notebooks de Exemplo

### Notebook Principal
- **Arquivo**: `notebooks/3W_integration_example.py`
- **Descrição**: Demonstração completa da integração
- **Funcionalidades**:
  - Verificação de disponibilidade
  - Carregamento de dados
  - Pré-processamento
  - Estatísticas dos dados
  - Visualizações

### Como Executar
```bash
# Ativar ambiente virtual
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows

# Executar notebook Marimo
marimo edit notebooks/3W_integration_example.py
```

## 🔧 Personalização

### 1. Adicionar Novos Problemas
```python
# Em src/config/threew_config.py
THREEW_AVAILABLE_PROBLEMS.append("novo_problema")

def get_threew_problem_config(problem_name: str):
    if problem_name == "novo_problema":
        return {
            "name": problem_name,
            "type": "classification",
            "target_column": 0,
            "binary": True,
            "metrics": ["accuracy", "f1_score"]
        }
    # ... resto do código
```

### 2. Novos Métodos de Pré-processamento
```python
# Em src/data/preprocessing.py
class CustomPreprocessor(TimeSeriesPreprocessor):
    def __init__(self, custom_param: str):
        super().__init__()
        self.custom_param = custom_param

    def custom_transform(self, X: np.ndarray) -> np.ndarray:
        # Implementação personalizada
        return X_modified
```

### 3. Configurações de Ambiente
```python
# Configurações específicas por ambiente
import os

if os.getenv("ENVIRONMENT") == "production":
    config = load_production_config()
else:
    config = load_development_config()
```

## 📈 Métricas e Avaliação

### Métricas Padrão
- **Classificação Binária**: Accuracy, Precision, Recall, F1-Score, ROC-AUC
- **Detecção de Anomalias**: AUC-PR, F1-Score (para dados desbalanceados)
- **Validação Cruzada**: Stratified K-Fold para dados desbalanceados

### Estratégias de Validação
```python
from sklearn.model_selection import StratifiedKFold

# Validação cruzada estratificada
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# Para cada fold
for train_idx, val_idx in cv.split(X, y):
    X_train_fold, X_val_fold = X[train_idx], X[val_idx]
    y_train_fold, y_val_fold = y[train_idx], y[val_idx]

    # Treinar modelo e avaliar
    # ...
```

## 🚨 Troubleshooting

### Problemas Comuns

#### 1. Dataset 3W Não Encontrado
```bash
# Verificar se o diretório existe
ls -la 3W/

# Clonar se necessário
git clone https://github.com/petrobras/3W.git
```

#### 2. Erro de Importação
```python
# Verificar se o toolkit está no sys.path
import sys
sys.path.insert(0, "3W")

# Verificar dependências
pip install pyarrow h5py tslearn ydata-profiling
```

#### 3. Erro de Memória
```python
# Reduzir tamanho do cache
loader = create_data_loader(cache_data=False)

# Usar processamento em lotes
loader = create_data_loader(batch_size=1000)
```

#### 4. Problemas de Performance
```python
# Habilitar multiprocessamento
from src.config.threew_config import get_threew_n_jobs
n_jobs = get_threew_n_jobs()

# Usar Polars para dados grandes
import polars as pl
df = pl.read_parquet("arquivo.parquet")
```

## 🔄 Atualizações e Manutenção

### Atualizar Dataset 3W
```bash
cd 3W
git pull origin main
```

### Verificar Versões
```python
from src.data.threew_dataset import get_threew_info

info = get_threew_info()
print(f"Versão atual: {info['version']}")
```

### Backup de Configurações
```python
from src.config.config_manager import get_config_manager

config_manager = get_config_manager()
config_manager.save_config("3w_backup", current_config)
```

## 📚 Recursos Adicionais

### Documentação Oficial
- [README do Projeto 3W](https://github.com/petrobras/3W)
- [Estrutura do Dataset](https://github.com/petrobras/3W/blob/main/3W_DATASET_STRUCTURE.md)
- [Estrutura do Toolkit](https://github.com/petrobras/3W/blob/main/3W_TOOLKIT_STRUCTURE.md)
- [Guia de Contribuição](https://github.com/petrobras/3W/blob/main/CONTRIBUTING.md)

### Artigos Científicos
- **Paper Principal**: [A realistic and public dataset with rare undesirable real events in oil wells](https://doi.org/10.1016/j.petrol.2019.106223)
- **Journal**: Journal of Petroleum Science and Engineering

### Comunidade
- [Workshop 3W](https://forms.gle/cmLa2u4VaXd1T7qp8) - 4ª edição em 2025
- [Discussions no GitHub](https://github.com/petrobras/3W/discussions)

## 🎯 Próximos Passos

### Desenvolvimento Futuro
1. **Novos Problemas**: Incorporação de mais tipos de eventos
2. **Modelos SOTA**: Implementação de TranAD, LSTM-VAE, USAD
3. **Otimização**: Hiperparâmetros com Optuna
4. **Deployment**: API para inferência em tempo real
5. **Monitoramento**: Dashboards para acompanhamento de performance

### Contribuições
- Implementar novos algoritmos
- Adicionar métricas de avaliação
- Melhorar documentação
- Otimizar performance
- Adicionar testes automatizados

---

## 📞 Suporte

Para dúvidas ou problemas com a integração:
1. Verificar a documentação oficial do 3W
2. Abrir uma issue no repositório do projeto
3. Consultar as discussions do 3W no GitHub
4. Participar do Workshop 3W anual

---

**Nota**: Esta integração é mantida pela comunidade e pode ser atualizada conforme novas versões do dataset 3W sejam lançadas.
