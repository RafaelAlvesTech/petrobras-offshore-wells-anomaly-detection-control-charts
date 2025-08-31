# Use the official Python 3.11 devcontainer image as a base
FROM mcr.microsoft.com/devcontainers/python:3.11

# Set environment variables to streamline Python and pip behavior
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive \
    UV_CACHE_DIR=~/.cache/uv \
    JUPYTER_CONFIG_DIR=~/.jupyter \
    JUPYTER_DATA_DIR=~/.local/share/jupyter

# Install essential system dependencies and development tools in a single layer
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    vim \
    nano \
    htop \
    tree \
    jq \
    unzip \
    wget \
    ca-certificates \
    zsh \
    fonts-powerline \
    fonts-firacode \
    software-properties-common \
    apt-transport-https \
    gnupg \
    lsb-release \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast Python package management
RUN pip install uv

# Switch to the vscode user to ensure proper permissions
USER vscode

# Set the working directory for the project
WORKDIR /workspaces/petrobras-offshore-wells-anomaly-detection-control-charts

# Create necessary directories for local user
RUN mkdir -p ~/.local/bin ~/.cache/uv ~/.jupyter ~/.local/share/jupyter

# Set up the shell environment with a comprehensive configuration
RUN echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc && \
    echo 'export PYTHONPATH="/workspaces/petrobras-offshore-wells-anomaly-detection-control-charts/src:$PYTHONPATH"' >> ~/.zshrc

# Expose ports for various services
EXPOSE 8888 8000 5000 6006 8080 3000

# Set the default command to zsh
CMD ["/bin/zsh"]
