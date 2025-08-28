#!/usr/bin/env python3
"""
🛢️ Petrobras Offshore Wells Anomaly Detection - Extensions Installer
Script Python cross-platform para instalação automática das extensões essenciais do VS Code/Cursor
Baseado nas suas configurações pessoais do VSCode
"""

import subprocess
import sys
import platform
import time


# Cores para output (ANSI escape codes)
class Colors:
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[0;34m"
    NC = "\033[0m"  # No Color


def print_colored(text: str, color: str) -> None:
    """Imprime texto colorido"""
    print(f"{color}{text}{Colors.NC}")


def check_code_installed() -> bool:
    """Verifica se o comando 'code' está disponível"""
    try:
        subprocess.run(
            ["code", "--version"], capture_output=True, text=True, check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def install_extension(extension: str, force: bool = False) -> bool:
    """Instala uma extensão específica"""
    try:
        cmd = ["code", "--install-extension", extension]
        if force:
            cmd.append("--force")

        subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def get_extensions() -> list[str]:
    """Retorna a lista de extensões essenciais baseada nas suas configurações"""
    return [
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
        "tim-koehler.helm-intellisense",
    ]


def main():
    """Função principal"""
    print_colored("🚀 Instalando extensões essenciais para o projeto...", Colors.BLUE)
    print_colored(
        "💡 Baseado nas suas configurações pessoais do VSCode!", Colors.YELLOW
    )

    # Verificar se o code está instalado
    if not check_code_installed():
        print_colored("❌ VS Code/Cursor não encontrado no PATH", Colors.RED)
        print_colored(
            "💡 Certifique-se de que o VS Code/Cursor está instalado e 'code' está no PATH",
            Colors.YELLOW,
        )
        sys.exit(1)

    print_colored("✅ VS Code/Cursor encontrado", Colors.GREEN)

    # Obter extensões
    extensions = get_extensions()
    total = len(extensions)
    installed = 0
    failed = 0

    print_colored(f"📦 Total de extensões a instalar: {total}", Colors.BLUE)
    print()

    # Instalar cada extensão
    for extension in extensions:
        print(f"📥 Instalando {extension}... ", end="")

        if install_extension(extension, force=True):
            print_colored("✅ Sucesso", Colors.GREEN)
            installed += 1
        else:
            print_colored("❌ Falha", Colors.RED)
            failed += 1

        # Pequena pausa para evitar sobrecarga
        time.sleep(0.5)

    # Resumo
    print()
    print_colored("📊 Resumo da instalação:", Colors.BLUE)
    print_colored(f"✅ Instaladas com sucesso: {installed}", Colors.GREEN)
    print_colored(f"❌ Falhas: {failed}", Colors.RED)
    print_colored(f"📦 Total: {total}", Colors.BLUE)

    if failed == 0:
        print()
        print_colored(
            "🎉 Todas as extensões foram instaladas com sucesso!", Colors.GREEN
        )
        print_colored(
            "💡 Reinicie o VS Code/Cursor para aplicar todas as configurações",
            Colors.YELLOW,
        )
    else:
        print()
        print_colored("⚠️  Algumas extensões falharam na instalação", Colors.YELLOW)
        print_colored(
            "💡 Tente instalar manualmente as extensões que falharam", Colors.YELLOW
        )

    # Próximos passos
    print()
    print_colored("🔧 Próximos passos:", Colors.BLUE)
    print("1. Reinicie o VS Code/Cursor")
    print(
        "2. Configure o Python interpreter (Ctrl+Shift+P > Python: Select Interpreter)"
    )
    print("3. Execute 'uv sync' para instalar dependências Python")
    print("4. Configure o pre-commit: uv run pre-commit install")
    print("5. Aproveite suas configurações personalizadas! 🎨")

    # Informações específicas do sistema
    system = platform.system()
    if system == "Windows":
        print_colored(
            "💡 No Windows, você pode executar: .\\scripts\\install_extensions.ps1",
            Colors.YELLOW,
        )
    elif system == "Linux":
        print_colored(
            "💡 No Linux, você pode executar: chmod +x scripts/install_extensions.sh && ./scripts/install_extensions.sh",
            Colors.YELLOW,
        )
    elif system == "Darwin":  # macOS
        print_colored(
            "💡 No macOS, você pode executar: chmod +x scripts/install_extensions.sh && ./scripts/install_extensions.sh",
            Colors.YELLOW,
        )


if __name__ == "__main__":
    main()
