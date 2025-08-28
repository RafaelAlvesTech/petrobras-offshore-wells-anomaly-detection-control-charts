# 🤖 Petrobras Offshore Wells Anomaly Detection - Claude Code Extensions Installer
# 🚀 Script PowerShell para instalar extensões específicas para Claude Code

param(
    [switch]$Force
)

Write-Host "🛢️  Petrobras Offshore Wells Anomaly Detection" -ForegroundColor Cyan
Write-Host "🤖 Claude Code Extensions Installer (PowerShell)" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# Verificar se o code está disponível
try {
    $codeVersion = code --version
    Write-Host "✅ VS Code CLI encontrado" -ForegroundColor Green
    Write-Host "📋 Versão: $($codeVersion[0])" -ForegroundColor Gray
} catch {
    Write-Host "❌ VS Code CLI não encontrado. Instale o VS Code primeiro." -ForegroundColor Red
    Write-Host "💡 Dica: Instale o VS Code e adicione 'code' ao PATH" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Extensões essenciais para Claude Code
Write-Host "🔌 Instalando extensões essenciais para Claude Code..." -ForegroundColor Blue

# 🐍 Python Development
Write-Host "🐍 Instalando extensões Python..." -ForegroundColor Green
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension ms-python.debugpy
code --install-extension ms-python.isort
code --install-extension charliermarsh.ruff

# 🤖 Claude Code - Extensões Específicas para IA e ML
Write-Host "🤖 Instalando extensões específicas para Claude Code..." -ForegroundColor Magenta
code --install-extension ms-python.black-formatter
code --install-extension ms-python.flake8
code --install-extension ms-python.mypy-type-checker
code --install-extension ms-python.pylint
code --install-extension ms-python.autopep8

# 📊 Data Science & Jupyter
Write-Host "📊 Instalando extensões de Data Science..." -ForegroundColor Cyan
code --install-extension ms-toolsai.jupyter
code --install-extension ms-toolsai.jupyter-keymap
code --install-extension ms-toolsai.jupyter-renderers

# 🔧 Development Tools
Write-Host "🔧 Instalando ferramentas de desenvolvimento..." -ForegroundColor Yellow
code --install-extension ms-vscode.vscode-json
code --install-extension yzhang.markdown-all-in-one
code --install-extension esbenp.prettier-vscode

# 🐳 Docker & Containers
Write-Host "🐳 Instalando extensões Docker..." -ForegroundColor Blue
code --install-extension ms-azuretools.vscode-docker
code --install-extension ms-kubernetes-tools.vscode-kubernetes-tools

# 🔄 Git & Version Control
Write-Host "🔄 Instalando extensões Git..." -ForegroundColor Green
code --install-extension eamodio.gitlens
code --install-extension donjayamanne.githistory
code --install-extension github.vscode-github-actions
code --install-extension github.vscode-pull-request-github
code --install-extension vivaxy.vscode-conventional-commits

# 🎨 Themes & Icons
Write-Host "🎨 Instalando temas e ícones..." -ForegroundColor Magenta
code --install-extension pkief.material-icon-theme
code --install-extension github.github-vscode-theme
code --install-extension johnpapa.vscode-peacock

# 🧪 Testing
Write-Host "🧪 Instalando extensões de teste..." -ForegroundColor Red
code --install-extension littlefoxteam.vscode-python-test-adapter
code --install-extension firsttris.vscode-jest-runner

# 🚀 AI & Productivity
Write-Host "🚀 Instalando extensões de IA e produtividade..." -ForegroundColor Cyan
code --install-extension GitHub.copilot
code --install-extension GitHub.copilot-chat
code --install-extension visualstudioexptteam.vscodeintellicode
code --install-extension visualstudioexptteam.intellicode-api-usage-examples

# 🔍 Code Quality & Analysis
Write-Host "🔍 Instalando extensões de qualidade de código..." -ForegroundColor Yellow
code --install-extension sonarsource.sonarlint-vscode
code --install-extension streetsidesoftware.code-spell-checker
code --install-extension streetsidesoftware.code-spell-checker-portuguese-brazilian
code --install-extension sourcery.sourcery

# 🎯 Language Support
Write-Host "🎯 Instalando suporte a linguagens..." -ForegroundColor Green
code --install-extension redhat.vscode-yaml
code --install-extension tamasfe.even-better-toml
code --install-extension ms-vscode.makefile-tools
code --install-extension naumovs.color-highlight
code --install-extension oderwat.indent-rainbow

# 🛠️ Utilities
Write-Host "🛠️ Instalando utilitários..." -ForegroundColor Gray
code --install-extension chakrounanas.turbo-console-log
code --install-extension christian-kohler.path-intellisense
code --install-extension gruntfuggly.todo-tree
code --install-extension wallabyjs.quokka-vscode
code --install-extension xyz.local-history

# 🌐 Web Development
Write-Host "🌐 Instalando extensões de desenvolvimento web..." -ForegroundColor Blue
code --install-extension ms-vscode.live-server
code --install-extension vue.volar
code --install-extension zignd.html-css-class-completion

# 📊 Database & APIs
Write-Host "📊 Instalando extensões de banco de dados e APIs..." -ForegroundColor Cyan
code --install-extension cweijan.dbclient-jdbc
code --install-extension cweijan.vscode-redis-client
code --install-extension humao.rest-client

# 🔧 Advanced Tools
Write-Host "🔧 Instalando ferramentas avançadas..." -ForegroundColor Yellow
code --install-extension adpyke.codesnap
code --install-extension jebbs.plantuml
code --install-extension quicktype.quicktype
code --install-extension tim-koehler.helm-intellisense

Write-Host ""
Write-Host "✅ Todas as extensões foram instaladas com sucesso!" -ForegroundColor Green
Write-Host ""
Write-Host "🎯 Próximos passos:" -ForegroundColor Yellow
Write-Host "1. Reinicie o VS Code/Cursor" -ForegroundColor White
Write-Host "2. Verifique se as extensões estão ativas" -ForegroundColor White
Write-Host "3. Configure o Python interpreter para ./.venv/bin/python" -ForegroundColor White
Write-Host "4. Execute 'uv sync' para sincronizar dependências" -ForegroundColor White
Write-Host ""
Write-Host "🚀 Configurações específicas para Claude Code já estão no .vscode/settings.json" -ForegroundColor Cyan
Write-Host "📚 Consulte o README.md para mais detalhes sobre as configurações" -ForegroundColor Cyan
Write-Host ""
Write-Host "🛢️  Petrobras Offshore Wells Anomaly Detection - Claude Code Ready!" -ForegroundColor Green

# Aguardar input do usuário se não for forçado
if (-not $Force) {
    Write-Host ""
    Write-Host "Pressione qualquer tecla para continuar..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}
