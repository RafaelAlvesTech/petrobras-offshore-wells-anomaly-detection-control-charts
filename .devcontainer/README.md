# 🛢️ Petrobras Offshore Wells Anomaly Detection - Dev Container

Este dev container está configurado para desenvolvimento de detecção de anomalias em séries temporais multivariadas de poços offshore da Petrobras.

## 🚀 Início Rápido

### Opção 1: VS Code Dev Containers (Recomendado)

1. **Instale a extensão Dev Containers** no VS Code
2. **Abra o projeto** no VS Code
3. **Pressione `Ctrl+Shift+P`** e selecione "Dev Containers: Reopen in Container"
4. **Aguarde** a construção do container (primeira vez pode demorar alguns minutos)

### Opção 2: Docker Compose

```bash
# Construir e executar o container
docker-compose up --build

# Ou usar o Dockerfile diretamente
docker build -t petrobras-anomaly .
docker run -it --rm -p 8888:8888 -p 8000:8000 petrobras-anomaly
```

## 🛠️ Ferramentas Incluídas

### 🐍 Python & Data Science

- **Python 3.11.13** - Versão estável e otimizada
- **uv** - Gerenciador de dependências ultra-rápido
- **Jupyter Lab** - Ambiente interativo para notebooks
- **Polars** - Manipulação de dados de alta performance
- **PyTorch** - Deep learning com suporte a GPU
- **Scikit-learn** - Machine learning tradicional
- **MLflow** - Experiment tracking e model registry

### 🔧 Ferramentas de Desenvolvimento

- **Pre-commit** - Hooks para qualidade de código
- **Ruff** - Linting e formatação rápida
- **Black** - Formatação de código Python
- **MyPy** - Verificação de tipos
- **Bandit** - Análise de segurança
- **Pytest** - Framework de testes

### 🎨 Interface e Produtividade

- **Oh My Zsh** - Shell interativo com plugins
- **Powerlevel10k** - Tema de prompt avançado
- **VS Code Extensions** - Extensões essenciais pré-instaladas
- **Git** - Controle de versão com configurações otimizadas

## 📊 Portas Disponíveis

- **8888** - Jupyter Lab
- **8000** - MLflow UI

## 🎯 Comandos Úteis

### Desenvolvimento

```bash
# Ativar ambiente virtual
source .venv/bin/activate

# Instalar dependências
uv sync

# Executar testes
pytest

# Formatar código
black .
ruff check --fix .

# Executar pre-commit em todos os arquivos
pre-commit run --all-files
```

### Jupyter e Análise

```bash
# Iniciar Jupyter Lab
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser

# Iniciar MLflow UI
mlflow ui --host 0.0.0.0 --port 8000

# Criar novo kernel Jupyter
python -m ipykernel install --user --name=petrobras-anomaly
```

### Git e Versionamento

```bash
# Commit com pre-commit
git add .
git commit -m "feat: nova funcionalidade"

# Verificar status
git status

# Sincronizar com repositório remoto
git push origin main
```

## 📁 Estrutura do Projeto

```
petrobras-offshore-wells-anomaly-detection-control-charts/
├── .devcontainer/          # Configuração do dev container
├── .vscode/               # Configurações do VS Code
├── data/                  # Dados do projeto
│   ├── raw/              # Dados brutos
│   ├── processed/        # Dados processados
│   └── external/         # Dados externos
├── notebooks/            # Notebooks Jupyter
│   └── experiments/      # Experimentos
├── src/                  # Código fonte
├── tests/                # Testes automatizados
├── models/               # Modelos treinados
├── logs/                 # Logs de execução
├── docs/                 # Documentação
└── scripts/              # Scripts utilitários
```

## 🔧 Configurações Personalizadas

### VS Code

- **Python interpreter** configurado para `.venv`
- **Formatação automática** com Black
- **Linting** com Ruff
- **Extensões essenciais** pré-instaladas

### Git

- **Pre-commit hooks** configurados
- **GPG signing** desabilitado por padrão
- **Configurações otimizadas** para desenvolvimento

### Terminal

- **Zsh** como shell padrão
- **Oh My Zsh** com plugins úteis
- **Powerlevel10k** para prompt avançado

## 🐛 Solução de Problemas

### Problema: Pre-commit não encontrado

```bash
# Solução: Instalar pre-commit
pip install pre-commit
pre-commit install
```

### Problema: Virtual environment não ativado

```bash
# Solução: Ativar manualmente
source .venv/bin/activate
```

### Problema: Portas não acessíveis

```bash
# Verificar se as portas estão abertas
netstat -tlnp | grep -E "(8888|8000)"
```

### Problema: Dependências desatualizadas

```bash
# Atualizar dependências
uv sync --upgrade
```

## 📚 Recursos Adicionais

- [Documentação do Projeto](../README.md)
- [Guia de Contribuição](../CONTRIBUTING.md)
- [Configuração AWS](../AWS_SETUP_SUMMARY.md)
- [Solução WSL2](../WSL2_SOLUTION_SUMMARY.md)

## 🤝 Suporte

Para dúvidas ou problemas:

1. Verifique a documentação do projeto
2. Consulte os logs em `logs/`
3. Abra uma issue no repositório
4. Entre em contato com a equipe de desenvolvimento

---

**Desenvolvido com ❤️ para a Petrobras**
