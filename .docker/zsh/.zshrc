# Petrobras Offshore Wells Anomaly Detection - Zsh Configuration
# This file is mounted into the container for persistent shell configuration

# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

# History configuration
HISTFILE=/home/python/zsh/.zsh_history
HISTSIZE=10000
SAVEHIST=10000
setopt SHARE_HISTORY
setopt HIST_IGNORE_DUPS
setopt HIST_IGNORE_ALL_DUPS
setopt HIST_REDUCE_BLANKS
setopt HIST_SAVE_NO_DUPS

# Load Powerlevel10k theme
if [[ -f ~/.p10k.zsh ]]; then
    source ~/.p10k.zsh
fi

# Petrobras project specific aliases
alias ll='ls -la'
alias la='ls -A'
alias l='ls -CF'
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'

# Python and development aliases
alias py='python'
alias pip='uv pip'
alias jupyter='jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root'
alias mlflow='mlflow server --host 0.0.0.0 --port 5000 --backend-store-uri sqlite:///mlflow.db'

# Project specific aliases
alias petrobras='cd /home/python/app'
alias data='cd /home/python/app/data'
alias notebooks='cd /home/python/app/notebooks'
alias src='cd /home/python/app/src'

# Git aliases
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gp='git push'
alias gl='git log --oneline'

# Docker aliases
alias dc='docker compose'
alias dcu='docker compose up'
alias dcd='docker compose down'
alias dcb='docker compose build'

# Environment variables
export PYTHONPATH="/home/python/app/src:$PYTHONPATH"
export TERM="xterm-256color"
export SHELL="/bin/zsh"

# Welcome message
echo "🛢️  Petrobras Offshore Wells Anomaly Detection Environment"
echo "================================================================"
echo "Available commands:"
echo "  - jupyter: Start Jupyter Lab"
echo "  - mlflow:  Start MLflow server"
echo "  - petrobras: Go to project root"
echo "  - data: Go to data directory"
echo "  - notebooks: Go to notebooks directory"
echo "================================================================"
