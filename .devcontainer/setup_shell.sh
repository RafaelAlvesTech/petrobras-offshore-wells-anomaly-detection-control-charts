#!/bin/bash
# 🛢️ Petrobras Offshore Wells Anomaly Detection - Shell Setup Script
# =================================================================

set -e

echo "🐚 Setting up Zsh configuration for Petrobras project..."

# =================================================================
# 📁 CREATE NECESSARY DIRECTORIES
# =================================================================

echo "📁 Creating configuration directories..."
mkdir -p ~/.oh-my-zsh/custom/plugins
mkdir -p ~/.config
mkdir -p ~/backups

# =================================================================
# 🔧 INSTALL OH MY ZSH (if not already installed)
# =================================================================

if [ ! -d "$HOME/.oh-my-zsh" ]; then
    echo "📦 Installing Oh My Zsh..."
    sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
else
    echo "✅ Oh My Zsh already installed"
fi

# =================================================================
# 🔌 INSTALL ZSH PLUGINS
# =================================================================

echo "🔌 Installing Zsh plugins..."

# zsh-autosuggestions
if [ ! -d "$HOME/.oh-my-zsh/custom/plugins/zsh-autosuggestions" ]; then
    echo "📥 Installing zsh-autosuggestions..."
    git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
else
    echo "✅ zsh-autosuggestions already installed"
fi

# zsh-syntax-highlighting
if [ ! -d "$HOME/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting" ]; then
    echo "📥 Installing zsh-syntax-highlighting..."
    git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
else
    echo "✅ zsh-syntax-highlighting already installed"
fi

# =================================================================
# 📝 COPY CONFIGURATION FILES
# =================================================================

echo "📝 Setting up configuration files..."

# Copy main .zshrc
if [ -f ".devcontainer/.zshrc" ]; then
    cp .devcontainer/.zshrc ~/.zshrc
    echo "✅ Main .zshrc configured"
else
    echo "❌ Main .zshrc not found"
fi

# Copy project-specific configuration
if [ -f ".devcontainer/.zshrc.project" ]; then
    cp .devcontainer/.zshrc.project ~/.zshrc.project
    echo "✅ Project configuration loaded"
else
    echo "❌ Project configuration not found"
fi

# Copy personal configuration template
if [ -f ".devcontainer/.zshrc.local.example" ]; then
    if [ ! -f ~/.zshrc.local ]; then
        cp .devcontainer/.zshrc.local.example ~/.zshrc.local.example
        echo "✅ Personal configuration template created"
        echo "💡 Edit ~/.zshrc.local.example and rename to ~/.zshrc.local to customize"
    else
        echo "✅ Personal configuration already exists"
    fi
else
    echo "❌ Personal configuration template not found"
fi

# =================================================================
# 🔐 SET PERMISSIONS
# =================================================================

echo "🔐 Setting file permissions..."
chmod 644 ~/.zshrc
chmod 644 ~/.zshrc.project
chmod 644 ~/.zshrc.local.example 2>/dev/null || true
chmod 644 ~/.zshrc.local 2>/dev/null || true

# =================================================================
# 🎨 CONFIGURE JUPYTER
# =================================================================

echo "🎨 Configuring Jupyter..."

# Create Jupyter config directory
mkdir -p ~/.jupyter

# Create Jupyter config
cat > ~/.jupyter/jupyter_lab_config.py << 'EOF'
# Jupyter Lab Configuration for Petrobras Project
c.ServerApp.ip = '0.0.0.0'
c.ServerApp.port = 8888
c.ServerApp.open_browser = False
c.ServerApp.allow_root = True
c.ServerApp.token = ''
c.ServerApp.password = ''
c.ServerApp.disable_check_xsrf = True
c.ServerApp.allow_origin = '*'
c.ServerApp.allow_credentials = True
c.ServerApp.tornado_settings = {
    'headers': {
        'Content-Security-Policy': "frame-ancestors * 'self'"
    }
}
EOF

echo "✅ Jupyter configuration created"

# =================================================================
# 🐍 SET UP PYTHON ENVIRONMENT
# =================================================================

echo "🐍 Setting up Python environment..."

# Create project directories
mkdir -p data/raw data/processed data/external
mkdir -p models
mkdir -p notebooks/experiments
mkdir -p src
mkdir -p tests
mkdir -p logs
mkdir -p config

echo "✅ Project directories created"

# =================================================================
# 🔧 CONFIGURE GIT
# =================================================================

echo "🔧 Configuring Git..."

# Set up git aliases
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.visual '!gitk'

# Disable GPG signing by default
git config --global commit.gpgsign false

echo "✅ Git configuration updated"

# =================================================================
# 🎯 SET SHELL TO ZSH
# =================================================================

echo "🎯 Setting Zsh as default shell..."

# Check if zsh is available
if command -v zsh >/dev/null 2>&1; then
    # Set zsh as default shell (only if not already set)
    if [ "$SHELL" != "$(which zsh)" ]; then
        echo "⚠️  To set Zsh as default shell, run: chsh -s $(which zsh)"
        echo "   Then restart your terminal or run: exec zsh"
    else
        echo "✅ Zsh is already the default shell"
    fi
else
    echo "❌ Zsh not found, please install it first"
fi

# =================================================================
# 🎉 COMPLETION MESSAGE
# =================================================================

echo ""
echo "🎉 Zsh configuration completed!"
echo ""
echo "📋 Next steps:"
echo "   1. Restart your terminal or run: exec zsh"
echo "   2. Customize personal settings: nano ~/.zshrc.local.example"
echo "   3. Rename personal config: mv ~/.zshrc.local.example ~/.zshrc.local"
echo "   4. Test configuration: source ~/.zshrc"
echo ""
echo "🎯 Available commands:"
echo "   - project_status    : Show project status"
echo "   - project_help      : Show project help"
echo "   - dev_start         : Start development environment"
echo "   - my_help           : Show personal commands (after setup)"
echo ""
echo "🛢️  Welcome to Petrobras Offshore Wells Anomaly Detection!"
echo ""

# =================================================================
# 🧪 TEST CONFIGURATION
# =================================================================

echo "🧪 Testing configuration..."

# Test if zsh can load the configuration
if zsh -c "source ~/.zshrc && echo '✅ Zsh configuration test passed'" 2>/dev/null; then
    echo "✅ Configuration test successful"
else
    echo "⚠️  Configuration test failed, but setup completed"
    echo "   Try running: source ~/.zshrc"
fi

echo ""
echo "🚀 Setup complete! Enjoy your enhanced development environment!"
