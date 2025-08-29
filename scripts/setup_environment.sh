#!/bin/bash

# 🛢️ Petrobras Offshore Wells Anomaly Detection - Setup Script
# Script para configurar o ambiente de desenvolvimento

set -e

echo "🚀 Configurando ambiente Petrobras Offshore Wells Anomaly Detection..."
echo "================================================================"

# Verificar se o uv está instalado
if ! command -v uv &> /dev/null; then
    echo "❌ uv não está instalado. Instalando..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source ~/.bashrc
else
    echo "✅ uv já está instalado: $(uv --version)"
fi

# Verificar se o Python 3.11+ está disponível
PYTHON_VERSION=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
if [[ $(echo "$PYTHON_VERSION >= 3.11" | bc -l) -eq 0 ]]; then
    echo "❌ Python 3.11+ é necessário. Versão atual: $PYTHON_VERSION"
    exit 1
else
    echo "✅ Python $PYTHON_VERSION detectado"
fi

# Criar ambiente virtual se não existir
if [ ! -d ".venv" ]; then
    echo "🔧 Criando ambiente virtual..."
    uv venv
else
    echo "✅ Ambiente virtual já existe"
fi

# Ativar ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source .venv/bin/activate

# Sincronizar dependências
echo "📦 Instalando dependências..."
uv sync

# Instalar pre-commit hooks
echo "🔧 Configurando pre-commit hooks..."
pre-commit install

# Verificar instalações
echo "🔍 Verificando instalações..."
echo "Python: $(which python)"
echo "Jupyter: $(jupyter --version)"
echo "Polars: $(python -c 'import polars; print(polars.__version__)')"
echo "PyTorch: $(python -c 'import torch; print(torch.__version__)')"

# Criar arquivo .env se não existir
if [ ! -f ".env" ]; then
    echo "🔧 Criando arquivo .env..."
    cp env.example .env
    echo "✅ Arquivo .env criado. Configure suas variáveis de ambiente."
fi

echo ""
echo "🎉 Ambiente configurado com sucesso!"
echo "================================================================"
echo ""
echo "📚 Próximos passos:"
echo "1. Configure suas variáveis de ambiente no arquivo .env"
echo "2. Ative o ambiente virtual: source .venv/bin/activate"
echo "3. Execute notebooks: jupyter lab notebooks/"
echo "4. Execute testes: pytest tests/"
echo ""
echo "🚀 Para começar a desenvolver:"
echo "   source .venv/bin/activate"
echo "   jupyter lab notebooks/"
echo ""
