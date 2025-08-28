#!/usr/bin/env python3
"""
🤖 Petrobras Offshore Wells Anomaly Detection - Claude Code Extensions Installer
🚀 Script Python cross-platform para instalar extensões específicas para Claude Code
"""

import subprocess
import sys


# Cores para output no terminal
class Colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def print_header():
    """Imprime o cabeçalho do script"""
    print(f"{Colors.HEADER}🛢️  Petrobras Offshore Wells Anomaly Detection{Colors.ENDC}")
    print(f"{Colors.HEADER}🤖 Claude Code Extensions Installer (Python){Colors.ENDC}")
    print(
        f"{Colors.HEADER}=================================================={Colors.ENDC}"
    )


def check_code_cli():
    """Verifica se o VS Code CLI está disponível"""
    try:
        result = subprocess.run(
            ["code", "--version"], capture_output=True, text=True, check=True
        )
        version = result.stdout.strip().split("\n")[0]
        print(f"{Colors.OKGREEN}✅ VS Code CLI encontrado{Colors.ENDC}")
        print(f"{Colors.OKBLUE}📋 Versão: {version}{Colors.ENDC}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(
            f"{Colors.FAIL}❌ VS Code CLI não encontrado. Instale o VS Code primeiro.{Colors.ENDC}"
        )
        print(
            f"{Colors.WARNING}💡 Dica: Instale o VS Code e adicione 'code' ao PATH{Colors.ENDC}"
        )
        return False


def install_extension(extension_id, description=""):
    """Instala uma extensão específica"""
    try:
        subprocess.run(
            ["code", "--install-extension", extension_id],
            check=True,
            capture_output=True,
        )
        print(f"  ✅ {extension_id} - {description}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ❌ {extension_id} - Erro: {e}")
        return False


