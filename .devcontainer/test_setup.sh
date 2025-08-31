#!/bin/bash
set -e

echo "🧪 Testing Petrobras Offshore Wells Anomaly Detection environment..."

# Test Python installation
echo "🐍 Testing Python installation..."
python3 --version
python3 -c "import sys; print(f'Python executable: {sys.executable}')"

# Test pip installation
echo "📦 Testing pip installation..."
pip3 --version

# Test uv installation
echo "⚡ Testing uv installation..."
if command -v uv &> /dev/null; then
    uv --version
else
    echo "⚠️  uv not found, installing..."
    pip3 install uv
fi

# Test project dependencies
echo "📚 Testing project dependencies..."
if [ -f "pyproject.toml" ]; then
    echo "Found pyproject.toml"
    if command -v uv &> /dev/null; then
        echo "Testing uv sync..."
        uv sync --dry-run
    fi
elif [ -f "requirements.txt" ]; then
    echo "Found requirements.txt"
    echo "Testing pip install (dry run)..."
    pip3 install --dry-run -r requirements.txt
else
    echo "⚠️  No dependency file found"
fi

# Test Jupyter kernel
echo "🔬 Testing Jupyter kernel..."
python3 -c "import jupyter_client; print('Jupyter client available')" || echo "⚠️  Jupyter not available"

# Test directory structure
echo "📁 Testing directory structure..."
for dir in data/raw data/processed data/external models notebooks/experiments logs; do
    if [ -d "$dir" ]; then
        echo "✅ $dir exists"
    else
        echo "⚠️  $dir missing"
    fi
done

# Test git configuration
echo "🔐 Testing git configuration..."
git config --get commit.gpgsign || echo "⚠️  Git GPG signing not configured"

# Test pre-commit
echo "🔧 Testing pre-commit..."
if command -v pre-commit &> /dev/null; then
    pre-commit --version
else
    echo "⚠️  pre-commit not available"
fi

echo ""
echo "✅ Environment test complete!"
echo ""
echo "📊 Summary:"
echo "   - Python: $(python3 --version)"
echo "   - Pip: $(pip3 --version)"
echo "   - UV: $(uv --version 2>/dev/null || echo 'Not installed')"
echo "   - Git: $(git --version)"
echo "   - Pre-commit: $(pre-commit --version 2>/dev/null || echo 'Not installed')"
echo ""
