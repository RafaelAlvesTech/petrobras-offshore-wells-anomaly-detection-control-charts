#!/bin/bash

# 🔧 Script para Corrigir Problemas de GPG no WSL
# Este script resolve problemas comuns de GPG em ambientes WSL

set -e

echo "🔧 Corrigindo problemas de GPG no WSL..."

# Parar o agente GPG atual
echo "🛑 Parando agente GPG atual..."
gpgconf --kill gpg-agent 2>/dev/null || true

# Limpar configurações conflitantes
echo "🧹 Limpando configurações conflitantes..."
rm -f ~/.gnupg/gpg-agent.conf
rm -f ~/.gnupg/gpg.conf

# Criar configuração GPG otimizada para WSL
echo "⚙️  Criando configuração GPG otimizada para WSL..."
cat > ~/.gnupg/gpg.conf << 'EOF'
use-agent
default-key 3E2E96B458A47E2B
EOF

# Criar configuração do agente GPG otimizada para WSL
echo "🔐 Configurando agente GPG para WSL..."
cat > ~/.gnupg/gpg-agent.conf << 'EOF'
pinentry-program /usr/bin/pinentry-curses
default-cache-ttl 600
max-cache-ttl 7200
allow-loopback-pinentry
keep-display
EOF

# Configurar variáveis de ambiente
echo "🌍 Configurando variáveis de ambiente..."
echo 'export GPG_TTY=$(tty)' >> ~/.zshrc
echo 'export GPG_AGENT_INFO="$HOME/.gnupg/S.gpg-agent:0:1"' >> ~/.zshrc

# Recarregar configurações
echo "🔄 Recarregando configurações..."
export GPG_TTY=$(tty)
export GPG_AGENT_INFO="$HOME/.gnupg/S.gpg-agent:0:1"

# Iniciar agente GPG
echo "🚀 Iniciando agente GPG..."
gpg-agent --daemon

# Testar configuração
echo "🧪 Testando configuração GPG..."
echo "test" | gpg --clearsign --default-key 3E2E96B458A47E2B 2>/dev/null && echo "✅ GPG funcionando!" || echo "⚠️  GPG ainda com problemas"

echo ""
echo "📋 Configuração concluída!"
echo "🔄 Reinicie o terminal ou execute: source ~/.zshrc"
echo ""
echo "🔑 Para testar, tente fazer um commit:"
echo "   git commit -m 'test: testando GPG'"
echo ""
echo "📖 Se ainda houver problemas, consulte: docs/GPG_SETUP.md"
