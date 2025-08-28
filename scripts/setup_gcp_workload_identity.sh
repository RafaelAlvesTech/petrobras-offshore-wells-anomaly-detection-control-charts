#!/bin/bash

# 🚀 Script para Configurar Workload Identity Federation no Google Cloud
# Este script configura automaticamente a autenticação segura para GitHub Actions

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para imprimir mensagens coloridas
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

# Verificar se gcloud está instalado
check_gcloud() {
    if ! command -v gcloud &> /dev/null; then
        print_error "Google Cloud SDK não está instalado."
        print_status "Instale com: curl https://sdk.cloud.google.com | bash"
        exit 1
    fi
    print_success "Google Cloud SDK encontrado: $(gcloud version --format='value(Google Cloud SDK)')"
}

# Verificar se está autenticado
check_auth() {
    if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
        print_error "Você não está autenticado no Google Cloud."
        print_status "Execute: gcloud auth login"
        exit 1
    fi
    print_success "Autenticado como: $(gcloud auth list --filter=status:ACTIVE --format='value(account)')"
}

# Obter configurações do usuário
get_config() {
    print_status "Configurando Workload Identity Federation..."

    # Ler configurações do arquivo gcp-config.yaml se existir
    if [ -f "gcp-config.yaml" ]; then
        print_status "Lendo configurações do gcp-config.yaml..."
        PROJECT_ID=$(grep "project_id:" gcp-config.yaml | head -1 | sed 's/.*project_id: *"\([^"]*\)".*/\1/')
        REGION=$(grep "region:" gcp-config.yaml | head -1 | sed 's/.*region: *"\([^"]*\)".*/\1/')
    fi

    # Solicitar configurações se não encontradas
    if [ -z "$PROJECT_ID" ]; then
        echo -n "Digite o ID do projeto Google Cloud: "
        read PROJECT_ID
    fi

    if [ -z "$REGION" ]; then
        echo -n "Digite a região (padrão: us-central1): "
        read REGION
        REGION=${REGION:-us-central1}
    fi

    echo -n "Digite o nome do usuário GitHub (ex: RafaelAlvesTech): "
    read GITHUB_USER

    echo -n "Digite o nome do repositório (ex: petrobras-offshore-wells-anomaly-detection-control-charts): "
    read GITHUB_REPO

    print_success "Configurações obtidas:"
    print_status "  Projeto: $PROJECT_ID"
    print_status "  Região: $REGION"
    print_status "  Usuário GitHub: $GITHUB_USER"
    print_status "  Repositório: $GITHUB_REPO"
}

# Configurar projeto
setup_project() {
    print_status "Configurando projeto..."
    gcloud config set project "$PROJECT_ID"
    gcloud config set compute/region "$REGION"
    print_success "Projeto configurado: $PROJECT_ID"
}

# Obter número do projeto
get_project_number() {
    PROJECT_NUMBER=$(gcloud projects describe "$PROJECT_ID" --format="value(projectNumber)")
    print_success "Número do projeto: $PROJECT_NUMBER"
}

# Configurar Workload Identity Pool
setup_workload_identity_pool() {
    print_status "Configurando Workload Identity Pool..."

    POOL_NAME="github-actions-pool"

    # Verificar se já existe
    if gcloud iam workload-identity-pools describe "$POOL_NAME" --location="global" --project="$PROJECT_ID" &>/dev/null; then
        print_warning "Workload Identity Pool '$POOL_NAME' já existe"
    else
        gcloud iam workload-identity-pools create "$POOL_NAME" \
            --project="$PROJECT_ID" \
            --location="global" \
            --display-name="GitHub Actions Pool"
        print_success "Workload Identity Pool criado: $POOL_NAME"
    fi
}

# Configurar Workload Identity Provider
setup_workload_identity_provider() {
    print_status "Configurando Workload Identity Provider..."

    PROVIDER_NAME="github-actions-provider"

    # Verificar se já existe
    if gcloud iam workload-identity-pools providers describe "$PROVIDER_NAME" --location="global" --workload-identity-pool="$POOL_NAME" --project="$PROJECT_ID" &>/dev/null; then
        print_warning "Workload Identity Provider '$PROVIDER_NAME' já existe"
    else
        gcloud iam workload-identity-pools providers create-oidc "$PROVIDER_NAME" \
            --project="$PROJECT_ID" \
            --location="global" \
            --workload-identity-pool="$POOL_NAME" \
            --issuer-uri="https://token.actions.githubusercontent.com" \
            --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository"
        print_success "Workload Identity Provider criado: $PROVIDER_NAME"
    fi
}

