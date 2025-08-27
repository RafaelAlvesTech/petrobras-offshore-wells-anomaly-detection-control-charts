#!/bin/bash

# =============================================================================
# Script de Setup AWS para Petrobras Offshore Wells Anomaly Detection
# =============================================================================
# Este script automatiza a configuração inicial da AWS para o projeto
# de detecção de anomalias em poços offshore.

set -e  # Para execução em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para logging
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Função para verificar se comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Função para verificar se arquivo existe
file_exists() {
    [ -f "$1" ]
}

# Função para verificar se diretório existe
dir_exists() {
    [ -d "$1" ]
}

# Função para criar diretório se não existir
create_dir_if_not_exists() {
    if [ ! -d "$1" ]; then
        mkdir -p "$1"
        log_info "Diretório criado: $1"
    fi
}

# Função para verificar permissões
check_permissions() {
    if [ ! -w "$1" ]; then
        log_error "Sem permissão de escrita em: $1"
        exit 1
    fi
}

# Função para backup de arquivo
backup_file() {
    local file="$1"
    if file_exists "$file"; then
        local backup="${file}.backup.$(date +%Y%m%d_%H%M%S)"
        cp "$file" "$backup"
        log_info "Backup criado: $backup"
    fi
}

# Função para instalar dependências do sistema
install_system_dependencies() {
    log_info "Instalando dependências do sistema..."

    # Detecta distribuição Linux
    if command_exists apt-get; then
        # Ubuntu/Debian
        log_info "Detectado Ubuntu/Debian"
        sudo apt-get update
        sudo apt-get install -y \
            python3 \
            python3-pip \
            python3-venv \
            curl \
            unzip \
            git \
            build-essential \
            libssl-dev \
            libffi-dev \
            python3-dev

    elif command_exists yum; then
        # CentOS/RHEL/Amazon Linux
        log_info "Detectado CentOS/RHEL/Amazon Linux"
        sudo yum update -y
        sudo yum install -y \
            python3 \
            python3-pip \
            curl \
            unzip \
            git \
            gcc \
            openssl-devel \
            libffi-devel \
            python3-devel

    elif command_exists dnf; then
        # Fedora
        log_info "Detectado Fedora"
        sudo dnf update -y
        sudo dnf install -y \
            python3 \
            python3-pip \
            curl \
            unzip \
            git \
            gcc \
            openssl-devel \
            libffi-devel \
            python3-devel

    else
        log_warning "Distribuição Linux não suportada. Instale manualmente:"
        log_warning "  - Python 3.8+"
        log_warning "  - pip"
        log_warning "  - curl"
        log_warning "  - unzip"
        log_warning "  - git"
        log_warning "  - build tools"
    fi

    log_success "Dependências do sistema instaladas"
}

# Função para instalar AWS CLI
install_aws_cli() {
    log_info "Verificando AWS CLI..."

    if command_exists aws; then
        local version=$(aws --version)
        log_info "AWS CLI já instalado: $version"
        return 0
    fi

    log_info "Instalando AWS CLI v2..."

    # Baixa AWS CLI v2
    local temp_dir=$(mktemp -d)
    cd "$temp_dir"

    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"

    if [ ! -f "awscliv2.zip" ]; then
        log_error "Falha ao baixar AWS CLI"
        return 1
    fi

    # Extrai e instala
    unzip -q awscliv2.zip
    sudo ./aws/install

    # Limpa arquivos temporários
    cd - > /dev/null
    rm -rf "$temp_dir"

    # Verifica instalação
    if command_exists aws; then
        local version=$(aws --version)
        log_success "AWS CLI instalado: $version"
    else
        log_error "Falha na instalação do AWS CLI"
        return 1
    fi
}

