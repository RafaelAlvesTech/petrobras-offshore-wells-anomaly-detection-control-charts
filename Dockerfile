FROM python:3.11-slim AS base

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on

# Instale dependências de sistema para ciência de dados e zsh
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl zsh git wget fonts-powerline default-jre

# Instale o uv (instalador oficial)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Prepare ambiente e usuário
RUN useradd -ms /bin/bash python
USER python
WORKDIR /home/python/app

# Copie apenas arquivos de dependências (build cache eficiente)
COPY --chown=python:python pyproject.toml .
# Se disponível (e recomendado p/ reprodutibilidade):
# COPY --chown=python:python uv.lock .

# Opcional — índices extras do torch
# ENV PIP_EXTRA_INDEX_URL https://download.pytorch.org/whl/cu117

# Instale dependências do projeto (prod e dev)
RUN uv pip install -r pyproject.toml --dev

# Copie o resto do código do projeto
COPY --chown=python:python . .

# (Opcional) ZSH personalizado e powerlevel10k
RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.2/zsh-in-docker.sh)" -- \
    -t https://github.com/romkatv/powerlevel10k \
    -p git \
    -p https://github.com/zsh-users/zsh-autosuggestions \
    -p https://github.com/zsh-users/zsh-completions \
    -a 'export TERM=xterm-256color'

# Entrada do container: Jupyter Notebook (ajuste para o que preferir)
CMD ["python", "-m", "jupyter", "notebook", "--ip=0.0.0.0", "--allow-root"]
