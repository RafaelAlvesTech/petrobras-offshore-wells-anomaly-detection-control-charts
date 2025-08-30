# 🐚 Resumo da Configuração do Zsh no DevContainer

## 📋 Arquivos Criados/Atualizados

### 1. **`.devcontainer/zshrc`** - Configuração Principal

- **Localização**: `.devcontainer/zshrc`
- **Função**: Configuração completa do Zsh otimizada para ambiente containerizado
- **Características**:
  - Prompt personalizado com branding Petrobras 🛢️
  - Variáveis de ambiente do projeto
  - Aliases para desenvolvimento
  - Funções úteis para data science
  - Integração com plugins

### 2. **`.devcontainer/zshrc.project`** - Configurações Específicas

- **Localização**: `.devcontainer/zshrc.project`
- **Função**: Configurações específicas do projeto de detecção de anomalias
- **Características**:
  - Variáveis específicas de ML/DL
  - Aliases para modelos de anomalia
  - Funções para pipeline completo
  - Configurações de experimentos
  - Funções de qualidade de código

### 3. **`.devcontainer/zshrc.local.example`** - Template de Configurações Pessoais

- **Localização**: `.devcontainer/zshrc.local.example`
- **Função**: Template para configurações pessoais não commitadas
- **Características**:
  - Configurações de usuário
  - Preferências pessoais
  - Diretórios pessoais
  - Funções personalizadas

### 4. **`.devcontainer/setup_shell.sh`** - Script de Instalação

- **Localização**: `.devcontainer/setup_shell.sh`
- **Função**: Instalação automática de todas as configurações do Zsh
- **Características**:
  - Cópia de arquivos de configuração
  - Instalação de plugins
  - Configuração do Jupyter
  - Configuração de permissões

### 5. **`.devcontainer/post-create.sh`** - Script de Pós-Criação

- **Localização**: `.devcontainer/post-create.sh`
- **Função**: Script executado após a criação do container
- **Características**:
  - Configuração do ambiente Python
  - Instalação de dependências
  - Configuração do Git
  - Mensagens informativas

### 6. **`.devcontainer/devcontainer.json`** - Configuração do Container

- **Localização**: `.devcontainer/devcontainer.json`
- **Função**: Configuração do ambiente de desenvolvimento
- **Características**:
  - Extensões do VS Code
  - Configurações do terminal
  - Portas forwardadas
  - Comandos de pós-criação

### 7. **`.devcontainer/README.md`** - Documentação

- **Localização**: `.devcontainer/README.md`
- **Função**: Documentação completa das configurações
- **Características**:
  - Guia de instalação
  - Lista de aliases
  - Explicação de funções
  - Solução de problemas

## 🎯 Principais Funcionalidades

### 🎨 Aparência

- **Prompt personalizado** com ícone Petrobras 🛢️
- **Cores personalizadas** para diferentes tipos de arquivos
- **Status do Git** integrado no prompt
- **Status do ambiente virtual** Python

### 🔧 Variáveis de Ambiente

- **Diretórios do projeto**: `DATA_DIR`, `MODELS_DIR`, `NOTEBOOKS_DIR`, etc.
- **Configurações Python**: `PYTHONPATH`, `PYTHONUNBUFFERED`, etc.
- **Configurações ML**: `MLFLOW_TRACKING_URI`, `TENSORBOARD_LOG_DIR`, etc.
- **Configurações de performance**: `OMP_NUM_THREADS`, `CUDA_VISIBLE_DEVICES`, etc.

### 🎯 Aliases Úteis

- **Navegação**: `pj`, `data`, `models`, `notebooks`, `src`, `logs`, `config`
- **Python**: `py`, `pip`, `uv-add`, `uv-sync`, `uv-run`
- **Jupyter**: `jlab`, `jnotebook`, `jstop`
- **MLflow**: `mlflow-ui`, `mlflow-server`
- **TensorBoard**: `tensorboard`
- **Testes**: `test`, `test-cov`, `test-fast`, `test-verbose`
- **Qualidade**: `lint`, `format`, `type-check`, `security`
- **Git**: `gs`, `ga`, `gc`, `gp`, `gl`, `gd`, `gb`, `gco`
- **Docker**: `dbuild`, `drun`, `dstop`, `dclean`
- **Limpeza**: `clean-pyc`, `clean-cache`, `clean-logs`, `clean-models`

### 🚀 Funções Personalizadas

- **Gerenciamento**: `activate_venv()`, `create_venv()`
- **Desenvolvimento**: `run_notebook()`, `train_model()`, `evaluate_model()`
- **Projeto**: `project_status()`, `backup_data()`, `clean_all()`
- **Específicas**: `run_pipeline()`, `run_experiment()`, `monitor_training()`

## 🔌 Plugins Incluídos

### Oh My Zsh

- **git**: Aliases e funções do Git
- **python**: Suporte ao Python
- **pip**: Suporte ao pip
- **docker**: Suporte ao Docker
- **jupyter**: Suporte ao Jupyter

### Plugins Adicionais

- **zsh-autosuggestions**: Sugestões baseadas no histórico
- **zsh-syntax-highlighting**: Highlighting de sintaxe
- **fzf**: Busca fuzzy para arquivos e histórico

## 🚀 Como Funciona

### Instalação Automática

1. **Criação do container**: O `devcontainer.json` define as configurações
2. **Pós-criação**: O `post-create.sh` configura o ambiente Python
3. **Configuração do shell**: O `setup_shell.sh` instala as configurações do Zsh
4. **Aplicação**: As configurações são aplicadas automaticamente

