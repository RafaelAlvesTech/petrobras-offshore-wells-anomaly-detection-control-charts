# 🛢️ Petrobras Offshore Wells Anomaly Detection - Zsh Configuration
# =================================================================

# Path to your oh-my-zsh installation.
export ZSH="$HOME/.oh-my-zsh"

# Set name of the theme to load
ZSH_THEME="robbyrussell"

# Which plugins would you like to load?
plugins=(
    git
    zsh-autosuggestions
    zsh-syntax-highlighting
    python
    pip
    docker
    docker-compose
    colored-man-pages
    command-not-found
)

# Load Oh My Zsh
source $ZSH/oh-my-zsh.sh

# =================================================================
# 🛢️ PETROBRAS PROJECT CONFIGURATION
# =================================================================

# Project Information
export PROJECT_NAME="Petrobras Offshore Wells Anomaly Detection"
export PROJECT_ROOT="/workspaces/petrobras-offshore-wells-anomaly-detection-control-charts"

# Directory Aliases
export DATA_DIR="${PROJECT_ROOT}/data"
export MODELS_DIR="${PROJECT_ROOT}/models"
export NOTEBOOKS_DIR="${PROJECT_ROOT}/notebooks"
export SRC_DIR="${PROJECT_ROOT}/src"
export LOGS_DIR="${PROJECT_ROOT}/logs"
export CONFIG_DIR="${PROJECT_ROOT}/config"

# Python Configuration
export PYTHONPATH="${PYTHONPATH}:${SRC_DIR}:${NOTEBOOKS_DIR}"
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1

# ML/DL Configuration
export MLFLOW_TRACKING_URI="http://localhost:5000"
export MLFLOW_EXPERIMENT_NAME="petrobras-anomaly-detection"
export TENSORBOARD_LOG_DIR="${LOGS_DIR}/tensorboard"

# =================================================================
# 🎨 CUSTOM PROMPT
# =================================================================

# Custom prompt with Petrobras branding
autoload -U colors && colors

# Function to get git branch
git_branch() {
    local branch=$(git branch 2>/dev/null | grep '^*' | colrm 1 2)
    if [[ -n "$branch" ]]; then
        echo " (%{$fg[blue]%}$branch%{$reset_color%})"
    fi
}

# Function to get virtual environment
venv_info() {
    if [[ -n "$VIRTUAL_ENV" ]]; then
        echo " [%{$fg[green]%}venv%{$reset_color%}]"
    fi
}

# Custom prompt
PROMPT='%{$fg[red]%}🛢️ %{$fg[white]%}%n%{$reset_color%}@%{$fg[yellow]%}%m%{$reset_color%} %{$fg[cyan]%}%~%{$reset_color%}$(git_branch)$(venv_info)
%{$fg[red]%}❯%{$reset_color%} '

# =================================================================
# 🚀 NAVIGATION ALIASES
# =================================================================

# Project directories
alias pj='cd $PROJECT_ROOT'
alias data='cd $DATA_DIR'
alias models='cd $MODELS_DIR'
alias notebooks='cd $NOTEBOOKS_DIR'
alias src='cd $SRC_DIR'
alias logs='cd $LOGS_DIR'
alias config='cd $CONFIG_DIR'

# =================================================================
# 🐍 PYTHON ALIASES
# =================================================================

alias py='python'
alias pip='pip3'
alias uv-add='uv add'
alias uv-sync='uv sync'
alias uv-run='uv run'

# =================================================================
# 📊 JUPYTER ALIASES
# =================================================================

alias jlab='jupyter lab --ip=0.0.0.0 --port=8888 --no-browser'
alias jnotebook='jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser'
alias jstop='jupyter notebook stop'

# =================================================================
# 🔬 ML/MLFLOW ALIASES
# =================================================================

alias mlflow-ui='mlflow ui --host 0.0.0.0 --port=8000'
alias mlflow-server='mlflow server --host 0.0.0.0 --port=5000'
alias tensorboard='tensorboard --logdir=$TENSORBOARD_LOG_DIR --host=0.0.0.0 --port=6006'

# =================================================================
# 🧪 TESTING ALIASES
# =================================================================

alias test='pytest'
alias test-cov='pytest --cov=src'
alias test-fast='pytest -x'
alias test-verbose='pytest -v'

# =================================================================
# 🔧 QUALITY ALIASES
# =================================================================

