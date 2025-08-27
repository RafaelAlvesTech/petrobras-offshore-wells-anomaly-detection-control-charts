# 🛢️ Petrobras Offshore Wells Anomaly Detection - Extensions Installer
# Script PowerShell para instalação automática das extensões essenciais do VS Code/Cursor
# Baseado nas suas configurações pessoais do VSCode

param(
    [switch]$Force
)

# Configurações de execução
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

Write-Host "🚀 Instalando extensões essenciais para o projeto..." -ForegroundColor Blue
Write-Host "💡 Baseado nas suas configurações pessoais do VSCode!" -ForegroundColor Yellow

# Verificar se o code está instalado
try {
    $codeVersion = code --version 2>$null
    if (-not $codeVersion) {
        throw "VS Code/Cursor não encontrado"
    }
    Write-Host "✅ VS Code/Cursor encontrado" -ForegroundColor Green
} catch {
    Write-Host "❌ VS Code/Cursor não encontrado no PATH" -ForegroundColor Red
    Write-Host "💡 Certifique-se de que o VS Code/Cursor está instalado e 'code' está no PATH" -ForegroundColor Yellow
    exit 1
}

# Lista de extensões essenciais baseada nas suas configurações
$Extensions = @(
    # 🐍 Python Development
    "ms-python.python",
    "ms-python.vscode-pylance",
    "ms-python.debugpy",
    "ms-python.isort",
    "charliermarsh.ruff",

    # 📊 Data Science & Jupyter
    "ms-toolsai.jupyter",
    "ms-toolsai.jupyter-keymap",

    # 🔧 Development Tools
    "ms-vscode.vscode-json",
    "yzhang.markdown-all-in-one",
    "esbenp.prettier-vscode",
    "ms-vscode.vscode-typescript-next",
    "bradlc.vscode-tailwindcss",

    # 🐳 Docker & Containers
    "ms-azuretools.vscode-docker",
    "ms-kubernetes-tools.vscode-kubernetes-tools",

    # 🔄 Git & Version Control
    "eamodio.gitlens",
    "donjayamanne.githistory",
    "github.vscode-github-actions",
    "github.vscode-pull-request-github",
    "vivaxy.vscode-conventional-commits",

    # 🎨 Themes & Icons
    "pkief.material-icon-theme",
    "github.github-vscode-theme",
    "johnpapa.vscode-peacock",

    # 🧪 Testing
    "littlefoxteam.vscode-python-test-adapter",
    "firsttris.vscode-jest-runner",
    "orta.vscode-jest",
    "vitest.explorer",

    # 🚀 AI & Productivity
    "GitHub.copilot",
    "GitHub.copilot-chat",
    "visualstudioexptteam.vscodeintellicode",
    "visualstudioexptteam.intellicode-api-usage-examples",

    # 🔍 Code Quality & Analysis
    "sonarsource.sonarlint-vscode",
    "streetsidesoftware.code-spell-checker",
    "streetsidesoftware.code-spell-checker-portuguese-brazilian",
    "sourcery.sourcery",

    # 🎯 Language Support
    "redhat.vscode-yaml",
    "tamasfe.even-better-toml",
    "ms-vscode.makefile-tools",
    "naumovs.color-highlight",
    "oderwat.indent-rainbow",

    # 🛠️ Utilities
    "chakrounanas.turbo-console-log",
    "christian-kohler.path-intellisense",
    "gruntfuggly.todo-tree",
    "wallabyjs.quokka-vscode",
    "xyz.local-history",

    # 🌐 Web Development
    "ms-vscode.live-server",
    "vue.volar",
    "zignd.html-css-class-completion",

    # 📊 Database & APIs
    "cweijan.dbclient-jdbc",
    "cweijan.vscode-redis-client",
    "humao.rest-client",

    # 🔧 Advanced Tools
    "adpyke.codesnap",
    "jebbs.plantuml",
    "quicktype.quicktype",
    "tim-koehler.helm-intellisense"
)

# Contadores
$Total = $Extensions.Count
$Installed = 0
$Failed = 0

Write-Host "📦 Total de extensões a instalar: $Total" -ForegroundColor Blue
Write-Host ""

# Instalar cada extensão
foreach ($extension in $Extensions) {
    Write-Host "📥 Instalando $extension... " -NoNewline

    try {
        if ($Force) {
            code --install-extension $extension --force 2>$null
        } else {
            code --install-extension $extension 2>$null
        }

        Write-Host "✅ Sucesso" -ForegroundColor Green
        $Installed++
    } catch {
        Write-Host "❌ Falha" -ForegroundColor Red
        $Failed++
    }

    # Pequena pausa para evitar sobrecarga
    Start-Sleep -Milliseconds 500
}

Write-Host ""
Write-Host "📊 Resumo da instalação:" -ForegroundColor Blue
Write-Host "✅ Instaladas com sucesso: $Installed" -ForegroundColor Green
Write-Host "❌ Falhas: $Failed" -ForegroundColor Red
Write-Host "📦 Total: $Total" -ForegroundColor Blue

if ($Failed -eq 0) {
    Write-Host ""
    Write-Host "🎉 Todas as extensões foram instaladas com sucesso!" -ForegroundColor Green
    Write-Host "💡 Reinicie o VS Code/Cursor para aplicar todas as configurações" -ForegroundColor Yellow
} else {
    Write-Host ""
    Write-Host "⚠️  Algumas extensões falharam na instalação" -ForegroundColor Yellow
    Write-Host "💡 Tente instalar manualmente as extensões que falharam" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🔧 Próximos passos:" -ForegroundColor Blue
Write-Host "1. Reinicie o VS Code/Cursor"
Write-Host "2. Configure o Python interpreter (Ctrl+Shift+P > Python: Select Interpreter)"
Write-Host "3. Execute 'uv sync' para instalar dependências Python"
Write-Host "4. Configure o pre-commit: uv run pre-commit install"
Write-Host "5. Aproveite suas configurações personalizadas! 🎨"
