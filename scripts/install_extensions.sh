#!/bin/bash

# 🛢️ Petrobras Offshore Wells Anomaly Detection - Extensions Installer
# Script para instalação automática das extensões essenciais do VS Code/Cursor

set -e  # Exit on any error

echo "🚀 Instalando extensões essenciais para o projeto..."

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Verificar se o code está instalado
if ! command -v code &> /dev/null; then
    echo -e "${RED}❌ VS Code/Cursor não encontrado no PATH${NC}"
    echo -e "${YELLOW}💡 Certifique-se de que o VS Code/Cursor está instalado e 'code' está no PATH${NC}"
    exit 1
fi

# Lista de extensões essenciais (baseadas nas suas configurações)
EXTENSIONS=(
    # 🐍 Python Development
    "ms-python.python"
    "ms-python.vscode-pylance"
    "ms-python.debugpy"
    "ms-python.isort"
    "charliermarsh.ruff"

    # 📊 Data Science & Jupyter
    "ms-toolsai.jupyter"
    "ms-toolsai.jupyter-keymap"

    # 🔧 Development Tools
    "ms-vscode.vscode-json"
    "yzhang.markdown-all-in-one"
    "esbenp.prettier-vscode"
    "ms-vscode.vscode-typescript-next"
    "bradlc.vscode-tailwindcss"

    # 🐳 Docker & Containers
    "ms-azuretools.vscode-docker"
    "ms-kubernetes-tools.vscode-kubernetes-tools"

    # 🔄 Git & Version Control
    "eamodio.gitlens"
    "donjayamanne.githistory"
    "github.vscode-github-actions"
    "github.vscode-pull-request-github"
    "vivaxy.vscode-conventional-commits"

    # 🎨 Themes & Icons
    "pkief.material-icon-theme"
    "github.github-vscode-theme"
    "johnpapa.vscode-peacock"

    # 🧪 Testing
    "littlefoxteam.vscode-python-test-adapter"
    "firsttris.vscode-jest-runner"
    "orta.vscode-jest"
    "vitest.explorer"

    # 🚀 AI & Productivity
    "GitHub.copilot"
    "GitHub.copilot-chat"
    "visualstudioexptteam.vscodeintellicode"
    "visualstudioexptteam.intellicode-api-usage-examples"

    # 🔍 Code Quality & Analysis
    "sonarsource.sonarlint-vscode"
    "streetsidesoftware.code-spell-checker"
    "streetsidesoftware.code-spell-checker-portuguese-brazilian"
    "sourcery.sourcery"

    # 🎯 Language Support
    "redhat.vscode-yaml"
    "tamasfe.even-better-toml"
    "ms-vscode.makefile-tools"
    "naumovs.color-highlight"
    "oderwat.indent-rainbow"

    # 🛠️ Utilities
    "chakrounanas.turbo-console-log"
    "christian-kohler.path-intellisense"
    "gruntfuggly.todo-tree"
    "wallabyjs.quokka-vscode"
    "xyz.local-history"

    # 🌐 Web Development
    "ms-vscode.live-server"
    "vue.volar"
    "zignd.html-css-class-completion"

    # 📊 Database & APIs
    "cweijan.dbclient-jdbc"
    "cweijan.vscode-redis-client"
    "humao.rest-client"

    # 🔧 Advanced Tools
    "adpyke.codesnap"
    "jebbs.plantuml"
    "quicktype.quicktype"
    "tim-koehler.helm-intellisense"
)

# Contadores
TOTAL=${#EXTENSIONS[@]}
INSTALLED=0
FAILED=0

echo -e "${BLUE}📦 Total de extensões a instalar: $TOTAL${NC}"
echo ""

# Instalar cada extensão
for extension in "${EXTENSIONS[@]}"; do
    echo -n "📥 Instalando $extension... "

    # Tentar instalar a extensão
    if code --install-extension "$extension" --force > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Sucesso${NC}"
        ((INSTALLED++))
    else
        echo -e "${RED}❌ Falha${NC}"
        ((FAILED++))
    fi

    # Pequena pausa para evitar sobrecarga
    sleep 0.5
done

echo ""
echo -e "${BLUE}📊 Resumo da instalação:${NC}"
echo -e "${GREEN}✅ Instaladas com sucesso: $INSTALLED${NC}"
echo -e "${RED}❌ Falhas: $FAILED${NC}"
echo -e "${BLUE}📦 Total: $TOTAL${NC}"

if [ $FAILED -eq 0 ]; then
    echo ""
    echo -e "${GREEN}🎉 Todas as extensões foram instaladas com sucesso!${NC}"
    echo -e "${YELLOW}💡 Reinicie o VS Code/Cursor para aplicar todas as configurações${NC}"
else
    echo ""
    echo -e "${YELLOW}⚠️  Algumas extensões falharam na instalação${NC}"
    echo -e "${YELLOW}💡 Tente instalar manualmente as extensões que falharam${NC}"
fi

echo ""
echo -e "${BLUE}🔧 Próximos passos:${NC}"
echo "1. Reinicie o VS Code/Cursor"
echo "2. Configure o Python interpreter (Ctrl+Shift+P > Python: Select Interpreter)"
echo "3. Execute 'uv sync' para instalar dependências Python"
echo "4. Configure o pre-commit: uv run pre-commit install"
echo "5. Aproveite suas configurações personalizadas! 🎨"
