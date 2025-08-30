#!/bin/bash

# Setup script for devcontainer shell environment
# This script runs during container creation to configure the shell

set -e

echo "🚀 Setting up shell environment for Petrobras Offshore Wells project..."

# Ensure we're in the right directory
cd /workspaces/petrobras-offshore-wells-anomaly-detection-control-charts

# Copy the main zsh configuration
if [ -f ".devcontainer/zshrc" ]; then
    echo "📝 Installing main zsh configuration..."
    cp .devcontainer/zshrc /home/vscode/.zshrc
    chown vscode:vscode /home/vscode/.zshrc
fi

# Copy the project-specific zsh configuration
if [ -f ".devcontainer/zshrc.project" ]; then
    echo "📝 Installing project-specific zsh configuration..."
    cp .devcontainer/zshrc.project /home/vscode/.zshrc.project
    chown vscode:vscode /home/vscode/.zshrc.project
fi

# Copy the local zsh configuration example
if [ -f ".devcontainer/zshrc.local.example" ]; then
    echo "📝 Installing local zsh configuration example..."
    cp .devcontainer/zshrc.local.example /home/vscode/.zshrc.local.example
    chown vscode:vscode /home/vscode/.zshrc.local.example
fi

# Install additional zsh plugins if not present
echo "📦 Installing zsh plugins..."
if [ ! -d "/home/vscode/.oh-my-zsh/custom/plugins/zsh-autosuggestions" ]; then
    echo "  - Installing zsh-autosuggestions plugin..."
    git clone --depth=1 https://github.com/zsh-users/zsh-autosuggestions /home/vscode/.oh-my-zsh/custom/plugins/zsh-autosuggestions
fi

if [ ! -d "/home/vscode/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting" ]; then
    echo "  - Installing zsh-syntax-highlighting plugin..."
    git clone --depth=1 https://github.com/zsh-users/zsh-syntax-highlighting /home/vscode/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting
fi

# The main zshrc already includes the project configuration
echo "🔧 Main zshrc configuration is complete"

# Set proper permissions
chown -R vscode:vscode /home/vscode/.oh-my-zsh
chown -R vscode:vscode /home/vscode/.zshrc

# Create Jupyter configuration directory
mkdir -p /home/vscode/.jupyter
cat > /home/vscode/.jupyter/jupyter_notebook_config.py << 'EOF'
# Jupyter Notebook Configuration
c = get_config()

# Allow connections from any IP
c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.port = 8888
c.NotebookApp.open_browser = False
c.NotebookApp.allow_root = True

# Security settings
c.NotebookApp.token = ''
c.NotebookApp.password = ''

# Working directory
c.NotebookApp.notebook_dir = '/workspaces/petrobras-offshore-wells-anomaly-detection-control-charts/notebooks'
EOF

chown -R vscode:vscode /home/vscode/.jupyter

# Create a simple test script to verify the setup
cat > /home/vscode/test_setup.sh << 'EOF'
#!/bin/bash
echo "🧪 Testing Petrobras environment setup..."
echo "Python version: $(python3 --version)"
echo "Pip version: $(pip3 --version)"
echo "Git version: $(git --version)"
echo "Docker version: $(docker --version)"
echo "Current user: $(whoami)"
echo "Home directory: $HOME"
echo "Project directory: /workspaces/petrobras-offshore-wells-anomaly-detection-control-charts"
echo "✅ Basic environment test complete!"
EOF

chmod +x /home/vscode/test_setup.sh
chown vscode:vscode /home/vscode/test_setup.sh

echo "✅ Shell environment setup complete!"
echo ""
echo "🎯 Next steps:"
echo "   1. Restart your terminal or run 'source ~/.zshrc' to apply changes"
echo "   2. Optional: Copy ~/.zshrc.local.example to ~/.zshrc.local and personalize"
echo "   3. Test the setup by running '~/.test_setup.sh'"
echo ""
echo "🐚 Zsh Configuration Features:"
echo "   - Custom prompt with Petrobras branding 🛢️"
echo "   - Project-specific aliases and functions"
echo "   - Enhanced development experience"
echo "   - Use 'project_status' to check project status"
echo "   - Use 'run_pipeline' to execute complete pipeline"
echo "   - Use 'run_experiment <name>' to run specific experiments"
echo ""
