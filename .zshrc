# =============================================================================
# 🛢️ PETROBRAS OFFSHORE WELLS ANOMALY DETECTION - ZSH CONFIGURATION
# =============================================================================
# Configuração personalizada para o projeto PIBIC de detecção de anomalias
# em séries temporais multivariadas de poços offshore da Petrobras
# =============================================================================

# =============================================================================
# 🚀 CONFIGURAÇÕES BÁSICAS DO ZSH
# =============================================================================

# Configurações de histórico
HISTSIZE=10000
SAVEHIST=10000
HISTFILE=~/.zsh_history
setopt HIST_VERIFY
setopt SHARE_HISTORY
setopt APPEND_HISTORY
setopt INC_APPEND_HISTORY
setopt HIST_IGNORE_DUPS
setopt HIST_IGNORE_ALL_DUPS
setopt HIST_REDUCE_BLANKS
setopt HIST_IGNORE_SPACE

# Configurações de autocompletar
autoload -U compinit && compinit
setopt AUTO_LIST
setopt AUTO_MENU
setopt COMPLETE_IN_WORD
setopt ALWAYS_TO_END

# Configurações de diretório
setopt AUTO_CD
setopt AUTO_PUSHD
setopt PUSHD_IGNORE_DUPS
setopt PUSHD_SILENT

# Configurações de correção
setopt CORRECT
setopt CORRECT_ALL

# =============================================================================
# 🎨 PERSONALIZAÇÕES DE APARÊNCIA
# =============================================================================

# Cores personalizadas
export TERM="xterm-256color"

# Cores para ls
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    alias ls='ls --color=auto'
    alias ll='ls -alF --color=auto'
    alias la='ls -A --color=auto'
    alias l='ls -CF --color=auto'
elif [[ "$OSTYPE" == "darwin"* ]]; then
    alias ls='ls -G'
    alias ll='ls -alFG'
    alias la='ls -AG'
    alias l='ls -CFG'
fi

# Cores para grep
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'

# =============================================================================
# 🐍 CONFIGURAÇÕES DO PYTHON E AMBIENTE
# =============================================================================

# Configurações do Python
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
export PYTHONPATH="${PYTHONPATH}:$(pwd)/notebooks"
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1

# Configurações do uv (gerenciador de dependências)
export UV_SYSTEM_PYTHON=1
export UV_CACHE_DIR=~/.cache/uv

# Configurações do Jupyter
export JUPYTER_CONFIG_DIR=~/.jupyter
export JUPYTER_DATA_DIR=~/.local/share/jupyter

# Configurações do MLflow
export MLFLOW_TRACKING_URI="http://localhost:5000"
export MLFLOW_EXPERIMENT_NAME="petrobras-anomaly-detection"

# Configurações do TensorBoard
export TENSORBOARD_LOG_DIR="./logs/tensorboard"

# =============================================================================
# 🛢️ VARIÁVEIS DE AMBIENTE DO PROJETO PETROBRAS
# =============================================================================

# Configurações do projeto
export PROJECT_NAME="petrobras-offshore-wells-anomaly-detection"
export PROJECT_ROOT="$(pwd)"
export DATA_DIR="${PROJECT_ROOT}/data"
export MODELS_DIR="${PROJECT_ROOT}/models"
export NOTEBOOKS_DIR="${PROJECT_ROOT}/notebooks"
export SRC_DIR="${PROJECT_ROOT}/src"
export LOGS_DIR="${PROJECT_ROOT}/logs"
export CONFIG_DIR="${PROJECT_ROOT}/config"

# Configurações de dados
export RAW_DATA_DIR="${DATA_DIR}/raw"
export PROCESSED_DATA_DIR="${DATA_DIR}/processed"
export FEATURES_DATA_DIR="${DATA_DIR}/features"
export RESULTS_DATA_DIR="${DATA_DIR}/results"

# Configurações de modelos
export MODEL_BATCH_SIZE=32
export MODEL_LEARNING_RATE=0.001
export MODEL_EPOCHS=100
export MODEL_VALIDATION_SPLIT=0.2
export MODEL_PATIENCE=10

# Configurações de logging
export LOG_LEVEL="INFO"
export ENABLE_TENSORBOARD=true
export ENABLE_MLFLOW=true

# Configurações de GPU (se disponível)
export CUDA_VISIBLE_DEVICES=0
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512

# =============================================================================
# 🔧 ALIASES ESPECÍFICOS DO PROJETO
# =============================================================================