# Função para configurar credenciais AWS
setup_aws_credentials() {
    log_info "Configurando credenciais AWS..."

    # Verifica se variáveis de ambiente estão definidas
    if [ -n "$AWS_ACCESS_KEY_ID" ] && [ -n "$AWS_SECRET_ACCESS_KEY" ]; then
        log_info "Usando credenciais de variáveis de ambiente"
        aws configure set aws_access_key_id "$AWS_ACCESS_KEY_ID"
        aws configure set aws_secret_access_key "$AWS_SECRET_ACCESS_KEY"

        if [ -n "$AWS_REGION" ]; then
            aws configure set region "$AWS_REGION"
        else
            aws configure set region "us-east-1"
        fi

        if [ -n "$AWS_SESSION_TOKEN" ]; then
            aws configure set aws_session_token "$AWS_SESSION_TOKEN"
        fi

    else
        log_warning "Credenciais AWS não encontradas nas variáveis de ambiente"
        log_info "Execute manualmente: aws configure"
        log_info "Ou configure as variáveis:"
        log_info "  export AWS_ACCESS_KEY_ID='sua-access-key'"
        log_info "  export AWS_SECRET_ACCESS_KEY='sua-secret-key'"
        log_info "  export AWS_REGION='us-east-1'"
        return 1
    fi

    # Testa credenciais
    if aws sts get-caller-identity > /dev/null 2>&1; then
        local account_id=$(aws sts get-caller-identity --query Account --output text)
        local user_arn=$(aws sts get-caller-identity --query Arn --output text)
        log_success "Credenciais AWS validadas"
        log_info "Account ID: $account_id"
        log_info "User ARN: $user_arn"
    else
        log_error "Falha na validação das credenciais AWS"
        return 1
    fi
}

# Função para criar bucket S3
create_s3_bucket() {
    local bucket_name="$1"
    local region="$2"

    log_info "Verificando bucket S3: $bucket_name"

    # Verifica se bucket já existe
    if aws s3api head-bucket --bucket "$bucket_name" > /dev/null 2>&1; then
        log_info "Bucket S3 já existe: $bucket_name"
        return 0
    fi

    log_info "Criando bucket S3: $bucket_name"

    # Cria bucket
    if [ "$region" = "us-east-1" ]; then
        aws s3api create-bucket --bucket "$bucket_name"
    else
        aws s3api create-bucket \
            --bucket "$bucket_name" \
            --create-bucket-configuration LocationConstraint="$region"
    fi

    # Configura versionamento
    aws s3api put-bucket-versioning \
        --bucket "$bucket_name" \
        --versioning-configuration Status=Enabled

    # Configura criptografia
    aws s3api put-bucket-encryption \
        --bucket "$bucket_name" \
        --server-side-encryption-configuration '{
            "Rules": [
                {
                    "ApplyServerSideEncryptionByDefault": {
                        "SSEAlgorithm": "AES256"
                    }
                }
            ]
        }'

    # Configura política de acesso público (bloqueia)
    aws s3api put-public-access-block \
        --bucket "$bucket_name" \
        --public-access-block-configuration \
        BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true

    log_success "Bucket S3 criado: $bucket_name"
}

# Função para configurar estrutura S3
setup_s3_structure() {
    local bucket_name="$1"

    log_info "Configurando estrutura de pastas no S3..."

    # Lista de pastas padrão
    local folders=(
        "data/"
        "models/"
        "experiments/"
        "logs/"
        "checkpoints/"
        "datasets/"
        "mlflow-artifacts/"
        "tensorboard-logs/"
        "code/"
    )

    for folder in "${folders[@]}"; do
        log_info "Criando pasta: $folder"
        aws s3api put-object \
            --bucket "$bucket_name" \
            --key "$folder" \
            --body "" > /dev/null 2>&1 || true
    done

    log_success "Estrutura S3 configurada"
}

