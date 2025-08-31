# 🛢️ Petrobras Offshore Wells Anomaly Detection - DevContainer Setup

## ✅ Configuração Completa

Sua configuração de devcontainer com Zsh persistente e Powerlevel10k está pronta! Aqui está o que foi configurado:

### 📁 Estrutura Criada

```
.docker/
├── Dockerfile              # Imagem Docker com Zsh e Powerlevel10k
├── docker-compose.yml      # Orquestração dos serviços
├── start-app.sh           # Script de inicialização
├── dev.sh                 # Script helper para comandos
├── README.md              # Documentação detalhada
└── zsh/
    ├── .zshrc             # Configuração personalizada do Zsh
    ├── .zsh_history       # Histórico persistente do Zsh
    ├── history/           # Diretório para histórico
    └── powerlevel10k/
        └── .p10k.zsh      # Configuração do Powerlevel10k

.devcontainer/
└── devcontainer.json      # Configuração do VS Code/Cursor

.vscode/
├── settings.json          # Configurações do VS Code
└── extensions.json        # Extensões recomendadas
```

## 🚀 Como Usar

### Opção 1: VS Code/Cursor DevContainer (Recomendado)

1. **Abrir no VS Code/Cursor**:

   ```bash
   code .  # ou cursor .
   ```

2. **Reabrir em Container**:
   - Pressione `Ctrl+Shift+P` (ou `Cmd+Shift+P` no Mac)
   - Digite "Dev Containers: Reopen in Container"
   - Aguarde a construção do container

3. **Pronto!** O ambiente estará configurado com:
   - Zsh com Powerlevel10k
   - Histórico persistente
   - Aliases personalizados
   - Serviços disponíveis

### Opção 2: Docker Compose Manual

1. **Navegar para o diretório**:

   ```bash
   cd .docker
   ```

2. **Usar o script helper**:

   ```bash
   # Construir e iniciar
   ./dev.sh build
   ./dev.sh up

   # Iniciar serviços específicos
   ./dev.sh jupyter   # Jupyter Lab
   ./dev.sh mlflow    # MLflow server
   ./dev.sh api       # API server

   # Abrir shell
   ./dev.sh shell

   # Ver logs
   ./dev.sh logs

   # Parar ambiente
   ./dev.sh down
   ```

3. **Ou usar docker-compose diretamente**:
   ```bash
   docker-compose up --build
   docker-compose exec app /bin/zsh
   ```

## 🎨 Recursos Configurados

### Zsh com Powerlevel10k

- ✅ **Tema**: Powerlevel10k com configuração personalizada
- ✅ **Plugins**:
  - `git` - Integração com Git
  - `git-flow` - Suporte ao Git Flow
  - `fast-syntax-highlighting` - Destaque de sintaxe
  - `zsh-autosuggestions` - Sugestões automáticas
  - `zsh-completions` - Completions avançadas

### Configurações Persistentes

- ✅ **Histórico do Zsh**: Persistido entre sessões
- ✅ **Configuração do Powerlevel10k**: Personalizada e persistente
- ✅ **Aliases personalizados**: Para comandos do projeto
- ✅ **Variáveis de ambiente**: Configuradas automaticamente

### Serviços Disponíveis

- ✅ **API Server**: http://localhost:8000
- ✅ **Jupyter Lab**: http://localhost:8888
- ✅ **MLflow Server**: http://localhost:5000

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

### Função de Serviços

```bash
start_service jupyter  # Iniciar Jupyter Lab
start_service mlflow   # Iniciar MLflow server
start_service api      # Iniciar API server
```

## 🐳 Comandos Docker

### Script Helper (.docker/dev.sh)

```bash
./dev.sh build     # Construir container
./dev.sh up        # Iniciar ambiente
./dev.sh down      # Parar ambiente
./dev.sh restart   # Reiniciar ambiente
./dev.sh logs      # Ver logs
./dev.sh shell     # Abrir shell
./dev.sh jupyter   # Iniciar Jupyter
./dev.sh mlflow    # Iniciar MLflow
./dev.sh api       # Iniciar API
./dev.sh clean     # Limpar containers
./dev.sh status    # Status dos containers
./dev.sh help      # Ajuda
```

### Docker Compose Direto

```bash
docker-compose up --build          # Construir e iniciar
docker-compose down                # Parar
docker-compose restart             # Reiniciar
docker-compose logs -f app         # Ver logs
docker-compose exec app /bin/zsh   # Abrir shell
```

## 🔄 Persistência de Dados

Os seguintes dados são persistidos entre sessões:

- ✅ Histórico do Zsh (`~/.zsh_history`)
- ✅ Configuração do Powerlevel10k (`~/.p10k.zsh`)
- ✅ Configuração personalizada do Zsh (`~/.zshrc`)
- ✅ Dados do projeto (montados como volume)

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

## 📚 Próximos Passos

1. **Teste o ambiente**:

   ```bash
   cd .docker
   ./dev.sh up
   ./dev.sh shell
   ```

2. **Configure o Powerlevel10k** (se necessário):

   ```bash
   p10k configure
   ```

3. **Inicie os serviços**:

   ```bash
   start_service jupyter
   start_service mlflow
   start_service api
   ```

4. **Desenvolva com conforto**! 🎉

## 🔗 Links Úteis

- [Powerlevel10k Documentation](https://github.com/romkatv/powerlevel10k)
- [Zsh Documentation](https://zsh.sourceforge.io/Doc/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [VS Code Dev Containers](https://code.visualstudio.com/docs/remote/containers)

---

**🎉 Seu ambiente de desenvolvimento está pronto! Aproveite o desenvolvimento com Zsh persistente e Powerlevel10k!**
