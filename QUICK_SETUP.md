# 🚀 Configuração Rápida - Petrobras Offshore Wells

## ⚡ Setup em 3 Passos

### 1. 🐍 Ambiente Python

```bash
# Verificar Python 3.11+
python3 --version

# Instalar uv (se necessário)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. 🔧 Configurar Projeto

```bash
# Clonar e entrar no diretório
git clone <seu-repositorio>
cd petrobras-offshore-wells-anomaly-detection-control-charts

# Executar setup automático
chmod +x scripts/setup_environment.sh
./scripts/setup_environment.sh
```

### 3. 🎯 Começar a Desenvolver

```bash
# Ativar ambiente
source .venv/bin/activate

# Abrir Jupyter Lab
jupyter lab notebooks/

# Ou executar testes
pytest tests/
```

## 🛠️ Ferramentas Principais

- **Jupyter**: Notebooks interativos
- **Polars**: Manipulação de dados rápida
- **PyTorch**: Deep Learning
- **MLflow**: Experiment tracking
- **uv**: Gerenciamento de dependências

## 📁 Estrutura do Projeto

```
├── src/                    # Código fonte
├── notebooks/             # Notebooks Jupyter
├── tests/                 # Testes
├── data/                  # Datasets
├── config/                # Configurações
└── docs/                  # Documentação
```

## 🔗 Links Úteis

- [Documentação Completa](README.md)
- [Setup GCP](docs/GCP_SETUP.md)
- [Contribuindo](CONTRIBUTING.md)

## 🆘 Problemas Comuns

**Erro: "Kernel não encontrado"**

```bash
# Instalar kernel no ambiente virtual
source .venv/bin/activate
python -m ipykernel install --user --name=petrobras --display-name="Python 3.11 (petrobras)"
```

**Erro: Ambiente virtual incorreto**

```bash
rm -rf .venv
uv venv
uv sync
```

**Erro: Dependências não encontradas**

```bash
uv sync --group dev
```

## 🎉 Pronto!

Seu ambiente está configurado para desenvolvimento de detecção de anomalias em poços offshore da Petrobras! 🛢️🚀