# Função para instalar Python dependencies
install_python_dependencies() {
    log_info "Instalando dependências Python..."

    # Verifica se uv está instalado
    if command_exists uv; then
        log_info "Usando uv para gerenciar dependências"

        # Adiciona dependências AWS
        uv add boto3 sagemaker sagemaker-pytorch-training

        # Sincroniza ambiente
        uv sync

    else
        log_info "Usando pip para gerenciar dependências"

        # Cria ambiente virtual se não existir
        if [ ! -d ".venv" ]; then
            python3 -m venv .venv
            log_info "Ambiente virtual criado: .venv"
        fi

        # Ativa ambiente virtual
        source .venv/bin/activate

        # Instala dependências
        pip install --upgrade pip
        pip install boto3 sagemaker sagemaker-pytorch-training

        log_info "Ambiente virtual ativado: .venv"
    fi

    log_success "Dependências Python instaladas"
}

# Função para configurar IAM
setup_iam() {
    log_info "Configurando IAM..."

    # Nome da role
    local role_name="PetrobrasAnomalyDetectionRole"

    # Verifica se role já existe
    if aws iam get-role --role-name "$role_name" > /dev/null 2>&1; then
        log_info "Role IAM já existe: $role_name"
        return 0
    fi

    log_info "Criando role IAM: $role_name"

    # Cria role
    aws iam create-role \
        --role-name "$role_name" \
        --assume-role-policy-document '{
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "sagemaker.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }'

    # Anexa políticas necessárias
    aws iam attach-role-policy \
        --role-name "$role_name" \
        --policy-arn "arn:aws:iam::aws:policy/AmazonSageMakerFullAccess"

    aws iam attach-role-policy \
        --role-name "$role_name" \
        --policy-arn "arn:aws:iam::aws:policy/AmazonS3FullAccess"

    aws iam attach-role-policy \
        --role-name "$role_name" \
        --policy-arn "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess"

    log_success "Role IAM criada: $role_name"
}

# Função para configurar CloudWatch
setup_cloudwatch() {
    log_info "Configurando CloudWatch..."

    # Nome do log group
    local log_group="/aws/sagemaker/petrobras-anomaly-detection"

    # Verifica se log group já existe
    if aws logs describe-log-groups --log-group-name-prefix "$log_group" --query 'logGroups[?logGroupName==`'"$log_group"'`]' --output text | grep -q "$log_group"; then
        log_info "Log group CloudWatch já existe: $log_group"
        return 0
    fi

    log_info "Criando log group CloudWatch: $log_group"

    # Cria log group
    aws logs create-log-group --log-group-name "$log_group"

    # Configura retenção (30 dias)
    aws logs put-retention-policy \
        --log-group-name "$log_group" \
        --retention-in-days 30

    log_success "Log group CloudWatch criado: $log_group"
}

# Função para configurar SageMaker
setup_sagemaker() {
    log_info "Configurando SageMaker..."

    # Verifica se SageMaker está disponível na região
    local region=$(aws configure get region)

    if ! aws sagemaker list-domains --region "$region" > /dev/null 2>&1; then
        log_warning "SageMaker não está disponível na região: $region"
        log_info "Considere usar uma das seguintes regiões:"
        log_info "  - us-east-1 (N. Virginia)"
        log_info "  - us-west-2 (Oregon)"
        log_info "  - eu-west-1 (Ireland)"
        log_info "  - ap-southeast-1 (Singapore)"
        return 1
    fi

    log_info "SageMaker disponível na região: $region"

    # Lista domínios existentes
    local domains=$(aws sagemaker list-domains --region "$region" --query 'Domains[?DomainName==`petrobras-anomaly-detection`]' --output text)

    if [ -n "$domains" ]; then
        log_info "Domínio SageMaker já existe: petrobras-anomaly-detection"
    else
        log_warning "Domínio SageMaker não encontrado"
        log_info "Crie manualmente no console AWS ou via AWS CLI:"
        log_info "  aws sagemaker create-domain --domain-name petrobras-anomaly-detection ..."
    fi

    log_success "Configuração SageMaker verificada"
}

