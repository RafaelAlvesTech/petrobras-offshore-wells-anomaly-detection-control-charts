#!/bin/bash

# 🚀 Gemini CLI Setup Script for Petrobras Offshore Wells Project
# This script installs and configures the official Google Gemini CLI

set -e

echo "🛢️  Setting up Gemini CLI for Petrobras Offshore Wells Anomaly Detection Project"
echo "=================================================================="

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

# Check if Node.js is installed and version
check_nodejs() {
    print_status "Checking Node.js installation..."

    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed. Please install Node.js 20+ first."
        exit 1
    fi

    NODE_VERSION=$(node --version | cut -d'v' -f2)
    NODE_MAJOR=$(echo $NODE_VERSION | cut -d'.' -f1)

    if [ "$NODE_MAJOR" -lt 20 ]; then
        print_error "Node.js version $NODE_VERSION is too old. Version 20+ is required."
        print_status "Current version: $NODE_VERSION"
        exit 1
    fi

    print_success "Node.js $NODE_VERSION is compatible"
}

# Install Gemini CLI
install_gemini_cli() {
    print_status "Installing Gemini CLI..."

    # Set npm prefix to avoid permission issues
    npm config set prefix ~/.npm-global

    # Install Gemini CLI globally
    npm install -g @google/gemini-cli

    print_success "Gemini CLI installed successfully"
}

# Configure PATH
configure_path() {
    print_status "Configuring PATH..."

    # Add npm global bin to PATH if not already there
    if [[ ":$PATH:" != *":$HOME/.npm-global/bin:"* ]]; then
        echo 'export PATH="$HOME/.npm-global/bin:$PATH"' >> ~/.zshrc
        print_success "Added npm global bin to PATH in ~/.zshrc"
    else
        print_status "PATH already configured"
    fi

    # Source the updated configuration
    export PATH="$HOME/.npm-global/bin:$PATH"
}

# Test Gemini CLI
test_gemini_cli() {
    print_status "Testing Gemini CLI installation..."

    if command -v gemini &> /dev/null; then
        VERSION=$(gemini --version)
        print_success "Gemini CLI is working! Version: $VERSION"

        # Test help command
        if gemini --help &> /dev/null; then
            print_success "Help command working correctly"
        else
            print_warning "Help command had issues, but CLI is functional"
        fi
    else
        print_error "Gemini CLI not found in PATH"
        exit 1
    fi
}

# Create configuration template
create_config_template() {
    print_status "Creating configuration template..."

    if [ ! -f "config/gemini.env.template" ]; then
        print_error "Configuration template not found. Please check the config directory."
    else
        print_success "Configuration template available at config/gemini.env.template"
        print_status "Copy this to .env and configure your API key"
    fi
}

# Setup instructions
show_setup_instructions() {
    echo ""
    echo "🎯 Next Steps:"
    echo "=============="
    echo "1. Get your Gemini API key from: https://aistudio.google.com/app/apikey"
    echo "2. Copy the configuration template:"
    echo "   cp config/gemini.env.template .env"
    echo "3. Edit .env and add your API key:"
    echo "   GEMINI_API_KEY=\"your_actual_api_key_here\""
    echo "4. Test the CLI:"
    echo "   gemini --help"
    echo "5. Start using Gemini CLI:"
    echo "   gemini"
    echo ""
    echo "💡 Example usage for your project:"
    echo "   gemini -p \"Analyze this anomaly detection code for offshore wells\""
    echo "   gemini -i \"Help me optimize this LSTM-VAE model\""
    echo "   gemini -s -p \"Test this algorithm in sandbox mode\""
}

# Main execution
main() {
    echo "Starting Gemini CLI setup..."

    check_nodejs
    install_gemini_cli
    configure_path
    test_gemini_cli
    create_config_template
    show_setup_instructions

    print_success "Gemini CLI setup completed successfully! 🎉"
    print_status "Please restart your terminal or run: source ~/.zshrc"
}

# Run main function
main "$@"
