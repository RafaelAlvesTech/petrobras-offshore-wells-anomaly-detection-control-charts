# Use the official Microsoft-maintained Python dev container image
# This image comes with Python, pip, and other common tools pre-installed.
FROM mcr.microsoft.com/devcontainers/python:1-3.11-bookworm

# Set environment variables to prevent interactive prompts during build
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1

# Install system dependencies, including zsh and other tools
RUN apt-get update && apt-get install -y \
    zsh \
    git \
    curl \
    wget \
    fzf \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    # The base image creates a non-root user 'vscode'. We'll use it.
# The user's home directory is /home/vscode.
USER vscode
WORKDIR /home/vscode/app

# Install user-specific tools
RUN curl --proto '=https' --tlsv1.2 -sSf https://setup.atuin.sh | sh && \
    curl -sS https://raw.githubusercontent.com/ajeetdsouza/zoxide/main/install.sh | bash && \
    pip install thefuck

# Install uv using pipx to ensure it's isolated and in the PATH
RUN pipx install uv

# Copy project dependency files
COPY --chown=vscode:vscode pyproject.toml uv.lock ./

# Add pipx bin to PATH and install dependencies
ENV PATH="/home/vscode/.local/bin:${PATH}"
RUN uv sync

# Install Oh My Zsh, Powerlevel10k, and other plugins for the vscode user
RUN rm -rf /home/vscode/.oh-my-zsh && \
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended \
    && git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/themes/powerlevel10k \
    && git clone https://github.com/Aloxaf/fzf-tab ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/fzf-tab \
    && git clone https://github.com/wfxr/forgit ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/forgit \
    && git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions \
    && git clone https://github.com/zsh-users/zsh-completions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-completions \
    && git clone https://github.com/MichaelAquilina/zsh-you-should-use ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/you-should-use \
    && git clone https://github.com/zdharma-continuum/fast-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/fast-syntax-highlighting


# The devcontainer.json will mount the local .zshrc and .p10k.zsh,
# so we don't need to configure them here in the image.

# Copy the rest of the application code
COPY --chown=vscode:vscode . .
