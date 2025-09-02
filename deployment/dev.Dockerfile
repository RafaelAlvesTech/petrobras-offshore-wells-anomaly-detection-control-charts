
# Use a modern and lightweight Python base image
FROM python:3.11-slim-bullseye

# Set environment variables for a streamlined and efficient build process
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies, including zsh and other development tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    git \
    zsh \
    wget \
    tini \
    locales \
    fonts-powerline \
    && sed -i '/pt_BR.UTF-8/s/^# //g' /etc/locale.gen \
    && locale-gen \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set locale to avoid issues with character encoding
ENV LANG=pt_BR.UTF-8 \
    LC_ALL=pt_BR.UTF-8

# Set the working directory
WORKDIR /app

# Install uv for fast Python package management
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:${PATH}"

# Create a non-root user for better security
RUN useradd -ms /bin/zsh python && chown -R python:python /app

# Switch to the non-root user
USER python
ENV HOME=/home/python
WORKDIR /home/python

# Install Oh My Zsh and essential plugins
RUN git clone --depth=1 https://github.com/ohmyzsh/ohmyzsh.git ${HOME}/.oh-my-zsh && \
    git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${HOME}/.oh-my-zsh/custom/themes/powerlevel10k && \
    git clone --depth=1 https://github.com/zsh-users/zsh-autosuggestions ${HOME}/.oh-my-zsh/custom/plugins/zsh-autosuggestions && \
    git clone --depth=1 https://github.com/zdharma-continuum/fast-syntax-highlighting ${HOME}/.oh-my-zsh/custom/plugins/fast-syntax-highlighting

# Configure zsh with a custom .zshrc file
COPY .devcontainer/zshrc ${HOME}/.zshrc

# Switch back to the root user to set the default shell for the python user
USER root
RUN chsh -s /bin/zsh python

# Switch back to the non-root user
USER python
WORKDIR /app

# Install project dependencies
COPY --chown=python:python pyproject.toml uv.lock* /app/
RUN uv sync --system

# Copy the project code
COPY --chown=python:python . /app

# Expose the Jupyter port
EXPOSE 8888

# Use tini as the entrypoint to properly handle signals
ENTRYPOINT ["/usr/bin/tini", "--"]

# Start the Jupyter Lab server by default
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser"]
