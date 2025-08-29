#!/bin/bash

# Test script for Petrobras devcontainer environment
# Run this to verify everything is working correctly

set -e

echo "🧪 Testing Petrobras DevContainer Environment"
echo "============================================="
echo ""

# Test 1: Basic system tools
echo "1️⃣ Testing basic system tools..."
echo "   Python: $(python3 --version)"
echo "   Pip: $(pip3 --version)"
echo "   Git: $(git --version)"
echo "   Docker: $(docker --version)"
echo "   Current user: $(whoami)"
echo "   Home directory: $HOME"
echo ""

# Test 2: Project structure
echo "2️⃣ Testing project structure..."
PROJECT_ROOT="/workspaces/petrobras-offshore-wells-anomaly-detection-control-charts"
if [ -d "$PROJECT_ROOT" ]; then
    echo "   ✅ Project root exists: $PROJECT_ROOT"
    echo "   📁 Source directory: $(ls -la $PROJECT_ROOT/src 2>/dev/null | wc -l) files"
    echo "   📚 Notebooks directory: $(ls -la $PROJECT_ROOT/notebooks 2>/dev/null | wc -l) files"
    echo "   📊 Data directory: $(ls -la $PROJECT_ROOT/data 2>/dev/null | wc -l) files"
else
    echo "   ❌ Project root not found: $PROJECT_ROOT"
fi
echo ""

# Test 3: Python environment
echo "3️⃣ Testing Python environment..."
if command -v python3 &> /dev/null; then
    echo "   ✅ Python3 is available"
    echo "   🐍 Python path: $(which python3)"
    echo "   📦 Python packages: $(pip3 list | wc -l) installed"
else
    echo "   ❌ Python3 not found"
fi
echo ""

# Test 4: Shell configuration
echo "4️⃣ Testing shell configuration..."
if [ -f "$HOME/.zshrc.project" ]; then
    echo "   ✅ Project zshrc found"
    echo "   🔧 Source line in main zshrc: $(grep -c 'zshrc.project' $HOME/.zshrc || echo '0')"
else
    echo "   ❌ Project zshrc not found"
fi

if [ -d "$HOME/.oh-my-zsh" ]; then
    echo "   ✅ Oh My Zsh installed"
    echo "   📦 Custom plugins: $(ls -la $HOME/.oh-my-zsh/custom/plugins/ 2>/dev/null | wc -l) plugins"
else
    echo "   ❌ Oh My Zsh not found"
fi
echo ""

# Test 5: Jupyter configuration
echo "5️⃣ Testing Jupyter configuration..."
if [ -d "$HOME/.jupyter" ]; then
    echo "   ✅ Jupyter config directory exists"
    if [ -f "$HOME/.jupyter/jupyter_notebook_config.py" ]; then
        echo "   ✅ Jupyter config file exists"
    else
        echo "   ❌ Jupyter config file missing"
    fi
else
    echo "   ❌ Jupyter config directory missing"
fi
echo ""

# Test 6: Project aliases and functions
echo "6️⃣ Testing project aliases and functions..."
if command -v petro &> /dev/null; then
    echo "   ✅ 'petro' alias available"
else
    echo "   ❌ 'petro' alias not available"
fi

if command -v petro-status &> /dev/null; then
    echo "   ✅ 'petro-status' function available"
else
    echo "   ❌ 'petro-status' function not available"
fi
echo ""

# Test 7: Port forwarding
echo "7️⃣ Testing port forwarding..."
if netstat -tlnp 2>/dev/null | grep -q ":8888"; then
    echo "   ✅ Port 8888 is listening"
else
    echo "   ℹ️  Port 8888 not listening (may need to start Jupyter)"
fi
echo ""

# Summary
echo "📊 Test Summary"
echo "==============="
echo "Environment: $(uname -s) $(uname -m)"
echo "Container: $(hostname)"
echo "User: $(whoami)"
echo "Project: Petrobras Offshore Wells Anomaly Detection"
echo ""

echo "🎯 Next Steps:"
echo "   - Run 'source ~/.zshrc' to load project configuration"
echo "   - Use 'petro-status' to check project status"
echo "   - Use 'petro' to go to project root"
echo "   - Use 'jup' or 'jup-lab' to start Jupyter"
echo "   - Check the README for more information"
echo ""

echo "✅ Environment test complete!"
