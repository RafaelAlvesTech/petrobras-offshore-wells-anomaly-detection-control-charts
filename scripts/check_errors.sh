#!/bin/bash

# Script para verificar erros específicos no ambiente WSL2

echo "🔍 Verificando erros específicos no ambiente..."
echo "=============================================="

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

# 1. Verificar se há processos do Cursor travados
echo ""
echo "1. 🔄 Verificando processos do Cursor..."
CURSOR_PROCESSES=$(ps aux | grep -i cursor | grep -v grep | wc -l)
if [ $CURSOR_PROCESSES -gt 0 ]; then
    print_success "Cursor está rodando ($CURSOR_PROCESSES processos)"
else
    print_warning "Nenhum processo do Cursor encontrado"
fi

# 2. Verificar uso de memória alto
echo ""
echo "2. 💾 Verificando uso de memória..."
MEMORY_USAGE=$(free | grep Mem | awk '{printf "%.1f", $3/$2 * 100.0}')
if (( $(echo "$MEMORY_USAGE > 80" | bc -l) )); then
    print_warning "Uso de memória alto: ${MEMORY_USAGE}%"
else
    print_success "Uso de memória normal: ${MEMORY_USAGE}%"
fi

# 3. Verificar se há arquivos de lock
echo ""
echo "3. 🔒 Verificando arquivos de lock..."
LOCK_FILES=$(find . -name "*.lock" -o -name ".lock" 2>/dev/null | wc -l)
if [ $LOCK_FILES -gt 0 ]; then
    print_warning "Encontrados $LOCK_FILES arquivos de lock"
    find . -name "*.lock" -o -name ".lock" 2>/dev/null | head -5
else
    print_success "Nenhum arquivo de lock encontrado"
fi

# 4. Verificar permissões de arquivos
echo ""
echo "4. 📁 Verificando permissões..."
if [ -w "." ]; then
    print_success "Diretório atual é gravável"
else
    print_error "Diretório atual não é gravável"
fi

# 5. Verificar se o ambiente virtual está ativo
echo ""
echo "5. 🐍 Verificando ambiente Python..."
if [ -n "$VIRTUAL_ENV" ]; then
    print_success "Ambiente virtual ativo: $VIRTUAL_ENV"
else
    print_warning "Ambiente virtual não está ativo"
fi

# 6. Verificar se há erros no git
echo ""
echo "6. 📝 Verificando status do Git..."
if git status &>/dev/null; then
    print_success "Git está funcionando"
    UNCOMMITTED=$(git status --porcelain | wc -l)
    if [ $UNCOMMITTED -gt 0 ]; then
        print_info "Há $UNCOMMITTED arquivos não commitados"
    fi
else
    print_error "Problemas com Git"
fi

# 7. Verificar se há problemas com Docker
echo ""
echo "7. 🐳 Verificando Docker..."
if docker info &>/dev/null; then
    print_success "Docker está funcionando"
    RUNNING_CONTAINERS=$(docker ps -q | wc -l)
    print_info "Containers rodando: $RUNNING_CONTAINERS"
else
    print_error "Docker não está funcionando"
fi

# 8. Verificar se há problemas com Jupyter
echo ""
echo "8. 📊 Verificando Jupyter..."
if command -v jupyter &>/dev/null; then
    print_success "Jupyter está instalado"
    if jupyter --version &>/dev/null; then
        print_success "Jupyter está funcionando"
    else
        print_warning "Jupyter instalado mas com problemas"
    fi
else
    print_error "Jupyter não está instalado"
fi

# 9. Verificar se há problemas com pre-commit
echo ""
echo "9. 🔧 Verificando pre-commit..."
if [ -f ".pre-commit-config.yaml" ]; then
    if pre-commit --version &>/dev/null; then
        print_success "Pre-commit está funcionando"
    else
        print_warning "Pre-commit configurado mas com problemas"
    fi
else
    print_info "Pre-commit não configurado"
fi

# 10. Verificar se há problemas com ruff
echo ""
echo "10. 🧹 Verificando Ruff..."
if command -v ruff &>/dev/null; then
    print_success "Ruff está instalado"
    if ruff --version &>/dev/null; then
        print_success "Ruff está funcionando"
    else
        print_warning "Ruff instalado mas com problemas"
    fi
else
    print_error "Ruff não está instalado"
fi

# 11. Verificar se há problemas com o devcontainer
echo ""
echo "11. 📦 Verificando devcontainer..."
if [ -f ".devcontainer/devcontainer.json" ]; then
    if python -m json.tool .devcontainer/devcontainer.json &>/dev/null; then
        print_success "devcontainer.json é válido"
    else
        print_error "devcontainer.json tem problemas de sintaxe"
    fi
else
    print_info "devcontainer.json não encontrado"
fi

# 12. Verificar se há problemas com o VS Code settings
echo ""
echo "12. ⚙️ Verificando VS Code settings..."
if [ -f ".vscode/settings.json" ]; then
    if python -m json.tool .vscode/settings.json &>/dev/null; then
        print_success "settings.json é válido"
    else
        print_error "settings.json tem problemas de sintaxe"
    fi
else
    print_info "settings.json não encontrado"
fi

# 13. Verificar se há problemas com o pyproject.toml
echo ""
echo "13. 📋 Verificando pyproject.toml..."
if [ -f "pyproject.toml" ]; then
    if python -c "import tomllib; tomllib.load(open('pyproject.toml', 'rb'))" &>/dev/null; then
        print_success "pyproject.toml é válido"
    else
        print_error "pyproject.toml tem problemas de sintaxe"
    fi
else
    print_error "pyproject.toml não encontrado"
fi

# 14. Verificar se há problemas com dependências
echo ""
echo "14. 📦 Verificando dependências..."
if [ -f "uv.lock" ]; then
    print_success "uv.lock encontrado"
    if uv sync --dry-run &>/dev/null; then
        print_success "Dependências estão sincronizadas"
    else
        print_warning "Problemas com sincronização de dependências"
    fi
else
    print_warning "uv.lock não encontrado"
fi

# 15. Verificar se há problemas com testes
echo ""
echo "15. 🧪 Verificando testes..."
if [ -d "tests" ]; then
    print_success "Diretório de testes encontrado"
    if python -m pytest --collect-only &>/dev/null; then
        print_success "Testes podem ser coletados"
    else
        print_warning "Problemas ao coletar testes"
    fi
else
    print_info "Diretório de testes não encontrado"
fi

echo ""
echo "🔍 Verificação completa!"
echo "========================"
echo ""
echo "💡 Se você encontrou erros específicos, execute:"
echo "   ./scripts/diagnose_wsl2.sh  # Diagnóstico completo"
echo "   ./scripts/setup_wsl2.sh     # Reconfigurar ambiente"
echo ""
echo "📚 Para mais ajuda, consulte:"
echo "   docs/WSL2_TROUBLESHOOTING.md"