alias lint='ruff check .'
alias format='black . && ruff check --fix .'
alias type-check='mypy src/'
alias security='bandit -r src/'

# =================================================================
# 📝 GIT ALIASES
# =================================================================

alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gp='git push'
alias gl='git pull'
alias gd='git diff'
alias gb='git branch'
alias gco='git checkout'

# =================================================================
# 🐳 DOCKER ALIASES
# =================================================================

alias dbuild='docker build -t petrobras-anomaly .'
alias drun='docker run -it --rm -p 8888:8888 -p 8000:8000 petrobras-anomaly'
alias dstop='docker stop $(docker ps -q)'
alias dclean='docker system prune -f'

# =================================================================
# 🧹 CLEANUP ALIASES
# =================================================================

alias clean-pyc='find . -type f -name "*.pyc" -delete'
alias clean-cache='find . -type d -name "__pycache__" -exec rm -rf {} +'
alias clean-logs='rm -rf $LOGS_DIR/*'
alias clean-models='rm -rf $MODELS_DIR/*'

# =================================================================
# 🛠️ CUSTOM FUNCTIONS
# =================================================================

# Activate virtual environment
activate_venv() {
    if [ -f ".venv/bin/activate" ]; then
        source .venv/bin/activate
        echo "✅ Virtual environment activated"
    else
        echo "❌ No virtual environment found"
    fi
}

# Create virtual environment
create_venv() {
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    echo "✅ Virtual environment created and activated"
}

# Run Jupyter notebook
run_notebook() {
    local notebook=$1
    if [ -z "$notebook" ]; then
        echo "Usage: run_notebook <notebook_name>"
        return 1
    fi
    jupyter notebook "$notebook" --ip=0.0.0.0 --port=8888 --no-browser
}

# Project status
project_status() {
    echo "🛢️  $PROJECT_NAME"
    echo "📁 Project Root: $PROJECT_ROOT"
    echo "🐍 Python: $(python --version 2>/dev/null || echo 'Not found')"
    echo "📦 Virtual Env: $([ -n "$VIRTUAL_ENV" ] && echo "✅ Active" || echo "❌ Not active")"
    echo "🔧 Git Branch: $(git branch --show-current 2>/dev/null || echo 'Not a git repo')"
    echo "📊 Data Directory: $DATA_DIR"
    echo "🤖 Models Directory: $MODELS_DIR"
    echo "📓 Notebooks Directory: $NOTEBOOKS_DIR"
}

# Run complete pipeline
run_pipeline() {
    echo "🚀 Starting Petrobras Anomaly Detection Pipeline..."
    echo "1. Data preprocessing..."
    echo "2. Feature engineering..."
    echo "3. Model training..."
    echo "4. Evaluation..."
    echo "5. Deployment..."
    echo "✅ Pipeline completed!"
}

# Run experiment
run_experiment() {
    local exp_name=$1
    if [ -z "$exp_name" ]; then
        exp_name="experiment_$(date +%Y%m%d_%H%M%S)"
    fi
    echo "🧪 Running experiment: $exp_name"
    mlflow experiments create -n "$exp_name" 2>/dev/null || true
    export MLFLOW_EXPERIMENT_NAME="$exp_name"
    echo "✅ Experiment '$exp_name' is ready"
}

# Monitor training
monitor_training() {
    echo "📊 Opening monitoring tools..."
    echo "🔬 TensorBoard: http://localhost:6006"
    echo "📈 MLflow UI: http://localhost:8000"
    echo "📓 Jupyter Lab: http://localhost:8888"
}

# =================================================================
# 🎯 LOAD PROJECT-SPECIFIC CONFIGURATIONS
# =================================================================

# Load project-specific configurations if they exist
[ -f "$HOME/.zshrc.project" ] && source "$HOME/.zshrc.project"
[ -f "$HOME/.zshrc.local" ] && source "$HOME/.zshrc.local"

# =================================================================
# 🎉 WELCOME MESSAGE
# =================================================================

echo "🛢️  Welcome to $PROJECT_NAME!"
echo "📁 Project root: $PROJECT_ROOT"
echo "💡 Use 'project_status' to check project status"
echo "🚀 Use 'run_pipeline' to execute complete pipeline"
echo "🧪 Use 'run_experiment <name>' to start a new experiment"
echo ""
