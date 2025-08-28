# 🚀 Complete Setup Guide - Petrobras Offshore Wells Anomaly Detection

> **🇧🇷 [Ver guia em Português Brasileiro](setup-guide.pt-BR.md)**

## 📋 Table of Contents

- [🎯 Overview](#-overview)
- [🔌 Extension Setup](#-extension-setup)
- [🔧 Robust Extension Script](#-robust-extension-script)
- [🐍 Python Environment Setup](#-python-environment-setup)
- [⚙️ Workspace Configuration](#️-workspace-configuration)
- [🧪 Testing Configuration](#-testing-configuration)
- [🔧 Troubleshooting](#-troubleshooting)

## 🎯 Overview

This guide provides step-by-step instructions to completely set up the development environment for the PIBIC project on anomaly detection in Petrobras offshore wells.

### 🎯 **What will be configured:**

- ✅ Essential VS Code/Cursor extensions
- ✅ Python environment with uv
- ✅ Project dependencies
- ✅ Pre-commit hooks
- ✅ Workspace configurations
- ✅ Testing environment

## 🔌 Extension Setup

### 🚀 **Automatic Installation (Recommended)**

#### **Linux/macOS - Robust Script (Recommended)**

```bash
# Give execution permission
chmod +x scripts/install_extensions_robust.sh

# Run robust script (continues even with errors)
./scripts/install_extensions_robust.sh
```

#### **Linux/macOS - Original Script**

```bash
# Give execution permission
chmod +x scripts/install_extensions.sh

# Run original script
./scripts/install_extensions.sh
```

#### **Windows (PowerShell)**

```powershell
# Run PowerShell script
.\scripts\install_extensions.ps1

# Or with force (reinstall)
.\scripts\install_extensions.ps1 -Force
```

#### **Cross-platform (Python)**

```bash
# Run Python script
python scripts/install_extensions.py
```

### 🔍 **Script Differences**

| Script                         | Characteristic                                                                                     | Recommendation     |
| ------------------------------ | -------------------------------------------------------------------------------------------------- | ------------------ |
| `install_extensions_robust.sh` | ✅ Continues even with errors<br>✅ Installs all extensions<br>✅ Better for complete installation | **🌟 Recommended** |
| `install_extensions.sh`        | ⚠️ Stops on error<br>⚠️ May not install all<br>⚠️ Better for debugging                             | For development    |
| `install_extensions.py`        | 🔄 Cross-platform<br>🔄 Installation via Python<br>🔄 Slower                                       | For Windows/Linux  |

### 📦 **Extensions that will be installed:**

| Category            | Extension           | ID                                       | Description             |
| ------------------- | ------------------- | ---------------------------------------- | ----------------------- |
| 🐍 **Python**       | Python              | ms-python.python                         | Complete Python support |
| 🐍 **Python**       | Pylance             | ms-python.vscode-pylance                 | Advanced IntelliSense   |
| 🐍 **Python**       | Ruff                | charliermarsh.ruff                       | Linting and formatting  |
| 📊 **Data Science** | Jupyter             | ms-toolsai.jupyter                       | Jupyter support         |
| 📊 **Data Science** | Jupyter Keymap      | ms-toolsai.jupyter-keymap                | Keyboard shortcuts      |
| 🔧 **Dev Tools**    | JSON                | ms-vscode.vscode-json                    | JSON support            |
| 🔧 **Dev Tools**    | Markdown            | yzhang.markdown-all-in-one               | Markdown editor         |
| 🐳 **Docker**       | Docker              | ms-azuretools.vscode-docker              | Docker support          |
| 🔄 **Git**          | GitLens             | eamodio.gitlens                          | Git supercharged        |
| 🎨 **Themes**       | Material Icons      | pkief.material-icon-theme                | Material icons          |
| 🧪 **Testing**      | Python Test Adapter | littlefoxteam.vscode-python-test-adapter | Test runner             |
| 🚀 **AI**           | GitHub Copilot      | GitHub.copilot                           | AI assistant            |
| 🚀 **AI**           | GitHub Copilot Chat | GitHub.copilot-chat                      | AI chat                 |

### 🔧 **Manual Installation (Alternative)**

If you prefer to install manually:

1. **Open VS Code/Cursor**
2. **Press `Ctrl+Shift+X`** (or `Cmd+Shift+X` on Mac)
3. **Search and install** each extension from the list above
4. **Restart the editor** after installation

## 🐍 Python Environment Setup

### 📋 **Prerequisites**

- Python 3.11+ installed
- Git installed
- VS Code/Cursor installed

### 🚀 **Step by Step**

#### **1. Clone the Repository**

```bash
git clone https://github.com/RafaelAlvesTech/petrobras-offshore-wells-anomaly-detection-control-charts.git
cd petrobras-offshore-wells-anomaly-detection-control-charts
```

#### **2. Install uv**

```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or via pip
pip install uv
```

#### **3. Create Virtual Environment**

```bash
# Create environment
uv venv

# Activate environment
# Linux/macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

#### **4. Install Dependencies**

```bash
# Sync project (recommended)
uv sync

# Or install manually
uv pip install -r requirements.txt
```

#### **5. Install Development Dependencies**

```bash
# Marimo for notebooks
uv add marimo

# Polars for data
uv add polars

# Pre-commit for hooks
uv add pre-commit

# Ruff for linting
uv add ruff

# Pytest for testing
uv add pytest
```

#### **6. Configure Pre-commit**

```bash
# Install hooks
uv run pre-commit install

# Verify installation
uv run pre-commit run --all-files
```

## ⚙️ Workspace Configuration

### 🔧 **Automatic Configuration**

The project includes optimized configurations in `.vscode/settings.json`:

- **Python interpreter**: Configured for `.venv`
- **Formatting**: Automatic with Ruff
- **Linting**: Automatic with Ruff
- **Terminal**: Configured for virtual environment
- **Performance**: Heavy folder exclusions

### 🎯 **Manual Configuration**

#### **1. Select Python Interpreter**

1. **Press `Ctrl+Shift+P`** (or `Cmd+Shift+P` on Mac)
2. **Type**: `Python: Select Interpreter`
3. **Select**: `./.venv/bin/python`

#### **2. Verify Configuration**

1. **Open Command Palette** (`Ctrl+Shift+P`)
2. **Type**: `Preferences: Open Workspace Settings (JSON)`
3. **Verify** if configurations are correct

### 📁 **Folder Structure**

```
petrobras-offshore-wells-anomaly-detection-control-charts/
├── 📁 .vscode/                    # Workspace configurations
│   ├── 📄 settings.json           # Project settings
│   ├── 📄 extensions.json         # Recommended extensions
│   ├── 📄 tasks.json              # Automated tasks
│   └── 📄 launch.json             # Debug configurations
├── 📁 scripts/                    # Setup scripts
│   ├── 📄 install_extensions_robust.sh  # Linux/macOS setup (Recommended)
│   ├── 📄 install_extensions.sh   # Linux/macOS setup (Original)
│   ├── 📄 install_extensions.ps1  # Windows setup
│   └── 📄 install_extensions.py   # Cross-platform setup
├── 📁 src/                        # Source code
├── 📁 notebooks/                  # Marimo notebooks
├── 📁 tests/                      # Tests
└── 📁 docs/                       # Documentation
```

## 🧪 Testing Configuration

### 🚀 **Run Tests**

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=html

# Run specific tests
uv run pytest tests/test_models.py

# Run in verbose mode
uv run pytest -v
```

### 🔧 **Debug Configuration**

The project includes debug configurations in `.vscode/launch.json`:

- **🐍 Python: Current File**: Debug current file
- **🧪 Python: Debug Tests**: Debug tests
- **📓 Python: Debug Marimo**: Debug notebooks
- **🐳 Docker: Debug Container**: Debug containers

## 🔧 Troubleshooting

### ❌ **Common Issues**

#### **1. Extensions don't install**

```bash
# Check if code is in PATH
code --version

# Try manual installation
code --install-extension ms-python.python

# Use robust script (recommended)
./scripts/install_extensions_robust.sh
```

#### **2. Python interpreter not found**

```bash
# Check if environment was created
ls -la .venv/bin/python

# Recreate environment
rm -rf .venv
uv venv
source .venv/bin/activate
uv sync
```

#### **3. Pre-commit fails**

```bash
# Reinstall hooks
uv run pre-commit uninstall
uv run pre-commit install

# Run manually
uv run pre-commit run --all-files
```

#### **4. Dependencies don't install**

```bash
# Clear uv cache
uv cache clean

# Reinstall dependencies
uv sync --reinstall
```

### 🆘 **Still Having Issues?**

1. **Check logs**: `uv run pre-commit run --all-files --verbose`
2. **Restart editor**: Close and open VS Code/Cursor
3. **Check versions**: `python --version`, `uv --version`
4. **Check issues**: Project GitHub

## 🔧 **Robust Extension Script**

### 🚀 **Why use the robust script?**

The `install_extensions_robust.sh` was created to solve common installation problems:

- **✅ Continues even with errors**: Doesn't stop if an extension fails
- **✅ Installs all extensions**: Ensures complete installation
- **✅ Better feedback**: Shows detailed progress
- **✅ Error handling**: Continues trying to install the rest

### 📊 **Installation Monitoring**

The script provides real-time feedback:

```bash
🚀 Installing essential extensions for the project...
📦 Total extensions to install: 54

📥 Installing ms-python.python... ✅ Success
📥 Installing ms-python.vscode-pylance... ✅ Success
📥 Installing ms-python.debugpy... ✅ Success
# ... continues with all extensions

📊 Installation summary:
✅ Successfully installed: 52
❌ Failures: 2
📦 Total: 54
```

### 🔄 **Extension Reinstallation**

To reinstall all extensions:

```bash
# Reinstall with force
./scripts/install_extensions_robust.sh

# Or use code command directly
code --install-extension ms-python.python --force
```

## 🎉 **Next Steps**

After complete setup:

1. **✅ Restart VS Code/Cursor**
2. **✅ Verify extensions are active**
3. **✅ Test Python environment**
4. **✅ Run some tests**
5. **✅ Start developing!**

### 🚀 **Useful Commands**

```bash
# Start Marimo
uv run marimo edit

# Format code
uv run ruff format .

# Lint code
uv run ruff check .

# Run tests
uv run pytest

# Update dependencies
uv sync --upgrade
```

---

**🎯 Now you have a complete and optimized development environment for the PIBIC project!**
