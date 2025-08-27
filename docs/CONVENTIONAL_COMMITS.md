# 🛢️ Conventional Commits com Emojis - Petrobras Offshore Wells

## 📋 Visão Geral

Este projeto utiliza **Conventional Commits** com emojis para manter um histórico de commits organizado e semântico. Esta abordagem facilita:

- 📚 **Geração automática de changelogs**
- 🏷️ **Versionamento semântico automático**
- 🔍 **Histórico de mudanças legível**
- 🤖 **Automação de releases**
- 📊 **Análise de impacto das mudanças**

## 🚀 Tipos de Commit

### Funcionalidades e Melhorias
- **🚀 feat** - Nova funcionalidade
- **⚡ perf** - Melhorias de performance
- **📊 data** - Mudanças em datasets ou dados
- **🤖 model** - Mudanças em modelos de ML/DL
- **📈 analysis** - Análises e experimentos

### Correções e Manutenção
- **🐛 fix** - Correção de bug
- **♻️ refactor** - Refatoração de código
- **🔧 chore** - Tarefas de manutenção
- **🎨 style** - Formatação de código
- **📚 docs** - Documentação

### Infraestrutura e Qualidade
- **🧪 test** - Adição ou correção de testes
- **🔨 build** - Mudanças no sistema de build
- **👷 ci** - Mudanças em CI/CD
- **⏪ revert** - Reverter commit anterior

## 🎯 Escopos Recomendados

### Domínio Principal
- **anomaly-detection** - Funcionalidades de detecção de anomalias
- **data-processing** - Processamento e limpeza de dados
- **models** - Modelos de machine learning
- **analysis** - Análises exploratórias e experimentos

### Infraestrutura
- **utils** - Utilitários e funções auxiliares
- **tests** - Testes automatizados
- **docs** - Documentação
- **ci** - Integração contínua
- **deps** - Dependências
- **notebooks** - Notebooks Marimo
- **scripts** - Scripts de automação

## 📝 Formato do Commit

```
<emoji><tipo>(<escopo>): <descrição>

[corpo opcional]

[rodapé opcional]
```

### Exemplos Práticos

#### 🚀 Nova Funcionalidade
```bash
🚀 feat(anomaly-detection): implementa modelo TranAD para detecção de anomalias

- Adiciona implementação do modelo TranAD
- Configura hiperparâmetros otimizados para dados offshore
- Inclui métricas de avaliação (AUC-PR, F1-Score)
- Adiciona testes unitários para o modelo
- Documenta uso e parâmetros

Closes #123
```

#### 🐛 Correção de Bug
```bash
🐛 fix(data-processing): corrige erro na normalização de dados de pressão

- Corrige divisão por zero na normalização min-max
- Adiciona validação para valores nulos
- Atualiza testes para cobrir casos extremos

Fixes #456
```

#### 📚 Documentação
```bash
📚 docs(readme): atualiza instruções de instalação e configuração

- Adiciona instruções para instalação com uv
- Inclui configuração de ambiente virtual
- Documenta dependências opcionais
- Adiciona exemplos de uso básico
```

#### ♻️ Refatoração
```bash
♻️ refactor(models): refatora arquitetura do LSTM-VAE para melhor performance

- Separa encoder e decoder em módulos independentes
- Implementa cache para embeddings intermediários
- Otimiza forward pass com torch.jit
- Mantém compatibilidade com modelos existentes

Breaking Change: Interface do modelo alterada
```

## 🔧 Configuração

### 1. Template de Commit
```bash
git config commit.template .gitmessage
```

### 2. Pre-commit Hooks
```bash
uv run pre-commit install
```

### 3. Script Helper
```bash
./scripts/commit-emoji.sh generate
```

## 📊 Exemplos por Categoria

### 🚀 Funcionalidades de ML
```bash
🚀 feat(models): implementa modelo USAD para detecção de anomalias
🚀 feat(anomaly-detection): adiciona threshold adaptativo baseado em percentil
🚀 feat(data-processing): implementa pipeline de feature engineering automático
```

### 📊 Análise de Dados
```bash
📈 analysis(eda): realiza análise exploratória dos dados de pressão
📊 data(wells): adiciona novos dados de poços offshore do campo Tupi
📈 analysis(visualization): cria dashboard interativo para monitoramento
```

### 🔧 Infraestrutura
```bash
🔧 chore(deps): atualiza Polars para versão 0.20.0
👷 ci(github): configura GitHub Actions para testes automáticos
🔨 build(docker): adiciona suporte a containerização
```

## 🚫 O que NÃO fazer

### ❌ Commits Ruins
```bash
# Muito vago
fix: bug fix

# Sem contexto
update: updated code

# Muito longo
feat: implementa funcionalidade complexa de detecção de anomalias usando modelo TranAD com otimização de hiperparâmetros e validação cruzada

# Sem emoji
feat(anomaly-detection): implementa modelo TranAD
```

### ✅ Commits Bons
```bash
# Específico e claro
🐛 fix(data-processing): corrige erro na normalização de dados de pressão

# Contexto adequado
🚀 feat(anomaly-detection): implementa modelo TranAD

# Escopo apropriado
📚 docs(readme): atualiza instruções de instalação
```

## 🎯 Dicas para Commits Eficazes

1. **Use imperativo**: "adiciona" não "adicionado"
2. **Seja específico**: Descreva o que foi feito, não como
3. **Mantenha foco**: Um commit = uma mudança lógica
4. **Use escopos**: Agrupe mudanças relacionadas
5. **Inclua contexto**: Explique o porquê quando necessário

## 🔗 Recursos Adicionais

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Commitizen](https://commitizen-tools.github.io/commitizen/)
- [Pre-commit Hooks](https://pre-commit.com/)
- [Emoji Cheat Sheet](https://www.webfx.com/tools/emoji-cheat-sheet/)

## 📞 Suporte

Para dúvidas sobre commits convencionais:
- Execute `./scripts/commit-emoji.sh help`
- Consulte este documento
- Abra uma issue no repositório
