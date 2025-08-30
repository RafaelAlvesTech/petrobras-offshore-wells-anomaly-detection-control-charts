#!/bin/bash

# =============================================================================
# 🛢️ SCRIPT DE CONFIGURAÇÃO DO ZSH PARA PROJETO PETROBRAS
# =============================================================================
# Este script configura o ambiente ZSH com todas as personalizações
# necessárias para o projeto de detecção de anomalias
# =============================================================================

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Função para imprimir mensagens coloridas
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Função para imprimir cabeçalho
print_header() {
    echo -e "${CYAN}"
    echo "============================================================================="
    echo "🛢️  CONFIGURAÇÃO DO ZSH - PROJETO PETROBRAS"
    echo "============================================================================="
    echo -e "${NC}"
}

# Função para verificar se o comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Função para instalar dependências do sistema
install_system_dependencies() {
    print_message $YELLOW "📦 Instalando dependências do sistema..."

    # Atualizar lista de pacotes
    sudo apt-get update

    # Instalar dependências básicas
    sudo apt-get install -y \
        zsh \
        curl \
        wget \
        git \
        build-essential \
        software-properties-common \
        apt-transport-https \
        ca-certificates \
        gnupg \
        lsb-release

    print_message $GREEN "✅ Dependências do sistema instaladas!"
}

# Função para instalar Oh My Zsh
install_oh_my_zsh() {
    if [ ! -d "$HOME/.oh-my-zsh" ]; then
        print_message $YELLOW "🎨 Instalando Oh My Zsh..."

        # Instalar Oh My Zsh
        sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

        print_message $GREEN "✅ Oh My Zsh instalado!"
    else
        print_message $BLUE "ℹ️  Oh My Zsh já está instalado"
    fi
}

# Função para instalar plugins do Zsh
install_zsh_plugins() {
    print_message $YELLOW "🔌 Instalando plugins do Zsh..."

    # Criar diretório de plugins
    mkdir -p "$HOME/.zsh"

    # Instalar zsh-autosuggestions
    if [ ! -d "$HOME/.zsh/zsh-autosuggestions" ]; then
        git clone https://github.com/zsh-users/zsh-autosuggestions "$HOME/.zsh/zsh-autosuggestions"
        print_message $GREEN "✅ zsh-autosuggestions instalado!"
    else
        print_message $BLUE "ℹ️  zsh-autosuggestions já está instalado"
    fi

    # Instalar zsh-syntax-highlighting
    if [ ! -d "$HOME/.zsh/zsh-syntax-highlighting" ]; then
        git clone https://github.com/zsh-users/zsh-syntax-highlighting.git "$HOME/.zsh/zsh-syntax-highlighting"
        print_message $GREEN "✅ zsh-syntax-highlighting instalado!"
    else
        print_message $BLUE "ℹ️  zsh-syntax-highlighting já está instalado"
    fi

    # Instalar fzf
    if ! command_exists fzf; then
        print_message $YELLOW "🔍 Instalando fzf..."
        git clone --depth 1 https://github.com/junegunn/fzf.git "$HOME/.fzf"
        "$HOME/.fzf/install" --key-bindings --completion --no-update-rc
        print_message $GREEN "✅ fzf instalado!"
    else
        print_message $BLUE "ℹ️  fzf já está instalado"
    fi
}

# Função para instalar uv
install_uv() {
    if ! command_exists uv; then
        print_message $YELLOW "🐍 Instalando uv..."

        # Instalar uv
        curl -LsSf https://astral.sh/uv/install.sh | sh

        # Adicionar ao PATH
        echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> "$HOME/.zshrc"

        print_message $GREEN "✅ uv instalado!"
    else
        print_message $BLUE "ℹ️  uv já está instalado"
    fi
}

# Função para configurar arquivos Zsh
setup_zsh_config() {
    print_message $YELLOW "⚙️  Configurando arquivos Zsh..."

    # Fazer backup do .zshrc existente
    if [ -f "$HOME/.zshrc" ]; then
        cp "$HOME/.zshrc" "$HOME/.zshrc.backup.$(date +%Y%m%d_%H%M%S)"
        print_message $BLUE "ℹ️  Backup do .zshrc criado"
    fi

    # Copiar configurações do projeto
    if [ -f ".zshrc" ]; then
        cp ".zshrc" "$HOME/.zshrc"
        print_message $GREEN "✅ .zshrc configurado!"
    else
        print_message $RED "❌ Arquivo .zshrc não encontrado no projeto"
        return 1
    fi

    # Copiar configurações específicas do projeto
    if [ -f ".zshrc.project" ]; then
        cp ".zshrc.project" "$HOME/.zshrc.project"
        print_message $GREEN "✅ .zshrc.project configurado!"
    else
        print_message $RED "❌ Arquivo .zshrc.project não encontrado no projeto"
        return 1
    fi
}

# Função para configurar ambiente Python
setup_python_environment() {
    print_message $YELLOW "🐍 Configurando ambiente Python..."

    # Verificar se uv está disponível
    if command_exists uv; then
        # Criar ambiente virtual
        uv venv

        # Ativar ambiente virtual
        source .venv/bin/activate

        # Instalar dependências
        uv sync

        print_message $GREEN "✅ Ambiente Python configurado!"
    else
        print_message $RED "❌ uv não está instalado. Execute: install_uv"
        return 1
    fi
}

