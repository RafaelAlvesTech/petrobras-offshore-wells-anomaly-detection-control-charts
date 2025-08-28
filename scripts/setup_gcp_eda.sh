#!/bin/bash

# 🚀 Script de Configuração Rápida para EDA no GCP
# Petrobras Offshore Wells Anomaly Detection
# Autor: Rafael Alves

set -e  # Parar em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para imprimir com cores
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Função para verificar se comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Função para verificar se usuário está logado no GCP
check_gcp_auth() {
    if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
        print_error "Você não está autenticado no Google Cloud"
        print_status "Execute: gcloud auth login"
        return 1
    fi
    return 0
}

# Função para criar projeto GCP
create_gcp_project() {
    local project_id="$1"
    local project_name="$2"

    print_status "Criando projeto GCP: $project_id"

    if gcloud projects create "$project_id" --name="$project_name" --quiet; then
        print_success "Projeto criado com sucesso!"
    else
        print_warning "Projeto já existe ou erro na criação"
    fi

    # Configurar como projeto padrão
    gcloud config set project "$project_id"
    print_success "Projeto configurado como padrão"
}

# Função para habilitar APIs
enable_gcp_apis() {
    local project_id="$1"

    print_status "Habilitando APIs necessárias..."

    local apis=(
        "storage.googleapis.com"
        "bigquery.googleapis.com"
        "aiplatform.googleapis.com"
        "compute.googleapis.com"
        "cloudfunctions.googleapis.com"
        "cloudscheduler.googleapis.com"
    )

    for api in "${apis[@]}"; do
        print_status "Habilitando: $api"
        gcloud services enable "$api" --project="$project_id"
    done

    print_success "Todas as APIs habilitadas!"
}

# Função para criar service account
create_service_account() {
    local project_id="$1"
    local sa_name="$2"
    local sa_email="$sa_name@$project_id.iam.gserviceaccount.com"

    print_status "Criando service account: $sa_name"

    if gcloud iam service-accounts create "$sa_name" \
        --display-name="EDA Service Account" \
        --description="Service account para EDA e análise de dados" \
        --quiet; then
        print_success "Service account criado!"
    else
        print_warning "Service account já existe"
    fi

    # Atribuir roles
    print_status "Atribuindo roles necessários..."

    local roles=(
        "roles/storage.admin"
        "roles/bigquery.dataEditor"
        "roles/bigquery.jobUser"
        "roles/aiplatform.user"
        "roles/compute.viewer"
    )

    for role in "${roles[@]}"; do
        print_status "Atribuindo role: $role"
        gcloud projects add-iam-policy-binding "$project_id" \
            --member="serviceAccount:$sa_email" \
            --role="$role" \
            --quiet
    done

    print_success "Roles atribuídos com sucesso!"

    # Criar e baixar chave
    print_status "Criando chave de autenticação..."
    local key_file="$HOME/gcp-credentials-$sa_name.json"

    gcloud iam service-accounts keys create "$key_file" \
        --iam-account="$sa_email" \
        --quiet

    print_success "Chave salva em: $key_file"
    echo "$key_file"
}

# Função para criar bucket GCS
create_gcs_bucket() {
    local project_id="$1"
    local bucket_name="$2"
    local location="$3"

    print_status "Criando bucket GCS: $bucket_name"

    if gsutil mb -p "$project_id" -c STANDARD -l "$location" "gs://$bucket_name"; then
        print_success "Bucket criado com sucesso!"
    else
        print_warning "Bucket já existe ou erro na criação"
    fi

    # Criar estrutura de pastas
    print_status "Criando estrutura de pastas..."

    local folders=(
        "raw-data"
        "processed-data"
        "eda-results"
        "models"
        "plots"
        "logs"
    )

    for folder in "${folders[@]}"; do
        gsutil mb "gs://$bucket_name/$folder" 2>/dev/null || true
        print_status "Pasta criada: $folder"
    done

    print_success "Estrutura de pastas criada!"
}

