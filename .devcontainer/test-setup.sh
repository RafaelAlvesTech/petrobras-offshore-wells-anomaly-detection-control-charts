#!/bin/bash

# =============================================================================
# 🛢️ PETROBRAS OFFSHORE WELLS ANOMALY DETECTION - TEST SETUP
# =============================================================================
# Script para testar a configuração completa do DevContainer
# =============================================================================

set -e

echo "🧪 Testando configuração do DevContainer..."
echo "=========================================="

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para testar comandos
test_command() {
    local cmd="$1"
    local description="$2"

    echo -n "🔍 Testando $description... "

    if command -v "$cmd" >/dev/null 2>&1; then
        echo -e "${GREEN}✅ OK${NC}"
        return 0
    else
        echo -e "${RED}❌ FALHOU${NC}"
        return 1
    fi
}

# Função para testar variáveis de ambiente
test_env_var() {
    local var="$1"
    local description="$2"

    echo -n "🔍 Testando $description... "

    if [ -n "${!var}" ]; then
        echo -e "${GREEN}✅ OK${NC} (${!var})"
        return 0
    else
        echo -e "${RED}❌ FALHOU${NC}"
        return 1
    fi
}

# Função para testar diretórios
test_directory() {
    local dir="$1"
    local description="$2"

    echo -n "🔍 Testando $description... "

    if [ -d "$dir" ]; then
        echo -e "${GREEN}✅ OK${NC} ($dir)"
        return 0
    else
        echo -e "${RED}❌ FALHOU${NC}"
        return 1
    fi
}

# Função para testar arquivos
test_file() {
    local file="$1"
    local description="$2"

    echo -n "🔍 Testando $description... "

    if [ -f "$file" ]; then
        echo -e "${GREEN}✅ OK${NC} ($file)"
        return 0
    else
        echo -e "${RED}❌ FALHOU${NC}"
        return 1
    fi
}

# Contadores
total_tests=0
passed_tests=0

# Função para executar teste e contar resultados
run_test() {
    local test_func="$1"
    local arg1="$2"
    local arg2="$3"

    total_tests=$((total_tests + 1))

    if $test_func "$arg1" "$arg2"; then
        passed_tests=$((passed_tests + 1))
    fi
}

echo ""
echo -e "${BLUE}📋 TESTANDO FERRAMENTAS BÁSICAS${NC}"
echo "=================================="

# Testar ferramentas básicas
run_test test_command "python3" "Python 3"
run_test test_command "pip3" "pip3"
run_test test_command "uv" "uv (gerenciador de dependências)"
run_test test_command "git" "Git"
run_test test_command "docker" "Docker"
run_test test_command "kubectl" "Kubernetes CLI"
run_test test_command "helm" "Helm"
run_test test_command "aws" "AWS CLI"
run_test test_command "az" "Azure CLI"
run_test test_command "gcloud" "Google Cloud CLI"

echo ""
echo -e "${BLUE}📋 TESTANDO FERRAMENTAS DE DATA SCIENCE${NC}"
echo "============================================="

# Testar ferramentas de data science
run_test test_command "jupyter" "Jupyter"
run_test test_command "mlflow" "MLflow"
run_test test_command "tensorboard" "TensorBoard"

echo ""
echo -e "${BLUE}📋 TESTANDO CONFIGURAÇÃO DO ZSH${NC}"
echo "=================================="

# Testar configuração do Zsh
run_test test_command "zsh" "Zsh"
run_test test_file "$HOME/.oh-my-zsh/oh-my-zsh.sh" "Oh My Zsh"
run_test test_file "$HOME/.zshrc.custom" "Configuração customizada do Zsh"
run_test test_directory "$HOME/.oh-my-zsh/custom/plugins/zsh-autosuggestions" "Plugin zsh-autosuggestions"
run_test test_directory "$HOME/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting" "Plugin zsh-syntax-highlighting"

echo ""
echo -e "${BLUE}📋 TESTANDO VARIÁVEIS DE AMBIENTE${NC}"
echo "===================================="

# Testar variáveis de ambiente
run_test test_env_var "PROJECT_NAME" "PROJECT_NAME"
run_test test_env_var "PROJECT_ROOT" "PROJECT_ROOT"
run_test test_env_var "DATA_DIR" "DATA_DIR"
run_test test_env_var "MODELS_DIR" "MODELS_DIR"
run_test test_env_var "NOTEBOOKS_DIR" "NOTEBOOKS_DIR"
run_test test_env_var "SRC_DIR" "SRC_DIR"
run_test test_env_var "LOGS_DIR" "LOGS_DIR"
run_test test_env_var "MLFLOW_TRACKING_URI" "MLFLOW_TRACKING_URI"
run_test test_env_var "MLFLOW_EXPERIMENT_NAME" "MLFLOW_EXPERIMENT_NAME"
run_test test_env_var "TENSORBOARD_LOG_DIR" "TENSORBOARD_LOG_DIR"

