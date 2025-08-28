#!/bin/bash

# 🤖 Petrobras Offshore Wells Anomaly Detection - Claude Code Extensions Installer
# 🚀 Script para instalar extensões específicas para Claude Code

set -e

echo "🛢️  Petrobras Offshore Wells Anomaly Detection"
echo "🤖 Claude Code Extensions Installer"
echo "=================================================="

# Verificar se o code está disponível
if ! command -v code &> /dev/null; then
    echo "❌ VS Code CLI não encontrado. Instale o VS Code primeiro."
    echo "💡 Dica: Instale o VS Code e adicione 'code' ao PATH"
    exit 1
fi

echo "✅ VS Code CLI encontrado"
echo ""

# Extensões essenciais para Claude Code
echo "🔌 Instalando extensões essenciais para Claude Code..."

# 🐍 Python Development
echo "🐍 Instalando extensões Python..."
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension ms-python.debugpy
code --install-extension ms-python.isort
code --install-extension charliermarsh.ruff

# 🤖 Claude Code - Extensões Específicas para IA e ML
echo "🤖 Instalando extensões específicas para Claude Code..."
code --install-extension ms-python.black-formatter
code --install-extension ms-python.flake8
code --install-extension ms-python.mypy-type-checker
code --install-extension ms-python.pylint
code --install-extension ms-python.autopep8

# 📊 Data Science & Jupyter
echo "📊 Instalando extensões de Data Science..."
code --install-extension ms-toolsai.jupyter
code --install-extension ms-toolsai.jupyter-keymap
code --install-extension ms-toolsai.jupyter-renderers

# 🔧 Development Tools
echo "🔧 Instalando ferramentas de desenvolvimento..."
code --install-extension ms-vscode.vscode-json
code --install-extension yzhang.markdown-all-in-one
code --install-extension esbenp.prettier-vscode

# 🐳 Docker & Containers
echo "🐳 Instalando extensões Docker..."
code --install-extension ms-azuretools.vscode-docker
code --install-extension ms-kubernetes-tools.vscode-kubernetes-tools

# 🔄 Git & Version Control
echo "🔄 Instalando extensões Git..."
code --install-extension eamodio.gitlens
code --install-extension donjayamanne.githistory
code --install-extension github.vscode-github-actions
code --install-extension github.vscode-pull-request-github
code --install-extension vivaxy.vscode-conventional-commits

# 🎨 Themes & Icons
echo "🎨 Instalando temas e ícones..."
code --install-extension pkief.material-icon-theme
code --install-extension github.github-vscode-theme
code --install-extension johnpapa.vscode-peacock

# 🧪 Testing
echo "🧪 Instalando extensões de teste..."
code --install-extension littlefoxteam.vscode-python-test-adapter
code --install-extension firsttris.vscode-jest-runner

# 🚀 AI & Productivity
echo "🚀 Instalando extensões de IA e produtividade..."
code --install-extension GitHub.copilot
code --install-extension GitHub.copilot-chat
code --install-extension visualstudioexptteam.vscodeintellicode
code --install-extension visualstudioexptteam.intellicode-api-usage-examples

# 🔍 Code Quality & Analysis
echo "🔍 Instalando extensões de qualidade de código..."
code --install-extension sonarsource.sonarlint-vscode
code --install-extension streetsidesoftware.code-spell-checker
code --install-extension streetsidesoftware.code-spell-checker-portuguese-brazilian
code --install-extension sourcery.sourcery

# 🎯 Language Support
echo "🎯 Instalando suporte a linguagens..."
code --install-extension redhat.vscode-yaml
code --install-extension tamasfe.even-better-toml
code --install-extension ms-vscode.makefile-tools
code --install-extension naumovs.color-highlight
code --install-extension oderwat.indent-rainbow

# 🛠️ Utilities
echo "🛠️ Instalando utilitários..."
code --install-extension chakrounanas.turbo-console-log
code --install-extension christian-kohler.path-intellisense
code --install-extension gruntfuggly.todo-tree
code --install-extension wallabyjs.quokka-vscode
code --install-extension xyz.local-history

# 🌐 Web Development
echo "🌐 Instalando extensões de desenvolvimento web..."
code --install-extension ms-vscode.live-server
code --install-extension vue.volar
code --install-extension zignd.html-css-class-completion

# 📊 Database & APIs
echo "📊 Instalando extensões de banco de dados e APIs..."
code --install-extension cweijan.dbclient-jdbc
code --install-extension cweijan.vscode-redis-client
code --install-extension humao.rest-client

# 🔧 Advanced Tools
echo "🔧 Instalando ferramentas avançadas..."
code --install-extension adpyke.codesnap
code --install-extension jebbs.plantuml
code --install-extension quicktype.quicktype
code --install-extension tim-koehler.helm-intellisense

echo ""
echo "✅ Todas as extensões foram instaladas com sucesso!"
echo ""
echo "🎯 Próximos passos:"
echo "1. Reinicie o VS Code/Cursor"
echo "2. Verifique se as extensões estão ativas"
echo "3. Configure o Python interpreter para ./.venv/bin/python"
echo "4. Execute 'uv sync' para sincronizar dependências"
echo ""
echo "🚀 Configurações específicas para Claude Code já estão no .vscode/settings.json"
echo "📚 Consulte o README.md para mais detalhes sobre as configurações"
echo ""
echo "🛢️  Petrobras Offshore Wells Anomaly Detection - Claude Code Ready!"
