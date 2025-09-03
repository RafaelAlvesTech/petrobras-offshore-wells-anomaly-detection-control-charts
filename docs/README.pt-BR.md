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
- **[Visão Geral do Projeto 3W](docs/3W_OVERVIEW.md)** - Visão completa do projeto 3W da Petrobras
- **[Configuração AWS](docs/AWS_SETUP.md)** - Implantação e configuração AWS
- **[Configuração GCP](docs/GCP_SETUP.md)** - Configuração Google Cloud Platform
- **[Autores e Contribuidores](docs/AUTHORS.pt-BR.md)** - Conheça a equipe do projeto

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

## 👨‍💻 Autores e Contribuidores

### 🎓 Rafael - Desenvolvedor Principal

<div align="center">
  <img src="https://github.com/rafael.png" alt="Rafael" width="150" height="150" style="border-radius: 50%;">
</div>

#### 🇧🇷 Português

Atualmente no Bacharelado em Engenharia de Controle e Automação em Processos na UFBA, sou um entusiasta apaixonado por lógica e conhecimento, especialmente em Inteligência Artificial (IA).

Ao longo da minha jornada, tenho buscado projetos que aprimoraram minhas habilidades em:

- **Machine Learning** - Desenvolvimento e implementação de modelos de IA
- **Análise de Dados** - Processamento e visualização de dados complexos
- **Python** - Desenvolvimento de soluções robustas e escaláveis

Além de aspirante à engenheiro e cientista de dados, sou gestor de marketing digital com especialidade em Google Ads e micro empresário, fortalecendo minha visão holística.

#### 🇺🇸 English

Currently pursuing a Bachelor's degree in Control and Process Automation Engineering at UFBA, I am an enthusiast passionate about logic and knowledge, especially in Artificial Intelligence (AI).

Throughout my journey, I have sought projects that have enhanced my skills in:

- **Machine Learning** - Development and implementation of AI models
- **Data Analysis** - Processing and visualization of complex data
- **Python** - Development of robust and scalable solutions

In addition to being an aspiring engineer and data scientist, I am a digital marketing manager specializing in Google Ads and a micro-entrepreneur, strengthening my holistic vision.

---

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

🎉 **Atualização de Conquistas do GitHub - Agosto 2025** 🏆

## 🔌 Extensões VS Code/Cursor

### Extensões Essenciais

- **ms-python.python**: Suporte completo para Python
- **ms-python.vscode-pylance**: IntelliSense avançado para Python
- **charliermarsh.ruff**: Linting e formatação rápidos
- **ms-toolsai.jupyter**: Suporte completo para Jupyter
- **ms-toolsai.jupyter-keymap**: Atalhos de teclado do Jupyter
- **ms-vscode.vscode-json**: Suporte para JSON
- **yzhang.markdown-all-in-one**: Editor Markdown avançado
- **ms-azuretools.vscode-docker**: Suporte para Docker
- **eamodio.gitlens**: Git supercharged
- **pkief.material-icon-theme**: Ícones Material Design
- **littlefoxteam.vscode-python-test-adapter**: Executor de testes Python
- **GitHub.copilot**: Assistente de código AI
- **GitHub.copilot-chat**: Chat de desenvolvimento AI

## 🤖 Configuração Claude Code

### Ferramentas de Desenvolvimento

- **ms-python.black-formatter**: Formatação automática de código Python
- **ms-python.isort**: Organização automática de imports
- **ms-python.flake8**: Linting avançado de Python
- **ms-python.mypy-type-checker**: Verificação estática de tipos
- **ms-python.pylint**: Análise de código Python
- **ms-python.autopep8**: Formatação automática PEP 8
- **ms-toolsai.jupyter-renderers**: Renderizadores para diferentes formatos

### ⚙️ Configurações Específicas do Projeto

#### Interpretador Python

```json
{
  "python.defaultInterpreterPath": "./.venv/bin/python",
  "python.terminal.activateEnvironment": true
}
```

#### Formatação Automática

