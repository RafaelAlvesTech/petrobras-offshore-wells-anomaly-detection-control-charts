# 🚀 Guia de Setup Completo - Detecção de Anomalias em Poços Offshore da Petrobras

> **🇺🇸 [View setup guide in English](setup-guide.md)**

## 📋 Índice

- [🎯 Visão Geral](#-visão-geral)
- [🔌 Setup das Extensões](#-setup-das-extensões)
- [🔧 Script Robusto de Extensões](#-script-robusto-de-extensões)
- [🐍 Setup do Ambiente Python](#-setup-do-ambiente-python)
- [⚙️ Configurações do Workspace](#️-configurações-do-workspace)
- [🧪 Configuração de Testes](#-configuração-de-testes)
- [🔧 Troubleshooting](#-troubleshooting)

## 🎯 Visão Geral

Este guia fornece instruções passo a passo para configurar completamente o ambiente de desenvolvimento do projeto PIBIC de detecção de anomalias em poços offshore da Petrobras.

### 🎯 **O que será configurado:**

- ✅ Extensões essenciais do VS Code/Cursor
- ✅ Ambiente Python com uv
- ✅ Dependências do projeto
- ✅ Pre-commit hooks
- ✅ Configurações do workspace
- ✅ Ambiente de testes

## 🔌 Setup das Extensões

### 🚀 **Instalação Automática (Recomendado)**

#### **Linux/macOS - Script Robusto (Recomendado)**

```bash
# Dar permissão de execução
chmod +x scripts/install_extensions_robust.sh

# Executar script robusto (continua mesmo com erros)
./scripts/install_extensions_robust.sh
```

#### **Linux/macOS - Script Original**

```bash
# Dar permissão de execução
chmod +x scripts/install_extensions.sh

# Executar script original
./scripts/install_extensions.sh
```

#### **Windows (PowerShell)**

```powershell
# Executar script PowerShell
.\scripts\install_extensions.ps1

# Ou com força (reinstalar)
.\scripts\install_extensions.ps1 -Force
```

#### **Cross-platform (Python)**

```bash
# Executar script Python
python scripts/install_extensions.py
```

### 🔍 **Diferenças entre os Scripts**

| Script                         | Característica                                                                                     | Recomendação         |
| ------------------------------ | -------------------------------------------------------------------------------------------------- | -------------------- |
| `install_extensions_robust.sh` | ✅ Continua mesmo com erros<br>✅ Instala todas as extensões<br>✅ Melhor para instalação completa | **🌟 Recomendado**   |
| `install_extensions.sh`        | ⚠️ Para em caso de erro<br>⚠️ Pode não instalar todas<br>⚠️ Melhor para debug                      | Para desenvolvimento |
| `install_extensions.py`        | 🔄 Cross-platform<br>🔄 Instalação via Python<br>🔄 Mais lento                                     | Para Windows/Linux   |

### 📦 **Extensões que serão instaladas:**

| Categoria           | Extensão            | ID                                       | Descrição                  |
| ------------------- | ------------------- | ---------------------------------------- | -------------------------- |
| 🐍 **Python**       | Python              | ms-python.python                         | Suporte completo ao Python |
| 🐍 **Python**       | Pylance             | ms-python.vscode-pylance                 | IntelliSense avançado      |
| 🐍 **Python**       | Ruff                | charliermarsh.ruff                       | Linting e formatação       |
| 📊 **Data Science** | Jupyter             | ms-toolsai.jupyter                       | Suporte ao Jupyter         |
| 📊 **Data Science** | Jupyter Keymap      | ms-toolsai.jupyter-keymap                | Atalhos de teclado         |
| 🔧 **Dev Tools**    | JSON                | ms-vscode.vscode-json                    | Suporte ao JSON            |
| 🔧 **Dev Tools**    | Markdown            | yzhang.markdown-all-in-one               | Editor Markdown            |
| 🐳 **Docker**       | Docker              | ms-azuretools.vscode-docker              | Suporte ao Docker          |
| 🔄 **Git**          | GitLens             | eamodio.gitlens                          | Git supercharged           |
| 🎨 **Themes**       | Material Icons      | pkief.material-icon-theme                | Ícones Material            |
| 🧪 **Testing**      | Python Test Adapter | littlefoxteam.vscode-python-test-adapter | Test runner                |
| 🚀 **AI**           | GitHub Copilot      | GitHub.copilot                           | Assistente de IA           |
| 🚀 **AI**           | GitHub Copilot Chat | GitHub.copilot-chat                      | Chat com IA                |

### 🔧 **Instalação Manual (Alternativa)**

Se preferir instalar manualmente:

1. **Abra o VS Code/Cursor**
2. **Pressione `Ctrl+Shift+X`** (ou `Cmd+Shift+X` no Mac)
3. **Pesquise e instale** cada extensão da lista acima
4. **Reinicie o editor** após a instalação

## 🐍 Setup do Ambiente Python

### 📋 **Pré-requisitos**

- Python 3.11+ instalado
- Git instalado
- VS Code/Cursor instalado

### 🚀 **Passo a Passo**

#### **1. Clone o Repositório**

```bash
git clone https://github.com/RafaelAlvesTech/petrobras-offshore-wells-anomaly-detection-control-charts.git
cd petrobras-offshore-wells-anomaly-detection-control-charts
```

#### **2. Instalar uv**

```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Ou via pip
pip install uv
```

#### **3. Criar Ambiente Virtual**

```bash
# Criar ambiente
uv venv

# Ativar ambiente
# Linux/macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

#### **4. Instalar Dependências**

```bash
# Sincronizar projeto (recomendado)
uv sync

# Ou instalar manualmente
uv pip install -r requirements.txt
```

#### **5. Instalar Dependências de Desenvolvimento**

```bash
# Marimo para notebooks
uv add marimo

# Polars para dados
uv add polars

# Pre-commit para hooks
uv add pre-commit

# Ruff para linting
uv add ruff

# Pytest para testes
uv add pytest
```

#### **6. Configurar Pre-commit**

```bash
# Instalar hooks
uv run pre-commit install

# Verificar instalação
uv run pre-commit run --all-files
```

## ⚙️ Configurações do Workspace

### 🔧 **Configurações Automáticas**

O projeto inclui configurações otimizadas em `.vscode/settings.json`:

- **Python interpreter**: Configurado para `.venv`
- **Formatação**: Automática com Ruff
- **Linting**: Automático com Ruff
- **Terminal**: Configurado para o ambiente virtual
- **Performance**: Exclusões de pastas pesadas

### 🎯 **Configurações Manuais**

#### **1. Selecionar Python Interpreter**

1. **Pressione `Ctrl+Shift+P`** (ou `Cmd+Shift+P` no Mac)
2. **Digite**: `Python: Select Interpreter`
3. **Selecione**: `./.venv/bin/python`

#### **2. Verificar Configurações**

1. **Abra Command Palette** (`Ctrl+Shift+P`)
2. **Digite**: `Preferences: Open Workspace Settings (JSON)`
3. **Verifique** se as configurações estão corretas

### 📁 **Estrutura de Pastas**

```
petrobras-offshore-wells-anomaly-detection/
├── .venv/                  # Ambiente virtual Python
├── src/                    # Código fonte
├── notebooks/              # Notebooks Marimo
├── data/                   # Dados e datasets
├── tests/                  # Testes automatizados
├── docs/                   # Documentação
├── config/                 # Arquivos de configuração
├── docker/                 # Configurações Docker
├── scripts/                # Scripts de automação
└── .vscode/                # Configurações do workspace
```

## 🧪 Configuração de Testes

### 🚀 **Executar Testes**

```bash
# Executar todos os testes
pytest

# Executar com cobertura
pytest --cov=src

# Executar testes específicos
pytest tests/test_models.py

# Executar com verbose
pytest -v

# Executar testes em paralelo
pytest -n auto
```

### 📊 **Cobertura de Testes**

```bash
# Gerar relatório de cobertura
pytest --cov=src --cov-report=html

# Abrir relatório no navegador
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### 🔧 **Configuração do Pytest**

O projeto inclui configuração automática do pytest em `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --tb=short"
```

## 🔧 Troubleshooting

### ❌ **Problemas Comuns**

#### **1. Extensões não instalam**

```bash
# Verificar permissões
ls -la scripts/

# Dar permissão de execução
chmod +x scripts/*.sh

# Executar como administrador (se necessário)
sudo ./scripts/install_extensions.sh
```

#### **2. Ambiente Python não ativa**

```bash
# Verificar se o ambiente existe
ls -la .venv/

# Recriar ambiente
rm -rf .venv
uv venv
source .venv/bin/activate
```

#### **3. Dependências não instalam**

```bash
# Limpar cache do uv
uv cache clean

# Reinstalar dependências
uv sync --reinstall
```

#### **4. Pre-commit não funciona**

```bash
# Reinstalar hooks
uv run pre-commit uninstall
uv run pre-commit install

# Verificar configuração
cat .pre-commit-config.yaml
```

### 🆘 **Ainda com Problemas?**

1. **Verifique os logs**: Execute com `--verbose`
2. **Consulte a documentação**: Links na seção de documentação
3. **Abra uma issue**: Use o template do GitHub
4. **Entre em contato**: Email na seção de contato

---

> **🇺🇸 [Ver guia em Inglês](setup-guide.md)**

<div align="center">
  <sub>Configurado com ❤️ para desenvolvimento eficiente</sub>
</div>
