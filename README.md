# 🛢️ Petrobras Offshore Wells Anomaly Detection

[![Python 3.11](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Linting: ruff](https://img.shields.io/badge/linting-ruff-red.svg)](https://github.com/astral-sh/ruff)

> **🇧🇷 [Ver documentação em Português Brasileiro](README.pt-BR.md)**

## 🎯 Project Overview

This is a PIBIC (Undergraduate Research) project focused on **anomaly detection in multivariate time series** from Petrobras offshore wells. The project leverages state-of-the-art machine learning and deep learning techniques to identify operational anomalies in real-time drilling and production data.

## 🏛️ Institutional Affiliation

**Risk Studies Center (CER-UFBA)**
Department of Statistics (DEst)
Federal University of Bahia (UFBA)
📍 Ondina, Salvador-BA, Brazil
🌐 [cer.ufba.br](https://cer.ufba.br) | [ufba.br](https://ufba.br)

CER-UFBA is an emerging research laboratory of the Department of Statistics (DEst) at the Federal University of Bahia (UFBA), located in Ondina, Salvador-BA, created in 2016. Its main objective is to bring together researchers involved in the study, proposal of statistical procedures, and risk data analysis.

This project is developed under the academic supervision and research infrastructure of CER-UFBA, contributing to the center's mission of advancing statistical methodologies for risk assessment and anomaly detection in complex industrial systems.

### 🎓 CER-UFBA Research Areas
- **Statistical Risk Analysis**: Advanced methodologies for risk assessment
- **Time Series Analysis**: Multivariate and univariate time series modeling
- **Anomaly Detection**: Statistical and machine learning approaches
- **Industrial Applications**: Oil & gas, manufacturing, and critical systems
- **Data Science**: Big data analytics and statistical computing

## 🚀 Key Features

- **Multivariate Time Series Analysis**: Handles complex interdependencies between multiple well parameters
- **State-of-the-Art Models**: Implements TranAD, LSTM-VAE, USAD, and ECOD algorithms
- **Real-time Processing**: Optimized for high-frequency offshore well data
- **Interpretable Results**: SHAP-based model explanations for operational decisions
- **Cloud-Ready**: AWS and GCP deployment configurations included

## 🏗️ Architecture

```
petrobras-offshore-wells-anomaly-detection/
├── src/                    # Core source code
│   ├── models/            # ML/DL model implementations
│   ├── data/              # Data processing pipelines
│   ├── features/          # Feature engineering
│   └── utils/             # Utility functions
├── notebooks/             # Marimo interactive notebooks
├── data/                  # Datasets and processed data
├── tests/                 # Automated test suite
├── docs/                  # Documentation
├── config/                # Configuration files
├── docker/                # Containerization
└── scripts/               # Automation scripts
```

## 🔬 CER-UFBA Research Project

### 📋 Project Details
- **Research Type**: PIBIC (Undergraduate Research) Project
- **Institution**: Federal University of Bahia (UFBA)
- **Research Center**: Risk Studies Center (CER-UFBA)
- **Department**: Department of Statistics (DEst)
- **Academic Year**: 2024-2025
- **Research Area**: Statistical Anomaly Detection in Industrial Systems

### 🎯 CER-UFBA Contribution
This project represents a significant contribution to CER-UFBA's research portfolio in:
- **Statistical Risk Assessment**: Developing novel methodologies for offshore well monitoring
- **Industrial Data Science**: Applying advanced statistical techniques to real-world oil & gas data
- **Time Series Analysis**: Advancing multivariate time series anomaly detection
- **Machine Learning Integration**: Combining traditional statistics with modern ML approaches

### 📚 Academic Context
The project aligns with CER-UFBA's mission to:
- Foster interdisciplinary research in statistical risk analysis
- Develop practical applications of statistical methodologies
- Contribute to the advancement of Brazilian oil & gas industry safety
- Train students in cutting-edge statistical and data science techniques

## 🛠️ Technology Stack

### Core Technologies
- **Python 3.11+** - Modern Python with type hints
- **Polars** - High-performance data manipulation (faster than Pandas)
- **Marimo** - Interactive notebooks for collaborative development
- **uv** - Fast Python package manager and environment management

### Machine Learning & Deep Learning
- **PyTorch** - Deep learning framework
- **Scikit-learn** - Traditional ML algorithms
- **Optuna** - Hyperparameter optimization
- **SHAP** - Model interpretability

### Data Science & Visualization
- **Plotly** - Interactive visualizations
- **ydata-profiling** - Automated EDA
- **tslearn** - Time series learning utilities

### Cloud & Deployment
- **AWS** - Cloud infrastructure and ML services
- **GCP** - Google Cloud Platform integration
- **MLflow** - Model lifecycle management
- **Docker** - Containerization

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- uv package manager
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/petrobras-offshore-wells-anomaly-detection.git
   cd petrobras-offshore-wells-anomaly-detection
   ```

2. **Install uv (if not already installed)**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Create virtual environment and install dependencies**
   ```bash
   uv sync
   ```

4. **Activate the environment**
   ```bash
   source .venv/bin/activate  # Linux/macOS
   # or
   .venv\Scripts\activate     # Windows
   ```

### Running the Project

1. **Start Marimo notebook server**
   ```bash
   marimo edit notebooks/
   ```

2. **Run anomaly detection models**
   ```bash
   python src/main.py
   ```

3. **Execute tests**
   ```bash
   pytest tests/
   ```

## 📊 Usage Examples

### Basic Anomaly Detection

```python
from src.models import TranADModel
from src.data import WellDataProcessor

# Load and preprocess well data
processor = WellDataProcessor()
data = processor.load_data("well_001.csv")

# Initialize and train model
model = TranADModel()
model.train(data)

# Detect anomalies
anomalies = model.detect_anomalies(data)
```

### Interactive Analysis with Marimo

```python
# In Marimo notebook
import marimo as mo
import polars as pl

# Load data
df = pl.read_csv("data/well_data.csv")

# Interactive visualization
mo.md(f"## Well Data Analysis\n\nDataset shape: {df.shape}")
```

## 📚 Documentation

### Core Documentation
- **[Setup Guide](docs/setup-guide.md)** - Complete project setup instructions
- **[Claude Code Setup](docs/CLAUDE_CODE_SETUP.md)** - Claude Code configuration and optimization
- **[3W Integration](docs/3W_INTEGRATION.md)** - Integration with 3W system
- **[AWS Setup](docs/AWS_SETUP.md)** - AWS deployment and configuration
- **[GCP Setup](docs/GCP_SETUP.md)** - Google Cloud Platform setup

### Development Guidelines
- **[Conventional Commits](docs/CONVENTIONAL_COMMITS.md)** - Git commit standards
- **[Contributing Guidelines](CONTRIBUTING.md)** - How to contribute to the project

## 🔬 Research Focus

### Anomaly Detection Challenges
- **Multivariate Dependencies**: Complex relationships between well parameters
- **Real-time Processing**: High-frequency data streams from offshore sensors
- **Operational Context**: Domain-specific anomaly definitions
- **Interpretability**: Explainable AI for operational decisions

### Model Performance Metrics
- **AUC-PR**: Precision-Recall curves for imbalanced data
- **F1-Score**: Balanced precision and recall
- **Detection Latency**: Time to anomaly identification
- **False Positive Rate**: Operational efficiency considerations

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test categories
pytest tests/test_models.py
pytest tests/test_data_processing.py
```

## 🚀 Performance Optimization

- **Polars**: 10-100x faster than Pandas for large datasets
- **Vectorized Operations**: Optimized numerical computations
- **Memory Management**: Efficient data structures for time series
- **Parallel Processing**: Multi-core support for model training

## 🌟 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Install development dependencies
uv sync --group dev

# Install pre-commit hooks
pre-commit install

# Run code quality checks
ruff check src/
black src/
mypy src/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.

## 🙏 Acknowledgments

### 🏛️ CER-UFBA Support
This project is made possible by the academic and research support of the **Risk Studies Center (CER-UFBA)** at the Federal University of Bahia.

**Special thanks to:**
- **CER-UFBA Research Team** - For providing the research infrastructure and statistical expertise
- **Department of Statistics (DEst)** - For academic supervision and methodological guidance
- **UFBA Faculty** - For supporting undergraduate research initiatives
- **Petrobras** - For providing real-world data and industry context

### 📞 Contact Information
- **CER-UFBA Website**: [cer.ufba.br](https://cer.ufba.br)
- **UFBA Main Site**: [ufba.br](https://ufba.br)
- **Location**: Department of Statistics, Ondina Campus, Salvador-BA, Brazil
- **Research Focus**: Statistical risk analysis, time series, anomaly detection, industrial applications

### 🔬 Join Our Research
CER-UFBA welcomes collaboration with:
- **Students**: Undergraduate and graduate research opportunities
- **Researchers**: Academic partnerships and joint publications
- **Industry**: Applied research projects and consulting
- **Institutions**: Research collaboration and knowledge exchange

---

**📚 This project is proudly developed under the academic supervision of CER-UFBA, contributing to the advancement of statistical methodologies for industrial risk assessment and anomaly detection.**

## 📞 Contact

- **Project Lead**: [Your Name]
- **Institution**: [Your University]
- **Email**: [your.email@university.edu]

---

> **🇧🇷 [Ver documentação em Português Brasileiro](README.pt-BR.md)**

<div align="center">
  <sub>Built with ❤️ for offshore well safety and efficiency</sub>
</div>

## 🔌 Extensões Essenciais do VS Code/Cursor
O projeto inclui configurações automáticas para as seguintes extensões essenciais:

### 🐍 Python Development
- **ms-python.python**: Suporte completo ao Python
- **ms-python.vscode-pylance**: IntelliSense avançado para Python
- **charliermarsh.ruff**: Linting e formatação rápida

### 📊 Data Science & Jupyter
- **ms-toolsai.jupyter**: Suporte completo ao Jupyter
- **ms-toolsai.jupyter-keymap**: Atalhos de teclado para Jupyter

### 🔧 Development Tools
- **ms-vscode.vscode-json**: Suporte ao JSON
- **yzhang.markdown-all-in-one**: Editor Markdown avançado

### 🐳 Docker & Containers
- **ms-azuretools.vscode-docker**: Suporte ao Docker

### 🔄 Git & Version Control
- **eamodio.gitlens**: Git supercharged

### 🎨 Themes & Icons
- **pkief.material-icon-theme**: Ícones Material Design

### 🧪 Testing
- **littlefoxteam.vscode-python-test-adapter**: Test runner para Python

### 🚀 AI & Productivity
- **GitHub.copilot**: Assistente de IA para código
- **GitHub.copilot-chat**: Chat com IA para desenvolvimento

## 🤖 Claude Code - Configurações Específicas

### 🧠 Extensões de IA e Machine Learning
- **ms-python.black-formatter**: Formatação automática de código Python
- **ms-python.isort**: Organização automática de imports
- **ms-python.flake8**: Linting avançado para Python
- **ms-python.mypy-type-checker**: Verificação de tipos estática
- **ms-python.pylint**: Análise de código Python
- **ms-python.autopep8**: Formatação automática PEP 8

### 📈 Análise de Dados e Visualização
- **ms-python.python**: Suporte nativo ao Python
- **ms-python.vscode-pylance**: IntelliSense e análise de código
- **ms-toolsai.jupyter**: Suporte completo ao Jupyter
- **ms-toolsai.jupyter-keymap**: Atalhos para notebooks
- **ms-toolsai.jupyter-renderers**: Renderizadores para diferentes formatos
- **ms-python.python**: Interpretador Python configurável

### 🔬 Ciência de Dados e ML
- **ms-python.python**: Suporte ao Python científico
- **ms-python.vscode-pylance**: Análise de código avançada
- **ms-toolsai.jupyter**: Notebooks interativos
- **ms-python.black-formatter**: Formatação consistente
- **ms-python.isort**: Organização de imports
- **ms-python.flake8**: Qualidade de código

### 🚀 Produtividade e Desenvolvimento
- **ms-vscode.vscode-json**: Suporte ao JSON
- **yzhang.markdown-all-in-one**: Editor Markdown
- **ms-azuretools.vscode-docker**: Suporte ao Docker
- **eamodio.gitlens**: Git avançado
- **pkief.material-icon-theme**: Ícones Material Design
- **littlefoxteam.vscode-python-test-adapter**: Testes Python

### ⚙️ Configurações Específicas para o Projeto

#### Python Interpreter
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
- Use o ambiente virtual `.venv` criado pelo `uv`
- Configure o Python interpreter para `./.venv/bin/python`
- Ative o ambiente automaticamente no terminal

#### 2. **Formatação e Linting**
- Black para formatação automática (linha 88)
- isort para organização de imports
- Flake8 para linting de código
- MyPy para verificação de tipos

#### 3. **Notebooks e Jupyter**
- Suporte completo ao Marimo
- Kernel Python 3.11 configurado
- Renderizadores para diferentes formatos de dados

#### 4. **Desenvolvimento Científico**
- IntelliSense avançado para bibliotecas científicas
- Suporte a Polars, PyTorch, TensorFlow
- Integração com ferramentas de ML

### 🚀 Setup Automático para Claude Code

#### Linux/macOS
```bash
chmod +x scripts/install_claude_extensions.sh
./scripts/install_claude_extensions.sh
```

#### Windows (PowerShell)
```powershell
.\scripts\install_claude_extensions.ps1
```

#### Cross-platform (Python)
```bash
python scripts/install_claude_extensions.py
```

### 📁 Estrutura de Configurações
```
.vscode/
├── settings.json          # Configurações do workspace
├── extensions.json        # Extensões recomendadas
├── launch.json           # Configurações de debug
└── tasks.json            # Tarefas automatizadas
```

### 🔧 Configurações Avançadas

#### Debug e Testing
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

## �� Setup Automático