# Criar Service Account
create_service_account() {
    print_status "Criando Service Account..."

    SA_NAME="github-actions-sa"
    SA_EMAIL="$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com"

    # Verificar se já existe
    if gcloud iam service-accounts describe "$SA_EMAIL" --project="$PROJECT_ID" &>/dev/null; then
        print_warning "Service Account '$SA_NAME' já existe"
    else
        gcloud iam service-accounts create "$SA_NAME" \
            --project="$PROJECT_ID" \
            --display-name="GitHub Actions Service Account"
        print_success "Service Account criado: $SA_NAME"
    fi
}

# Configurar permissões do Service Account
setup_service_account_permissions() {
    print_status "Configurando permissões do Service Account..."

    SA_EMAIL="$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com"

    # Permitir que o Service Account use Workload Identity
    gcloud iam service-accounts add-iam-policy-binding "$SA_EMAIL" \
        --project="$PROJECT_ID" \
        --role="roles/iam.workloadIdentityUser" \
        --member="principalSet://iam.googleapis.com/projects/$PROJECT_NUMBER/locations/global/workloadIdentityPools/$POOL_NAME/attribute.repository/$GITHUB_USER/$GITHUB_REPO"

    # Adicionar roles necessárias
    ROLES=(
        "roles/storage.admin"
        "roles/aiplatform.admin"
        "roles/ml.admin"
        "roles/compute.admin"
        "roles/cloudbuild.builds.builder"
        "roles/logging.admin"
        "roles/monitoring.admin"
    )

    for role in "${ROLES[@]}"; do
        print_status "Adicionando role: $role"
        gcloud projects add-iam-policy-binding "$PROJECT_ID" \
            --member="serviceAccount:$SA_EMAIL" \
            --role="$role"
    done

    print_success "Permissões configuradas para o Service Account"
}

# Obter informações para GitHub Secrets
get_github_secrets_info() {
    print_status "Configurando GitHub Secrets..."

    # Obter o Workload Identity Provider
    WORKLOAD_IDENTITY_PROVIDER=$(gcloud iam workload-identity-pools providers describe "$PROVIDER_NAME" \
        --project="$PROJECT_ID" \
        --location="global" \
        --workload-identity-pool="$POOL_NAME" \
        --format="value(name)")

    SA_EMAIL="$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com"

    print_success "GitHub Secrets configurados:"
    echo ""
    echo "Adicione os seguintes secrets no seu repositório GitHub:"
    echo "  Settings > Secrets and variables > Actions"
    echo ""
    echo "GCP_PROJECT_ID: $PROJECT_ID"
    echo "GCP_WORKLOAD_IDENTITY_PROVIDER: $WORKLOAD_IDENTITY_PROVIDER"
    echo "GCP_SERVICE_ACCOUNT: $SA_EMAIL"
    echo "GCP_REGION: $REGION"
    echo ""

    # Salvar em arquivo para referência
    cat > "gcp-secrets.txt" << EOF
# Google Cloud Secrets para GitHub Actions
# Adicione estes secrets no seu repositório: Settings > Secrets and variables > Actions

GCP_PROJECT_ID=$PROJECT_ID
GCP_WORKLOAD_IDENTITY_PROVIDER=$WORKLOAD_IDENTITY_PROVIDER
GCP_SERVICE_ACCOUNT=$SA_EMAIL
GCP_REGION=$REGION

# Configurações adicionais
GCP_BUCKET_NAME=${PROJECT_ID}-petrobras-anomaly-detection
EOF

    print_success "Secrets salvos em: gcp-secrets.txt"
}

# Habilitar APIs necessárias
enable_required_apis() {
    print_status "Habilitando APIs necessárias..."

    APIS=(
        "aiplatform.googleapis.com"
        "ml.googleapis.com"
        "storage.googleapis.com"
        "logging.googleapis.com"
        "monitoring.googleapis.com"
        "compute.googleapis.com"
        "cloudbuild.googleapis.com"
        "containerregistry.googleapis.com"
        "iam.googleapis.com"
    )

    for api in "${APIS[@]}"; do
        print_status "Habilitando: $api"
        gcloud services enable "$api" --project="$PROJECT_ID"
    done

    print_success "APIs habilitadas"
}

# Função principal
main() {
    echo "🚀 Configurando Workload Identity Federation para Google Cloud"
    echo "================================================================"
    echo ""

    check_gcloud
    check_auth
    get_config
    setup_project
    get_project_number
    setup_workload_identity_pool
    setup_workload_identity_provider
    create_service_account
    setup_service_account_permissions
    enable_required_apis
    get_github_secrets_info

    echo ""
    echo "🎉 Configuração concluída com sucesso!"
    echo ""
    echo "📋 Próximos passos:"
    echo "1. Adicione os secrets listados acima no GitHub"
    echo "2. Execute o workflow 'Test GCP Authentication'"
    echo "3. Verifique se a autenticação está funcionando"
    echo ""
    echo "📚 Para mais informações, consulte: docs/GCP_SETUP.md"
}

# Executar script
main "$@"
