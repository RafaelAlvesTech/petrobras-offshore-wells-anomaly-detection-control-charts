# 🔌 VS Code/Cursor Extensions

## Essential Extensions

- **ms-python.python**: Complete Python support
- **ms-python.vscode-pylance**: Advanced IntelliSense for Python
- **charliermarsh.ruff**: Fast linting and formatting
- **ms-toolsai.jupyter**: Complete Jupyter support
- **ms-toolsai.jupyter-keymap**: Jupyter keyboard shortcuts
- **ms-vscode.vscode-json**: JSON support
- **yzhang.markdown-all-in-one**: Advanced Markdown editor
- **ms-azuretools.vscode-docker**: Docker support
- **eamodio.gitlens**: Git supercharged
- **pkief.material-icon-theme**: Material Design icons
- **littlefoxteam.vscode-python-test-adapter**: Python test runner
- **GitHub.copilot**: AI code assistant
- **GitHub.copilot-chat**: AI development chat

## 🤖 Claude Code Configuration

### Development Tools

- **ms-python.black-formatter**: Automatic Python code formatting
- **ms-python.isort**: Automatic import organization
- **ms-python.flake8**: Advanced Python linting
- **ms-python.mypy-type-checker**: Static type checking
- **ms-python.pylint**: Python code analysis
- **ms-python.autopep8**: Automatic PEP 8 formatting
- **ms-toolsai.jupyter-renderers**: Renderers for different formats

### ⚙️ Project Specific Settings

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

### 🎯 Recommended Settings for Claude Code

#### 1. **Python Environment Setup**

- Use virtual environment `.venv` created by `uv`
- Configure Python interpreter to `./.venv/bin/python`
- Activate environment automatically in terminal

#### 2. **Formatting and Linting**

- Black for automatic formatting (line 88)
- isort for import organization
- Flake8 for code linting
- MyPy for type checking

#### 3. **Notebooks and Jupyter**

- Complete Jupyter support
- Python 3.11 kernel configured
- Renderers for different data formats

#### 4. **Scientific Development**

- Advanced IntelliSense for scientific libraries
- Support for Polars, PyTorch, TensorFlow
- Integration with ML tools

### 🚀 Automatic Setup for Claude Code

#### Linux/macOS

```bash
chmod +x scripts/install_claude_extensions.sh
./scripts/install_claude_extensions.sh
```

#### Windows (PowerShell)

```powershell
.\scripts/install_claude_extensions.ps1
```

#### Cross-platform (Python)

```bash
python scripts/install_claude_extensions.py
```

### 📁 Configuration Structure

```
.vscode/
├── settings.json          # Workspace settings
├── extensions.json        # Recommended extensions
├── launch.json           # Debug configurations
└── tasks.json            # Automated tasks
```

### 🔧 Advanced Settings

#### Debug and Testing

```json
{
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["tests"],
  "python.testing.unittestEnabled": false,
  "python.testing.nosetestsEnabled": false
}
```

#### Terminal and Environment

```json
{
  "terminal.integrated.defaultProfile.linux": "zsh",
  "terminal.integrated.env.linux": {
    "PYTHONPATH": "${workspaceFolder}/src"
  }
}
```

#### Git and Versioning

```json
{
  "git.enableSmartCommit": true,
  "git.confirmSync": false,
  "git.autofetch": true
}
```
