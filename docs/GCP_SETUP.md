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

| Serviço                        | Custo/Hora | Uso Estimado | Custo Mensal |
| ------------------------------ | ---------- | ------------ | ------------ |
| Vertex AI (n1-standard-4 + T4) | $0.47      | 10 horas     | $4.70        |
| Cloud Storage                  | $0.02/GB   | 100 GB       | $2.00        |
| Cloud Build                    | $0.003/min | 30 min       | $0.09        |
| **Total**                      | -          | -            | **~$6.79**   |

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

## 🔐 Configuração de Autenticação Google Cloud para GitHub Actions

## 📋 Visão Geral

Este documento explica como configurar a autenticação do Google Cloud para as GitHub Actions usando **Workload Identity Federation**, que é o método recomendado e mais seguro.

## 🚀 Método Recomendado: Workload Identity Federation

### 1. Configurar Workload Identity no Google Cloud

```bash
# Definir variáveis de ambiente
export PROJECT_ID="seu-projeto-id"
export PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
export WORKLOAD_IDENTITY_POOL="github-actions-pool"
export WORKLOAD_IDENTITY_PROVIDER="github-actions-provider"
export SERVICE_ACCOUNT_NAME="github-actions-sa"
export SERVICE_ACCOUNT_EMAIL="$SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com"

# Criar Workload Identity Pool
gcloud iam workload-identity-pools create "$WORKLOAD_IDENTITY_POOL" \
  --project="$PROJECT_ID" \
  --location="global" \
  --display-name="GitHub Actions Pool"

# Criar Workload Identity Provider
gcloud iam workload-identity-pools providers create-oidc "$WORKLOAD_IDENTITY_PROVIDER" \
  --project="$PROJECT_ID" \
  --location="global" \
  --workload-identity-pool="$WORKLOAD_IDENTITY_POOL" \
  --issuer-uri="https://token.actions.githubusercontent.com" \
  --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository"

# Criar Service Account
gcloud iam service-accounts create "$SERVICE_ACCOUNT_NAME" \
  --project="$PROJECT_ID" \
  --display-name="GitHub Actions Service Account"

# Permitir que o Service Account use Workload Identity
gcloud iam service-accounts add-iam-policy-binding "$SERVICE_ACCOUNT_EMAIL" \
  --project="$PROJECT_ID" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/$PROJECT_NUMBER/locations/global/workloadIdentityPools/$WORKLOAD_IDENTITY_POOL/attribute.repository/seu-usuario/seu-repositorio"

# Adicionar roles necessárias ao Service Account
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
  --role="roles/storage.admin"

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
  --role="roles/aiplatform.admin"

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
  --role="roles/ml.admin"

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
  --role="roles/compute.admin"

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
  --role="roles/cloudbuild.builds.builder"
```

### 2. Obter o Workload Identity Provider

```bash
# Obter o Workload Identity Provider
gcloud iam workload-identity-pools providers describe "$WORKLOAD_IDENTITY_PROVIDER" \
  --project="$PROJECT_ID" \
  --location="global" \
  --workload-identity-pool="$WORKLOAD_IDENTITY_POOL" \
  --format="value(name)"
```

## 🔑 Configurar Secrets no GitHub

### 1. Acessar Settings do Repositório

- Vá para `Settings` > `Secrets and variables` > `Actions`

### 2. Adicionar os Seguintes Secrets

| Secret Name                      | Valor                                                                                                             | Descrição                             |
| -------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ------------------------------------- |
| `GCP_PROJECT_ID`                 | `seu-projeto-id`                                                                                                  | ID do projeto Google Cloud            |
| `GCP_WORKLOAD_IDENTITY_PROVIDER` | `projects/123456789/locations/global/workloadIdentityPools/github-actions-pool/providers/github-actions-provider` | Provider do Workload Identity         |
| `GCP_SERVICE_ACCOUNT`            | `github-actions-sa@seu-projeto-id.iam.gserviceaccount.com`                                                        | Email do Service Account              |
| `GCP_BUCKET_NAME`                | `nome-do-bucket`                                                                                                  | Nome do bucket do Cloud Storage       |
| `GOOGLE_CLOUD_PROJECT`           | `seu-projeto-id`                                                                                                  | ID do projeto (para compatibilidade)  |
| `GOOGLE_CLOUD_REGION`            | `us-central1`                                                                                                     | Região padrão do Google Cloud         |
| `GCS_BUCKET_NAME`                | `nome-do-bucket`                                                                                                  | Nome do bucket (para compatibilidade) |

## 🧪 Testar a Configuração

### 1. Executar Workflow de Teste

- Vá para `Actions` no repositório
- Execute o workflow `Test GCP Authentication` manualmente
- Verifique se a autenticação foi bem-sucedida

### 2. Verificar Logs

- Se houver erros, verifique:
  - Se todos os secrets estão configurados
  - Se o Workload Identity está configurado corretamente
  - Se o Service Account tem as permissões necessárias

## 🔒 Segurança

### Vantagens do Workload Identity Federation:

- ✅ **Sem chaves de serviço**: Não há risco de vazamento de credenciais
- ✅ **Tempo de vida limitado**: Tokens expiram automaticamente
- ✅ **Auditoria**: Todas as ações são registradas no Cloud Audit Logs
- ✅ **Princípio do menor privilégio**: Permite granularidade nas permissões

### Permissões Mínimas Recomendadas:

- `roles/storage.admin` - Para gerenciar buckets e objetos
- `roles/aiplatform.admin` - Para treinar modelos no Vertex AI
- `roles/ml.admin` - Para usar AI Platform (legacy)
- `roles/compute.admin` - Para criar e gerenciar VMs
- `roles/cloudbuild.builds.builder` - Para builds do Cloud Build

## 🚨 Troubleshooting

### Erro: "workload_identity_provider or credentials_json must be specified"

- ✅ Verifique se `GCP_WORKLOAD_IDENTITY_PROVIDER` está configurado
- ✅ Verifique se `GCP_SERVICE_ACCOUNT` está configurado
- ❌ Não use `credentials_json` (método legado)

### Erro: "Permission denied"

- ✅ Verifique se o Service Account tem as permissões necessárias
- ✅ Verifique se o Workload Identity está configurado corretamente
- ✅ Verifique se o repositório está na lista de repositórios permitidos

### Erro: "Service account not found"

- ✅ Verifique se o Service Account existe
- ✅ Verifique se o email está correto no secret `GCP_SERVICE_ACCOUNT`

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