echo ""
echo -e "${BLUE}📋 TESTANDO ESTRUTURA DE DIRETÓRIOS${NC}"
echo "======================================="

# Testar estrutura de diretórios
run_test test_directory "$PROJECT_ROOT" "Diretório raiz do projeto"
run_test test_directory "$DATA_DIR" "Diretório de dados"
run_test test_directory "$MODELS_DIR" "Diretório de modelos"
run_test test_directory "$NOTEBOOKS_DIR" "Diretório de notebooks"
run_test test_directory "$SRC_DIR" "Diretório de código fonte"
run_test test_directory "$LOGS_DIR" "Diretório de logs"
run_test test_directory "$DATA_DIR/raw" "Diretório de dados brutos"
run_test test_directory "$DATA_DIR/processed" "Diretório de dados processados"
run_test test_directory "$LOGS_DIR/tensorboard" "Diretório do TensorBoard"

echo ""
echo -e "${BLUE}📋 TESTANDO CONFIGURAÇÕES DO JUPYTER${NC}"
echo "======================================="

# Testar configurações do Jupyter
run_test test_file "$HOME/.jupyter/jupyter_lab_config.py" "Configuração do Jupyter Lab"
run_test test_command "jupyter" "Jupyter Lab"

echo ""
echo -e "${BLUE}📋 TESTANDO ALIASES E FUNÇÕES${NC}"
echo "==============================="

# Testar se os aliases estão funcionando
echo -n "🔍 Testando aliases do projeto... "
if alias pj >/dev/null 2>&1; then
    echo -e "${GREEN}✅ OK${NC}"
    passed_tests=$((passed_tests + 1))
else
    echo -e "${RED}❌ FALHOU${NC}"
fi
total_tests=$((total_tests + 1))

echo -n "🔍 Testando função project_status... "
if type project_status >/dev/null 2>&1; then
    echo -e "${GREEN}✅ OK${NC}"
    passed_tests=$((passed_tests + 1))
else
    echo -e "${RED}❌ FALHOU${NC}"
fi
total_tests=$((total_tests + 1))

echo ""
echo -e "${BLUE}📋 TESTANDO DEPENDÊNCIAS PYTHON${NC}"
echo "=================================="

# Testar importação de bibliotecas Python
test_python_import() {
    local module="$1"
    local description="$2"

    echo -n "🔍 Testando $description... "

    if python3 -c "import $module" >/dev/null 2>&1; then
        echo -e "${GREEN}✅ OK${NC}"
        return 0
    else
        echo -e "${RED}❌ FALHOU${NC}"
        return 1
    fi
}

run_test test_python_import "pandas" "Pandas"
run_test test_python_import "numpy" "NumPy"
run_test test_python_import "sklearn" "Scikit-learn"
run_test test_python_import "polars" "Polars"
run_test test_python_import "matplotlib" "Matplotlib"
run_test test_python_import "seaborn" "Seaborn"
run_test test_python_import "jupyter" "Jupyter"
run_test test_python_import "mlflow" "MLflow"

echo ""
echo -e "${BLUE}📋 TESTANDO CONECTIVIDADE DE REDE${NC}"
echo "====================================="

# Testar conectividade de rede
test_network() {
    local url="$1"
    local description="$2"

    echo -n "🔍 Testando $description... "

    if curl -s --connect-timeout 5 "$url" >/dev/null 2>&1; then
        echo -e "${GREEN}✅ OK${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠️  AVISO${NC} (pode ser normal se não estiver rodando)"
        return 1
    fi
}

run_test test_network "http://localhost:8888" "Jupyter Lab (porta 8888)"
run_test test_network "http://localhost:5000" "MLflow UI (porta 5000)"
run_test test_network "http://localhost:6006" "TensorBoard (porta 6006)"

echo ""
echo -e "${BLUE}📊 RESUMO DOS TESTES${NC}"
echo "===================="

echo "Total de testes: $total_tests"
echo -e "Testes aprovados: ${GREEN}$passed_tests${NC}"
echo -e "Testes falharam: ${RED}$((total_tests - passed_tests))${NC}"

if [ $passed_tests -eq $total_tests ]; then
    echo ""
    echo -e "${GREEN}🎉 TODOS OS TESTES PASSARAM!${NC}"
    echo -e "${GREEN}✅ O DevContainer está configurado corretamente.${NC}"
    exit 0
elif [ $passed_tests -gt $((total_tests * 80 / 100)) ]; then
    echo ""
    echo -e "${YELLOW}⚠️  MAIORIA DOS TESTES PASSOU${NC}"
    echo -e "${YELLOW}🔧 Algumas configurações podem precisar de ajustes.${NC}"
    exit 1
else
    echo ""
    echo -e "${RED}❌ MUITOS TESTES FALHARAM${NC}"
    echo -e "${RED}🔧 A configuração do DevContainer precisa ser corrigida.${NC}"
    exit 2
fi
