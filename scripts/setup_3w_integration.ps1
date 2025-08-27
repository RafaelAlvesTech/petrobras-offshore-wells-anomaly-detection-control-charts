# Script de configuração para integração com Dataset 3W da Petrobras (Windows)
# Este script automatiza a configuração da integração com o 3W no Windows

param(
    [switch]$Force
)

# Configurações de erro
$ErrorActionPreference = "Stop"

# Função para logging
function Write-Log {
    param(
        [string]$Message,
        [string]$Level = "INFO"
    )

    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $color = switch ($Level) {
        "INFO" { "Green" }
        "WARN" { "Yellow" }
        "ERROR" { "Red" }
        "INFO_BLUE" { "Blue" }
        default { "White" }
    }

    Write-Host "[$timestamp] [$Level] $Message" -ForegroundColor $color
}

function Write-Info {
    param([string]$Message)
    Write-Log $Message "INFO"
}

function Write-Warn {
    param([string]$Message)
    Write-Log $Message "WARN"
}

function Write-Error {
    param([string]$Message)
    Write-Log $Message "ERROR"
}

function Write-InfoBlue {
    param([string]$Message)
    Write-Log $Message "INFO_BLUE"
}

# Verifica se estamos no diretório raiz do projeto
if (-not (Test-Path "pyproject.toml")) {
    Write-Error "Execute este script no diretório raiz do projeto"
    exit 1
}

Write-Info "🚀 Iniciando configuração da integração 3W..."

# 1. Verificar se o diretório 3W já existe
if (Test-Path "3W") {
    Write-Warn "Diretório 3W já existe. Atualizando..."
    Set-Location "3W"
    git pull origin main
    Set-Location ".."
} else {
    Write-Info "📥 Clonando repositório 3W..."
    git clone https://github.com/petrobras/3W.git
}

# 2. Verificar se o git está disponível
try {
    $null = git --version
    Write-Info "✅ Git encontrado"
} catch {
    Write-Error "Git não está instalado. Instale o Git primeiro."
    exit 1
}

# 3. Verificar se o Python está disponível
try {
    $null = python --version
    Write-Info "✅ Python encontrado"
} catch {
    Write-Error "Python não está instalado. Instale o Python 3.11+ primeiro."
    exit 1
}

# 4. Verificar se o uv está disponível
try {
    $null = uv --version
    Write-Info "✅ uv encontrado"
} catch {
    Write-Warn "uv não está instalado. Instalando..."
    # Instalação do uv no Windows
    Invoke-WebRequest -Uri "https://astral.sh/uv/install.ps1" -OutFile "install_uv.ps1"
    & "install_uv.ps1"
    Remove-Item "install_uv.ps1"

    # Recarrega o PATH
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}

# 5. Criar diretório de logs se não existir
if (-not (Test-Path "logs")) {
    Write-Info "📁 Criando diretório de logs..."
    New-Item -ItemType Directory -Path "logs" -Force | Out-Null
}

# 6. Criar diretório de configurações se não existir
if (-not (Test-Path "config")) {
    Write-Info "📁 Criando diretório de configurações..."
    New-Item -ItemType Directory -Path "config" -Force | Out-Null
}

# 7. Verificar se o ambiente virtual existe
if (-not (Test-Path ".venv")) {
    Write-Info "🐍 Criando ambiente virtual..."
    uv venv
}

# 8. Ativar ambiente virtual
Write-Info "🔧 Ativando ambiente virtual..."
& ".venv\Scripts\Activate.ps1"

# 9. Sincronizar dependências
Write-Info "📦 Sincronizando dependências..."
uv sync

# 10. Verificar se as dependências do 3W estão instaladas
Write-Info "🔍 Verificando dependências do 3W..."
python -c "
import sys
try:
    import pyarrow
    import h5py
    import tslearn
    import ydata_profiling
    import numba
    import missingno
    import alive_progress
    import natsort
    import plotly
    import pydantic
    print('✅ Todas as dependências do 3W estão instaladas')
except ImportError as e:
    print(f'❌ Dependência não encontrada: {e}')
    sys.exit(1)
"

# 11. Testar a integração
Write-Info "🧪 Testando integração..."
python -c "
import sys
from pathlib import Path

# Adiciona o caminho do projeto
project_root = Path.cwd()
sys.path.insert(0, str(project_root))

try:
    from src.data.threew_dataset import is_threew_available, get_threew_info
    from src.config.threew_config import get_threew_dataset_config

    if is_threew_available():
        info = get_threew_info()
        print(f'✅ Integração 3W funcionando - Versão: {info.get(\"version\", \"N/A\")}')

        config = get_threew_dataset_config()
        print(f'✅ Configurações carregadas - Problemas: {len(config.get(\"problems\", []))}')
    else:
        print('⚠️ Dataset 3W não disponível (verificar se o diretório 3W está presente)')

except Exception as e:
    print(f'❌ Erro na integração: {e}')
    sys.exit(1)
"

