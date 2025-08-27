# Base Python moderna e leve
FROM python:3.11-slim-bullseye

# Ambiente
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on

# Pacotes base, incluindo zsh e utilitários
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates git zsh wget tini locales \
    fonts-powerline procps nano less \
    && apt-get upgrade -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Locale (evita problemas com acentos)
RUN sed -i '/pt_BR.UTF-8/s/^# //g' /etc/locale.gen || true && \
    sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen || true && \
    locale-gen || true
ENV LANG=pt_BR.UTF-8 LC_ALL=pt_BR.UTF-8

# Diretório de trabalho
WORKDIR /app

# Instalar uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:${PATH}"

# Criar usuário não-root
RUN useradd -ms /bin/zsh python && chown -R python:python /app

# Instalar Oh My Zsh + plugins (como root, mas para o user python)
# Clonamos no HOME do usuário e ajustamos permissões
USER python
ENV HOME=/home/python
WORKDIR /home/python

# Oh My Zsh e plugins
RUN git clone --depth=1 https://github.com/ohmyzsh/ohmyzsh.git ${HOME}/.oh-my-zsh && \
    git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${HOME}/.oh-my-zsh/custom/themes/powerlevel10k && \
    git clone --depth=1 https://github.com/zsh-users/zsh-autosuggestions ${HOME}/.oh-my-zsh/custom/plugins/zsh-autosuggestions && \
    git clone --depth=1 https://github.com/zsh-users/zsh-completions ${HOME}/.oh-my-zsh/custom/plugins/zsh-completions && \
    git clone --depth=1 https://github.com/zdharma-continuum/fast-syntax-highlighting ${HOME}/.oh-my-zsh/custom/plugins/fast-syntax-highlighting

# .zshrc com personalizações úteis para dev em Python/Jupyter
# - tema powerlevel10k
# - plugins: git, zsh-autosuggestions, zsh-completions, fast-syntax-highlighting
# - PATH e aliases comuns
# - export de variáveis úteis
RUN cat > ${HOME}/.zshrc <<'ZSHRC'
export LANG=pt_BR.UTF-8
export LC_ALL=pt_BR.UTF-8

export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="powerlevel10k/powerlevel10k"
plugins=(git zsh-autosuggestions zsh-completions fast-syntax-highlighting)

source $ZSH/oh-my-zsh.sh

# Hist e cores
export HISTFILE=$HOME/.zsh_history
export HISTSIZE=50000
export SAVEHIST=50000
setopt HIST_IGNORE_ALL_DUPS
autoload -U colors && colors

# Python/uv paths
export PATH="$HOME/.local/bin:$PATH"

# Prompt extra leve se powerlevel10k indisponível
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

# Compleções adicionais
fpath+=($HOME/.oh-my-zsh/custom/plugins/zsh-completions/src)

# Aliases úteis
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias gst='git status'
alias gp='git pull'
alias gd='git diff'

# Jupyter helpers
alias jl='jupyter lab --ip=0.0.0.0 --port=8888 --no-browser'
alias jn='jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser'

# Detecta container e mostra no prompt (via var, se quiser usar em PS1)
export IN_DOCKER=1
ZSHRC

# Garantir shell padrão zsh para o usuário (redundante por useradd -s /bin/zsh, mas explícito)
USER root
RUN chsh -s /bin/zsh python

# Voltar ao usuário
USER python
WORKDIR /app

# Dependências do projeto
COPY --chown=python:python requirements.txt /app/requirements.txt
RUN uv pip install --user -r /app/requirements.txt

# Garantir jupyter/ipykernel caso não estejam no requirements
RUN uv pip install --user jupyter ipykernel

# Copiar código
COPY --chown=python:python . /app

# Expor Jupyter
EXPOSE 8888

# tini como init para sinais limpos; iniciar Jupyter Notebook por padrão
USER python
ENTRYPOINT ["/usr/bin/tini","--"]
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser"]
