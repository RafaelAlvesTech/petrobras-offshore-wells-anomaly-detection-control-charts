# 🚀 Guia de Configuração Unificado - Petrobras Offshore Wells

Este guia centraliza toda a documentação de configuração para o projeto de detecção de anomalias em poços offshore da Petrobras, cobrindo desde o setup local até a configuração em nuvem e a manutenção do projeto.

## 📋 Índice

1.  [Visão Geral e Pré-requisitos](#-visão-geral-e-pré-requisitos)
2.  [Setup Rápido (Local)](#-setup-rápido-local)
3.  [Setup com Devcontainer (Recomendado)](#-setup-com-devcontainer-recomendado)
4.  [Configuração para Cloud](#-configuração-para-cloud)
    - [Google Cloud Platform (GCP)](#google-cloud-platform-gcp)
    - [Amazon Web Services (AWS)](#amazon-web-services-aws)
5.  [Ambiente de Desenvolvimento (Zsh)](#-ambiente-de-desenvolvimento-zsh)
6.  [Manutenção do Projeto](#-manutenção-do-projeto)
7.  [Troubleshooting (WSL2)](#-troubleshooting-wsl2)

---

## 🎯 Visão Geral e Pré-requisitos

### Software Necessário

- **Python 3.11+**: Versão LTS recomendada.
- **uv**: Gerenciador de pacotes e ambientes virtuais.
- **Git**: Para versionamento de código.
- **Docker**: Essencial para o setup com Devcontainer.
- **Cloud CLIs (Opcional)**: `gcloud` (Google Cloud SDK) e `aws-cli` (AWS CLI) para interação com as plataformas de nuvem.

### Instalação das Ferramentas Base

```bash
# Verificar Python 3.11+
python3 --version

# Instalar uv (se necessário)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Instalar CLIs (se for usar a nuvem)
# Google Cloud SDK
curl https://sdk.cloud.google.com | bash
# AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

---

## ⚡ Setup Rápido (Local)

Este método é ideal para configurações rápidas e desenvolvimento direto na sua máquina.

### 1. Clone o Repositório

```bash
git clone <seu-repositorio>
cd petrobras-offshore-wells-anomaly-detection-control-charts
```

### 2. Execute o Setup Automático

O script `setup_environment.sh` irá:

- Criar um ambiente virtual com `uv`.
- Instalar todas as dependências.
- Configurar hooks de pré-commit.

```bash
chmod +x scripts/setup_environment.sh
./scripts/setup_environment.sh
```

### 3. Comece a Desenvolver

```bash
# Ativar ambiente virtual
source .venv/bin/activate

# Abrir Jupyter Lab
jupyter lab notebooks/

# Ou executar testes
pytest tests/
```

---

## 🐳 Setup com Devcontainer (Recomendado)

O Devcontainer oferece um ambiente de desenvolvimento encapsulado, consistente e reproduzível.

### 1. Pré-requisitos

- **VS Code** ou **Cursor** com a extensão [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).
- **Docker Desktop** instalado e em execução.

### 2. Como Usar

1.  **Abra o projeto** no VS Code ou Cursor.
2.  Pressione `Ctrl+Shift+P` e selecione **"Dev Containers: Reopen in Container"**.
3.  Aguarde a construção do container.

O ambiente estará pronto com Zsh, Powerlevel10k, histórico persistente e todos os serviços (Jupyter, MLflow) disponíveis.

### Comandos Úteis (Dentro do Container)

Use o script `dev.sh` no diretório `.docker` para gerenciar o ambiente:

```bash
# Construir e iniciar
./dev.sh build && ./dev.sh up

# Abrir um shell no container
./dev.sh shell

# Iniciar serviços
./dev.sh jupyter   # Jupyter Lab em http://localhost:8888
./dev.sh mlflow    # MLflow server em http://localhost:5000

# Parar o ambiente
./dev.sh down
```

---

## ☁️ Configuração para Cloud

### Google Cloud Platform (GCP)

Guia para configurar o GCP para treinamento e análise de dados.

#### 1. Configuração Inicial e APIs

```bash
# Login e configuração do projeto
gcloud auth login
gcloud config set project SEU_PROJECT_ID

# Habilitar APIs necessárias
gcloud services enable aiplatform.googleapis.com storage.googleapis.com compute.googleapis.com
```

#### 2. Autenticação (Workload Identity para GitHub Actions)

Este é o método mais seguro para CI/CD.

```bash
# Crie um Workload Identity Pool e Provider
gcloud iam workload-identity-pools create "github-pool" --location="global"
gcloud iam workload-identity-pools providers create-oidc "github-provider" \
    --workload-identity-pool="github-pool" \
    --issuer-uri="https://token.actions.githubusercontent.com" \
    --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository"

# Crie uma Service Account
gcloud iam service-accounts create "github-actions-sa"

# Vincule a Service Account ao Provider
gcloud iam service-accounts add-iam-policy-binding "github-actions-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/iam.workloadIdentityUser" \
    --member="principalSet://iam.googleapis.com/projects/$PROJECT_NUMBER/locations/global/workloadIdentityPools/github-pool/attribute.repository/seu-usuario/seu-repo"

# Atribua as permissões necessárias à Service Account
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:github-actions-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.admin"
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:github-actions-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/aiplatform.admin"
```

#### 3. Configurar Secrets no GitHub

Vá para `Settings > Secrets and variables > Actions` e adicione:

- `GCP_PROJECT_ID`: ID do seu projeto GCP.
- `GCP_WORKLOAD_IDENTITY_PROVIDER`: O nome do provider criado.
- `GCP_SERVICE_ACCOUNT`: O e-mail da Service Account.

#### 4. Uso (Exemplo: EDA)

- **Armazenamento:** Crie um bucket no Cloud Storage para armazenar datasets e resultados.
- **Execução:** Use notebooks no Vertex AI Workbench para análises escaláveis.
- **Exemplo:** O notebook `notebooks/gcp_eda_example.py` demonstra como carregar dados do GCS, analisá-los com Polars e salvar os resultados.

### Amazon Web Services (AWS)

Guia para configurar a AWS para treinamento de modelos.

#### 1. Configuração Inicial

```bash
# Instale e configure o AWS CLI
aws configure
# AWS Access Key ID: [sua-access-key]
# AWS Secret Access Key: [sua-secret-key]
# Default region name: us-east-1
```

#### 2. Setup Automatizado

O script `setup_aws.sh` auxilia na configuração inicial.

```bash
chmod +x scripts/setup_aws.sh
./scripts/setup_aws.sh
```

#### 3. Arquitetura e Serviços

- **Amazon SageMaker**: Plataforma principal para treinamento e deploy.
- **Amazon S3**: Para armazenamento de dados, modelos e artefatos.
- **IAM**: Para gerenciamento de permissões.

#### 4. Configuração

- **`aws-config.yaml`**: Arquivo central para configurar instâncias, buckets e regiões.
- **`.env.aws`**: Para armazenar credenciais de forma segura.

#### 5. Uso

- **`src/aws_config_manager.py`**: Gerencia a configuração da infraestrutura (criação de buckets, etc.).
- **`src/aws_training.py`**: Gerencia os jobs de treinamento no SageMaker.

```python
# Exemplo de como iniciar um treinamento
from src.aws_training import AWSTrainingManager

manager = AWSTrainingManager()
config = manager.get_training_config('lstm_vae')
job_name = manager.create_training_job(config)
manager.monitor_training_job(job_name)
```

---

## 🐚 Ambiente de Desenvolvimento (Zsh)

O projeto vem com uma configuração Zsh otimizada, especialmente dentro do Devcontainer.

### Recursos

- **Prompt Personalizado**: Mostra informações do projeto, ambiente Python e status do Git.
- **Variáveis de Ambiente**: `PROJECT_ROOT`, `DATA_DIR`, `MLFLOW_TRACKING_URI`, etc., são pré-configuradas.
- **Aliases Úteis**:
  - **Navegação**: `pj` (raiz do projeto), `data`, `notebooks`, `src`.
  - **Python**: `py`, `pip`, `uv-sync`.
  - **Ferramentas**: `jlab` (Jupyter Lab), `mlflow-ui`.
  - **Qualidade**: `test`, `lint`, `format`, `type-check`.
- **Funções Customizadas**: `activate_venv()`, `train_model <nome>`, `project_status()`.

Para detalhes completos, consulte o arquivo `.zshrc.project`.

---

## 🛠️ Manutenção do Projeto

### Atualização de Dependências

Para resolver vulnerabilidades de segurança ou atualizar pacotes.

#### Opção 1: Script Automático (Recomendado)

```bash
./scripts/update_dependencies.sh
```

#### Opção 2: Manualmente com `uv`

```bash
# Edite as versões no pyproject.toml

# Sincronize o ambiente
uv sync

# Verifique vulnerabilidades
uv pip audit

# Regenere o requirements.txt
uv pip freeze > requirements.txt
```

Após a atualização, sempre execute a suíte de testes para garantir que nada quebrou.

---

## 🐛 Troubleshooting (WSL2)

Guia para resolver problemas comuns no ambiente WSL2 para usuários Windows.

### Performance Lenta

Crie ou edite o arquivo `C:\Users\<seu_usuario>\.wslconfig` para limitar os recursos:

```ini
[wsl2]
memory=8GB      # Limita a RAM para 8GB
processors=4    # Limita a 4 processadores
```

### Erros de Rede

Execute os seguintes comandos no PowerShell (como Administrador):

```powershell
wsl --shutdown
netsh winsock reset
netsh int ip reset
ipconfig /flushdns
wsl
```

### Docker não funciona

- Garanta que o Docker Desktop esteja em execução no Windows e configurado para usar o backend do WSL2.
- Adicione seu usuário ao grupo `docker` no WSL:

```bash
sudo usermod -aG docker $USER
newgrp docker
```

### Permissão de Arquivos

Evite trabalhar em arquivos localizados no sistema de arquivos do Windows (`/mnt/c/`). Clone o repositório e trabalhe dentro do sistema de arquivos do Linux (`/home/<user>/`) para melhor performance e para evitar problemas de permissão.

```

```
