# 🐳 Petrobras DevContainer

Este diretório contém a configuração do DevContainer para o projeto **Petrobras Offshore Wells Anomaly Detection**.

## 🚀 O que é o DevContainer?

O DevContainer é uma funcionalidade do VS Code/Cursor que permite desenvolver dentro de um container Docker, garantindo um ambiente consistente e isolado para todos os desenvolvedores.

## 📋 Pré-requisitos

- Docker Desktop instalado e rodando
- VS Code ou Cursor com extensão "Dev Containers"
- Git configurado

## 🔧 Configuração

### Arquivos Principais

- **`devcontainer.json`**: Configuração principal do container
- **`setup_shell.sh`**: Script de configuração do ambiente shell
- **`zshrc.project`**: Configurações específicas do projeto para zsh
- **`test_environment.sh`**: Script de teste do ambiente

### Extensões Instaladas Automaticamente

- Python e Pylance
- Jupyter
- Docker
- GitHub Copilot
- Ruff (linter e formatter)
- GitLens
- Material Icon Theme
- Python Test Adapter

## 🚀 Como Usar

### 1. Abrir no DevContainer

1. Abra o projeto no VS Code/Cursor
2. Pressione `Ctrl+Shift+P` (ou `Cmd+Shift+P` no Mac)
3. Digite "Dev Containers: Reopen in Container"
4. Aguarde o build do container

### 2. Primeira Execução

Na primeira execução, o container irá:

- Instalar Python 3.11
- Configurar Oh My Zsh com plugins
- Instalar dependências Python
- Configurar Jupyter
- Criar aliases e funções personalizadas

### 3. Verificar Configuração

Após o build, execute:

```bash
source ~/.zshrc
.devcontainer/test_environment.sh
```

## 🎯 Comandos Úteis

### Aliases do Projeto

- `petro` - Ir para o diretório raiz do projeto
- `src` - Ir para o código fonte
- `notebooks` - Ir para os notebooks Jupyter
- `data` - Ir para os dados
- `tests` - Ir para os testes

### Funções do Projeto

- `petro-status` - Mostrar status do projeto
- `petro-setup` - Configurar ambiente de desenvolvimento
- `petro-clean` - Limpar arquivos de cache
- `petro-welcome` - Mostrar mensagem de boas-vindas

### Jupyter

- `jup` - Iniciar Jupyter Notebook
- `jup-lab` - Iniciar Jupyter Lab
- `jup-convert` - Converter notebooks para Python

### Desenvolvimento

- `ruff` - Executar linter
- `ruff-fix` - Corrigir problemas automaticamente
- `pytest` - Executar testes
- `mypy` - Verificação de tipos

## 🔍 Troubleshooting

### Problemas Comuns

#### 1. Container não inicia

```bash
# Verificar logs do Docker
docker logs <container_id>

# Reconstruir container
# VS Code: Dev Containers > Rebuild Container
```

#### 2. Script setup_shell.sh não executa

```bash
# Verificar permissões
chmod +x .devcontainer/setup_shell.sh

# Executar manualmente
bash .devcontainer/setup_shell.sh
```

#### 3. Zsh não carrega configuração

```bash
# Recarregar configuração
source ~/.zshrc

# Verificar se arquivo existe
ls -la ~/.zshrc.project
```

#### 4. Jupyter não inicia

```bash
# Verificar configuração
cat ~/.jupyter/jupyter_notebook_config.py

# Iniciar manualmente
jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root
```

### Logs e Debug

Para ver logs detalhados:

```bash
# Logs do container
docker logs <container_id>

# Logs do VS Code
# Help > Toggle Developer Tools > Console
```

## 📊 Ambiente

### Python

- **Versão**: 3.11
- **Gerenciador**: pip
- **Ambiente**: Container isolado

### Ferramentas

- **Shell**: Zsh com Oh My Zsh
- **Editor**: VS Code/Cursor
- **Container**: Docker
- **Porta**: 8888 (Jupyter)

### Dependências

As dependências são instaladas automaticamente do `requirements.txt` durante o build do container.

## 🔄 Atualizações

Para atualizar o ambiente:

1. Modifique os arquivos de configuração
2. Reconstrua o container: `Dev Containers > Rebuild Container`
3. Execute o script de teste: `.devcontainer/test_environment.sh`

## 📚 Recursos Adicionais

- [Dev Containers Documentation](https://containers.dev/)
- [VS Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers)
- [Oh My Zsh](https://ohmyz.sh/)
- [Jupyter Configuration](https://jupyter.readthedocs.io/en/latest/projects/jupyter-directories.html)

## 🆘 Suporte

Se encontrar problemas:

1. Execute `.devcontainer/test_environment.sh`
2. Verifique os logs do container
3. Consulte a documentação do VS Code Dev Containers
4. Abra uma issue no repositório do projeto
