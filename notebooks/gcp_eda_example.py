"""
🔍 GCP EDA (Exploratory Data Analysis) Example
===============================================

Este notebook demonstra como fazer EDA no Google Cloud Platform usando:
- Google Cloud Storage para dados
- BigQuery para consultas SQL
- Vertex AI para notebooks
- Polars para manipulação de dados
- Marimo para interface interativa

Autor: Rafael Alves
Projeto: Petrobras Offshore Wells Anomaly Detection
"""

import mo
import polars as pl
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import sys

# Adicionar src ao path para importar módulos do projeto
sys.path.append("src")

# Configurações do GCP
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-project-id")
GCP_REGION = os.getenv("GCP_REGION", "us-central1")
GCS_BUCKET = os.getenv("GCS_BUCKET", "your-bucket-name")

# Configurar estilo dos gráficos
plt.style.use("seaborn-v0_8")
sns.set_palette("husl")

# ============================================================================
# 🔧 CONFIGURAÇÃO DO GCP
# ============================================================================


def setup_gcp_connection():
    """Configura conexão com Google Cloud Platform"""
    try:
        from google.auth import default

        # Autenticação automática
        credentials, project = default()

        if project:
            print(f"✅ Conectado ao projeto GCP: {project}")
            return True
        else:
            print("❌ Falha na autenticação GCP")
            return False

    except ImportError:
        print(
            "❌ Bibliotecas GCP não instaladas. Execute: pip install google-cloud-storage google-cloud-bigquery"
        )
        return False
    except Exception as e:
        print(f"❌ Erro na configuração GCP: {e}")
        return False


# ============================================================================
# 📊 FUNÇÕES DE EDA
# ============================================================================


def load_sample_data():
    """Carrega dados de exemplo para demonstração"""
    # Dados simulados de poços offshore
    np.random.seed(42)
    n_samples = 1000

    data = {
        "timestamp": pl.date_range(
            start=datetime(2023, 1, 1),
            end=datetime(2023, 12, 31),
            interval="1h",
            eager=True,
        )[:n_samples],
        "well_id": np.random.choice(["WELL_001", "WELL_002", "WELL_003"], n_samples),
        "pressure": np.random.normal(150, 20, n_samples),
        "temperature": np.random.normal(85, 10, n_samples),
        "flow_rate": np.random.normal(1000, 200, n_samples),
        "vibration": np.random.normal(0.5, 0.1, n_samples),
        "oil_content": np.random.normal(0.8, 0.05, n_samples),
        "water_content": np.random.normal(0.15, 0.03, n_samples),
        "gas_content": np.random.normal(0.05, 0.02, n_samples),
    }

    # Adicionar algumas anomalias
    anomaly_indices = np.random.choice(n_samples, size=50, replace=False)
    data["pressure"][anomaly_indices] += np.random.normal(50, 10, 50)
    data["temperature"][anomaly_indices] += np.random.normal(15, 5, 50)

    return pl.DataFrame(data)


def basic_eda(df):
    """Análise exploratória básica dos dados"""
    print("🔍 ANÁLISE EXPLORATÓRIA BÁSICA")
    print("=" * 50)

    # Informações básicas
    print(f"📊 Dimensões: {df.shape}")
    print(f"📅 Período: {df['timestamp'].min()} a {df['timestamp'].max()}")
    print(f"🕳️  Poços únicos: {df['well_id'].n_unique()}")

    # Estatísticas descritivas
    print("\n📈 ESTATÍSTICAS DESCRITIVAS:")
    print(df.describe())

    # Valores únicos
    print(f"\n🏷️  POÇOS: {df['well_id'].unique().to_list()}")

    return df


