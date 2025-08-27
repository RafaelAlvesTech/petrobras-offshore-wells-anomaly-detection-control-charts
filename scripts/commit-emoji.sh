#!/bin/bash

# 🛢️ Petrobras Offshore Wells - Commit Helper Script
# Script para facilitar commits convencionais com emojis

echo "🛢️ Petrobras Offshore Wells - Commit Helper"
echo "=============================================="
echo ""

# Função para mostrar tipos de commit
show_commit_types() {
    echo "📋 Tipos de commit disponíveis:"
    echo "  🚀 feat     - Nova funcionalidade"
    echo "  🐛 fix      - Correção de bug"
    echo "  📚 docs     - Documentação"
    echo "  🎨 style    - Formatação de código"
    echo "  ♻️ refactor - Refatoração de código"
    echo "  ⚡ perf     - Melhorias de performance"
    echo "  🧪 test     - Adição ou correção de testes"
    echo "  🔨 build    - Mudanças no sistema de build"
    echo "  👷 ci       - Mudanças em CI/CD"
    echo "  🔧 chore    - Tarefas de manutenção"
    echo "  ⏪ revert   - Reverter commit anterior"
    echo "  📊 data     - Mudanças em datasets ou dados"
    echo "  🤖 model    - Mudanças em modelos de ML/DL"
    echo "  📈 analysis - Análises e experimentos"
    echo ""
}

# Função para mostrar escopos sugeridos
show_scopes() {
    echo "🎯 Escopos sugeridos:"
    echo "  - anomaly-detection: funcionalidades de detecção de anomalias"
    echo "  - data-processing: processamento e limpeza de dados"
    echo "  - models: modelos de machine learning"
    echo "  - utils: utilitários e funções auxiliares"
    echo "  - tests: testes automatizados"
    echo "  - docs: documentação"
    echo "  - ci: integração contínua"
    echo "  - deps: dependências"
    echo "  - notebooks: notebooks Marimo"
    echo "  - scripts: scripts de automação"
    echo ""
}

# Função para gerar commit
generate_commit() {
    echo "🚀 Gerador de Commit Convencional"
    echo "=================================="
    echo ""

    show_commit_types
    show_scopes

    echo "💡 Exemplos de uso:"
    echo "  🚀 feat(anomaly-detection): implementa modelo TranAD"
    echo "  🐛 fix(data-processing): corrige erro na normalização"
    echo "  📚 docs(readme): atualiza instruções de instalação"
    echo "  🎨 style(src): aplica formatação com ruff"
    echo "  ♻️ refactor(models): refatora arquitetura do LSTM-VAE"
    echo "  ⚡ perf(data): otimiza carregamento com Polars"
    echo ""

    echo "📝 Dicas para commits:"
    echo "  - Use imperativo na descrição ('adiciona' não 'adicionado')"
    echo "  - Primeira letra minúscula"
    echo "  - Sem ponto final"
    echo "  - Máximo 72 caracteres no título"
    echo "  - Use emoji apropriado para o tipo"
    echo ""

    echo "🔗 Recursos adicionais:"
    echo "  - Template de commit: .gitmessage"
    echo "  - Configuração: .commitlintrc.json"
    echo "  - Pre-commit hooks configurados"
    echo ""
}

# Função para configurar git
setup_git() {
    echo "⚙️ Configurando Git para commits convencionais..."

    # Configurar template de commit
    if [ -f ".gitmessage" ]; then
        git config commit.template .gitmessage
        echo "✅ Template de commit configurado"
    else
        echo "❌ Arquivo .gitmessage não encontrado"
    fi

    # Verificar configurações
    echo ""
    echo "🔍 Configurações atuais do Git:"
    echo "Template de commit: $(git config commit.template)"
    echo ""
}

# Menu principal
case "${1:-help}" in
    "types"|"tipos")
        show_commit_types
        ;;
    "scopes"|"escopos")
        show_scopes
        ;;
    "generate"|"gerar")
        generate_commit
        ;;
    "setup"|"configurar")
        setup_git
        ;;
    "help"|"ajuda"|*)
        echo "🛢️ Petrobras Offshore Wells - Commit Helper"
        echo "=============================================="
        echo ""
        echo "Uso: $0 [comando]"
        echo ""
        echo "Comandos disponíveis:"
        echo "  types|tipos      - Mostra tipos de commit"
        echo "  scopes|escopos   - Mostra escopos sugeridos"
        echo "  generate|gerar   - Mostra guia completo"
        echo "  setup|configurar - Configura Git para commits convencionais"
        echo "  help|ajuda       - Mostra esta ajuda"
        echo ""
        echo "Exemplo: $0 generate"
        echo ""
        ;;
esac
