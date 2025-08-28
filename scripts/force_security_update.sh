#!/bin/bash

# Script para forçar atualização de dependências de segurança específicas
# Este script resolve as vulnerabilidades conhecidas do Dependabot

set -e

echo "🚀 Forçando atualização de dependências de segurança..."

# Verificar se estamos no diretório correto
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Erro: pyproject.toml não encontrado. Execute este script do diretório raiz do projeto."
    exit 1
fi

# Verificar se uv está instalado
echo "🔄 Verificando versão do uv..."
if ! uv --version > /dev/null 2>&1; then
    echo "❌ Erro: uv não está instalado ou não está no PATH"
    exit 1
fi
echo "✅ uv encontrado"

# Backup do pyproject.toml original
cp pyproject.toml pyproject.toml.backup
echo "💾 Backup do pyproject.toml criado"

# Atualizar dependências específicas de segurança
echo -e "\n🔒 Atualizando dependências de segurança..."

# Forçar atualização de dependências vulneráveis
echo "🔄 Atualizando certifi..."
uv add "certifi>=2024.2.2" --upgrade

echo "🔄 Atualizando charset-normalizer..."
uv add "charset-normalizer>=3.3.2" --upgrade

echo "🔄 Atualizando requests..."
uv add "requests>=2.31.0" --upgrade

echo "🔄 Atualizando urllib3..."
uv add "urllib3>=2.0.7" --upgrade

echo "🔄 Atualizando cffi..."
uv add "cffi>=1.17.1" --upgrade

# Sincronizar todas as dependências
echo -e "\n🔄 Sincronizando todas as dependências..."
if ! uv sync; then
    echo "⚠️  Sincronização falhou, tentando com estratégia de fallback..."
    if ! uv sync --index-strategy unsafe-best-match; then
        echo "❌ Falha na sincronização. Restaurando backup..."
        mv pyproject.toml.backup pyproject.toml
        exit 1
    fi
fi

# Verificar vulnerabilidades
echo -e "\n🔍 Verificando vulnerabilidades..."
if ! uv pip audit; then
    echo "⚠️  Vulnerabilidades ainda podem existir"
fi

# Regenerar requirements.txt
echo -e "\n📝 Regenerando requirements.txt..."
if ! uv export --frozen --output-file=requirements.txt; then
    echo "❌ Falha ao exportar requirements.txt"
    exit 1
fi

# Limpar backup
rm pyproject.toml.backup
echo "🗑️  Backup removido"

echo -e "\n🎉 Atualização forçada de segurança concluída!"
echo -e "\n📋 Próximos passos:"
echo "1. Teste o projeto: uv run pytest"
echo "2. Verifique se não há quebras: uv run python -c 'import src'"
echo "3. Commit as mudanças: git add . && git commit -m 'chore(deps): force security updates'"
echo "4. Push para o repositório: git push"

echo -e "\n🔍 Verificando versões das dependências de segurança:"
uv pip show certifi charset-normalizer requests urllib3
