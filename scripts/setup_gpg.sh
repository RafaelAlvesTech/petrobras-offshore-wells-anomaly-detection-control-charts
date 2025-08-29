#!/bin/bash

# 🚀 Script de Configuração GPG para Petrobras Offshore Wells Project
# Este script configura a assinatura GPG para todos os commits

set -e

echo "🔐 Configurando Assinatura GPG para o Projeto Petrobras Offshore Wells..."

# Verificar se GPG está instalado
if ! command -v gpg &> /dev/null; then
    echo "❌ GPG não está instalado. Instale o GPG primeiro."
    exit 1
fi

# Verificar se há chaves GPG
if ! gpg --list-secret-keys --keyid-format LONG | grep -q "sec"; then
    echo "❌ Nenhuma chave GPG encontrada. Crie uma chave GPG primeiro."
    exit 1
fi

# Obter a chave principal
MAIN_KEY=$(gpg --list-secret-keys --keyid-format LONG | grep "sec" | head -1 | awk '{print $2}' | cut -d'/' -f2)

if [ -z "$MAIN_KEY" ]; then
    echo "❌ Não foi possível obter a chave GPG principal."
    exit 1
fi

echo "🔑 Chave GPG encontrada: $MAIN_KEY"

# Configurar Git globalmente
echo "⚙️  Configurando Git globalmente..."
git config --global user.signingkey "$MAIN_KEY"
git config --global commit.gpgsign true
git config --global tag.gpgsign true
git config --global gpg.program gpg

# Configurar Git localmente para este repositório
echo "🏠 Configurando Git localmente..."
git config user.signingkey "$MAIN_KEY"
git config commit.gpgsign true
git config tag.gpgsign true

echo "✅ Configuração GPG concluída!"
echo ""
echo "📋 Resumo da configuração:"
echo "   Chave GPG: $MAIN_KEY"
echo "   Assinatura de commits: ✅"
echo "   Assinatura de tags: ✅"
echo ""
echo "🔍 Verificando configuração..."

# Verificar configuração
echo "📊 Configuração Git Global:"
git config --global --list | grep -E "(signingkey|gpgsign|gpg\.program)" || echo "   Nenhuma configuração GPG encontrada globalmente"

echo ""
echo "📊 Configuração Git Local:"
git config --list | grep -E "(signingkey|gpgsign|gpg\.program)" || echo "   Nenhuma configuração GPG encontrada localmente"

echo ""
echo "🎯 Para testar a assinatura, faça um commit:"
echo "   git commit -m 'test: testando assinatura GPG'"
echo ""
echo "🔑 Para adicionar a chave ao GitHub, copie a chave pública acima e adicione em:"
echo "   https://github.com/settings/keys"
echo ""
echo "📝 Chave pública GPG:"
gpg --armor --export "$MAIN_KEY"
