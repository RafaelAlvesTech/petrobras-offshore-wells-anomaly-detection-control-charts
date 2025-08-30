#!/bin/bash

# Setup script for WSL2 environment without devcontainer
# This script configures the environment for Petrobras Offshore Wells project

set -e

echo "🚀 Setting up WSL2 environment for Petrobras Offshore Wells project..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

print_status "Checking system requirements..."

# Check Python version
if command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3.11"
    print_success "Python 3.11 found"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PYTHON_VERSION=$($PYTHON_CMD --version | cut -d' ' -f2)
    if [[ "$PYTHON_VERSION" < "3.11" ]]; then
        print_warning "Python version $PYTHON_VERSION found, but 3.11+ is recommended"
    else
        print_success "Python $PYTHON_VERSION found"
    fi
else
    print_error "Python not found. Please install Python 3.11+"
    exit 1
fi

# Check uv
if command -v uv &> /dev/null; then
    print_success "uv package manager found"
else
    print_warning "uv not found. Installing..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source ~/.bashrc
fi

# Check Docker
if command -v docker &> /dev/null; then
    if docker info &> /dev/null; then
        print_success "Docker is running"
    else
        print_warning "Docker found but not running. Starting..."
        sudo systemctl start docker
        sudo usermod -aG docker $USER
        print_warning "Please log out and back in for Docker group changes to take effect"
    fi
else
    print_warning "Docker not found. Consider installing for containerized development"
fi

print_status "Setting up Python environment..."

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    print_status "Creating virtual environment..."
    uv venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
print_status "Installing dependencies..."
uv sync

# Install Jupyter kernel
print_status "Installing Jupyter kernel..."
python -m ipykernel install --user --name petrobras-3.11 --display-name "Python 3.11 (petrobras)"

# Setup pre-commit hooks
if [ -f ".pre-commit-config.yaml" ]; then
    print_status "Setting up pre-commit hooks..."
    pre-commit install
fi

# Create Jupyter configuration
print_status "Configuring Jupyter..."
mkdir -p ~/.jupyter
cat > ~/.jupyter/jupyter_notebook_config.py << 'EOF'
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
c.NotebookApp.notebook_dir = '$(pwd)/notebooks'
EOF

print_status "Setting up shell configuration..."

# Create project-specific zsh configuration
cat > ~/.zshrc.project << 'EOF'
# Petrobras Project Configuration

# Activate virtual environment
if [ -f "$(pwd)/.venv/bin/activate" ]; then
    source "$(pwd)/.venv/bin/activate"
fi

# Add project paths to PYTHONPATH
export PYTHONPATH="$(pwd)/src:$(pwd)/notebooks:$PYTHONPATH"

# Aliases
alias petro="cd $(pwd)"
alias venv="source .venv/bin/activate"
alias test="python -m pytest"
alias lint="ruff check ."
alias format="ruff format ."
alias jupyter="jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root"

# Function to start Jupyter
start_jupyter() {
    cd "$(pwd)/notebooks"
    jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root
}

# Function to run tests
run_tests() {
    python -m pytest "$@"
}

# Function to check code quality
check_code() {
    echo "🔍 Running code quality checks..."
    ruff check .
    ruff format --check .
    mypy src/
    echo "✅ Code quality checks complete!"
}
EOF

# Source the project configuration in main zshrc
if ! grep -q "source.*zshrc.project" ~/.zshrc; then
    echo "" >> ~/.zshrc
    echo "# Source Petrobras project configuration" >> ~/.zshrc
    echo "if [ -f ~/.zshrc.project ]; then" >> ~/.zshrc
    echo "    source ~/.zshrc.project" >> ~/.zshrc
    echo "fi" >> ~/.zshrc
fi

print_status "Creating convenience scripts..."

# Create test script
cat > test_setup.sh << 'EOF'
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
EOF

chmod +x test_setup.sh

# Create start script
cat > start_jupyter.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting Jupyter Notebook for Petrobras project..."
cd "$(dirname "$0")/notebooks"
jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root
EOF

chmod +x start_jupyter.sh

print_success "WSL2 environment setup complete!"
echo ""
echo "🔄 Next steps:"
echo "1. Restart your terminal or run: source ~/.zshrc"
echo "2. Test the setup: ./test_setup.sh"
echo "3. Start Jupyter: ./start_jupyter.sh"
echo "4. Activate virtual environment: source .venv/bin/activate"
echo ""
echo "📚 Useful commands:"
echo "  - petro: Go to project directory"
echo "  - venv: Activate virtual environment"
echo "  - test: Run tests"
echo "  - lint: Check code with ruff"
echo "  - format: Format code with ruff"
echo "  - check_code: Run all code quality checks"
echo ""
echo "🌐 Jupyter will be available at: http://localhost:8888"