```json
{
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": ["--line-length", "88"],
  "editor.formatOnSave": true,
  "python.sortImports.args": ["--profile", "black"]
}
```

#### Linting e Qualidade

```json
{
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.linting.flake8Enabled": true,
  "python.linting.mypyEnabled": true
}
```

#### Jupyter e Notebooks

```json
{
  "jupyter.defaultKernel": "Python 3.11",
  "jupyter.askForKernelRestart": false,
  "jupyter.enableAutoMatcher": true
}
```

### 🎯 Configurações Recomendadas para Claude Code

#### 1. **Configuração do Ambiente Python**

- Usar ambiente virtual `.venv` criado pelo `uv`
- Configurar interpretador Python para `./.venv/bin/python`
- Ativar ambiente automaticamente no terminal

#### 2. **Formatação e Linting**

- Black para formatação automática (linha 88)
- isort para organização de imports
- Flake8 para linting de código
- MyPy para verificação de tipos

#### 3. **Notebooks e Jupyter**

- Suporte completo para Jupyter
- Kernel Python 3.11 configurado
- Renderizadores para diferentes formatos de dados

#### 4. **Desenvolvimento Científico**

- IntelliSense avançado para bibliotecas científicas
- Suporte para Polars, PyTorch, TensorFlow
- Integração com ferramentas de ML

### 🚀 Configuração Automática para Claude Code

#### Linux/macOS

```bash
chmod +x scripts/install_claude_extensions.sh
./scripts/install_claude_extensions.sh
```

#### Windows (PowerShell)

```powershell
.\scripts\install_claude_extensions.ps1
```

#### Multiplataforma (Python)

```bash
python scripts/install_claude_extensions.py
```

### 📁 Estrutura de Configuração

```
.vscode/
├── settings.json          # Configurações do workspace
├── extensions.json        # Extensões recomendadas
├── launch.json           # Configurações de debug
└── tasks.json            # Tarefas automatizadas
```

### 🔧 Configurações Avançadas

#### Debug e Testes

```json
{
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["tests"],
  "python.testing.unittestEnabled": false,
  "python.testing.nosetestsEnabled": false
}
```

#### Terminal e Ambiente

```json
{
  "terminal.integrated.defaultProfile.linux": "zsh",
  "terminal.integrated.env.linux": {
    "PYTHONPATH": "${workspaceFolder}/src"
  }
}
```

#### Git e Versionamento

```json
{
  "git.enableSmartCommit": true,
  "git.confirmSync": false,
  "git.autofetch": true
}
```

### ✅ Implementadas

- [ ] Análise exploratória de dados (EDA)
- [ ] Pré-processamento e limpeza de dados
- [ ] Engenharia de atributos avançada
- [ ] Implementação de modelos SOTA
- [ ] Avaliação comparativa de performance
- [ ] Protótipo de API para inferência
- [ ] Containerização com Docker
- [ ] CI/CD básico com GitHub Actions

### 🔄 Em Desenvolvimento

- [ ] Treinamento dos modelos selecionados
- [ ] Otimização de hiperparâmetros
- [ ] Análise de interpretabilidade

### 📋 Planejadas

- [ ] Interface de usuário para monitorament

- [ ] Relatório final PIBIC

## 📊 Dataset

### Dataset 3W da Petrobras

- **Tipo**: Séries temporais multivariadas
- **Variáveis**: Pressão, temperatura, vazão, vibração
- **Características**:
  - Grande volume de dados
  - Alta dimensionalidade
  - Interdependência entre variáveis
  - Eventos anômalos raros e imprevisíveis

### 🎯 Foco Especial

- **Falhas de equipamento**: Identificação de problemas incipientes
- **Instabilidades de fluxo**: Monitoramento de operações anormais ## 📈 Metodologia

### 🔄 CRISP-DM Adaptado

```mermaid
graph TD
    A[Entendimento do Negócio] --> B[Entendimento dos Dados]
    B --> C[Preparação dos Dados]
    C --> D[Modelagem]
    D --> E[Avaliação]
    E --> F[Deployment]
    F --> G[Monitoramento]
```