# Função para configurar variáveis de ambiente
setup_environment_vars() {
    local project_id="$1"
    local region="$2"
    local bucket_name="$3"
    local credentials_file="$4"

    print_status "Configurando variáveis de ambiente..."

    local shell_rc="$HOME/.bashrc"
    if [[ "$SHELL" == *"zsh"* ]]; then
        shell_rc="$HOME/.zshrc"
    fi

    # Adicionar variáveis ao arquivo de configuração do shell
    {
        echo ""
        echo "# GCP Configuration for Petrobras EDA"
        echo "export GCP_PROJECT_ID=\"$project_id\""
        echo "export GCP_REGION=\"$region\""
        echo "export GCS_BUCKET=\"$bucket_name\""
        echo "export GOOGLE_APPLICATION_CREDENTIALS=\"$credentials_file\""
        echo "export GOOGLE_CLOUD_PROJECT=\"$project_id\""
    } >> "$shell_rc"

    print_success "Variáveis de ambiente configuradas em: $shell_rc"
    print_warning "Execute 'source $shell_rc' para carregar as variáveis"
}

# Função para instalar dependências Python
install_python_deps() {
    print_status "Instalando dependências Python..."

    if command_exists uv; then
        print_status "Usando uv para instalar dependências..."
        uv add google-cloud-storage google-cloud-bigquery google-auth matplotlib seaborn
    elif command_exists pip; then
        print_status "Usando pip para instalar dependências..."
        pip install google-cloud-storage google-cloud-bigquery google-auth matplotlib seaborn
    else
        print_error "Nem uv nem pip encontrados. Instale um deles primeiro."
        return 1
    fi

    print_success "Dependências Python instaladas!"
}

# Função para criar dados de exemplo
create_sample_data() {
    local bucket_name="$1"

    print_status "Criando dados de exemplo..."

    python3 -c "
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Dados simulados de poços offshore
np.random.seed(42)
dates = pd.date_range('2023-01-01', '2023-12-31', freq='H')
n_samples = len(dates)

data = pd.DataFrame({
    'timestamp': dates,
    'well_id': np.random.choice(['WELL_001', 'WELL_002', 'WELL_003'], n_samples),
    'pressure': np.random.normal(150, 20, n_samples),
    'temperature': np.random.normal(85, 10, n_samples),
    'flow_rate': np.random.normal(1000, 200, n_samples),
    'vibration': np.random.normal(0.5, 0.1, n_samples),
    'oil_content': np.random.normal(0.8, 0.05, n_samples),
    'water_content': np.random.normal(0.15, 0.03, n_samples),
    'gas_content': np.random.normal(0.05, 0.02, n_samples)
})

# Adicionar algumas anomalias
anomaly_indices = np.random.choice(n_samples, size=50, replace=False)
data.loc[anomaly_indices, 'pressure'] += np.random.normal(50, 10, 50)
data.loc[anomaly_indices, 'temperature'] += np.random.normal(15, 5, 50)

# Salvar localmente
data.to_csv('sample_well_data.csv', index=False)
print('✅ Dados de exemplo criados: sample_well_data.csv')
print(f'📊 {len(data)} registros criados')
print(f'📅 Período: {data.timestamp.min()} a {data.timestamp.max()}')
print(f'🕳️  Poços: {data.well_id.unique()}')
"

    # Upload para GCS
    print_status "Fazendo upload dos dados para GCS..."
    gsutil cp sample_well_data.csv "gs://$bucket_name/raw-data/"

    print_success "Dados de exemplo enviados para GCS!"
}

