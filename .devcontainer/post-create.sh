#!/bin/bash
set -e

echo "🚀 Setting up Petrobras Offshore Wells Anomaly Detection environment..."

# Activate virtual environment
source .venv/bin/activate

# Install uv and pre-commit if not already installed
echo "📦 Installing uv and pre-commit..."
pip install uv pre-commit

# Install pre-commit hooks
echo "🔧 Installing pre-commit hooks..."
pre-commit install

# Disable GPG signing for commits (can be re-enabled later if needed)
echo "🔐 Configuring git..."
git config commit.gpgsign false

# Install project dependencies using uv
echo "📚 Installing project dependencies..."
if [ -f "pyproject.toml" ]; then
    uv sync
else
    pip install -r requirements.txt
fi

# Create necessary directories
echo "📁 Creating project directories..."
mkdir -p data/raw data/processed data/external
mkdir -p models
mkdir -p notebooks/experiments
mkdir -p logs

# Set up Jupyter kernel
echo "🔬 Setting up Jupyter kernel..."
python -m ipykernel install --user --name=petrobras-anomaly --display-name="Petrobras Anomaly Detection"

echo "✅ Environment setup complete!"
echo ""
echo "🎯 Next steps:"
echo "   1. Start Jupyter Lab: jupyter lab --ip=0.0.0.0 --port=8888 --no-browser"
echo "   2. Open notebooks in the notebooks/ directory"
echo "   3. Run experiments and analysis"
echo ""
echo "📊 Available tools:"
echo "   - Jupyter Lab: http://localhost:8888"
echo "   - MLflow UI: mlflow ui --host 0.0.0.0 --port 8000"
echo "   - Pre-commit hooks: pre-commit run --all-files"
echo ""
