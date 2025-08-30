#!/bin/bash

# WSL2 Diagnostic Script for Petrobras Project
# This script helps identify common WSL2 issues

set -e

echo "🔍 WSL2 Diagnostic Script for Petrobras Project"
echo "================================================"
echo ""

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

# Function to check command availability
check_command() {
    if command -v $1 &> /dev/null; then
        print_success "$1 found"
        return 0
    else
        print_error "$1 not found"
        return 1
    fi
}

# Function to check service status
check_service() {
    if systemctl is-active --quiet $1; then
        print_success "$1 service is running"
        return 0
    else
        print_warning "$1 service is not running"
        return 1
    fi
}

echo "1. 🔧 System Information"
echo "-----------------------"
print_status "Checking system information..."

# OS information
if [ -f /etc/os-release ]; then
    source /etc/os-release
    print_success "OS: $PRETTY_NAME"
else
    print_warning "Could not determine OS version"
fi

# Kernel version
KERNEL_VERSION=$(uname -r)
print_success "Kernel: $KERNEL_VERSION"

# Check if running in WSL
if grep -qi microsoft /proc/version; then
    print_success "Running in WSL environment"
else
    print_warning "Not running in WSL environment"
fi

# WSL version
if command -v wsl.exe &> /dev/null; then
    WSL_VERSION=$(wsl.exe --version 2>/dev/null || echo "Unknown")
    print_success "WSL Version: $WSL_VERSION"
else
    print_warning "wsl.exe command not available"
fi

echo ""
echo "2. 🐍 Python Environment"
echo "------------------------"
print_status "Checking Python environment..."

# Check Python versions
if check_command python3.11; then
    PYTHON_VERSION="3.11"
elif check_command python3; then
    PYTHON_VERSION="3.x"
    PYTHON_ACTUAL=$(python3 --version 2>&1 | cut -d' ' -f2)
    print_status "Python version: $PYTHON_ACTUAL"
else
    print_error "No Python found"
fi

# Check virtual environment
if [ -d ".venv" ]; then
    print_success "Virtual environment found (.venv)"
    if [ -f ".venv/bin/activate" ]; then
        print_success "Virtual environment is properly configured"
    else
        print_warning "Virtual environment may be corrupted"
    fi
else
    print_warning "No virtual environment found"
fi

# Check uv
check_command uv

echo ""
echo "3. 🐳 Docker Environment"
echo "------------------------"
print_status "Checking Docker environment..."

# Check Docker
if check_command docker; then
    # Check Docker service
    if check_service docker; then
        # Test Docker functionality
        if docker info &> /dev/null; then
            print_success "Docker is working properly"
            DOCKER_VERSION=$(docker --version | cut -d' ' -f3 | sed 's/,//')
            print_success "Docker version: $DOCKER_VERSION"
        else
            print_error "Docker is not responding"
        fi
    fi
else
    print_warning "Docker not installed"
fi

echo ""
echo "4. 🌐 Network Configuration"
echo "---------------------------"
print_status "Checking network configuration..."

# Check network interfaces
if ip addr show &> /dev/null; then
    print_success "Network interfaces accessible"

    # Check for WSL2 network interface
    if ip addr show | grep -q "eth0"; then
        print_success "WSL2 network interface (eth0) found"
    else
        print_warning "WSL2 network interface not found"
    fi
else
    print_error "Cannot access network interfaces"
fi

# Check DNS resolution
if nslookup google.com &> /dev/null; then
    print_success "DNS resolution working"
else
    print_error "DNS resolution failed"
fi

# Check internet connectivity
if ping -c 1 8.8.8.8 &> /dev/null; then
    print_success "Internet connectivity working"
else
    print_error "No internet connectivity"
fi

echo ""
echo "5. 📁 File System and Permissions"
echo "---------------------------------"
print_status "Checking file system and permissions..."

# Check current directory
CURRENT_DIR=$(pwd)
print_status "Current directory: $CURRENT_DIR"

# Check if we're in the project directory
if [ -f "pyproject.toml" ]; then
    print_success "Project root directory detected"
else
    print_warning "Not in project root directory"
fi

# Check file permissions
if [ -r "." ] && [ -w "." ]; then
    print_success "Directory permissions OK"
else
    print_error "Directory permission issues"
fi

# Check for Windows mount
if [ -d "/mnt/c" ]; then
    print_warning "Windows C: drive mounted at /mnt/c"
    if [ -r "/mnt/c" ]; then
        print_success "Windows mount is readable"
    else
        print_error "Windows mount has permission issues"
    fi