# 12. Criar arquivo de configuração padrão se não existir
if (-not (Test-Path "config/3w_config.yaml")) {
    Write-Info "⚙️ Criando arquivo de configuração padrão..."
    @"
# Configuração para integração com o Dataset 3W da Petrobras
dataset:
  name: "3W"
  version: "1.1.0"
  description: "Dataset 3W da Petrobras para detecção de anomalias em poços offshore"

  paths:
    toolkit: "3W/toolkit"
    dataset: "3W/dataset"
    folds: "3W/dataset/folds"
    problems: "3W/problems"
    overviews: "3W/overviews"

  loading:
    use_cache: true
    cache_size: 1000
    normalize_data: true
    test_size: 0.2
    random_state: 42

  preprocessing:
    imputation_strategy: "mean"
    scaling_method: "robust"
    feature_selection_method: "mutual_info"
    n_features: null
    pca_components: null

  rolling_window:
    window_size: 100
    step_size: 1
    padding: "same"

problems:
  - name: "01_binary_classifier_of_spurious_closure_of_dhsv"
    description: "Classificador binário para fechamento espúrio de DHSV"
    type: "classification"
    target_column: 0

experiments:
  default:
    n_folds: 5
    cross_validation: true
    hyperparameter_optimization: true
    optimization_trials: 100

logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: "logs/3w_integration.log"

cache:
  enabled: true
  max_size: 1000
  ttl: 3600
  backend: "memory"

validation:
  check_data_integrity: true
  validate_schema: true
  check_missing_values: true
  outlier_detection: true

performance:
  use_multiprocessing: true
  n_jobs: -1
  batch_size: 1000
  memory_efficient: true

export:
  formats: ["parquet", "csv", "numpy"]
  compression: "brotli"
  include_metadata: true
  save_preprocessing_pipeline: true
"@ | Out-File -FilePath "config/3w_config.yaml" -Encoding UTF8
}

# 13. Verificar se o notebook de exemplo existe
if (-not (Test-Path "notebooks/3W_integration_example.py")) {
    Write-Warn "Notebook de exemplo não encontrado. Verifique se foi criado corretamente."
} else {
    Write-Info "📓 Notebook de exemplo encontrado"
}

# 14. Testar carregamento de dados
Write-Info "📊 Testando carregamento de dados..."
python -c "
import sys
from pathlib import Path

# Adiciona o caminho do projeto
project_root = Path.cwd()
sys.path.insert(0, str(project_root))

try:
    from src.data.data_loader import create_data_loader

    # Tenta criar o carregador
    loader = create_data_loader(use_threew=True, cache_data=True)
    print('✅ Carregador de dados criado com sucesso')

    # Lista problemas disponíveis
    problems = loader.list_available_problems()
    print(f'✅ Problemas disponíveis: {problems}')

except Exception as e:
    print(f'⚠️ Aviso no carregador de dados: {e}')
"

# 15. Verificar estrutura do projeto
Write-Info "📁 Verificando estrutura do projeto..."
$requiredDirs = @("src/data", "src/config", "notebooks", "config", "logs")
foreach ($dir in $requiredDirs) {
    if (Test-Path $dir) {
        Write-Info "✅ Diretório $dir existe"
    } else {
        Write-Warn "⚠️ Diretório $dir não encontrado"
    }
}

# 16. Resumo final
Write-Info "🎉 Configuração da integração 3W concluída!"
Write-Host ""
Write-InfoBlue "📋 Resumo da configuração:"
Write-Host "   • Repositório 3W: $(if (Test-Path "3W") { "✅ Clonado" } else { "❌ Não encontrado" })"
Write-Host "   • Ambiente virtual: $(if (Test-Path ".venv") { "✅ Criado" } else { "❌ Não encontrado" })"
Write-Host "   • Dependências: $(if (Test-Path ".venv") { "✅ Sincronizadas" } else { "❌ Não sincronizadas" })"
Write-Host "   • Configurações: $(if (Test-Path "config/3w_config.yaml") { "✅ Criadas" } else { "❌ Não criadas" })"
Write-Host "   • Logs: $(if (Test-Path "logs") { "✅ Diretório criado" } else { "❌ Não criado" })"
Write-Host ""

# 17. Instruções de uso
Write-InfoBlue "🚀 Para usar a integração 3W:"
Write-Host ""
Write-Host "1. Execute o notebook de exemplo:"
Write-Host "   marimo edit notebooks/3W_integration_example.py"
Write-Host ""
Write-Host "2. Ou use no seu código Python:"
Write-Host "   from src.data.threew_dataset import is_threew_available"
Write-Host "   from src.data.data_loader import create_data_loader"
Write-Host ""
Write-Host "3. Verifique a documentação completa em: docs/3W_INTEGRATION.md"
Write-Host ""

# 18. Verificar se há problemas
if ((Test-Path "3W") -and (Test-Path ".venv") -and (Test-Path "config/3w_config.yaml")) {
    Write-Info "🎯 Integração 3W configurada com sucesso!"
    Write-Info "📚 Consulte a documentação para começar a usar: docs/3W_INTEGRATION.md"
} else {
    Write-Warn "⚠️ Alguns componentes podem não ter sido configurados corretamente."
    Write-Warn "Verifique os logs acima e execute o script novamente se necessário."
}

Write-Host ""
Write-Info "✨ Configuração concluída! Boa sorte com sua pesquisa em detecção de anomalias!"
