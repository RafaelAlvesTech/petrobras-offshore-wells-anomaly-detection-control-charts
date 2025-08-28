# 🛢️ Detecção de Anomalias em Poços Offshore da Petrobras

[![Python 3.11](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Linting: ruff](https://img.shields.io/badge/linting-ruff-red.svg)](https://github.com/astral-sh/ruff)

> **🇺🇸 [View documentation in English](README.md)**

## 🎯 Visão Geral do Projeto

Este é um projeto PIBIC (Programa Institucional de Bolsas de Iniciação Científica) focado na **detecção de anomalias em séries temporais multivariadas** de poços offshore da Petrobras. O projeto utiliza técnicas de machine learning e deep learning de última geração para identificar anomalias operacionais em dados de perfuração e produção em tempo real.

## 🚀 Principais Características

- **Análise de Séries Temporais Multivariadas**: Gerencia interdependências complexas entre múltiplos parâmetros dos poços
- **Modelos de Última Geração**: Implementa algoritmos TranAD, LSTM-VAE, USAD e ECOD
- **Processamento em Tempo Real**: Otimizado para fluxos de dados de alta frequência de sensores offshore
- **Resultados Interpretáveis**: Explicações baseadas em SHAP para decisões operacionais
- **Pronto para Cloud**: Configurações de implantação AWS e GCP incluídas

## 🏗️ Arquitetura

```
petrobras-offshore-wells-anomaly-detection/
├── src/                    # Código fonte principal
│   ├── models/            # Implementações de modelos ML/DL
│   ├── data/              # Pipelines de processamento de dados
│   ├── features/          # Engenharia de features
│   └── utils/             # Funções utilitárias
├── notebooks/             # Notebooks interativos Marimo
├── data/                  # Datasets e dados processados
├── tests/                 # Suite de testes automatizados
├── docs/                  # Documentação
├── config/                # Arquivos de configuração
├── docker/                # Containerização
└── scripts/               # Scripts de automação
```

## 🛠️ Stack Tecnológico

### Tecnologias Principais

- **Python 3.11+** - Python moderno com type hints
- **Polars** - Manipulação de dados de alta performance (mais rápido que Pandas)
- **Marimo** - Notebooks interativos para desenvolvimento colaborativo
- **uv** - Gerenciador de pacotes Python rápido e gerenciamento de ambiente

### Machine Learning & Deep Learning

- **PyTorch** - Framework de deep learning
- **Scikit-learn** - Algoritmos tradicionais de ML
- **Optuna** - Otimização de hiperparâmetros
- **SHAP** - Interpretabilidade de modelos

### Data Science & Visualização

- **Plotly** - Visualizações interativas
- **ydata-profiling** - EDA automatizado
- **tslearn** - Utilitários para aprendizado de séries temporais

### Cloud & Implantação

- **AWS** - Infraestrutura cloud e serviços de ML
- **GCP** - Integração com Google Cloud Platform
- **MLflow** - Gerenciamento do ciclo de vida dos modelos
- **Docker** - Containerização

## 🚀 Início Rápido

### Pré-requisitos

- Python 3.11+
- Gerenciador de pacotes uv
- Git

### Instalação

1. **Clone o repositório**

   ```bash
   git clone https://github.com/your-username/petrobras-offshore-wells-anomaly-detection.git
   cd petrobras-offshore-wells-anomaly-detection
   ```

2. **Instale o uv (se ainda não estiver instalado)**

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Crie o ambiente virtual e instale as dependências**

   ```bash
   uv sync
   ```

4. **Ative o ambiente**
   ```bash
   source .venv/bin/activate  # Linux/macOS
   # ou
   .venv\Scripts\activate     # Windows
   ```

### Executando o Projeto

1. **Inicie o servidor de notebooks Marimo**

   ```bash
   marimo edit notebooks/
   ```

2. **Execute os modelos de detecção de anomalias**

   ```bash
   python src/main.py
   ```

3. **Execute os testes**
   ```bash
   pytest tests/
   ```

## 📊 Exemplos de Uso

### Detecção Básica de Anomalias

```python
from src.models import TranADModel
from src.data import WellDataProcessor

# Carrega e pré-processa dados do poço
processor = WellDataProcessor()
data = processor.load_data("well_001.csv")

# Inicializa e treina o modelo
model = TranADModel()
model.train(data)

# Detecta anomalias
anomalies = model.detect_anomalies(data)
```

### Análise Interativa com Marimo

```python
# No notebook Marimo
import marimo as mo
import polars as pl

# Carrega dados
df = pl.read_csv("data/well_data.csv")

# Visualização interativa
mo.md(f"## Análise de Dados do Poço\n\nFormato do dataset: {df.shape}")
```

## 📚 Documentação

### Documentação Principal

- **[Guia de Configuração](docs/setup-guide.md)** - Instruções completas de configuração do projeto
- **[Integração 3W](docs/3W_INTEGRATION.md)** - Integração com sistema 3W
- **[Configuração AWS](docs/AWS_SETUP.md)** - Implantação e configuração AWS
- **[Configuração GCP](docs/GCP_SETUP.md)** - Configuração Google Cloud Platform

### Diretrizes de Desenvolvimento

- **[Commits Convencionais](docs/CONVENTIONAL_COMMITS.md)** - Padrões de commits Git
- **[Diretrizes de Contribuição](CONTRIBUTING.md)** - Como contribuir para o projeto

## 🔬 Foco da Pesquisa

### Desafios da Detecção de Anomalias

- **Dependências Multivariadas**: Relacionamentos complexos entre parâmetros dos poços
- **Processamento em Tempo Real**: Fluxos de dados de alta frequência de sensores offshore
- **Contexto Operacional**: Definições de anomalias específicas do domínio
- **Interpretabilidade**: IA explicável para decisões operacionais

### Métricas de Performance dos Modelos

- **AUC-PR**: Curvas Precision-Recall para dados desbalanceados
- **F1-Score**: Precisão e recall balanceados
- **Latência de Detecção**: Tempo para identificação de anomalias
- **Taxa de Falsos Positivos**: Considerações de eficiência operacional

## 🧪 Testes

```bash
# Execute todos os testes
pytest

# Execute com cobertura
pytest --cov=src

# Execute categorias específicas de testes
pytest tests/test_models.py
pytest tests/test_data_processing.py
```

## 🚀 Otimização de Performance

- **Polars**: 10-100x mais rápido que Pandas para grandes datasets
- **Operações Vetorizadas**: Computações numéricas otimizadas
- **Gerenciamento de Memória**: Estruturas de dados eficientes para séries temporais
- **Processamento Paralelo**: Suporte multi-core para treinamento de modelos

## 🌟 Contribuindo

Aceitamos contribuições! Por favor, veja nossas [Diretrizes de Contribuição](CONTRIBUTING.md) para detalhes.

### Configuração de Desenvolvimento

```bash
# Instale dependências de desenvolvimento
uv sync --group dev

# Instale hooks pre-commit
pre-commit install

# Execute verificações de qualidade de código
ruff check src/
black src/
mypy src/
```

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE.md) para detalhes.

## 🤝 Agradecimentos

- **Petrobras** - Por fornecer expertise do domínio e acesso aos dados
- **Programa PIBIC** - Financiamento de pesquisa de graduação
- **Comunidade Open Source** - Pelas incríveis ferramentas e bibliotecas

## 📞 Contato

- **Líder do Projeto**: [Seu Nome]
- **Instituição**: [Sua Universidade]
- **Email**: [seu.email@universidade.edu]

---

> **🇺🇸 [Ver documentação em Inglês](README.md)**

<div align="center">
  <sub>Construído com ❤️ para segurança e eficiência de poços offshore</sub>
</div>
