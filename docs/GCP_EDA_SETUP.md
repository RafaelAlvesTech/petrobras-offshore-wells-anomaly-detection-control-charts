# 🔍 Guia Completo: EDA no Google Cloud Platform

## 📋 Visão Geral

Este guia te ajudará a configurar e executar **Exploratory Data Analysis (EDA)** no Google Cloud Platform para o projeto de detecção de anomalias em poços offshore da Petrobras.

## 🎯 O que Você Vai Aprender

- ✅ Configurar autenticação no Google Cloud
- ✅ Usar Google Cloud Storage para dados
- ✅ Executar EDA com Polars e Python
- ✅ Detectar anomalias em séries temporais
- ✅ Visualizar dados com gráficos interativos
- ✅ Exportar resultados para o GCP

## 🚀 Passo 1: Configuração do Google Cloud

### 1.1 Criar Projeto GCP

```bash
# Via gcloud CLI
gcloud projects create petrobras-anomaly-detection --name="Petrobras Anomaly Detection"
gcloud config set project petrobras-anomaly-detection

# Ou via Console Web: https://console.cloud.google.com/
```

### 1.2 Habilitar APIs Necessárias

```bash
# APIs essenciais para EDA
gcloud services enable storage.googleapis.com
gcloud services enable bigquery.googleapis.com
gcloud services enable aiplatform.googleapis.com
gcloud services enable compute.googleapis.com
```

### 1.3 Configurar Autenticação

#### Opção A: Service Account (Recomendado para CI/CD)

```bash
# Criar conta de serviço
gcloud iam service-accounts create eda-service-account \
    --display-name="EDA Service Account"

# Atribuir roles necessários
gcloud projects add-iam-policy-binding petrobras-anomaly-detection \
    --member="serviceAccount:eda-service-account@petrobras-anomaly-detection.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

gcloud projects add-iam-policy-binding petrobras-anomaly-detection \
    --member="serviceAccount:eda-service-account@petrobras-anomaly-detection.iam.gserviceaccount.com" \
    --role="roles/bigquery.dataEditor"

# Baixar credenciais
gcloud iam service-accounts keys create ~/gcp-credentials.json \
    --iam-account=eda-service-account@petrobras-anomaly-detection.iam.gserviceaccount.com
```

#### Opção B: Workload Identity Federation (Recomendado para GitHub Actions)

```bash
# Configurar Workload Identity Pool
gcloud iam workload-identity-pool create "github-actions-pool" \
    --location="global" \
    --display-name="GitHub Actions Pool"

# Configurar Workload Identity Provider
gcloud iam workload-identity-pool-providers create-oidc "github-provider" \
    --workload-identity-pool="github-actions-pool" \
    --location="global" \
    --issuer-uri="https://token.actions.githubusercontent.com" \
    --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository"

# Configurar Service Account
gcloud iam service-accounts create github-actions-sa \
    --display-name="GitHub Actions Service Account"

# Atribuir roles
gcloud projects add-iam-policy-binding petrobras-anomaly-detection \
    --member="serviceAccount:github-actions-sa@petrobras-anomaly-detection.iam.gserviceaccount.com" \
    --role="roles/storage.admin"
```

## 🗄️ Passo 2: Configurar Google Cloud Storage

### 2.1 Criar Bucket para Dados

```bash
# Criar bucket principal
gsutil mb -p petrobras-anomaly-detection -c STANDARD -l us-central1 gs://petrobras-eda-data

# Criar estrutura de pastas
gsutil mb gs://petrobras-eda-data/raw-data
gsutil mb gs://petrobras-eda-data/processed-data
gsutil mb gs://petrobras-eda-data/eda-results
gsutil mb gs://petrobras-eda-data/models
```

### 2.2 Upload de Dados de Exemplo

```bash
# Criar dados de exemplo
python -c "
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
    'vibration': np.random.normal(0.5, 0.1, n_samples)
})

# Salvar localmente
data.to_csv('sample_well_data.csv', index=False)
print('Dados de exemplo criados: sample_well_data.csv')
"

# Upload para GCS
gsutil cp sample_well_data.csv gs://petrobras-eda-data/raw-data/
```

## 🐍 Passo 3: Configurar Ambiente Python

### 3.1 Instalar Dependências

```bash
# Atualizar requirements.txt
uv add google-cloud-storage google-cloud-bigquery google-auth

# Ou instalar manualmente
pip install google-cloud-storage google-cloud-bigquery google-auth
```

### 3.2 Configurar Variáveis de Ambiente