### Processo de Instalação

```bash
# 1. Cópia dos arquivos de configuração
cp .devcontainer/zshrc ~/.zshrc
cp .devcontainer/zshrc.project ~/.zshrc.project
cp .devcontainer/zshrc.local.example ~/.zshrc.local.example

# 2. Instalação de plugins
git clone zsh-autosuggestions
git clone zsh-syntax-highlighting

# 3. Configuração do Jupyter
mkdir -p ~/.jupyter
# Configuração personalizada

# 4. Configuração de permissões
chown -R vscode:vscode ~/.zshrc*
```

## 🎯 Comandos Principais

### Verificação

```bash
project_status          # Status do projeto
check_dependencies      # Verificar dependências
```

### Desenvolvimento

```bash
run_pipeline           # Pipeline completo
run_experiment <nome>  # Experimento específico
monitor_training       # Monitorar treinamento
```

### Qualidade

```bash
check_code_quality     # Verificar qualidade
fix_code_quality       # Corrigir qualidade
```

### Limpeza

```bash
clean_all             # Limpeza completa
cleanup_experiments   # Limpar experimentos antigos
```

## 🔧 Configurações de Ambiente

### Variáveis do Projeto

```bash
PROJECT_ROOT="/workspaces/petrobras-offshore-wells-anomaly-detection-control-charts"
DATA_DIR="${PROJECT_ROOT}/data"
MODELS_DIR="${PROJECT_ROOT}/models"
NOTEBOOKS_DIR="${PROJECT_ROOT}/notebooks"
SRC_DIR="${PROJECT_ROOT}/src"
LOGS_DIR="${PROJECT_ROOT}/logs"
CONFIG_DIR="${PROJECT_ROOT}/config"
```

### Variáveis Python

```bash
PYTHONPATH="${PYTHONPATH}:$(pwd)/src:$(pwd)/notebooks"
PYTHONUNBUFFERED=1
PYTHONDONTWRITEBYTECODE=1
```

### Variáveis de ML

```bash
MLFLOW_TRACKING_URI="http://localhost:5000"
MLFLOW_EXPERIMENT_NAME="petrobras-anomaly-detection"
TENSORBOARD_LOG_DIR="./logs/tensorboard"
```

## 🎨 Personalização

### Configurações Pessoais

```bash
# 1. Copiar template
cp ~/.zshrc.local.example ~/.zshrc.local

# 2. Personalizar
nano ~/.zshrc.local

# 3. Recarregar
source ~/.zshrc
```

### Configurações Disponíveis

- **Usuário**: Nome, email, departamento
- **Preferências**: Editor, browser, terminal
- **Performance**: Threads, memória, GPU
- **Dados**: Diretórios pessoais, formatos
- **Modelos**: Tipos, parâmetros, experimentos
- **Monitoramento**: Logging, métricas, alertas

## 🧪 Testando a Configuração

### Verificar Instalação

```bash
# Verificar se Zsh está funcionando
zsh --version

# Verificar plugins
ls ~/.oh-my-zsh/custom/plugins/

# Verificar configurações
echo $PROJECT_NAME
echo $DATA_DIR
```

### Testar Funções

```bash
# Testar status do projeto
project_status

# Testar aliases
pj
data
models

# Testar funções
create_venv
```

## 🔧 Solução de Problemas

### Problema: Zsh não está sendo usado

```bash
# Verificar shell atual
echo $SHELL

# Alterar para Zsh
chsh -s $(which zsh)

# Reiniciar terminal
```

### Problema: Plugins não carregam

```bash
# Verificar se os diretórios existem
ls ~/.oh-my-zsh/custom/plugins/

# Recarregar configurações
source ~/.zshrc
```

### Problema: Variáveis não definidas

```bash
# Verificar se os arquivos existem
ls ~/.zshrc
ls ~/.zshrc.project

# Recarregar configurações
source ~/.zshrc
```

## 📚 Documentação

- **README.md**: Documentação principal atualizada
- **.devcontainer/README.md**: Documentação específica do devcontainer
- **docs/ZSH_CONFIGURATION.md**: Documentação detalhada do Zsh
- **.devcontainer/zshrc.local.example**: Template de configurações pessoais

## ✅ Benefícios

1. **Instalação Automática**: Configurações aplicadas automaticamente no container
2. **Ambiente Consistente**: Mesmo ambiente para todos os desenvolvedores
3. **Produtividade**: Aliases e funções aceleram o desenvolvimento
4. **Organização**: Variáveis de ambiente organizam o projeto
5. **Aparência**: Prompt personalizado melhora a experiência
6. **Automação**: Funções automatizam tarefas repetitivas
7. **Integração**: Plugins melhoram a funcionalidade do terminal
8. **Personalização**: Configurações pessoais permitem customização

## 🎉 Resultado Final

O ambiente Zsh está completamente configurado no `.devcontainer` com:

- ✅ Instalação automática no container
- ✅ Prompt personalizado com branding Petrobras
- ✅ Todas as variáveis de ambiente necessárias
- ✅ Aliases para todos os comandos comuns
- ✅ Funções para automação de tarefas
- ✅ Plugins para melhorar a experiência
- ✅ Documentação completa
- ✅ Template para configurações pessoais
- ✅ Scripts de instalação automatizados

**🛢️ O projeto está pronto para desenvolvimento com uma experiência de terminal otimizada no ambiente containerizado!**
