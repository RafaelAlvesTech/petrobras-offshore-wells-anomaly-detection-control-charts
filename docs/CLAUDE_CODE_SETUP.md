# 🤖 Claude Code - Configuração e Uso

## 🎯 Visão Geral

Este documento descreve a configuração específica do **Claude Code** para o projeto **Petrobras Offshore Wells Anomaly Detection**. As configurações foram otimizadas para desenvolvimento científico, análise de dados e machine learning.

## 🚀 Configurações Implementadas

### 🐍 Python Development
- **Interpreter**: Configurado para `.venv/bin/python`
- **Type Checking**: Modo estrito para melhor qualidade de código
- **Auto-imports**: Completamento automático de imports
- **Path Analysis**: Análise inteligente de caminhos do projeto

### 🧠 Formatação e Linting
- **Black**: Formatação automática com linha 88
- **isort**: Organização automática de imports
- **Flake8**: Linting com configurações específicas
- **MyPy**: Verificação de tipos estática
- **Pylint**: Análise de código avançada

### 📊 Jupyter e Notebooks
- **Kernel**: Python 3.11 (petrobras)
- **Auto-matcher**: Ativação automática de kernels
- **Renderers**: Suporte a diferentes formatos de dados
- **Interactive Windows**: Modo por arquivo

### 🎯 Desenvolvimento Científico
- **Análise de Código**: Modo workspace para melhor performance
- **Stubs**: Suporte a type hints e stubs
- **Extra Paths**: Inclusão de bibliotecas científicas
- **Diagnósticos**: Análise em tempo real

## 🔧 Instalação das Extensões

### Linux/macOS
```bash
chmod +x scripts/install_claude_extensions.sh
./scripts/install_claude_extensions.sh
```

### Windows (PowerShell)
```powershell
.\scripts\install_claude_extensions.ps1
```

### Cross-platform (Python)
```bash
python scripts/install_claude_extensions.py
```

## 📁 Estrutura de Configurações

```
.vscode/
├── settings.json              # Configurações principais
├── claude-code-settings.json  # Configurações específicas Claude Code
├── extensions.json            # Extensões recomendadas
├── launch.json               # Configurações de debug
└── tasks.json                # Tarefas automatizadas
```

## 🎨 Configurações de Interface

### Tema e Ícones
- **Tema**: GitHub Dark Default
- **Ícones**: Material Icon Theme
- **Fonte**: JetBrains Mono com ligaduras
- **Tamanho**: 14px com line-height 1.6

### Editor
- **Régua**: Linha 88 (padrão Black)
- **Tab Size**: 4 espaços
- **Format on Save**: Ativado
- **Auto-organize Imports**: Ativado

### Terminal
- **Perfil**: zsh (Linux/macOS), PowerShell (Windows)
- **PYTHONPATH**: Configurado para workspace
- **PYTHONUNBUFFERED**: Ativado para melhor output

## 🚀 Performance e Escalabilidade

### Exclusões de Arquivos
- **Ambiente Virtual**: `.venv/**`
- **Cache Python**: `__pycache__/**`, `*.pyc`
- **Dados**: `data/raw/**`, `data/processed/**`
- **Modelos**: `models/**`
- **Logs**: `logs/**`

### Watchers
- **File Watching**: Otimizado para performance
- **Exclusões**: Pastas pesadas e temporárias
- **Cache**: Ruff cache excluído

## 🔍 Ferramentas de Qualidade

### SonarLint
- **Regras Desabilitadas**: S1481, S1172, S1066
- **Análise**: Em tempo real
- **Integração**: Com configurações do projeto

### Code Spell Checker
- **Idioma**: Português brasileiro
- **Integração**: Com extensões de qualidade
- **Customização**: Para termos técnicos do projeto

## 📊 Data Science e ML

### Jupyter Integration
- **Kernel**: Python 3.11 específico
- **Auto-restart**: Desabilitado para estabilidade
- **Matcher**: Ativado para melhor UX
- **Renderers**: Suporte a múltiplos formatos

### Python Analysis
- **Type Checking**: Modo estrito
- **Auto-completion**: Ativado para bibliotecas científicas
- **Path Resolution**: Inteligente para imports
- **Diagnostics**: Workspace-wide