# Função para criar arquivo de configuração
create_config_files() {
    log_info "Criando arquivos de configuração..."

    # Cria diretório de configuração se não existir
    create_dir_if_not_exists "config"

    # Copia arquivo de configuração AWS se existir
    if file_exists "aws-config.yaml"; then
        cp "aws-config.yaml" "config/aws-config.yaml"
        log_info "Arquivo de configuração copiado: config/aws-config.yaml"
    fi

    # Copia arquivo de variáveis de ambiente se existir
    if file_exists "env.aws.example"; then
        if [ ! -f ".env.aws" ]; then
            cp "env.aws.example" ".env.aws"
            log_warning "Arquivo .env.aws criado. Configure suas credenciais AWS."
        else
            log_info "Arquivo .env.aws já existe"
        fi
    fi

    log_success "Arquivos de configuração criados"
}

# Função para testar configuração
test_configuration() {
    log_info "Testando configuração AWS..."

    # Testa S3
    local bucket_name="petrobras-anomaly-detection"
    local region=$(aws configure get region)

    if aws s3 ls "s3://$bucket_name" > /dev/null 2>&1; then
        log_success "Acesso ao S3 funcionando"
    else
        log_error "Falha no acesso ao S3"
        return 1
    fi

    # Testa SageMaker
    if aws sagemaker list-training-jobs --max-items 1 > /dev/null 2>&1; then
        log_success "Acesso ao SageMaker funcionando"
    else
        log_warning "Falha no acesso ao SageMaker"
    fi

    # Testa CloudWatch
    if aws logs describe-log-groups --max-items 1 > /dev/null 2>&1; then
        log_success "Acesso ao CloudWatch funcionando"
    else
        log_warning "Falha no acesso ao CloudWatch"
    fi

    log_success "Testes de configuração concluídos"
}

# Função para mostrar próximos passos
show_next_steps() {
    echo
    echo "============================================================================="
    echo "🎉 SETUP AWS CONCLUÍDO COM SUCESSO!"
    echo "============================================================================="
    echo
    echo "📋 Próximos passos:"
    echo
    echo "1. 🔐 Configure suas credenciais AWS:"
    echo "   - Edite o arquivo .env.aws com suas credenciais"
    echo "   - Ou execute: aws configure"
    echo
    echo "2. 🚀 Teste a configuração:"
    echo "   python src/aws_config_manager.py"
    echo
    echo "3. 📊 Inicie treinamento:"
    echo "   python src/aws_training.py"
    echo
    echo "4. 📚 Documentação:"
    echo "   - AWS SageMaker: https://docs.aws.amazon.com/sagemaker/"
    echo "   - Boto3: https://boto3.amazonaws.com/v1/documentation/api/latest/index.html"
    echo
    echo "5. 💰 Monitoramento de custos:"
    echo "   - Configure alertas no CloudWatch"
    echo "   - Use AWS Cost Explorer para análise de custos"
    echo
    echo "6. 🔒 Segurança:"
    echo "   - Revise as políticas IAM criadas"
    echo "   - Configure VPC se necessário"
    echo "   - Ative CloudTrail para auditoria"
    echo
    echo "============================================================================="
}

# Função principal
main() {
    echo "🚀 Iniciando setup AWS para Petrobras Offshore Wells Anomaly Detection"
    echo "============================================================================="
    echo

    # Verifica se está rodando como root
    if [ "$EUID" -eq 0 ]; then
        log_error "Não execute este script como root"
        exit 1
    fi

    # Verifica se está no diretório correto
    if [ ! -f "pyproject.toml" ] && [ ! -f "requirements.txt" ]; then
        log_error "Execute este script no diretório raiz do projeto"
        exit 1
    fi

    # Verifica permissões
    check_permissions "."

    # Executa setup
    install_system_dependencies
    install_aws_cli
    setup_aws_credentials
    create_s3_bucket "petrobras-anomaly-detection" "$(aws configure get region)"
    setup_s3_structure "petrobras-anomaly-detection"
    install_python_dependencies
    setup_iam
    setup_cloudwatch
    setup_sagemaker
    create_config_files
    test_configuration

    # Mostra próximos passos
    show_next_steps
}

# Executa função principal
main "$@"