def install_extensions():
    """Instala todas as extensões necessárias"""
    print(
        f"\n{Colors.OKBLUE}🔌 Instalando extensões essenciais para Claude Code...{Colors.ENDC}"
    )

    # 🐍 Python Development
    print(f"\n{Colors.OKGREEN}🐍 Instalando extensões Python...{Colors.ENDC}")
    python_extensions = [
        ("ms-python.python", "Suporte completo ao Python"),
        ("ms-python.vscode-pylance", "IntelliSense avançado para Python"),
        ("ms-python.debugpy", "Debugger Python"),
        ("ms-python.isort", "Organização de imports"),
        ("charliermarsh.ruff", "Linting e formatação rápida"),
    ]

    for ext_id, desc in python_extensions:
        install_extension(ext_id, desc)

    # 🤖 Claude Code - Extensões Específicas para IA e ML
    print(
        f"\n{Colors.HEADER}🤖 Instalando extensões específicas para Claude Code...{Colors.ENDC}"
    )
    claude_extensions = [
        ("ms-python.black-formatter", "Formatação automática Black"),
        ("ms-python.flake8", "Linting Flake8"),
        ("ms-python.mypy-type-checker", "Verificação de tipos MyPy"),
        ("ms-python.pylint", "Análise de código Pylint"),
        ("ms-python.autopep8", "Formatação automática PEP 8"),
    ]

    for ext_id, desc in claude_extensions:
        install_extension(ext_id, desc)

    # 📊 Data Science & Jupyter
    print(f"\n{Colors.OKCYAN}📊 Instalando extensões de Data Science...{Colors.ENDC}")
    ds_extensions = [
        ("ms-toolsai.jupyter", "Suporte completo ao Jupyter"),
        ("ms-toolsai.jupyter-keymap", "Atalhos para Jupyter"),
        ("ms-toolsai.jupyter-renderers", "Renderizadores para diferentes formatos"),
    ]

    for ext_id, desc in ds_extensions:
        install_extension(ext_id, desc)

    # 🔧 Development Tools
    print(
        f"\n{Colors.WARNING}🔧 Instalando ferramentas de desenvolvimento...{Colors.ENDC}"
    )
    dev_extensions = [
        ("ms-vscode.vscode-json", "Suporte ao JSON"),
        ("yzhang.markdown-all-in-one", "Editor Markdown avançado"),
        ("esbenp.prettier-vscode", "Formatador de código"),
    ]

    for ext_id, desc in dev_extensions:
        install_extension(ext_id, desc)

    # 🐳 Docker & Containers
    print(f"\n{Colors.OKBLUE}🐳 Instalando extensões Docker...{Colors.ENDC}")
    docker_extensions = [
        ("ms-azuretools.vscode-docker", "Suporte ao Docker"),
        ("ms-kubernetes-tools.vscode-kubernetes-tools", "Suporte ao Kubernetes"),
    ]

    for ext_id, desc in docker_extensions:
        install_extension(ext_id, desc)

    # 🔄 Git & Version Control
    print(f"\n{Colors.OKGREEN}🔄 Instalando extensões Git...{Colors.ENDC}")
    git_extensions = [
        ("eamodio.gitlens", "Git supercharged"),
        ("donjayamanne.githistory", "Histórico Git"),
        ("github.vscode-github-actions", "GitHub Actions"),
        ("github.vscode-pull-request-github", "Pull Requests GitHub"),
        ("vivaxy.vscode-conventional-commits", "Commits convencionais"),
    ]

    for ext_id, desc in git_extensions:
        install_extension(ext_id, desc)

    # 🎨 Themes & Icons
    print(f"\n{Colors.HEADER}🎨 Instalando temas e ícones...{Colors.ENDC}")
    theme_extensions = [
        ("pkief.material-icon-theme", "Ícones Material Design"),
        ("github.github-vscode-theme", "Tema GitHub"),
        ("johnpapa.vscode-peacock", "Cores personalizadas"),
    ]

    for ext_id, desc in theme_extensions:
        install_extension(ext_id, desc)

    # 🧪 Testing
    print(f"\n{Colors.FAIL}🧪 Instalando extensões de teste...{Colors.ENDC}")
    test_extensions = [
        ("littlefoxteam.vscode-python-test-adapter", "Test runner Python"),
        ("firsttris.vscode-jest-runner", "Test runner Jest"),
    ]

    for ext_id, desc in test_extensions:
        install_extension(ext_id, desc)

    # 🚀 AI & Productivity
    print(
        f"\n{Colors.OKCYAN}🚀 Instalando extensões de IA e produtividade...{Colors.ENDC}"
    )
    ai_extensions = [
        ("GitHub.copilot", "Assistente de IA para código"),
        ("GitHub.copilot-chat", "Chat com IA para desenvolvimento"),
        ("visualstudioexptteam.vscodeintellicode", "IntelliCode"),
        ("visualstudioexptteam.intellicode-api-usage-examples", "Exemplos de API"),
    ]

    for ext_id, desc in ai_extensions:
        install_extension(ext_id, desc)

    # 🔍 Code Quality & Analysis
    print(
        f"\n{Colors.WARNING}🔍 Instalando extensões de qualidade de código...{Colors.ENDC}"
    )
    quality_extensions = [
        ("sonarsource.sonarlint-vscode", "Análise de código SonarLint"),
        ("streetsidesoftware.code-spell-checker", "Verificador de ortografia"),
        (
            "streetsidesoftware.code-spell-checker-portuguese-brazilian",
            "Português brasileiro",
        ),
        ("sourcery.sourcery", "Refatoração automática"),
    ]

    for ext_id, desc in quality_extensions:
        install_extension(ext_id, desc)

    # 🎯 Language Support
    print(f"\n{Colors.OKGREEN}🎯 Instalando suporte a linguagens...{Colors.ENDC}")
    lang_extensions = [
        ("redhat.vscode-yaml", "Suporte ao YAML"),
        ("tamasfe.even-better-toml", "Suporte ao TOML"),
        ("ms-vscode.makefile-tools", "Suporte ao Makefile"),
        ("naumovs.color-highlight", "Destaque de cores"),
        ("oderwat.indent-rainbow", "Indentação colorida"),
    ]

    for ext_id, desc in lang_extensions:
        install_extension(ext_id, desc)

    # 🛠️ Utilities
    print(f"\n{Colors.OKBLUE}🛠️ Instalando utilitários...{Colors.ENDC}")
    util_extensions = [
        ("chakrounanas.turbo-console-log", "Console log rápido"),
        ("christian-kohler.path-intellisense", "Autocompletar de caminhos"),
        ("gruntfuggly.todo-tree", "Árvore de TODOs"),
        ("wallabyjs.quokka-vscode", "Quokka.js"),
        ("xyz.local-history", "Histórico local"),
    ]

    for ext_id, desc in util_extensions:
        install_extension(ext_id, desc)

    # 🌐 Web Development
    print(
        f"\n{Colors.OKBLUE}🌐 Instalando extensões de desenvolvimento web...{Colors.ENDC}"
    )
    web_extensions = [
        ("ms-vscode.live-server", "Live Server"),
        ("vue.volar", "Suporte ao Vue"),
        ("zignd.html-css-class-completion", "Autocompletar CSS"),
    ]

    for ext_id, desc in web_extensions:
        install_extension(ext_id, desc)

    # 📊 Database & APIs
    print(
        f"\n{Colors.OKCYAN}📊 Instalando extensões de banco de dados e APIs...{Colors.ENDC}"
    )
    db_extensions = [
        ("cweijan.dbclient-jdbc", "Cliente JDBC"),
        ("cweijan.vscode-redis-client", "Cliente Redis"),
        ("humao.rest-client", "Cliente REST"),
    ]

    for ext_id, desc in db_extensions:
        install_extension(ext_id, desc)

    # 🔧 Advanced Tools
    print(f"\n{Colors.WARNING}🔧 Instalando ferramentas avançadas...{Colors.ENDC}")
    advanced_extensions = [
        ("adpyke.codesnap", "Captura de código"),
        ("jebbs.plantuml", "PlantUML"),
        ("quicktype.quicktype", "QuickType"),
        ("tim-koehler.helm-intellisense", "Helm IntelliSense"),
    ]

    for ext_id, desc in advanced_extensions:
        install_extension(ext_id, desc)


def print_next_steps():
    """Imprime os próximos passos"""
    print(
        f"\n{Colors.OKGREEN}✅ Todas as extensões foram instaladas com sucesso!{Colors.ENDC}"
    )
    print(f"\n{Colors.WARNING}🎯 Próximos passos:{Colors.ENDC}")
    print("1. Reinicie o VS Code/Cursor")
    print("2. Verifique se as extensões estão ativas")
    print("3. Configure o Python interpreter para ./.venv/bin/python")
    print("4. Execute 'uv sync' para sincronizar dependências")
    print(
        f"\n{Colors.OKCYAN}🚀 Configurações específicas para Claude Code já estão no .vscode/settings.json{Colors.ENDC}"
    )
    print(
        f"{Colors.OKCYAN}📚 Consulte o README.md para mais detalhes sobre as configurações{Colors.ENDC}"
    )
    print(
        f"\n{Colors.OKGREEN}🛢️  Petrobras Offshore Wells Anomaly Detection - Claude Code Ready!{Colors.ENDC}"
    )


def main():
    """Função principal"""
    print_header()

    if not check_code_cli():
        sys.exit(1)

    install_extensions()
    print_next_steps()


if __name__ == "__main__":
    main()