# Aliases para navegação do projeto
alias pj='cd ${PROJECT_ROOT}'
alias data='cd ${DATA_DIR}'
alias models='cd ${MODELS_DIR}'
alias notebooks='cd ${NOTEBOOKS_DIR}'
alias src='cd ${SRC_DIR}'
alias logs='cd ${LOGS_DIR}'
alias config='cd ${CONFIG_DIR}'

# Aliases para Python e desenvolvimento
alias py='python'
alias pip='uv pip'
alias uv-add='uv add'
alias uv-sync='uv sync'
alias uv-run='uv run'
alias uv-install='uv install'

# Aliases para Jupyter
alias jlab='jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root'
alias jnotebook='jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root'
alias jstop='jupyter notebook stop'

# Aliases para MLflow
alias mlflow-ui='mlflow ui --host 0.0.0.0 --port 5000'
alias mlflow-server='python mlflow_server.py'

# Aliases para TensorBoard
alias tensorboard='tensorboard --logdir=${TENSORBOARD_LOG_DIR} --host=0.0.0.0 --port=6006'

# Aliases para testes
alias test='pytest'
alias test-cov='pytest --cov=src --cov-report=html --cov-report=term'
alias test-fast='pytest -x -q'
alias test-verbose='pytest -v'

# Aliases para qualidade de código
alias lint='ruff check src/ tests/'
alias format='ruff format src/ tests/'
alias type-check='mypy src/'
alias security='bandit -r src/'

# Aliases para Git
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gp='git push'
alias gl='git log --oneline'
alias gd='git diff'
alias gb='git branch'
alias gco='git checkout'

# Aliases para Docker
alias dbuild='docker build -t ${PROJECT_NAME} .'
alias drun='docker run -it --rm -p 8888:8888 -p 5000:5000 ${PROJECT_NAME}'
alias dstop='docker stop $(docker ps -q)'
alias dclean='docker system prune -f'

# Aliases para limpeza
alias clean-pyc='find . -type f -name "*.pyc" -delete'
alias clean-cache='find . -type d -name "__pycache__" -exec rm -rf {} +'
alias clean-logs='rm -rf ${LOGS_DIR}/*'
alias clean-models='rm -rf ${MODELS_DIR}/*'

# =============================================================================
# 🚀 FUNÇÕES ÚTEIS
# =============================================================================

# Função para ativar ambiente virtual
activate_venv() {
    if [ -d ".venv" ]; then
        source .venv/bin/activate
        echo "✅ Ambiente virtual ativado"
    else
        echo "❌ Ambiente virtual não encontrado. Execute: uv venv"
    fi
}

# Função para criar ambiente virtual
create_venv() {
    echo "🔧 Criando ambiente virtual..."
    uv venv
    source .venv/bin/activate
    echo "📦 Instalando dependências..."
    uv sync
    echo "✅ Ambiente virtual criado e configurado!"
}

# Função para executar notebooks
run_notebook() {
    local notebook_name=$1
    if [ -z "$notebook_name" ]; then
        echo "📓 Iniciando Jupyter Lab..."
        jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root
    else
        echo "📓 Executando notebook: $notebook_name"
        jupyter nbconvert --execute --to notebook --inplace "$notebook_name"
    fi
}

# Função para treinar modelo
train_model() {
    local model_name=${1:-"default"}
    echo "🤖 Iniciando treinamento do modelo: $model_name"
    python src/train.py --model_name "$model_name"
}

# Função para avaliar modelo
evaluate_model() {
    local model_name=${1:-"default"}
    echo "📊 Avaliando modelo: $model_name"
    python src/evaluate.py --model_name "$model_name"
}

# Função para gerar relatório
generate_report() {
    echo "📈 Gerando relatório de análise..."
    python src/report.py
}

# Função para backup de dados
backup_data() {
    local backup_name="backup_$(date +%Y%m%d_%H%M%S)"
    echo "💾 Criando backup: $backup_name"
    tar -czf "${backup_name}.tar.gz" data/ models/ logs/
    echo "✅ Backup criado: ${backup_name}.tar.gz"
}

# Função para limpeza completa
clean_all() {
    echo "🧹 Limpando arquivos temporários..."
    clean-pyc
    clean-cache
    clean-logs
    echo "✅ Limpeza concluída!"
}

