# 🚀 Setup AWS para Petrobras Offshore Wells Anomaly Detection

Este documento descreve como configurar e usar a AWS para treinamento de modelos de detecção de anomalias em poços offshore da Petrobras.

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Pré-requisitos](#pré-requisitos)
- [Setup Automatizado](#setup-automatizado)
- [Setup Manual](#setup-manual)
- [Configuração](#configuração)
- [Uso](#uso)
- [Monitoramento](#monitoramento)
- [Custos](#custos)
- [Segurança](#segurança)
- [Troubleshooting](#troubleshooting)

## 🌟 Visão Geral

O projeto utiliza os seguintes serviços AWS para treinamento de modelos:

- **Amazon SageMaker**: Plataforma de ML para treinamento e deployment
- **Amazon S3**: Armazenamento de dados, modelos e artefatos
- **Amazon EC2**: Instâncias para treinamento customizado
- **Amazon CloudWatch**: Monitoramento e logging
- **AWS IAM**: Gerenciamento de permissões e segurança

### 🎯 Benefícios

- **Escalabilidade**: Treinamento distribuído com múltiplas GPUs
- **Custo-efetividade**: Spot instances e otimização de recursos
- **Integração**: MLflow, TensorBoard e outras ferramentas ML
- **Segurança**: Criptografia, IAM e VPC isolation
- **Monitoramento**: CloudWatch, alertas e métricas

## 🔧 Pré-requisitos

### Sistema

- Linux (Ubuntu 18.04+, CentOS 7+, Amazon Linux 2)
- Python 3.8+
- 4GB RAM mínimo
- 10GB espaço em disco

### Conta AWS

- Conta AWS ativa
- Access Key ID e Secret Access Key
- Permissões para SageMaker, S3, EC2, IAM, CloudWatch
- Região com SageMaker disponível (us-east-1, us-west-2, eu-west-1)

### Software

- AWS CLI v2
- Python 3.8+
- Git

## 🚀 Setup Automatizado

### 1. Clone e Setup Inicial

```bash
# Clone o repositório
git clone <repository-url>
cd petrobras-offshore-wells-anomaly-detection-control-charts

# Torne o script executável
chmod +x scripts/setup_aws.sh

# Execute o setup automatizado
./scripts/setup_aws.sh
```

### 2. Configure Credenciais

```bash
# Configure suas credenciais AWS
export AWS_ACCESS_KEY_ID='sua-access-key'
export AWS_SECRET_ACCESS_KEY='sua-secret-key'
export AWS_REGION='us-east-1'

# Ou use o arquivo .env.aws
cp env.aws.example .env.aws
# Edite .env.aws com suas credenciais
```

### 3. Verifique a Instalação

```bash
# Teste a configuração
python src/aws_config_manager.py

# Verifique o status
aws sts get-caller-identity
```

## 🔧 Setup Manual

### 1. Instalar AWS CLI

```bash
# Ubuntu/Debian
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Verificar instalação
aws --version
```

### 2. Configurar Credenciais

```bash
aws configure
# AWS Access Key ID: [sua-access-key]
# AWS Secret Access Key: [sua-secret-key]
# Default region name: us-east-1
# Default output format: json
```

### 3. Instalar Dependências Python

```bash
# Usando uv (recomendado)
uv add boto3 sagemaker sagemaker-pytorch-training

# Ou usando pip
pip install boto3 sagemaker sagemaker-pytorch-training
```

### 4. Criar Bucket S3

```bash
# Criar bucket
aws s3 mb s3://petrobras-anomaly-detection --region us-east-1

# Configurar versionamento
aws s3api put-bucket-versioning \
    --bucket petrobras-anomaly-detection \
    --versioning-configuration Status=Enabled

# Configurar criptografia
aws s3api put-bucket-encryption \
    --bucket petrobras-anomaly-detection \
    --server-side-encryption-configuration '{
        "Rules": [
            {
                "ApplyServerSideEncryptionByDefault": {
                    "SSEAlgorithm": "AES256"
                }
            }
        ]
    }'
```

### 5. Configurar IAM

```bash
# Criar role para SageMaker
aws iam create-role \
    --role-name PetrobrasAnomalyDetectionRole \
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

# Anexar políticas
aws iam attach-role-policy \
    --role-name PetrobrasAnomalyDetectionRole \
    --policy-arn arn:aws:iam::aws:policy/AmazonSageMakerFullAccess

aws iam attach-role-policy \
    --role-name PetrobrasAnomalyDetectionRole \
    --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess
```

## ⚙️ Configuração

### Arquivo de Configuração

O arquivo `aws-config.yaml` contém todas as configurações:

```yaml
aws:
  region: "us-east-1"
  account_id: "your-account-id"

sagemaker:
  region: "us-east-1"
  domain:
    name: "petrobras-anomaly-detection"
  training:
    default_instance_type: "ml.p3.2xlarge"
    gpu_instance_types:
      - "ml.p3.2xlarge" # 1x V100
      - "ml.p3.8xlarge" # 4x V100
      - "ml.g5.xlarge" # 1x A10G

s3:
  bucket_name: "petrobras-anomaly-detection"
  region: "us-east-1"
```

### Variáveis de Ambiente

Configure o arquivo `.env.aws`:

```bash
# Credenciais AWS
AWS_ACCESS_KEY_ID=your-access-key-id
AWS_SECRET_ACCESS_KEY=your-secret-access-key
AWS_REGION=us-east-1

# SageMaker
SAGEMAKER_ROLE_ARN=arn:aws:iam::your-account:role/PetrobrasAnomalyDetectionRole

# S3
S3_BUCKET_NAME=petrobras-anomaly-detection
```

## 🚀 Uso

### 1. Gerenciador de Configuração

```python
from src.aws_config_manager import AWSConfigManager

# Inicializar gerenciador
manager = AWSConfigManager()

# Verificar status
manager.print_status()

# Criar bucket S3
manager.create_s3_bucket()

# Configurar estrutura S3
manager.setup_s3_structure()
```

### 2. Gerenciador de Treinamento

```python
from src.aws_training import AWSTrainingManager

# Inicializar gerenciador
manager = AWSTrainingManager()

# Obter configuração para LSTM-VAE
config = manager.get_training_config('lstm_vae')

# Criar job de treinamento
job_name = manager.create_training_job(config)

# Monitorar treinamento
status = manager.monitor_training_job(job_name)

# Fazer deploy do modelo
endpoint_name = manager.deploy_model('lstm_vae', job_name)
```

### 3. Treinamento com Hiperparâmetros

```python
# Job de tuning de hiperparâmetros
tuning_job_name = manager.create_hyperparameter_tuning_job(config)

# Monitorar tuning
tuning_status = manager.monitor_training_job(tuning_job_name)
```

### 4. Comandos AWS CLI

```bash
# Listar jobs de treinamento
aws sagemaker list-training-jobs --name-contains petrobras

# Descrever job específico
aws sagemaker describe-training-job --training-job-name <job-name>

# Listar modelos
aws sagemaker list-models --name-contains petrobras

# Listar endpoints
aws sagemaker list-endpoints --name-contains petrobras
```

## 📊 Monitoramento

### CloudWatch

```bash
# Criar log group
aws logs create-log-group --log-group-name "/aws/sagemaker/petrobras-anomaly-detection"

# Configurar retenção
aws logs put-retention-policy \
    --log-group-name "/aws/sagemaker/petrobras-anomaly-detection" \
    --retention-in-days 30

# Criar alarme de custo
aws cloudwatch put-metric-alarm \
    --alarm-name "petrobras-cost-alarm" \
    --metric-name "EstimatedCharges" \
    --namespace "AWS/Billing" \
    --threshold 100 \
    --comparison-operator "GreaterThanThreshold"
```

### SageMaker Studio

- Acesse o console AWS SageMaker
- Vá para "Domains" → "petrobras-anomaly-detection"
- Clique em "Launch app" → "Studio"
- Use notebooks para monitorar treinamentos

### MLflow

```python
import mlflow

# Configurar MLflow
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("petrobras-anomaly-detection")

# Log de métricas
mlflow.log_metric("training_loss", loss_value)
mlflow.log_metric("validation_loss", val_loss_value)
```

## 💰 Custos

### Estimativas de Custo

| Instance Type | GPU     | vCPU | RAM   | Custo/Hora | Custo/Dia |
| ------------- | ------- | ---- | ----- | ---------- | --------- |
| ml.p3.2xlarge | 1x V100 | 8    | 61GB  | $3.06      | $73.44    |
| ml.p3.8xlarge | 4x V100 | 32   | 244GB | $12.24     | $293.76   |
| ml.g5.xlarge  | 1x A10G | 4    | 16GB  | $0.526     | $12.62    |
| ml.g5.2xlarge | 1x A10G | 8    | 32GB  | $0.736     | $17.66    |

### Otimização de Custos

```python
# Usar Spot Instances
estimator = PyTorch(
    # ... outras configurações
    use_spot_instances=True,
    max_wait_time=3600
)

# Estimativa de custo
cost_estimate = manager.get_cost_estimate(config)
print(f"Custo estimado: ${cost_estimate['total_cost']:.2f}")
```

### Alertas de Custo

```bash
# Alarme diário
aws cloudwatch put-metric-alarm \
    --alarm-name "petrobras-daily-cost" \
    --metric-name "EstimatedCharges" \
    --threshold 50 \
    --period 86400

# Alarme mensal
aws cloudwatch put-metric-alarm \
    --alarm-name "petrobras-monthly-cost" \
    --metric-name "EstimatedCharges" \
    --threshold 1000 \
    --period 2592000
```

## 🔒 Segurança

### IAM Best Practices

```bash
# Política de menor privilégio
aws iam create-policy \
    --policy-name PetrobrasAnomalyDetectionPolicy \
    --policy-document '{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:PutObject",
                    "s3:ListBucket"
                ],
                "Resource": [
                    "arn:aws:s3:::petrobras-anomaly-detection",
                    "arn:aws:s3:::petrobras-anomaly-detection/*"
                ]
            }
        ]
    }'
```

### Criptografia

```bash
# S3 Server-Side Encryption
aws s3api put-bucket-encryption \
    --bucket petrobras-anomaly-detection \
    --server-side-encryption-configuration '{
        "Rules": [
            {
                "ApplyServerSideEncryptionByDefault": {
                    "SSEAlgorithm": "AES256"
                }
            }
        ]
    }'

# EBS Encryption (para EC2)
aws ec2 enable-ebs-encryption-by-default
```

### VPC e Networking

```bash
# Criar VPC dedicada
aws ec2 create-vpc --cidr-block 10.0.0.0/16

# Configurar SageMaker com VPC
aws sagemaker create-domain \
    --domain-name petrobras-anomaly-detection \
    --vpc-id vpc-xxxxxxxxx \
    --subnet-ids subnet-xxxxxxxxx subnet-xxxxxxxxx
```

## 🐛 Troubleshooting

### Problemas Comuns

#### 1. Credenciais Inválidas

```bash
# Verificar credenciais
aws sts get-caller-identity

# Reconfigurar
aws configure
```

#### 2. Permissões Insuficientes

```bash
# Verificar políticas anexadas
aws iam list-attached-role-policies --role-name PetrobrasAnomalyDetectionRole

# Anexar política necessária
aws iam attach-role-policy \
    --role-name PetrobrasAnomalyDetectionRole \
    --policy-arn arn:aws:iam::aws:policy/AmazonSageMakerFullAccess
```

#### 3. Região Não Suportada

```bash
# Listar regiões com SageMaker
aws sagemaker list-domains --region us-east-1
aws sagemaker list-domains --region us-west-2
aws sagemaker list-domains --region eu-west-1

# Alterar região padrão
aws configure set region us-east-1
```

#### 4. Bucket S3 Não Acessível

```bash
# Verificar permissões do bucket
aws s3api get-bucket-policy --bucket petrobras-anomaly-detection

# Verificar bloqueios de acesso público
aws s3api get-public-access-block --bucket petrobras-anomaly-detection
```

### Logs e Debug

```bash
# Logs do SageMaker
aws logs describe-log-streams \
    --log-group-name "/aws/sagemaker/petrobras-anomaly-detection"

# Logs específicos do job
aws logs filter-log-events \
    --log-group-name "/aws/sagemaker/petrobras-anomaly-detection" \
    --log-stream-names <log-stream-name>
```

### Suporte AWS

- **AWS Support**: Para problemas técnicos
- **AWS Documentation**: [SageMaker](https://docs.aws.amazon.com/sagemaker/)
- **AWS Forums**: [SageMaker Community](https://forums.aws.amazon.com/forum.jspa?forumID=243)
- **Stack Overflow**: Tag `amazon-sagemaker`

## 📚 Recursos Adicionais

### Documentação

- [AWS SageMaker Developer Guide](https://docs.aws.amazon.com/sagemaker/)
- [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [SageMaker Python SDK](https://sagemaker.readthedocs.io/)

### Exemplos e Tutoriais

- [SageMaker Examples](https://github.com/aws/amazon-sagemaker-examples)
- [MLOps with SageMaker](https://aws.amazon.com/sagemaker/mlops/)
- [Distributed Training](https://docs.aws.amazon.com/sagemaker/latest/dg/distributed-training.html)

### Comunidade

- [AWS ML Blog](https://aws.amazon.com/blogs/machine-learning/)
- [SageMaker Community](https://aws.amazon.com/sagemaker/community/)
- [AWS re:Invent Sessions](https://reinvent.awsevents.com/)

## 🤝 Contribuição

Para contribuir com melhorias na configuração AWS:

1. Fork o repositório
2. Crie uma branch para sua feature
3. Implemente as mudanças
4. Adicione testes
5. Submeta um Pull Request

## 📄 Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE.md](../LICENSE.md) para detalhes.

---

**⚠️ Importante**: Sempre revise as configurações de segurança e custos antes de usar em produção. Configure alertas de custo e monitore o uso dos recursos AWS regularmente.