# Função para testar configuração
test_configuration() {
    local project_id="$1"
    local bucket_name="$2"

    print_status "Testando configuração..."

    # Testar acesso ao projeto
    if gcloud config get-value project | grep -q "$project_id"; then
        print_success "✅ Acesso ao projeto GCP OK"
    else
        print_error "❌ Falha no acesso ao projeto GCP"
        return 1
    fi

    # Testar acesso ao bucket
    if gsutil ls "gs://$bucket_name" >/dev/null 2>&1; then
        print_success "✅ Acesso ao bucket GCS OK"
    else
        print_error "❌ Falha no acesso ao bucket GCS"
        return 1
    fi

    # Testar Python
    python3 -c "
from google.cloud import storage
import os

try:
    client = storage.Client()
    bucket = client.bucket('$bucket_name')
    blobs = list(bucket.list_blobs(max_results=5))
    print(f'✅ Python GCP client OK - {len(blobs)} objetos encontrados')
except Exception as e:
    print(f'❌ Erro no Python GCP client: {e}')
    exit(1)
"

    print_success "🎉 Configuração testada com sucesso!"
}

# Função principal
main() {
    echo "🚀 CONFIGURAÇÃO RÁPIDA PARA EDA NO GCP"
    echo "======================================"
    echo ""

    # Verificar pré-requisitos
    if ! command_exists gcloud; then
        print_error "Google Cloud SDK não encontrado"
        print_status "Instale em: https://cloud.google.com/sdk/docs/install"
        exit 1
    fi

    if ! command_exists gsutil; then
        print_error "gsutil não encontrado"
        print_status "Instale o Google Cloud SDK completo"
        exit 1
    fi

    # Verificar autenticação
    if ! check_gcp_auth; then
        exit 1
    fi

    # Configurações padrão
    local project_id="petrobras-anomaly-detection"
    local project_name="Petrobras Anomaly Detection"
    local region="us-central1"
    local bucket_name="petrobras-eda-data"
    local sa_name="eda-service-account"

    # Perguntar ao usuário se quer usar configurações padrão
    echo ""
    read -p "Usar configurações padrão? (y/n): " -n 1 -r
    echo ""

    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        read -p "ID do projeto GCP: " project_id
        read -p "Nome do projeto: " project_name
        read -p "Região (ex: us-central1): " region
        read -p "Nome do bucket: " bucket_name
        read -p "Nome da service account: " sa_name
    fi

    echo ""
    print_status "Configurações selecionadas:"
    echo "  - Projeto: $project_id"
    echo "  - Região: $region"
    echo "  - Bucket: $bucket_name"
    echo "  - Service Account: $sa_name"
    echo ""

    # Confirmar execução
    read -p "Continuar com a configuração? (y/n): " -n 1 -r
    echo ""

    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_status "Configuração cancelada pelo usuário"
        exit 0
    fi

    # Executar configuração
    create_gcp_project "$project_id" "$project_name"
    enable_gcp_apis "$project_id"

    local credentials_file
    credentials_file=$(create_service_account "$project_id" "$sa_name")

    create_gcs_bucket "$project_id" "$bucket_name" "$region"
    setup_environment_vars "$project_id" "$region" "$bucket_name" "$credentials_file"
    install_python_deps
    create_sample_data "$bucket_name"

    # Testar configuração
    test_configuration "$project_id" "$bucket_name"

    echo ""
    echo "🎉 CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!"
    echo "======================================"
    echo ""
    echo "📋 PRÓXIMOS PASSOS:"
    echo "1. Recarregue as variáveis de ambiente:"
    echo "   source ~/.bashrc  # ou ~/.zshrc"
    echo ""
    echo "2. Execute o notebook de exemplo:"
    echo "   python notebooks/gcp_eda_example.py"
    echo ""
    echo "3. Ou use Marimo:"
    echo "   marimo edit notebooks/gcp_eda_example.py"
    echo ""
    echo "4. Configure GitHub Actions (opcional):"
    echo "   Veja docs/GCP_EDA_SETUP.md"
    echo ""
    echo "📚 Documentação: docs/GCP_EDA_SETUP.md"
    echo "🔧 Scripts: scripts/setup_gcp_eda.sh"
    echo ""
    echo "✅ Seu ambiente GCP está pronto para EDA!"
}

# Executar função principal
main "$@"