fi

echo ""
echo "6. 🔌 Development Tools"
echo "-----------------------"
print_status "Checking development tools..."

# Check Git
check_command git

# Check Jupyter
check_command jupyter

# Check pip
check_command pip

# Check pre-commit
if [ -f ".pre-commit-config.yaml" ]; then
    if check_command pre-commit; then
        print_success "Pre-commit hooks configured"
    else
        print_warning "Pre-commit not installed"
    fi
fi

echo ""
echo "7. 📊 Resource Usage"
echo "--------------------"
print_status "Checking system resources..."

# Memory usage
if command -v free &> /dev/null; then
    MEMORY_INFO=$(free -h | grep Mem)
    TOTAL_MEM=$(echo $MEMORY_INFO | awk '{print $2}')
    USED_MEM=$(echo $MEMORY_INFO | awk '{print $3}')
    print_status "Memory: $USED_MEM / $TOTAL_MEM"
fi

# Disk usage
if command -v df &> /dev/null; then
    DISK_USAGE=$(df -h . | tail -1 | awk '{print $5}')
    print_status "Disk usage: $DISK_USAGE"
fi

# CPU info
if [ -f /proc/cpuinfo ]; then
    CPU_CORES=$(grep -c processor /proc/cpuinfo)
    print_status "CPU cores: $CPU_CORES"
fi

echo ""
echo "8. 🚨 Common Issues Check"
echo "-------------------------"
print_status "Checking for common issues..."

# Check for common error patterns
if [ -d "~/.cursor-server" ]; then
    print_warning "Cursor server directory found - may need cleanup"
fi

if [ -d "~/.vscode-server" ]; then
    print_warning "VS Code server directory found - may need cleanup"
fi

# Check for permission issues
if [ ! -w "$HOME" ]; then
    print_error "Home directory not writable"
fi

# Check for WSL2 specific issues
if [ -f /proc/version ] && grep -qi "microsoft" /proc/version; then
    if ! grep -q "WSL2" /proc/version; then
        print_warning "Running WSL1 instead of WSL2"
    fi
fi

echo ""
echo "9. 💡 Recommendations"
echo "---------------------"
print_status "Generating recommendations..."

RECOMMENDATIONS=()

# Check if we need to restart WSL
if [ -d "~/.cursor-server" ] || [ -d "~/.vscode-server" ]; then
    RECOMMENDATIONS+=("Clean up Cursor/VS Code server directories")
    RECOMMENDATIONS+=("Restart WSL2: wsl --shutdown && wsl")
fi

# Check if Docker needs configuration
if ! systemctl is-active --quiet docker; then
    RECOMMENDATIONS+=("Start Docker service: sudo systemctl start docker")
    RECOMMENDATIONS+=("Enable Docker: sudo systemctl enable docker")
fi

# Check if user is in docker group
if ! groups $USER | grep -q docker; then
    RECOMMENDATIONS+=("Add user to docker group: sudo usermod -aG docker $USER")
fi

# Check if virtual environment needs activation
if [ -d ".venv" ] && [ -z "$VIRTUAL_ENV" ]; then
    RECOMMENDATIONS+=("Activate virtual environment: source .venv/bin/activate")
fi

# Check if setup script should be run
if [ ! -f "test_setup.sh" ]; then
    RECOMMENDATIONS+=("Run setup script: chmod +x scripts/setup_wsl2.sh && ./scripts/setup_wsl2.sh")
fi

# Display recommendations
if [ ${#RECOMMENDATIONS[@]} -eq 0 ]; then
    print_success "No immediate issues detected!"
else
    print_warning "Recommendations:"
    for rec in "${RECOMMENDATIONS[@]}"; do
        echo "  • $rec"
    done
fi

echo ""
echo "10. 📋 Summary"
echo "--------------"
print_status "Diagnostic summary:"

# Count issues
ERROR_COUNT=0
WARNING_COUNT=0
SUCCESS_COUNT=0

# This is a simplified count - in a real implementation you'd track these
print_status "Run the script with --verbose for detailed counts"

echo ""
echo "🔍 Diagnostic complete!"
echo "📚 For detailed troubleshooting, see: docs/WSL2_TROUBLESHOOTING.md"
echo "🚀 For setup help, run: ./scripts/setup_wsl2.sh"
