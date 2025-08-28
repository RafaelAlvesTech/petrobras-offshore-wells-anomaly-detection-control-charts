#!/bin/bash

# Script para atualizar dependências e resolver vulnerabilidades de segurança
# Este script atualiza as dependências Python para versões mais seguras.

set -e  # Para o script se qualquer comando falhar

echo "🚀 Iniciando atualização de dependências de segurança..."

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

# Atualizar dependências
echo -e "\n📦 Atualizando dependências..."

# Remover arquivo de lock antigo
if [ -f "uv.lock" ]; then
    rm uv.lock
    echo "🗑️  Arquivo uv.lock removido"
fi

    # Sincronizar dependências com estratégia de fallback
    echo "🔄 Sincronizando dependências com uv..."

    # Primeira tentativa: sincronização normal
    if uv sync; then
        echo "✅ Dependências sincronizadas com sucesso"
    else
        echo "⚠️  Primeira tentativa falhou, tentando com estratégia de fallback..."

        # Segunda tentativa: usar estratégia de melhor combinação
        if uv sync --index-strategy unsafe-best-match; then
            echo "✅ Dependências sincronizadas com estratégia de fallback"
        else
            echo "❌ Falha ao sincronizar dependências mesmo com fallback"
            exit 1
        fi
    fi

# Verificar vulnerabilidades
echo -e "\n🔍 Verificando vulnerabilidades..."
if ! uv pip audit; then
    echo "⚠️  Não foi possível executar auditoria de segurança ou foram encontradas vulnerabilidades"
fi

# Regenerar requirements.txt
echo -e "\n📝 Regenerando requirements.txt..."
if ! uv export --frozen --output-file=requirements.txt; then
    echo "❌ Falha ao exportar requirements.txt"
    exit 1
fi
echo "✅ requirements.txt regenerado com sucesso"

echo -e "\n🎉 Atualização de dependências concluída com sucesso!"
echo -e "\n📋 Próximos passos:"
echo "1. Teste o projeto: uv run pytest"
echo "2. Verifique se não há quebras: uv run python -m src"
echo "3. Commit as mudanças: git add . && git commit -m 'chore(deps): update dependencies for security'"
echo "4. Push para o repositório: git push"
