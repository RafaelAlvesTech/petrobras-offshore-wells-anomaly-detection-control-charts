# Enables Powerlevel10k instant prompt. Should stay at the top of ~/.zshrc.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

# Add user's local binaries to PATH
export PATH="$HOME/.local/bin:$PATH"

# Source Oh My Zsh if it exists
if [ -f ~/.oh-my-zsh/oh-my-zsh.sh ]; then
    source ~/.oh-my-zsh/oh-my-zsh.sh
fi

# Zsh plugins and theme configuration from zsh-in-docker
ZSH_THEME="powerlevel10k/powerlevel10k"
plugins=(
    git
    git-flow
    sudo
    fzf-tab
    forgit
    zsh-autosuggestions
    zsh-completions
    you-should-use
    fast-syntax-highlighting
)
source $ZSH/oh-my-zsh.sh

# -- Tool Initializations --

# Atuin - Magical Shell History
eval "$(atuin init zsh)"

# Zoxide - A smarter cd command
eval "$(zoxide init zsh)"

# The Fuck - Corrects your previous console command
eval "$(thefuck --alias)"


# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

# History configuration
HISTFILE=/home/python/zsh/.zsh_history
HISTSIZE=10000
SAVEHIST=10000
setopt SHARE_HISTORY
setopt HIST_IGNORE_DUPS
setopt HIST_IGNORE_ALL_DUPS
setopt HIST_REDUCE_BLANKS
setopt HIST_SAVE_NO_DUPS

# Set TERM for color support
export TERM=xterm-256color

# Activate the virtual environment
source /home/vscode/app/.venv/bin/activate