# Função para status do projeto
project_status() {
    echo "🛢️  STATUS DO PROJETO PETROBRAS"
    echo "================================"
    echo "📁 Diretório do projeto: ${PROJECT_ROOT}"
    echo "🐍 Python: $(python --version)"
    echo "📦 uv: $(uv --version)"
    echo "📊 Jupyter: $(jupyter --version 2>/dev/null || echo 'Não instalado')"
    echo "🤖 MLflow: $(mlflow --version 2>/dev/null || echo 'Não instalado')"
    echo ""
    echo "📂 Estrutura de diretórios:"
    echo "  📊 Dados: ${DATA_DIR}"
    echo "  🤖 Modelos: ${MODELS_DIR}"
    echo "  📓 Notebooks: ${NOTEBOOKS_DIR}"
    echo "  🔧 Código: ${SRC_DIR}"
    echo "  📝 Logs: ${LOGS_DIR}"
    echo ""
    echo "🌐 Serviços disponíveis:"
    echo "  📓 Jupyter Lab: http://localhost:8888"
    echo "  📊 MLflow UI: http://localhost:5000"
    echo "  📈 TensorBoard: http://localhost:6006"
}

# =============================================================================
# 🎯 PROMPT PERSONALIZADO
# =============================================================================

# Função para obter status do Git
git_status() {
    local branch=$(git branch 2>/dev/null | grep '^*' | sed 's/* //')
    if [ -n "$branch" ]; then
        local status=$(git status --porcelain 2>/dev/null)
        if [ -n "$status" ]; then
            echo " %F{red}($branch)%f"
        else
            echo " %F{green}($branch)%f"
        fi
    fi
}

# Função para obter status do ambiente virtual
venv_status() {
    if [ -n "$VIRTUAL_ENV" ]; then
        local venv_name=$(basename "$VIRTUAL_ENV")
        echo " %F{blue}[$venv_name]%f"
    fi
}

# Configuração do prompt
setopt PROMPT_SUBST
PROMPT='%F{cyan}🛢️ %F{yellow}%n%f@%F{green}%m%f %F{blue}%~%f$(git_status)$(venv_status)
%F{red}❯%f '

# =============================================================================
# 🔌 PLUGINS E EXTENSÕES
# =============================================================================

# Configuração do Oh My Zsh (se instalado)
if [ -d "$HOME/.oh-my-zsh" ]; then
    export ZSH="$HOME/.oh-my-zsh"
    ZSH_THEME="robbyrussell"
    plugins=(
        git
        python
        pip
        docker
        docker-compose
        jupyter
        conda-zsh-completion
    )
    source $ZSH/oh-my-zsh.sh
fi

# Configuração do zsh-autosuggestions (se instalado)
if [ -f "$HOME/.zsh/zsh-autosuggestions/zsh-autosuggestions.zsh" ]; then
    source "$HOME/.zsh/zsh-autosuggestions/zsh-autosuggestions.zsh"
fi

# Configuração do zsh-syntax-highlighting (se instalado)
if [ -f "$HOME/.zsh/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh" ]; then
    source "$HOME/.zsh/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh"
fi

# =============================================================================
# 🚀 INICIALIZAÇÃO
# =============================================================================

# Mensagem de boas-vindas
echo "🛢️  Bem-vindo ao projeto Petrobras Offshore Wells Anomaly Detection!"
echo "📊 Use 'project_status' para ver o status do projeto"
echo "🔧 Use 'create_venv' para configurar o ambiente virtual"
echo "📓 Use 'jlab' para iniciar o Jupyter Lab"
echo ""

# Ativar ambiente virtual se existir
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "✅ Ambiente virtual ativado automaticamente"
fi

# =============================================================================
# 📝 CONFIGURAÇÕES ADICIONAIS
# =============================================================================

# Configurações de segurança
umask 022

# Configurações de locale
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# Configurações de editor
export EDITOR='code'
export VISUAL='code'

# Configurações de pager
export PAGER='less'
export LESS='-R'

# Configurações de fzf (se instalado)
if command -v fzf &> /dev/null; then
    export FZF_DEFAULT_OPTS='--height 40% --layout=reverse --border'
    export FZF_DEFAULT_COMMAND='fd --type f --hidden --follow --exclude .git'
fi

# =============================================================================
# 🎉 FINALIZAÇÃO
# =============================================================================

# Carregar configurações locais se existirem
if [ -f "$HOME/.zshrc.local" ]; then
    source "$HOME/.zshrc.local"
fi

# Carregar configurações do projeto se existirem
if [ -f "${PROJECT_ROOT}/.zshrc.project" ]; then
    source "${PROJECT_ROOT}/.zshrc.project"
fi

echo "🎯 Configuração do ZSH carregada com sucesso!"