## 🐳 Docker e Containers

### Configurações
- **Build**: `docker build -t ${imageName} .`
- **Run**: `docker run -it --rm ${imageName}`
- **Push/Pull**: Comandos otimizados
- **Extensions**: Instaladas automaticamente

### Remote Development
- **Container Extensions**: Configuradas para Claude Code
- **Python Support**: Completo no container
- **Jupyter**: Funcionando em containers

## 🔄 Git e Versionamento

### Configurações
- **Smart Commit**: Ativado
- **Auto-fetch**: A cada 5 minutos
- **Auto-stash**: Para operações seguras
- **Conventional Commits**: Suporte completo

### Extensões
- **GitLens**: Git supercharged
- **Git History**: Histórico visual
- **GitHub Actions**: Integração nativa
- **Pull Requests**: Suporte completo

## 🧪 Testing e Debug

### Pytest Integration
- **Enabled**: Pytest ativado
- **Args**: `tests/` como diretório padrão
- **Path**: `./.venv/bin/pytest`
- **Unittest/Nosetests**: Desabilitados

### Debug Configuration
- **Console**: Terminal integrado
- **Titles**: Personalizados com emojis
- **Templates**: Formatos consistentes

## 🎯 Configurações Específicas para Séries Temporais

### Análise de Dados
- **Polars**: Suporte completo
- **Time Series**: Otimizações específicas
- **Multivariate**: Análise de dependências
- **Performance**: Configurações para grandes datasets

### Machine Learning
- **PyTorch/TensorFlow**: Suporte nativo
- **Scikit-learn**: Integração completa
- **SHAP**: Para interpretabilidade
- **Optuna**: Para otimização de hiperparâmetros

## 🚀 Otimizações para Claude Code

### IntelliSense
- **Auto-completion**: Ativado para todas as bibliotecas
- **Type hints**: Suporte completo
- **Documentation**: Docstrings em tempo real
- **Signatures**: Parâmetros e tipos

### Performance
- **Analysis Mode**: Workspace para melhor performance
- **Stub Paths**: Para bibliotecas externas
- **Extra Paths**: Inclusão de dependências
- **Exclusions**: Pastas não relevantes

## 🔧 Troubleshooting

### Problemas Comuns

#### Extensões não funcionando
```bash
# Verificar se o VS Code CLI está disponível
code --version

# Reinstalar extensões
code --install-extension <extension-id>
```

#### Python Interpreter não encontrado
```bash
# Verificar ambiente virtual
ls -la .venv/bin/python

# Ativar ambiente
source .venv/bin/activate
```

#### Performance lenta
```bash
# Verificar configurações de exclusão
# Verificar tamanho de pastas de dados
# Limpar cache Python
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +
```

### Logs e Debug
- **Output Panel**: Verificar mensagens de erro
- **Developer Tools**: Console para debugging
- **Extension Host**: Logs de extensões
- **Python Language Server**: Logs do Pylance

## 📚 Recursos Adicionais

### Documentação
- [VS Code Python](https://code.visualstudio.com/docs/languages/python)
- [Python Extension Pack](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Jupyter Extension](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter)

### Comunidade
- [VS Code Python Issues](https://github.com/microsoft/vscode-python/issues)
- [Python Extension Discussions](https://github.com/microsoft/vscode-python/discussions)
- [Jupyter Extension Issues](https://github.com/microsoft/vscode-jupyter/issues)

## 🎯 Próximos Passos

1. **Instalar Extensões**: Execute os scripts de instalação
2. **Configurar Python**: Verifique o interpreter
3. **Testar Jupyter**: Abra um notebook Marimo
4. **Verificar Linting**: Execute análise de código
5. **Customizar Tema**: Ajuste cores e fontes conforme preferência

## 🤝 Contribuição

Para melhorar as configurações do Claude Code:

1. **Teste**: Verifique se funciona em seu ambiente
2. **Documente**: Adicione novas configurações
3. **Otimize**: Sugira melhorias de performance
4. **Compartilhe**: Compartilhe experiências com a equipe

---

> **🚀 Claude Code está configurado e otimizado para o projeto Petrobras Offshore Wells Anomaly Detection!**
