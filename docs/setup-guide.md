# 🚀 Guia de Setup Completo - Petrobras Offshore Wells Anomaly Detection

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

| Script | Característica | Recomendação |
|--------|----------------|--------------|
| `install_extensions_robust.sh` | ✅ Continua mesmo com erros<br>✅ Instala todas as extensões<br>✅ Melhor para instalação completa | **🌟 Recomendado** |
| `install_extensions.sh` | ⚠️ Para em caso de erro<br>⚠️ Pode não instalar todas<br>⚠️ Melhor para debug | Para desenvolvimento |
| `install_extensions.py` | 🔄 Cross-platform<br>🔄 Instalação via Python<br>🔄 Mais lento | Para Windows/Linux |

### 📦 **Extensões que serão instaladas:**

| Categoria | Extensão | ID | Descrição |
|-----------|----------|-----|-----------|
| 🐍 **Python** | Python | ms-python.python | Suporte completo ao Python |
| 🐍 **Python** | Pylance | ms-python.vscode-pylance | IntelliSense avançado |
| 🐍 **Python** | Ruff | charliermarsh.ruff | Linting e formatação |
| 📊 **Data Science** | Jupyter | ms-toolsai.jupyter | Suporte ao Jupyter |
| 📊 **Data Science** | Jupyter Keymap | ms-toolsai.jupyter-keymap | Atalhos de teclado |
| 🔧 **Dev Tools** | JSON | ms-vscode.vscode-json | Suporte ao JSON |
| 🔧 **Dev Tools** | Markdown | yzhang.markdown-all-in-one | Editor Markdown |
| 🐳 **Docker** | Docker | ms-azuretools.vscode-docker | Suporte ao Docker |
| 🔄 **Git** | GitLens | eamodio.gitlens | Git supercharged |
| 🎨 **Themes** | Material Icons | pkief.material-icon-theme | Ícones Material |
| 🧪 **Testing** | Python Test Adapter | littlefoxteam.vscode-python-test-adapter | Test runner |
| 🚀 **AI** | GitHub Copilot | GitHub.copilot | Assistente de IA |
| 🚀 **AI** | GitHub Copilot Chat | GitHub.copilot-chat | Chat com IA |

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
petrobras-offshore-wells-anomaly-detection-control-charts/
├── 📁 .vscode/                    # Configurações do workspace
│   ├── 📄 settings.json           # Configurações do projeto
│   ├── 📄 extensions.json         # Extensões recomendadas
│   ├── 📄 tasks.json              # Tasks automatizadas
│   └── 📄 launch.json             # Configurações de debug
├── 📁 scripts/                    # Scripts de setup
│   ├── 📄 install_extensions_robust.sh  # Setup Linux/macOS (Recomendado)
│   ├── 📄 install_extensions.sh   # Setup Linux/macOS (Original)
│   ├── 📄 install_extensions.ps1  # Setup Windows
│   └── 📄 install_extensions.py   # Setup cross-platform
├── 📁 src/                        # Código fonte
├── 📁 notebooks/                  # Notebooks Marimo
├── 📁 tests/                      # Testes
└── 📁 docs/                       # Documentação
```

## 🧪 Configuração de Testes

### 🚀 **Executar Testes**

```bash
# Executar todos os testes
uv run pytest

# Executar com coverage
uv run pytest --cov=src --cov-report=html

# Executar testes específicos
uv run pytest tests/test_models.py

# Executar em modo verbose
uv run pytest -v
```

### 🔧 **Configuração de Debug**

O projeto inclui configurações de debug em `.vscode/launch.json`:

- **🐍 Python: Current File**: Debug do arquivo atual
- **🧪 Python: Debug Tests**: Debug de testes
- **📓 Python: Debug Marimo**: Debug de notebooks
- **🐳 Docker: Debug Container**: Debug de containers

## 🔧 Troubleshooting

### ❌ **Problemas Comuns**

#### **1. Extensões não instalam**
```bash
# Verificar se o code está no PATH
code --version

# Tentar instalação manual
code --install-extension ms-python.python

# Usar script robusto (recomendado)
./scripts/install_extensions_robust.sh
```

#### **2. Python interpreter não encontrado**
```bash
# Verificar se o ambiente foi criado
ls -la .venv/bin/python

# Recriar ambiente
rm -rf .venv
uv venv
source .venv/bin/activate
uv sync
```

#### **3. Pre-commit falha**
```bash
# Reinstalar hooks
uv run pre-commit uninstall
uv run pre-commit install

# Executar manualmente
uv run pre-commit run --all-files
```

#### **4. Dependências não instalam**
```bash
# Limpar cache do uv
uv cache clean

# Reinstalar dependências
uv sync --reinstall
```

### 🆘 **Ainda com Problemas?**

1. **Verifique logs**: `uv run pre-commit run --all-files --verbose`
2. **Reinicie o editor**: Feche e abra o VS Code/Cursor
3. **Verifique versões**: `python --version`, `uv --version`
4. **Consulte issues**: GitHub do projeto

## 🔧 **Script Robusto de Extensões**

### 🚀 **Por que usar o script robusto?**

O `install_extensions_robust.sh` foi criado para resolver problemas comuns de instalação:

- **✅ Continua mesmo com erros**: Não para se uma extensão falhar
- **✅ Instala todas as extensões**: Garante instalação completa
- **✅ Melhor feedback**: Mostra progresso detalhado
- **✅ Tratamento de erros**: Continua tentando instalar as demais

### 📊 **Monitoramento da Instalação**

O script fornece feedback em tempo real:

```bash
🚀 Instalando extensões essenciais para o projeto...
📦 Total de extensões a instalar: 54

📥 Instalando ms-python.python... ✅ Sucesso
📥 Instalando ms-python.vscode-pylance... ✅ Sucesso
📥 Instalando ms-python.debugpy... ✅ Sucesso
# ... continua com todas as extensões

📊 Resumo da instalação:
✅ Instaladas com sucesso: 52
❌ Falhas: 2
📦 Total: 54
```

### 🔄 **Reinstalação de Extensões**

Para reinstalar todas as extensões:

```bash
# Reinstalar com força
./scripts/install_extensions_robust.sh

# Ou usar o comando code diretamente
code --install-extension ms-python.python --force
```

## 🎉 **Próximos Passos**

Após o setup completo:

1. **✅ Reinicie o VS Code/Cursor**
2. **✅ Verifique se as extensões estão ativas**
3. **✅ Teste o ambiente Python**
4. **✅ Execute alguns testes**
5. **✅ Comece a desenvolver!**

### 🚀 **Comandos Úteis**

```bash
# Iniciar Marimo
uv run marimo edit

# Formatar código
uv run ruff format .

# Lint código
uv run ruff check .

# Executar testes
uv run pytest

# Atualizar dependências
uv sync --upgrade
```

---

**🎯 Agora você tem um ambiente de desenvolvimento completo e otimizado para o projeto PIBIC!**