```bash
# Adicionar ao ~/.bashrc ou ~/.zshrc
export GCP_PROJECT_ID="petrobras-anomaly-detection"
export GCP_REGION="us-central1"
export GCS_BUCKET="petrobras-eda-data"
export GOOGLE_APPLICATION_CREDENTIALS="~/gcp-credentials.json"

# Recarregar
source ~/.bashrc
```

## 🔍 Passo 4: Executar EDA

### 4.1 Executar Notebook Local

```bash
# Executar o notebook de exemplo
python notebooks/gcp_eda_example.py
```

### 4.2 Executar via Marimo

```bash
# Iniciar interface Marimo
marimo edit notebooks/gcp_eda_example.py
```

### 4.3 Executar no Vertex AI (Recomendado para Produção)

```bash
# Criar notebook no Vertex AI
gcloud ai notebooks instances create petrobras-eda-notebook \
    --vm-image-project=deeplearning-platform-release \
    --vm-image-family=tf-latest-cpu \
    --machine-type=e2-medium \
    --location=us-central1

# Acessar via console web
# https://console.cloud.google.com/vertex-ai/workbench
```

## 📊 Passo 5: Análise de Dados

### 5.1 EDA Básica

```python
import polars as pl
from google.cloud import storage

# Carregar dados do GCS
client = storage.Client()
bucket = client.bucket('petrobras-eda-data')
blob = bucket.blob('raw-data/sample_well_data.csv')

# Ler dados
df = pl.read_csv(blob.download_as_string())

# EDA básica
print(f"Dimensões: {df.shape}")
print(f"Colunas: {df.columns}")
print(f"Tipos: {df.schema}")
print(f"Estatísticas: {df.describe()}")
```

### 5.2 Análise de Séries Temporais

```python
# Agregação por hora
hourly_stats = df.group_by(
    pl.col('timestamp').dt.hour().alias('hour')
).agg([
    pl.col('pressure').mean().alias('avg_pressure'),
    pl.col('temperature').mean().alias('avg_temperature'),
    pl.col('flow_rate').mean().alias('avg_flow_rate')
]).sort('hour')

print(hourly_stats)
```

### 5.3 Detecção de Anomalias

```python
# Detectar outliers usando IQR
def detect_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = df.filter(
        (pl.col(column) < lower_bound) | (pl.col(column) > upper_bound)
    )

    return outliers, lower_bound, upper_bound

# Aplicar para cada coluna numérica
numeric_cols = ['pressure', 'temperature', 'flow_rate', 'vibration']
for col in numeric_cols:
    outliers, lower, upper = detect_outliers(df, col)
    print(f"{col}: {len(outliers)} outliers [{lower:.2f}, {upper:.2f}]")
```

## 📈 Passo 6: Visualizações

### 6.1 Gráficos de Séries Temporais

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Configurar estilo
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Gráfico de pressão ao longo do tempo
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# Pressão
axes[0, 0].plot(df['timestamp'], df['pressure'])
axes[0, 0].set_title('Pressão ao Longo do Tempo')
axes[0, 0].set_xlabel('Tempo')
axes[0, 0].set_ylabel('Pressão (bar)')

# Temperatura
axes[0, 1].plot(df['timestamp'], df['temperature'])
axes[0, 1].set_title('Temperatura ao Longo do Tempo')
axes[0, 1].set_xlabel('Tempo')
axes[0, 1].set_ylabel('Temperatura (°C)')

# Taxa de fluxo
axes[1, 0].plot(df['timestamp'], df['flow_rate'])
axes[1, 0].set_title('Taxa de Fluxo ao Longo do Tempo')
axes[1, 0].set_xlabel('Tempo')
axes[1, 0].set_ylabel('Taxa de Fluxo (bbl/d)')

# Vibração
axes[1, 1].plot(df['timestamp'], df['vibration'])
axes[1, 1].set_title('Vibração ao Longo do Tempo')
axes[1, 1].set_xlabel('Tempo')
axes[1, 1].set_ylabel('Vibração (g)')

plt.tight_layout()
plt.show()
```

### 6.2 Matriz de Correlação

```python
# Calcular correlação
corr_matrix = df.select([
    'pressure', 'temperature', 'flow_rate', 'vibration'
]).corr()

# Visualizar
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Matriz de Correlação - Variáveis dos Poços')
plt.show()
```

## 💾 Passo 7: Exportar Resultados

### 7.1 Salvar no GCS

```python
# Exportar resultados processados
def export_to_gcs(df, filename, bucket_name='petrobras-eda-data'):
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    # Salvar como CSV
    csv_content = df.write_csv()
    blob = bucket.blob(f'eda-results/{filename}')
    blob.upload_from_string(csv_content, content_type='text/csv')

    print(f"✅ Exportado para: gs://{bucket_name}/eda-results/{filename}")

