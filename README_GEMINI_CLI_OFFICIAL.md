# 🤖 Gemini CLI Oficial

**CLI oficial do Google Gemini** instalado e configurado com sucesso! 🎉

## 🚀 Instalação Concluída

- ✅ **Node.js atualizado**: v22.19.0 (LTS)
- ✅ **npm atualizado**: v10.9.3
- ✅ **Gemini CLI instalado**: v0.2.2
- ✅ **Configuração automática**: PATH e aliases configurados

## 🔑 Configuração da API

Para usar o Gemini CLI, configure sua chave da API:

```bash
export GOOGLE_API_KEY="sua_chave_aqui"
```

## 📖 Como Usar

### Modo Interativo (Padrão)

```bash
gemini
```

### Modo com Prompt Específico

```bash
gemini -p "Explique detecção de anomalias em séries temporais"
```

### Modo Interativo com Prompt Inicial

```bash
gemini -i "Analise este código Python"
```

### Modo Sandbox (Seguro)

```bash
gemini -s
```

## 🎯 Comandos Principais

### Comandos Básicos

- `gemini` - Inicia o CLI interativo
- `gemini --help` - Mostra ajuda completa
- `gemini --version` - Mostra versão

### Comandos Avançados

- `gemini mcp` - Gerencia servidores MCP
- `gemini -l` - Lista extensões disponíveis
- `gemini -e [extensões]` - Usa extensões específicas

## 🔧 Opções Principais

### Modelo e Prompt

- `-m, --model` - Especifica o modelo Gemini
- `-p, --prompt` - Executa prompt não-interativo
- `-i, --prompt-interactive` - Executa prompt e continua interativo

### Segurança e Controle

- `-s, --sandbox` - Executa em modo sandbox
- `-y, --yolo` - Aceita automaticamente todas as ações
- `--approval-mode` - Define modo de aprovação

### Arquivos e Workspace

- `-a, --all-files` - Inclui todos os arquivos no contexto
- `--include-directories` - Diretórios adicionais para incluir

## 💡 Exemplos de Uso para o Projeto

### Análise de Código

```bash
gemini -p "Analise este código Python para detecção de anomalias"
```

### Debugging

```bash
gemini -i "Ajude-me a debugar este erro de machine learning"
```

### Documentação

```bash
gemini -p "Gere documentação para esta função de detecção de anomalias"
```

### Otimização

```bash
gemini -p "Como otimizar este modelo LSTM-VAE para melhor performance?"
```

## 🚀 Funcionalidades Avançadas

### Extensões

```bash
# Listar extensões disponíveis
gemini -l

# Usar extensões específicas
gemini -e "python,ml,data-analysis"
```

### Modo Sandbox

```bash
# Executar em ambiente seguro
gemini -s -p "Teste este algoritmo"
```

### Checkpointing

```bash
# Habilitar checkpointing de edições
gemini -c -p "Refatore este código"
```

## 🔒 Segurança

- **Modo Sandbox**: Execute código em ambiente isolado
- **Aprovação Manual**: Controle total sobre ações executadas
- **YOLO Mode**: Apenas para desenvolvimento/testes

## 🐛 Solução de Problemas

### Erro: "Command not found"

```bash
# Recarregue o shell
source ~/.zshrc

# Verifique o PATH
echo $PATH | grep npm-global
```

### Erro: "API key not found"

```bash
# Configure a variável de ambiente
export GOOGLE_API_KEY="sua_chave_aqui"
```

### Problemas de Node.js

```bash
# Use nvm para gerenciar versões
nvm use v22.19.0
```

## 🌟 Vantagens do CLI Oficial

- ✅ **Suporte oficial** do Google
- ✅ **Atualizações regulares** via npm
- ✅ **Funcionalidades avançadas** (sandbox, extensões)
- ✅ **Integração nativa** com serviços Google
- ✅ **Performance otimizada**
- ✅ **Documentação completa**

## 📚 Recursos Adicionais

- [Documentação oficial](https://ai.google.dev/docs)
- [Google AI Studio](https://aistudio.google.com/)
- [Repositório npm](https://www.npmjs.com/package/@google/gemini-cli)

## 🔄 Atualizações

Para atualizar o CLI:

```bash
npm update -g @google/gemini-cli
```

---

**🎯 CLI oficial configurado e pronto para uso no projeto PIBIC de Detecção de Anomalias em Poços Offshore da Petrobras!** 🛢️
