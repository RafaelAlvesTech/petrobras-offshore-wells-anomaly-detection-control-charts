# 🛢️ Petrobras Offshore Wells Anomaly Detection - DevContainer

Este diretório contém a configuração completa do DevContainer para o projeto de detecção de anomalias em séries temporais multivariadas de poços offshore da Petrobras.

## 📋 Visão Geral

O DevContainer está configurado para fornecer um ambiente de desenvolvimento completo e otimizado para o projeto, incluindo:

- **Python 3.11** com todas as dependências necessárias
- **Zsh** com Oh My Zsh e plugins personalizados
- **Jupyter Lab** para notebooks interativos
- **MLflow** para experimentos e tracking
- **TensorBoard** para visualização de métricas
- **Docker-in-Docker** para containerização
- **Ferramentas de Cloud** (AWS, Azure, GCP)
- **Kubernetes** e Helm para orquestração

## 🚀 Como Usar

### 1. Abrir no DevContainer

1. Abra o projeto no VS Code
2. Pressione `Ctrl+Shift+P` (ou `Cmd+Shift+P` no Mac)
3. Digite "Dev Containers: Reopen in Container"
4. Aguarde a construção e configuração do container

### 2. Primeira Execução

Na primeira execução, o script `post-create.sh` será executado automaticamente e irá:

- Instalar todas as dependências Python
- Configurar o ambiente Zsh
- Criar a estrutura de diretórios
- Configurar Jupyter Lab
- Instalar plugins do Zsh
- Configurar pre-commit hooks

### 3. Comandos Úteis

Após a configuração, você terá acesso aos seguintes comandos:

```bash
# Navegação do projeto
pj          # Ir para o diretório raiz do projeto
data        # Ir para o diretório de dados
models      # Ir para o diretório de modelos
notebooks   # Ir para o diretório de notebooks
src         # Ir para o diretório de código fonte
logs        # Ir para o diretório de logs

# Desenvolvimento
jlab        # Iniciar Jupyter Lab
mlflow-ui   # Iniciar MLflow UI
tensorboard # Iniciar TensorBoard

# Status e informações
project_status  # Ver status completo do projeto
status          # Alias para project_status

# Limpeza
clean-pyc       # Limpar arquivos .pyc
clean-cache     # Limpar cache Python
clean-logs      # Limpar logs
clean-all       # Limpeza completa
```

## 🔧 Configuração

### Estrutura de Arquivos

```
.devcontainer/
├── devcontainer.json      # Configuração principal do DevContainer
├── Dockerfile            # Imagem Docker customizada
├── post-create.sh        # Script de pós-criação
├── zshrc.custom          # Configuração personalizada do Zsh
├── README.md             # Este arquivo
└── ...
```

### Variáveis de Ambiente

O DevContainer define as seguintes variáveis de ambiente:

```bash
PROJECT_NAME=petrobras-offshore-wells-anomaly-detection
PROJECT_ROOT=/workspaces/petrobras-offshore-wells-anomaly-detection-control-charts
DATA_DIR=/workspaces/petrobras-offshore-wells-anomaly-detection-control-charts/data
MODELS_DIR=/workspaces/petrobras-offshore-wells-anomaly-detection-control-charts/models
NOTEBOOKS_DIR=/workspaces/petrobras-offshore-wells-anomaly-detection-control-charts/notebooks
SRC_DIR=/workspaces/petrobras-offshore-wells-anomaly-detection-control-charts/src
LOGS_DIR=/workspaces/petrobras-offshore-wells-anomaly-detection-control-charts/logs
MLFLOW_TRACKING_URI=http://localhost:5000
MLFLOW_EXPERIMENT_NAME=petrobras-anomaly-detection
TENSORBOARD_LOG_DIR=/workspaces/petrobras-offshore-wells-anomaly-detection-control-charts/logs/tensorboard
```

### Portas Expostas

O DevContainer expõe as seguintes portas:

- **8888**: Jupyter Lab
- **8000**: MLflow UI
- **5000**: MLflow Tracking
- **6006**: TensorBoard
- **8080**: Web App
- **3000**: React Dev Server

## 🐚 Configuração do Zsh

### Oh My Zsh

O ambiente inclui Oh My Zsh com os seguintes plugins:

- `git`: Comandos Git úteis
- `python`: Comandos Python
- `pip`: Comandos pip
- `docker`: Comandos Docker
- `docker-compose`: Comandos Docker Compose
- `jupyter`: Comandos Jupyter
- `conda-zsh-completion`: Completions para Conda

### Plugins Adicionais

- **zsh-autosuggestions**: Sugestões automáticas baseadas no histórico
- **zsh-syntax-highlighting**: Destaque de sintaxe para comandos

### Prompt Personalizado

O prompt inclui:

- 🛢️ Ícone da Petrobras
- Nome do usuário e host
- Diretório atual
- Status do Git (branch e modificações)
- Status do ambiente virtual

## 📊 Ferramentas Incluídas

### Desenvolvimento Python

- **Python 3.11**: Versão mais recente do Python
- **uv**: Gerenciador de dependências rápido
- **pip**: Gerenciador de pacotes Python
- **pre-commit**: Hooks de pré-commit

### Data Science

- **Jupyter Lab**: Ambiente interativo
- **Pandas**: Manipulação de dados
- **Polars**: Manipulação de dados de alta performance
- **NumPy**: Computação numérica
- **Scikit-learn**: Machine learning
- **PyTorch**: Deep learning
- **TensorFlow**: Deep learning

### Experimentos e Tracking

- **MLflow**: Tracking de experimentos
- **TensorBoard**: Visualização de métricas
- **Optuna**: Otimização de hiperparâmetros
- **Weights & Biases**: Tracking de experimentos

### Cloud e DevOps

- **Docker**: Containerização
- **Kubernetes**: Orquestração
- **Helm**: Gerenciamento de pacotes Kubernetes
- **AWS CLI**: Amazon Web Services
- **Azure CLI**: Microsoft Azure
- **Google Cloud CLI**: Google Cloud Platform

## 🔍 Solução de Problemas

### Problemas Comuns

1. **Container não inicia**
   - Verifique se o Docker está rodando
   - Tente reconstruir o container

2. **Dependências não instaladas**
   - Execute `uv sync` manualmente
   - Verifique o arquivo `pyproject.toml`

3. **Zsh não carrega**
   - Execute `source ~/.zshrc`
   - Verifique se o arquivo `.zshrc.custom` existe

4. **Jupyter não inicia**
   - Verifique se a porta 8888 está disponível
   - Execute `jlab` para iniciar manualmente

### Logs e Debug

- Logs do container: `docker logs <container_id>`
- Logs do Jupyter: `~/.jupyter/logs/`
- Logs do projeto: `./logs/`

## 📚 Recursos Adicionais

### Documentação

- [Dev Containers](https://code.visualstudio.com/docs/remote/containers)
- [Oh My Zsh](https://ohmyz.sh/)
- [Jupyter Lab](https://jupyterlab.readthedocs.io/)
- [MLflow](https://mlflow.org/)

### Comandos Úteis

```bash
# Reconstruir o container
Ctrl+Shift+P -> "Dev Containers: Rebuild Container"

# Abrir terminal integrado
Ctrl+` (backtick)

# Ver status do projeto
project_status

# Iniciar todos os serviços
jlab & mlflow-ui & tensorboard
```

## 🤝 Contribuição

Para contribuir com melhorias no DevContainer:

1. Faça suas alterações nos arquivos de configuração
2. Teste localmente
3. Documente as mudanças
4. Submeta um pull request

## 📄 Licença

Este projeto está sob a licença do projeto principal.
