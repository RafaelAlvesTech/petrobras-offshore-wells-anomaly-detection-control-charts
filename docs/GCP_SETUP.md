# ☁️ Google Cloud Platform Setup Guide

> **Guia completo para configuração e uso do Google Cloud Platform para treinamento de modelos de detecção de anomalias**

## 📋 Índice

- [🎯 Visão Geral](#-visão-geral)
- [🚀 Pré-requisitos](#-pré-requisitos)
- [⚙️ Configuração Inicial](#️-configuração-inicial)
- [🔐 Autenticação](#-autenticação)
- [🏗️ Setup Automático](#️-setup-automático)
- [🔧 Configuração Manual](#-configuração-manual)
- [📊 Primeiro Treinamento](#-primeiro-treinamento)
- [📈 Monitoramento](#-monitoramento)
- [💰 Custos e Otimização](#-custos-e-otimização)
- [🚨 Troubleshooting](#-troubleshooting)
- [📚 Referências](#-referências)

## 🎯 Visão Geral

Este projeto está configurado para treinamento de modelos de detecção de anomalias na Google Cloud Platform, oferecendo:

- **Escalabilidade**: Treinamento em múltiplas GPUs e máquinas
- **Custo-efetividade**: Pagamento apenas pelo uso
- **Integração**: Seamless integration com MLflow e experiment tracking
- **Automação**: CI/CD pipeline para treinamento automático

### 🏗️ Arquitetura

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Local Dev     │    │   Google Cloud   │    │   MLflow UI     │
│                 │    │                  │    │                 │
│ ┌─────────────┐ │    │ ┌──────────────┐ │    │ ┌─────────────┐ │
│ │   Code      │ │───▶│ │ Vertex AI    │ │───▶│ │ Experiments │ │
│ │             │ │    │ │              │ │    │ │             │
│ └─────────────┘ │    │ └──────────────┘ │    │ └─────────────┘ │
│                 │    │                  │    │                 │
│ ┌─────────────┐ │    │ ┌──────────────┐ │    │ ┌─────────────┐ │
│ │   Data      │ │───▶│ │ Cloud Storage│ │───▶│ │ Model      │ │
│ │             │ │    │ │              │ │    │ │ Registry   │ │
│ └─────────────┘ │    │ └──────────────┘ │    │ └─────────────┘ │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🚀 Pré-requisitos

### 📋 Software Necessário

- **Python 3.11+**: Versão LTS recomendada
- **Google Cloud SDK**: CLI para interação com GCP
- **Docker**: Para containerização (opcional)
- **Git**: Para versionamento

### 🔐 Conta Google Cloud

- **Projeto GCP**: Criado e configurado
- **Billing**: Habilitado para o projeto
- **IAM**: Permissões adequadas configuradas

### 💰 Orçamento Estimado

| Serviço | Custo/Hora | Uso Estimado | Custo Mensal |
|----------|------------|--------------|--------------|
| Vertex AI (n1-standard-4 + T4) | $0.47 | 10 horas | $4.70 |
| Cloud Storage | $0.02/GB | 100 GB | $2.00 |
| Cloud Build | $0.003/min | 30 min | $0.09 |
| **Total** | - | - | **~$6.79** |

## ⚙️ Configuração Inicial

### 1. Instalar Google Cloud SDK

#### Linux/macOS
```bash
# Baixar e instalar
curl https://sdk.cloud.google.com | bash

# Reiniciar shell
exec -l $SHELL

# Verificar instalação
gcloud version
```

#### Windows
```bash
# Baixar do site oficial
# https://cloud.google.com/sdk/docs/install

# Ou usar winget
winget install Google.CloudSDK
```

### 2. Autenticação Inicial

```bash
# Login interativo
gcloud auth login

# Configurar projeto padrão
gcloud config set project YOUR_PROJECT_ID

# Configurar região padrão
gcloud config set compute/region us-central1
```

### 3. Habilitar APIs Necessárias

```bash
# APIs principais
gcloud services enable aiplatform.googleapis.com
gcloud services enable ml.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable logging.googleapis.com
gcloud services enable monitoring.googleapis.com
gcloud services enable compute.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable iam.googleapis.com
```

## 🔐 Autenticação

### Método 1: Application Default Credentials (Recomendado)

```bash
# Configurar credenciais padrão
gcloud auth application-default login

# Verificar
gcloud auth application-default print-access-token
```

### Método 2: Service Account Key

```bash
# Criar service account
gcloud iam service-accounts create anomaly-detection-training \
    --display-name="Anomaly Detection Training Service Account"

# Criar chave
gcloud iam service-accounts keys create service-account-key.json \
    --iam-account=anomaly-detection-training@YOUR_PROJECT_ID.iam.gserviceaccount.com

# Configurar variável de ambiente
export GOOGLE_APPLICATION_CREDENTIALS="service-account-key.json"
```

### Método 3: Workload Identity (Para Kubernetes)

```bash
# Configurar Workload Identity
gcloud iam service-accounts add-iam-policy-binding \
    anomaly-detection-training@YOUR_PROJECT_ID.iam.gserviceaccount.com \
    --role="roles/iam.workloadIdentityUser" \
    --member="serviceAccount:YOUR_PROJECT_ID.svc.id.goog[NAMESPACE/SERVICE_ACCOUNT]"
```

## 🏗️ Setup Automático

### 🚀 Script de Setup

O projeto inclui um script automatizado para configuração completa:

```bash
# Configurar variáveis de ambiente
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_REGION="us-central1"
export GCS_BUCKET_NAME="your-bucket-name"

# Executar setup automático
chmod +x scripts/setup_gcp.sh
./scripts/setup_gcp.sh
```

### 🔧 O que o Script Faz

1. **Verifica pré-requisitos**: gcloud, docker, etc.
2. **Habilita APIs**: Todas as APIs necessárias
3. **Cria bucket**: Cloud Storage com estrutura de pastas
4. **Configura IAM**: Service account com permissões adequadas
5. **Deploy MLflow**: Servidor na Cloud Run (opcional)
6. **Cria arquivos**: .env e configurações
7. **Testa setup**: Validação completa

### 📝 Variáveis de Ambiente

```bash
# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_REGION=us-central1
GOOGLE_CLOUD_ZONE=us-central1-a

# Vertex AI Configuration
VERTEX_AI_LOCATION=us-central1
VERTEX_AI_EXPERIMENT_NAME=petrobras-anomaly-detection
VERTEX_AI_MODEL_DISPLAY_NAME=anomaly-detection-model

# Cloud Storage
GCS_BUCKET_NAME=your-bucket-name
GCS_MODEL_PATH=gs://your-bucket-name/models
GCS_DATA_PATH=gs://your-bucket-name/data

# AI Platform Training
AI_PLATFORM_TRAINING_REGION=us-central1
AI_PLATFORM_TRAINING_SCALE_TIER=BASIC_GPU
AI_PLATFORM_TRAINING_MASTER_TYPE=n1-standard-4
AI_PLATFORM_TRAINING_WORKER_TYPE=n1-standard-4
AI_PLATFORM_TRAINING_WORKER_COUNT=2

# Authentication
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account-key.json

# MLflow Configuration
MLFLOW_TRACKING_URI=http://localhost:5000
MLFLOW_EXPERIMENT_NAME=petrobras-anomaly-detection
```

## 🔧 Configuração Manual

### 1. Cloud Storage Bucket

```bash
# Criar bucket
gsutil mb -p YOUR_PROJECT_ID -c STANDARD -l us-central1 gs://YOUR_BUCKET_NAME

# Criar estrutura de pastas
gsutil cp /dev/null gs://YOUR_BUCKET_NAME/data/
gsutil cp /dev/null gs://YOUR_BUCKET_NAME/models/
gsutil cp /dev/null gs://YOUR_BUCKET_NAME/experiments/
gsutil cp /dev/null gs://YOUR_BUCKET_NAME/logs/
gsutil cp /dev/null gs://YOUR_BUCKET_NAME/checkpoints/
gsutil cp /dev/null gs://YOUR_BUCKET_NAME/mlflow-artifacts/
gsutil cp /dev/null gs://YOUR_BUCKET_NAME/training_scripts/
```

### 2. Service Account e IAM

```bash
# Criar service account
gcloud iam service-accounts create anomaly-detection-training \
    --display-name="Anomaly Detection Training Service Account"

# Conceder roles
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:anomaly-detection-training@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/aiplatform.admin"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:anomaly-detection-training@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:anomaly-detection-training@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/logging.admin"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:anomaly-detection-training@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/monitoring.admin"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:anomaly-detection-training@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/compute.admin"
```

### 3. MLflow Server (Opcional)

```bash
# Build da imagem
docker build -t gcr.io/YOUR_PROJECT_ID/mlflow-server:latest -f docker/mlflow.Dockerfile .

# Push para Container Registry
docker push gcr.io/YOUR_PROJECT_ID/mlflow-server:latest

# Deploy na Cloud Run
gcloud run deploy mlflow-server \
    --image=gcr.io/YOUR_PROJECT_ID/mlflow-server:latest \
    --platform=managed \
    --region=us-central1 \
    --project=YOUR_PROJECT_ID \
    --allow-unauthenticated \
    --port=5000 \
    --memory=2Gi \
    --cpu=1 \
    --set-env-vars="MLFLOW_TRACKING_URI=http://localhost:5000" \
    --set-env-vars="GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID" \
    --set-env-vars="GCS_BUCKET_NAME=YOUR_BUCKET_NAME"
```

## 📊 Primeiro Treinamento

### 1. Preparar Dados

```bash
# Upload de dados para Cloud Storage
gsutil cp data/your_dataset.csv gs://YOUR_BUCKET_NAME/data/
```

### 2. Executar Treinamento

```bash
# Usando script de exemplo
python examples/train_lstm_vae_gcp.py \
    --config gcp-config.yaml \
    --data-path data/your_dataset.csv \
    --model-name lstm-vae-anomaly-detection \
    --epochs 100 \
    --batch-size 64 \
    --learning-rate 0.0001
```

### 3. Monitorar Progresso

```bash
# Ver jobs de treinamento
gcloud ai custom-jobs list --region=us-central1

# Ver logs de um job específico
gcloud ai custom-jobs stream-logs JOB_ID --region=us-central1

# Ver experimentos no Vertex AI
gcloud ai experiments list --region=us-central1
```

## 📈 Monitoramento

### MLflow UI

```bash
# Acessar MLflow localmente
mlflow ui --host 0.0.0.0 --port 5000

# Ou acessar na Cloud Run (se configurado)
# URL será fornecida após deploy
```

### Cloud Logging

```bash
# Ver logs de treinamento
gcloud logging read "resource.type=ml_job" --limit=50

# Filtrar por projeto
gcloud logging read "resource.labels.project_id=YOUR_PROJECT_ID" --limit=50
```

### Cloud Monitoring

```bash
# Ver métricas de uso
gcloud monitoring metrics list --filter="metric.type:aiplatform.googleapis.com"

# Criar alertas para falhas
gcloud alpha monitoring policies create --policy-from-file=alert-policy.yaml
```

## 💰 Custos e Otimização

### 📊 Estimativas de Custo

| Cenário | Horas/Mês | Custo Estimado |
|---------|-----------|----------------|
| **Desenvolvimento** | 10 | $6.79 |
| **Treinamento Leve** | 50 | $23.50 |
| **Treinamento Intensivo** | 200 | $94.00 |
| **Produção** | 500+ | $235.00+ |

### 🎯 Dicas de Otimização

1. **Usar Spot Instances**: Até 80% de desconto
2. **Auto-scaling**: Escalar apenas quando necessário
3. **Preemptible VMs**: Para jobs não críticos
4. **Reserved Instances**: Para uso contínuo
5. **Cleanup automático**: Remover recursos não utilizados

### 🧹 Cleanup Automático

```bash
# Limpar jobs antigos (mais de 7 dias)
gcloud ai custom-jobs list --region=us-central1 \
    --filter="createTime<$(date -d '7 days ago' -u +%Y-%m-%dT%H:%M:%SZ)" \
    --format="value(name)" | \
while read job; do
    gcloud ai custom-jobs delete "$job" --region=us-central1 --quiet
done

# Limpar modelos antigos
gcloud ai models list --region=us-central1 \
    --filter="createTime<$(date -d '30 days ago' -u +%Y-%m-%dT%H:%M:%SZ)" \
    --format="value(name)" | \
while read model; do
    gcloud ai models delete "$model" --region=us-central1 --quiet
done
```

## 🚨 Troubleshooting

### Problemas Comuns

#### 1. Erro de Autenticação

```bash
# Verificar credenciais
gcloud auth list
gcloud config list

# Reautenticar se necessário
gcloud auth login
gcloud auth application-default login
```

#### 2. API não habilitada

```bash
# Verificar APIs habilitadas
gcloud services list --enabled

# Habilitar API específica
gcloud services enable aiplatform.googleapis.com
```

#### 3. Quota excedida

```bash
# Verificar quotas
gcloud compute regions describe us-central1

# Solicitar aumento
# https://console.cloud.google.com/iam-admin/quotas
```

#### 4. Erro de permissão

```bash
# Verificar permissões
gcloud projects get-iam-policy YOUR_PROJECT_ID

# Adicionar permissões
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="user:YOUR_EMAIL" \
    --role="roles/aiplatform.admin"
```

### 🔍 Debugging

#### Logs Detalhados

```bash
# Habilitar logs detalhados
export GOOGLE_CLOUD_VERBOSE=1

# Ver logs de uma operação específica
gcloud logging read "resource.labels.operation_id=OPERATION_ID" --limit=100
```

#### Teste de Conectividade

```bash
# Testar acesso ao Vertex AI
gcloud ai operations list --region=us-central1 --limit=1

# Testar acesso ao Cloud Storage
gsutil ls gs://YOUR_BUCKET_NAME/

# Testar acesso ao IAM
gcloud iam service-accounts list
```

## 📚 Referências

### 📖 Documentação Oficial

- [Google Cloud AI Platform](https://cloud.google.com/ai-platform)
- [Vertex AI](https://cloud.google.com/vertex-ai)
- [Cloud Storage](https://cloud.google.com/storage)
- [Cloud IAM](https://cloud.google.com/iam)

### 🎥 Tutoriais

- [Getting Started with Vertex AI](https://cloud.google.com/vertex-ai/docs/start)
- [Custom Training Jobs](https://cloud.google.com/ai-platform/docs/custom-training)
- [MLflow on Google Cloud](https://mlflow.org/docs/latest/tracking.html)

### 💬 Comunidade

- [Google Cloud Community](https://cloud.google.com/community)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/google-cloud-platform)
- [GitHub Issues](https://github.com/RafaelAlvesTech/petrobras-offshore-wells-anomaly-detection-control-charts/issues)

### 🔧 Ferramentas Úteis

- [Google Cloud Console](https://console.cloud.google.com/)
- [Cloud Shell](https://shell.cloud.google.com/)
- [Cloud Code](https://cloud.google.com/code) (VS Code extension)

---

## 🚀 Próximos Passos

1. **Configurar ambiente**: Execute o script de setup automático
2. **Testar integração**: Execute um job de treinamento simples
3. **Otimizar configuração**: Ajuste parâmetros para seu caso de uso
4. **Monitorar custos**: Configure alertas de billing
5. **Automatizar**: Configure CI/CD pipeline

**Happy training! 🎯🚀**
