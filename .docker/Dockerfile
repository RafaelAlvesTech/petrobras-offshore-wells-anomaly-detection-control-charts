# Use Python 3.11 slim image with latest security updates
FROM python:3.11.7-slim-bookworm

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV TERM=xterm-256color
ENV SHELL=/bin/zsh

# Install system dependencies and security updates
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    curl \
    wget \
    git \
    zsh \
    vim \
    nano \
    build-essential \
    software-properties-common \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/* \
    && rm -rf /var/tmp/*

# Install uv for Python package management as root
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Create app directory and set as working directory
RUN mkdir -p /home/python/app
WORKDIR /home/python/app

# Copy requirements and install Python dependencies as root
COPY requirements.txt .
RUN /root/.local/bin/uv pip install --system -r requirements.txt

# Create user with home directory and set permissions
RUN useradd -m -s /bin/zsh python && \
    usermod -aG sudo python && \
    echo "python ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    chown -R python:python /home/python

# Switch to python user
USER python
WORKDIR /home/python

# Install zsh-in-docker with Powerlevel10k and plugins
RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.2/zsh-in-docker.sh)" -- \
    -t https://github.com/romkatv/powerlevel10k \
    -p git \
    -p git-flow \
    -p https://github.com/zdharma-continuum/fast-syntax-highlighting \
    -p https://github.com/zsh-users/zsh-autosuggestions \
    -p https://github.com/zsh-users/zsh-completions \
    -a 'export TERM=xterm-256color'

# Configure zsh history and additional settings
RUN echo '[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh' >> ~/.zshrc && \
    echo 'HISTFILE=/home/python/zsh/.zsh_history' >> ~/.zshrc && \
    echo 'HISTSIZE=10000' >> ~/.zshrc && \
    echo 'SAVEHIST=10000' >> ~/.zshrc && \
    echo 'setopt SHARE_HISTORY' >> ~/.zshrc && \
    echo 'setopt HIST_IGNORE_DUPS' >> ~/.zshrc && \
    echo 'setopt HIST_IGNORE_ALL_DUPS' >> ~/.zshrc && \
    echo 'setopt HIST_REDUCE_BLANKS' >> ~/.zshrc && \
    echo 'setopt HIST_SAVE_NO_DUPS' >> ~/.zshrc

# Create zsh history directory
RUN mkdir -p /home/python/zsh

# Add uv to PATH for the python user
ENV PATH="/home/python/.local/bin:$PATH"
RUN echo 'export PATH="/home/python/.local/bin:$PATH"' >> ~/.zshrc && \
    echo 'export PATH="/home/python/.local/bin:$PATH"' >> ~/.bashrc

# Set working directory to app
WORKDIR /home/python/app

# Copy the rest of the application
COPY --chown=python:python . .

# Make start script executable
RUN chmod +x ./.docker/start-app.sh

# Expose port
EXPOSE 8000

# Set default command
CMD ["./.docker/start-app.sh", "api"]
