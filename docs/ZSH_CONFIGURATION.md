# 🐚 Configuração do Zsh - Projeto Petrobras

Este documento descreve as configurações personalizadas do Zsh para o projeto de detecção de anomalias em poços offshore da Petrobras.

## 📋 Visão Geral

O projeto inclui configurações completas do Zsh com:

- Personalizações de aparência e prompt
- Variáveis de ambiente específicas do projeto
- Aliases úteis para desenvolvimento
- Funções personalizadas para automação
- Integração com ferramentas de ML e data science

## 🚀 Instalação Rápida

### Opção 1: Script Automático (Recomendado)

```bash
# Execute o script de configuração automática
./scripts/setup_zsh.sh
```

### Opção 2: Instalação Manual

```bash
# 1. Instalar dependências do sistema
sudo apt-get update
sudo apt-get install -y zsh curl wget git build-essential

# 2. Instalar Oh My Zsh
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# 3. Instalar plugins
git clone https://github.com/zsh-users/zsh-autosuggestions ~/.zsh/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ~/.zsh/zsh-syntax-highlighting

# 4. Instalar uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 5. Copiar configurações
cp .zshrc ~/.zshrc
cp .zshrc.project ~/.zshrc.project

# 6. Recarregar configurações
source ~/.zshrc
```

## 📁 Estrutura de Arquivos

```
├── .zshrc                 # Configuração principal do Zsh
├── .zshrc.project         # Configurações específicas do projeto
├── scripts/
│   └── setup_zsh.sh      # Script de instalação automática
└── docs/
    └── ZSH_CONFIGURATION.md  # Esta documentação
```

## 🎨 Personalizações de Aparência

### Prompt Personalizado

O prompt inclui:

- 🛢️ Ícone do projeto Petrobras
- Nome do usuário e hostname
- Diretório atual
- Status do Git (branch e modificações)
- Status do ambiente virtual Python

### Cores e Temas

- Cores personalizadas para diferentes tipos de arquivos
- Syntax highlighting para comandos
- Autosuggestions baseadas no histórico

## 🔧 Variáveis de Ambiente

### Variáveis do Projeto

```bash
PROJECT_NAME="petrobras-offshore-wells-anomaly-detection"
PROJECT_ROOT="$(pwd)"
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

## 🎯 Aliases Úteis

### Navegação do Projeto

```bash
pj      # Ir para o diretório raiz do projeto
data    # Ir para o diretório de dados
models  # Ir para o diretório de modelos
notebooks # Ir para o diretório de notebooks
src     # Ir para o diretório de código fonte
logs    # Ir para o diretório de logs
config  # Ir para o diretório de configurações
```

### Python e Desenvolvimento

```bash
py      # python
pip     # uv pip
uv-add  # uv add
uv-sync # uv sync
uv-run  # uv run
```

### Jupyter

```bash
jlab        # Iniciar Jupyter Lab
jnotebook   # Iniciar Jupyter Notebook
jstop       # Parar Jupyter
```

### MLflow e TensorBoard

```bash
mlflow-ui      # Iniciar MLflow UI
mlflow-server  # Iniciar servidor MLflow
tensorboard    # Iniciar TensorBoard
```

### Testes e Qualidade

```bash
test        # pytest
test-cov    # pytest com cobertura
lint        # ruff check
format      # ruff format
type-check  # mypy
security    # bandit
```

### Git

```bash
gs  # git status
ga  # git add
gc  # git commit
gp  # git push
gl  # git log --oneline
gd  # git diff
gb  # git branch
gco # git checkout
```

### Docker

```bash
dbuild  # docker build
drun    # docker run
dstop   # docker stop
dclean  # docker system prune
```

### Limpeza

```bash
clean-pyc     # Remover arquivos .pyc
clean-cache   # Remover __pycache__
clean-logs    # Limpar logs
clean-models  # Limpar modelos
```

## 🚀 Funções Personalizadas

### Gerenciamento de Ambiente

```bash
activate_venv()    # Ativar ambiente virtual
create_venv()      # Criar ambiente virtual
```

### Desenvolvimento

```bash
run_notebook <nome>     # Executar notebook
train_model <nome>      # Treinar modelo
evaluate_model <nome>   # Avaliar modelo
generate_report()       # Gerar relatório
```

### Projeto

```bash
project_status()        # Status do projeto
backup_data()          # Backup de dados
clean_all()            # Limpeza completa
```

### Específicas do Projeto Petrobras

```bash
run_pipeline()                    # Pipeline completo
run_experiment <nome> <modelo>    # Executar experimento
monitor_training()                # Monitorar treinamento
cleanup_experiments <dias>        # Limpar experimentos antigos
backup_experiments()              # Backup de experimentos
check_code_quality()              # Verificar qualidade
fix_code_quality()                # Corrigir qualidade
```

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

## ⚙️ Configurações Avançadas

### Histórico

```bash
HISTSIZE=10000
SAVEHIST=10000
HISTFILE=~/.zsh_history
```

### Autocompletar

```bash
setopt AUTO_LIST
setopt AUTO_MENU
setopt COMPLETE_IN_WORD
setopt ALWAYS_TO_END
```

### Diretório

```bash
setopt AUTO_CD
setopt AUTO_PUSHD
setopt PUSHD_IGNORE_DUPS
```

### Correção

```bash
setopt CORRECT
setopt CORRECT_ALL
```

## 🧪 Testando a Configuração

### Verificar Instalação

```bash
# Verificar se Zsh está funcionando
zsh --version

# Verificar plugins
ls ~/.zsh/

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
ls ~/.zsh/

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

### Problema: Comandos não encontrados

```bash
# Verificar PATH
echo $PATH

# Adicionar ao PATH se necessário
export PATH="$HOME/.cargo/bin:$PATH"
```

## 📚 Recursos Adicionais

### Documentação

- [Oh My Zsh](https://ohmyz.sh/)
- [Zsh Documentation](https://zsh.sourceforge.io/Doc/)
- [fzf](https://github.com/junegunn/fzf)

### Comandos Úteis

```bash
# Ver histórico de comandos
history

# Buscar no histórico
Ctrl+R

# Autocompletar
Tab

# Buscar arquivos
fzf
```

## 🤝 Contribuindo

Para contribuir com melhorias nas configurações do Zsh:

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Modifique os arquivos de configuração
4. Teste as mudanças
5. Faça um pull request

### Estrutura de Contribuição

- `.zshrc`: Configurações gerais
- `.zshrc.project`: Configurações específicas do projeto
- `scripts/setup_zsh.sh`: Script de instalação
- `docs/ZSH_CONFIGURATION.md`: Documentação

## 📄 Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

**🛢️ Projeto Petrobras Offshore Wells Anomaly Detection**
_Configurações otimizadas para desenvolvimento em Python e Machine Learning_