def time_series_analysis(df):
    """Análise de séries temporais"""
    print("\n⏰ ANÁLISE DE SÉRIES TEMPORAIS")
    print("=" * 50)

    # Agregação por hora
    hourly_stats = (
        df.group_by(pl.col("timestamp").dt.hour().alias("hour"))
        .agg(
            [
                pl.col("pressure").mean().alias("avg_pressure"),
                pl.col("temperature").mean().alias("avg_temperature"),
                pl.col("flow_rate").mean().alias("avg_flow_rate"),
            ]
        )
        .sort("hour")
    )

    print("📊 MÉDIAS POR HORA DO DIA:")
    print(hourly_stats)

    return hourly_stats


def anomaly_detection(df):
    """Detecção básica de anomalias usando estatísticas"""
    print("\n🚨 DETECÇÃO DE ANOMALIAS")
    print("=" * 50)

    # Calcular limites para detecção de outliers
    numeric_cols = ["pressure", "temperature", "flow_rate", "vibration"]

    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers = df.filter((pl.col(col) < lower_bound) | (pl.col(col) > upper_bound))

        print(f"🔍 {col.upper()}:")
        print(f"   - Limites: [{lower_bound:.2f}, {upper_bound:.2f}]")
        print(f"   - Outliers: {len(outliers)} ({len(outliers)/len(df)*100:.1f}%)")

    return df


def correlation_analysis(df):
    """Análise de correlação entre variáveis"""
    print("\n🔗 ANÁLISE DE CORRELAÇÃO")
    print("=" * 50)

    # Selecionar colunas numéricas
    numeric_df = df.select(
        [
            "pressure",
            "temperature",
            "flow_rate",
            "vibration",
            "oil_content",
            "water_content",
            "gas_content",
        ]
    )

    # Calcular matriz de correlação
    corr_matrix = numeric_df.corr()

    print("📊 MATRIZ DE CORRELAÇÃO:")
    print(corr_matrix)

    return corr_matrix


def well_comparison(df):
    """Comparação entre diferentes poços"""
    print("\n🕳️  COMPARAÇÃO ENTRE POÇOS")
    print("=" * 50)

    well_stats = df.group_by("well_id").agg(
        [
            pl.col("pressure").mean().alias("avg_pressure"),
            pl.col("temperature").mean().alias("avg_temperature"),
            pl.col("flow_rate").mean().alias("avg_flow_rate"),
            pl.col("vibration").mean().alias("avg_vibration"),
            pl.col("oil_content").mean().alias("avg_oil_content"),
            pl.count().alias("total_readings"),
        ]
    )

    print("📊 ESTATÍSTICAS POR POÇO:")
    print(well_stats)

    return well_stats


def data_quality_check(df):
    """Verificação da qualidade dos dados"""
    print("\n✅ VERIFICAÇÃO DA QUALIDADE DOS DADOS")
    print("=" * 50)

    # Verificar valores nulos
    null_counts = df.null_count()
    print("🔍 VALORES NULOS:")
    for col, count in null_counts.items():
        if count > 0:
            print(f"   - {col}: {count} ({count/len(df)*100:.1f}%)")
        else:
            print(f"   - {col}: ✅ Sem valores nulos")

    # Verificar duplicatas
    duplicates = df.duplicated().sum()
    print(f"\n🔄 DUPLICATAS: {duplicates}")

    # Verificar tipos de dados
    print("\n📝 TIPOS DE DADOS:")
    for col, dtype in df.schema.items():
        print(f"   - {col}: {dtype}")

    return df


def export_to_gcs(df, filename="eda_results.csv"):
    """Exporta resultados para Google Cloud Storage"""
    try:
        from google.cloud import storage

        # Criar cliente do GCS
        client = storage.Client()
        bucket = client.bucket(GCS_BUCKET)

        # Salvar DataFrame como CSV
        csv_content = df.write_csv()
        blob = bucket.blob(f"eda_results/{filename}")
        blob.upload_from_string(csv_content, content_type="text/csv")

        print(f"✅ Dados exportados para GCS: gs://{GCS_BUCKET}/eda_results/{filename}")
        return True

    except Exception as e:
        print(f"❌ Erro ao exportar para GCS: {e}")
        return False


# ============================================================================
# 🎯 EXECUÇÃO PRINCIPAL
# ============================================================================


