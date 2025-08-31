# 🛢️ Petrobras Offshore Wells Anomaly Detection - DevContainer

Este diretório contém toda a configuração necessária para executar o projeto em um ambiente de desenvolvimento containerizado com Zsh persistente e Powerlevel10k.

## 📁 Estrutura de Arquivos

```
.docker/
├── Dockerfile              # Imagem Docker com Zsh e Powerlevel10k
├── docker-compose.yml      # Orquestração dos serviços
├── start-app.sh           # Script de inicialização
├── README.md              # Este arquivo
└── zsh/
    ├── .zshrc             # Configuração personalizada do Zsh
    ├── .zsh_history       # Histórico persistente do Zsh
    ├── history/           # Diretório para histórico
    └── powerlevel10k/
        └── .p10k.zsh      # Configuração do Powerlevel10k
```

## 🚀 Como Usar

### Opção 1: VS Code/Cursor DevContainer (Recomendado)

1. Abra o projeto no VS Code ou Cursor
2. Pressione `Ctrl+Shift+P` (ou `Cmd+Shift+P` no Mac)
3. Digite "Dev Containers: Reopen in Container"
4. Aguarde a construção do container

### Opção 2: Docker Compose Manual

```bash
# Construir e iniciar o container
cd .docker
docker-compose up --build

# Executar comandos específicos
docker-compose exec app start_service jupyter
docker-compose exec app start_service mlflow
docker-compose exec app start_service api
```

## 🎨 Recursos do Ambiente

### Zsh com Powerlevel10k

- **Tema**: Powerlevel10k com configuração personalizada
- **Plugins**:
  - `git` - Integração com Git
  - `git-flow` - Suporte ao Git Flow
  - `fast-syntax-highlighting` - Destaque de sintaxe
  - `zsh-autosuggestions` - Sugestões automáticas
  - `zsh-completions` - Completions avançadas

### Configurações Persistentes

- **Histórico do Zsh**: Persistido entre sessões
- **Configuração do Powerlevel10k**: Personalizada e persistente
- **Aliases personalizados**: Para comandos do projeto
- **Variáveis de ambiente**: Configuradas automaticamente

### Serviços Disponíveis

- **API Server**: http://localhost:8000
- **Jupyter Lab**: http://localhost:8888
- **MLflow Server**: http://localhost:5000

## 🔧 Comandos Úteis

### Aliases do Projeto

```bash
petrobras    # Ir para o diretório raiz do projeto
src          # Ir para o código fonte
notebooks    # Ir para os notebooks
data         # Ir para os dados
tests        # Ir para os testes
```

### Aliases de Desenvolvimento

```bash
py           # python
pip          # uv pip
sync         # uv sync
add          # uv add
run          # uv run
```

### Aliases de Serviços

```bash
jupyter      # Iniciar Jupyter Lab
mlflow-server # Iniciar MLflow server
```

### Função de Serviços

```bash
start_service jupyter  # Iniciar Jupyter Lab
start_service mlflow   # Iniciar MLflow server
start_service api      # Iniciar API server
```

## 🐳 Configuração Docker

### Dockerfile

- Base: Python 3.11 slim
- Zsh com Powerlevel10k e plugins
- uv para gerenciamento de dependências
- Usuário `python` com sudo

### Docker Compose

- Volumes persistentes para configurações Zsh
- Portas expostas: 8000, 8888, 5000
- Rede personalizada
- Variáveis de ambiente configuradas

## 🔄 Persistência de Dados

Os seguintes dados são persistidos entre sessões:

- Histórico do Zsh (`~/.zsh_history`)
- Configuração do Powerlevel10k (`~/.p10k.zsh`)
- Configuração personalizada do Zsh (`~/.zshrc`)
- Dados do projeto (montados como volume)

## 🛠️ Personalização

### Modificar Configuração do Powerlevel10k

1. Edite `.docker/zsh/powerlevel10k/.p10k.zsh`
2. Reinicie o container

### Adicionar Novos Aliases

1. Edite `.docker/zsh/.zshrc`
2. Reinicie o container ou execute `source ~/.zshrc`

### Modificar Script de Inicialização

1. Edite `.docker/start-app.sh`
2. Reconstrua o container

## 🐛 Troubleshooting

### Container não inicia

```bash
# Verificar logs
docker-compose logs app

# Reconstruir container
docker-compose down
docker-compose up --build
```

### Zsh não carrega configurações

```bash
# Verificar se os volumes estão montados
docker-compose exec app ls -la /home/python/.p10k.zsh

# Recarregar configuração
docker-compose exec app source ~/.zshrc
```

### Portas em uso

```bash
# Verificar portas em uso
netstat -tulpn | grep :8000
netstat -tulpn | grep :8888
netstat -tulpn | grep :5000

# Parar containers existentes
docker-compose down
```

## 📚 Recursos Adicionais

- [Powerlevel10k Documentation](https://github.com/romkatv/powerlevel10k)
- [Zsh Documentation](https://zsh.sourceforge.io/Doc/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [VS Code Dev Containers](https://code.visualstudio.com/docs/remote/containers)