# Exportar estatísticas
export_to_gcs(hourly_stats, 'hourly_statistics.csv')
export_to_gcs(well_comparison, 'well_comparison.csv')
```

### 7.2 Salvar Gráficos

```python
# Salvar gráficos no GCS
def save_plot_to_gcs(fig, filename, bucket_name='petrobras-eda-data'):
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    # Salvar localmente primeiro
    local_path = f'/tmp/{filename}'
    fig.savefig(local_path, dpi=300, bbox_inches='tight')

    # Upload para GCS
    blob = bucket.blob(f'eda-results/plots/{filename}')
    blob.upload_from_filename(local_path)

    print(f"✅ Gráfico salvo em: gs://{bucket_name}/eda-results/plots/{filename}")

# Salvar gráficos
save_plot_to_gcs(fig, 'time_series_analysis.png')
```

## 🔄 Passo 8: Automação

### 8.1 Workflow Diário

```python
# Criar script para EDA automática
def daily_eda_workflow():
    """Executa EDA diária automaticamente"""
    from datetime import datetime

    print(f"🚀 Iniciando EDA diária: {datetime.now()}")

    # 1. Carregar dados mais recentes
    df = load_latest_data_from_gcs()

    # 2. Executar análises
    results = run_complete_eda(df)

    # 3. Salvar resultados
    save_results_to_gcs(results)

    # 4. Enviar notificação (opcional)
    send_notification("EDA diária concluída")

    print("✅ EDA diária concluída com sucesso!")

# Agendar execução
# Usar cron ou Cloud Scheduler
```

### 8.2 Cloud Function para EDA

```python
# main.py para Cloud Function
import functions_framework
from google.cloud import storage
import polars as pl

@functions_framework.http
def eda_trigger(request):
    """Cloud Function para EDA automática"""

    # Executar EDA
    results = run_eda_workflow()

    # Salvar resultados
    save_to_gcs(results)

    return {"status": "success", "message": "EDA executada"}
```

## 🚨 Solução de Problemas

### Problema: Erro de Autenticação

```bash
# Verificar credenciais
gcloud auth list
gcloud config list

# Reautenticar se necessário
gcloud auth login
gcloud auth application-default login
```

### Problema: Permissões Insuficientes

```bash
# Verificar permissões
gcloud projects get-iam-policy petrobras-anomaly-detection

# Adicionar permissões
gcloud projects add-iam-policy-binding petrobras-anomaly-detection \
    --member="user:seu-email@gmail.com" \
    --role="roles/storage.admin"
```

### Problema: Dados Não Carregam

```python
# Verificar se o bucket existe
from google.cloud import storage
client = storage.Client()
buckets = list(client.list_buckets())
print([b.name for b in buckets])

# Verificar se o arquivo existe
bucket = client.bucket('petrobras-eda-data')
blobs = list(bucket.list_blobs())
print([b.name for b in blobs])
```

## 📚 Recursos Adicionais

### Documentação Oficial

- [Google Cloud Storage](https://cloud.google.com/storage/docs)
- [BigQuery](https://cloud.google.com/bigquery/docs)
- [Vertex AI](https://cloud.google.com/vertex-ai/docs)
- [Google Cloud Python Client](https://googleapis.dev/python/storage/latest/index.html)

### Tutoriais e Exemplos

- [EDA com Python no GCP](https://cloud.google.com/ai-platform/notebooks/docs/tutorials)
- [Análise de Séries Temporais](https://cloud.google.com/architecture/time-series-analysis)
- [Detecção de Anomalias](https://cloud.google.com/architecture/anomaly-detection)

### Comunidade

- [Google Cloud Community](https://cloud.google.com/community)
- [Stack Overflow - Google Cloud](https://stackoverflow.com/questions/tagged/google-cloud-platform)
- [GitHub - Google Cloud Samples](https://github.com/GoogleCloudPlatform)

## 🎉 Próximos Passos

1. **Configure seu projeto GCP** seguindo os passos acima
2. **Execute o notebook de exemplo** para familiarizar-se com o processo
3. **Personalize as análises** para seus dados específicos
4. **Implemente automação** para EDA contínua
5. **Integre com modelos de ML** para detecção de anomalias avançada

---

**🎯 Dica Pro**: Comece com o notebook de exemplo e vá incrementando gradualmente. O GCP oferece muitas ferramentas poderosas, mas é melhor dominar o básico primeiro!

**📞 Suporte**: Se encontrar problemas, verifique os logs do GCP e consulte a documentação oficial. A comunidade é muito ativa e útil!