### 📊 Fases do Projeto

| Fase          | Duração  | Atividades Principais                      |
| ------------- | -------- | ------------------------------------------ |
| 🎯 **Fase 1** | Mês 1-2  | Revisão bibliográfica, EDA inicial         |
| 🔧 **Fase 2** | Mês 3-4  | Pré-processamento, engenharia de atributos |
| 🤖 **Fase 3** | Mês 5-8  | Implementação e treinamento dos modelos    |
| 📊 **Fase 4** | Mês 9-10 | Avaliação, interpretabilidade              |
| 🚀 **Fase 5** | Mês 11   | Prototipagem, MLOps                        |
| 📝 **Fase 6** | Mês 12   | Documentação, relatório final              |

## 📅 Cronograma

### 📅 Visão Geral (12 meses)

```mermaid
gantt
    title Cronograma do Projeto PIBIC
    dateFormat  YYYY-MM-DD
    section Fase 1
    Revisão Bibliográfica    :done,    des1, 2024-01-01, 2024-02-29
    EDA Inicial             :active,  des2, 2024-02-01, 2024-02-29
    section Fase 2
    Pré-processamento       :         des3, 2024-03-01, 2024-04-30
    Engenharia de Atributos :         des4, 2024-04-01, 2024-04-30
    section Fase 3
    Modelo 1 (LSTM-VAE)     :         des5, 2024-05-01, 2024-06-30
    Modelo 2 (TranAD)       :         des6, 2024-06-01, 2024-07-31
    Modelo 3 (ECOD)         :         des7, 2024-07-01, 2024-08-31
    section Fase 4
    Avaliação               :         des8, 2024-09-01, 2024-10-31
    section Fase 5
    Prototipagem            :         des9, 2024-11-01, 2024-11-30
    section Fase 6
    Documentação            :         des10, 2024-12-01, 2024-12-31
```

### 📋 Marcos Principais

- [x] **Mês 2**: EDA completa e dicionário de dados
- [ ] **Mês 4**: Dataset limpo e pré-processado
- [ ] **Mês 8**: 3+ modelos implementados e treinados
- [ ] **Mês 10**: Avaliação comparativa completa
- [ ] **Mês 11**: Protótipo funcional
- [ ] **Mês 12**: Relatório final PIBIC

## 🔬 Modelos Implementados

### 🏆 Modelos Selecionados (SOTA - Últimos 3 anos)

| Modelo       | Tipo                    | Características               | Status              |
| ------------ | ----------------------- | ----------------------------- | ------------------- |
| **TranAD**   | Transformer             | Dependências temporais longas | 🔄 Em implementação |
| **LSTM-VAE** | RNN + Autoencoder       | Modelagem de sequências       | 🔄 Em implementação |
| **USAD**     | Autoencoder Adversarial | Treinamento rápido            | ⏳ Pendente         |
| **ECOD**     | Não-paramétrico         | Interpretável, escalável      | ⏳ Pendente         |

### 🎯 Foco Especial: Detecção de Anomalias

- **Features específicas**: Taxas de variação de pressão/vazão
- **Correlações cruzadas**: Relações entre múltiplos sensores
- **Análise temporal**: Padrões de evolução das anomalias
- **Processamento eficiente**: Uso do Polars para análise de grandes volumes de dados em tempo real

## 📊 Métricas de Avaliação

### 🎯 Métricas Principais

| Métrica         | Descrição                            | Importância                 |
| --------------- | ------------------------------------ | --------------------------- |
| **AUC-PR**      | Área sob curva Precision-Recall      | Alta (dados desbalanceados) |
| **F1-Score**    | Média harmônica de precisão e recall | Alta                        |
| **Precision@k** | Precisão nos top-k predições         | Média                       |
| **Recall@k**    | Recall nos top-k predições           | Média                       |

### 📈 Baselines de Comparação

- **Isolation Forest**: Algoritmo clássico de detecção de outliers
- **One-Class SVM**: Método de separação de classes
- **LOF (Local Outlier Factor)**: Detecção baseada em densidade local
