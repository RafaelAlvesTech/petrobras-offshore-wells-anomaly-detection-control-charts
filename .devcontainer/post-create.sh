#!/bin/bash
set -e

echo "🚀 Setting up Petrobras Offshore Wells Anomaly Detection environment..."

# Install Oh My Zsh and plugins
if [ ! -d "$HOME/.oh-my-zsh" ]; then
    echo "🐚 Setting up Oh My Zsh..."
    sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
    git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
    git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
    git clone https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/themes/powerlevel10k
fi

# Copy the custom zsh configuration
cp -f .devcontainer/zshrc ~/.zshrc.custom

# Append custom configuration to zshrc
if ! grep -q "source ~/.zshrc.custom" ~/.zshrc; then
    echo 'source ~/.zshrc.custom' >> ~/.zshrc
fi

# Install project dependencies using uv
echo "📚 Installing project dependencies..."
if [ -f "pyproject.toml" ]; then
    uv sync
fi

# Install pre-commit hooks
echo "🔧 Installing pre-commit hooks..."
pre-commit install

# Configure git to disable GPG signing
echo "🔐 Configuring git..."
git config commit.gpgsign false

# Create necessary project directories
echo "📁 Creating project directories..."
mkdir -p data/raw data/processed models notebooks/experiments logs

# Set up Jupyter kernel
echo "🔬 Setting up Jupyter kernel..."
python3 -m ipykernel install --user --name=petrobras-anomaly --display-name="Petrobras Anomaly Detection"

# Configure Jupyter
echo "🔧 Configuring Jupyter..."
mkdir -p ~/.jupyter
cat > ~/.jupyter/jupyter_server_config.py << EOF
c.ServerApp.ip = '0.0.0.0'
c.ServerApp.port = 8888
c.ServerApp.open_browser = False
c.ServerApp.allow_root = True
c.ServerApp.token = ''
c.ServerApp.password = ''
c.ServerApp.allow_origin = '*'
c.ServerApp.disable_check_xsrf = True
EOF

echo "✅ Environment setup complete!"
echo ""
echo "🎯 To apply changes, please restart your terminal."
