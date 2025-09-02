#!/bin/bash
echo "🧪 Testing Petrobras environment setup..."
echo "Python version: $(python --version)"
echo "Pip version: $(pip --version)"
echo "Git version: $(git --version)"
if command -v docker &> /dev/null; then
    echo "Docker version: $(docker --version)"
fi
echo "Current user: $(whoami)"
echo "Home directory: $HOME"
echo "Project directory: $(pwd)"
echo "Virtual environment: $VIRTUAL_ENV"
echo "✅ Basic environment test complete!"