# Função para configurar Git
setup_git() {
    print_message $YELLOW "🔧 Configurando Git..."

    # Configurar Git globalmente (se não estiver configurado)
    if [ -z "$(git config --global user.name)" ]; then
        git config --global user.name "Petrobras Developer"
        print_message $BLUE "ℹ️  Nome do usuário Git configurado"
    fi

    if [ -z "$(git config --global user.email)" ]; then
        git config --global user.email "developer@petrobras.com.br"
        print_message $BLUE "ℹ️  Email do usuário Git configurado"
    fi

    # Configurar aliases úteis
    git config --global alias.st status
    git config --global alias.co checkout
    git config --global alias.br branch
    git config --global alias.ci commit
    git config --global alias.unstage 'reset HEAD --'
    git config --global alias.last 'log -1 HEAD'
    git config --global alias.visual '!gitk'

    print_message $GREEN "✅ Git configurado!"
}

# Função para configurar VS Code/Cursor
setup_vscode() {
    print_message $YELLOW "💻 Configurando VS Code/Cursor..."

    # Criar diretório de configurações
    mkdir -p "$HOME/.vscode"

    # Configurar settings.json
    cat > "$HOME/.vscode/settings.json" << 'EOF'
{
    "python.defaultInterpreterPath": "./.venv/bin/python",
    "python.terminal.activateEnvironment": true,
    "python.terminal.activateEnvInCurrentTerminal": true,
    "python.linting.enabled": true,
    "python.linting.ruffEnabled": true,
    "python.formatting.provider": "black",
    "python.sortImports.args": ["--profile", "black"],
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": "explicit"
    },
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        "**/.pytest_cache": true,
        "**/.mypy_cache": true,
        "**/.ruff_cache": true
    },
    "terminal.integrated.defaultProfile.linux": "zsh",
    "terminal.integrated.profiles.linux": {
        "zsh": {
            "path": "/bin/zsh"
        }
    }
}
EOF

    print_message $GREEN "✅ VS Code/Cursor configurado!"
}

# Função para testar configuração
test_configuration() {
    print_message $YELLOW "🧪 Testando configuração..."

    # Testar Zsh
    if command_exists zsh; then
        print_message $GREEN "✅ Zsh está disponível"
    else
        print_message $RED "❌ Zsh não está disponível"
    fi

    # Testar Python
    if command_exists python; then
        print_message $GREEN "✅ Python está disponível"
    else
        print_message $RED "❌ Python não está disponível"
    fi

    # Testar uv
    if command_exists uv; then
        print_message $GREEN "✅ uv está disponível"
    else
        print_message $RED "❌ uv não está disponível"
    fi

    # Testar Git
    if command_exists git; then
        print_message $GREEN "✅ Git está disponível"
    else
        print_message $RED "❌ Git não está disponível"
    fi

    print_message $GREEN "✅ Teste de configuração concluído!"
}

# Função para exibir informações finais
show_final_info() {
    print_message $CYAN
    echo "============================================================================="
    echo "🎉 CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!"
    echo "============================================================================="
    echo -e "${NC}"

    print_message $GREEN "✅ Configurações aplicadas:"
    echo "  🐚 Zsh com Oh My Zsh"
    echo "  🔌 Plugins: autosuggestions, syntax-highlighting, fzf"
    echo "  🐍 Python com uv"
    echo "  🔧 Git configurado"
    echo "  💻 VS Code/Cursor configurado"
    echo "  🛢️  Configurações específicas do projeto Petrobras"

    print_message $YELLOW "📋 Próximos passos:"
    echo "  1. Reinicie o terminal ou execute: source ~/.zshrc"
    echo "  2. Execute: project_status para verificar o status"
    echo "  3. Execute: create_venv para configurar o ambiente virtual"
    echo "  4. Execute: jlab para iniciar o Jupyter Lab"

    print_message $BLUE "🔗 Comandos úteis:"
    echo "  • project_status - Status do projeto"
    echo "  • run_pipeline - Executar pipeline completo"
    echo "  • run_experiment <nome> - Executar experimento"
    echo "  • monitor_training - Monitorar treinamento"
    echo "  • check_code_quality - Verificar qualidade do código"

    print_message $PURPLE "📚 Documentação:"
    echo "  • README.md - Documentação principal"
    echo "  • CONTRIBUTING.md - Guia de contribuição"
    echo "  • docs/ - Documentação detalhada"

    echo ""
    print_message $GREEN "🛢️  Bem-vindo ao projeto Petrobras Offshore Wells Anomaly Detection!"
}

# Função principal
main() {
    print_header

    # Verificar se está no diretório correto
    if [ ! -f "pyproject.toml" ]; then
        print_message $RED "❌ Execute este script no diretório raiz do projeto"
        exit 1
    fi

    # Instalar dependências do sistema
    install_system_dependencies

    # Instalar Oh My Zsh
    install_oh_my_zsh

    # Instalar plugins do Zsh
    install_zsh_plugins

    # Instalar uv
    install_uv

    # Configurar arquivos Zsh
    setup_zsh_config

    # Configurar ambiente Python
    setup_python_environment

    # Configurar Git
    setup_git

    # Configurar VS Code/Cursor
    setup_vscode

    # Testar configuração
    test_configuration

    # Exibir informações finais
    show_final_info
}

# Executar função principal
main "$@"