def main_eda_workflow():
    """Fluxo principal de EDA"""
    print("🚀 INICIANDO EDA NO GOOGLE CLOUD PLATFORM")
    print("=" * 60)

    # 1. Configurar GCP
    if not setup_gcp_connection():
        print("⚠️  Continuando com dados locais...")

    # 2. Carregar dados
    print("\n📥 CARREGANDO DADOS...")
    df = load_sample_data()
    print(f"✅ Dados carregados: {len(df)} registros")

    # 3. EDA Básica
    df = basic_eda(df)

    # 4. Análise temporal
    hourly_stats = time_series_analysis(df)

    # 5. Detecção de anomalias
    df = anomaly_detection(df)

    # 6. Análise de correlação
    corr_matrix = correlation_analysis(df)

    # 7. Comparação entre poços
    well_stats = well_comparison(df)

    # 8. Verificação de qualidade
    df = data_quality_check(df)

    # 9. Exportar para GCS (se configurado)
    if GCP_PROJECT_ID != "your-project-id":
        export_to_gcs(df)

    print("\n🎉 EDA CONCLUÍDA COM SUCESSO!")
    print("=" * 60)

    return df, hourly_stats, corr_matrix, well_stats


# ============================================================================
# 📱 INTERFACE MARIMO
# ============================================================================

# Célula 1: Título e configuração
title_cell = mo.md(
    """
# 🔍 EDA no Google Cloud Platform
## Petrobras Offshore Wells Anomaly Detection

Este notebook demonstra como fazer análise exploratória de dados no GCP usando as melhores práticas do projeto.
"""
)

# Célula 2: Configuração do GCP
gcp_config = mo.md(
    f"""
## ⚙️ Configuração do GCP

- **Projeto**: `{GCP_PROJECT_ID}`
- **Região**: `{GCP_REGION}`
- **Bucket**: `{GCS_BUCKET}`

Para configurar, defina as variáveis de ambiente:
```bash
export GCP_PROJECT_ID="seu-projeto-id"
export GCP_REGION="us-central1"
export GCS_BUCKET="seu-bucket-name"
```
"""
)


# Célula 3: Executar EDA
def run_eda():
    """Executa o workflow completo de EDA"""
    try:
        df, hourly_stats, corr_matrix, well_stats = main_eda_workflow()
        return f"✅ EDA executado com sucesso! {len(df)} registros processados."
    except Exception as e:
        return f"❌ Erro na execução: {e}"


eda_button = mo.md("### 🚀 Executar EDA Completa")
eda_result = mo.md(run_eda)

# Célula 4: Resultados
results_cell = mo.md(
    """
## 📊 Resultados da EDA

Os resultados incluem:
- Análise exploratória básica
- Análise de séries temporais
- Detecção de anomalias
- Análise de correlação
- Comparação entre poços
- Verificação de qualidade dos dados

Execute a célula acima para ver os resultados detalhados.
"""
)

# Célula 5: Próximos passos
next_steps = mo.md(
    """
## 🔮 Próximos Passos

1. **Configurar GCP**: Defina as variáveis de ambiente
2. **Executar EDA**: Use o botão acima para análise completa
3. **Personalizar**: Modifique as funções para seus dados específicos
4. **Integrar**: Use os resultados em modelos de ML
5. **Automatizar**: Configure workflows no GCP para EDA contínua

## 📚 Recursos Adicionais

- [Google Cloud Storage](https://cloud.google.com/storage)
- [BigQuery](https://cloud.google.com/bigquery)
- [Vertex AI](https://cloud.google.com/vertex-ai)
- [Polars Documentation](https://pola.rs/)
- [Marimo Documentation](https://marimo.io/)
"""
)

# Criar aplicação Marimo
app = mo.App(
    title="GCP EDA Example",
    cells=[title_cell, gcp_config, eda_button, eda_result, results_cell, next_steps],
)

if __name__ == "__main__":
    app.run()
