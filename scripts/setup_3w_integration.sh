#!/bin/bash

# Script de configuração para integração com Dataset 3W da Petrobras
# Este script automatiza a configuração da integração com o 3W

set -e  # Para em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para logging
log() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

# Verifica se estamos no diretório raiz do projeto
if [ ! -f "pyproject.toml" ]; then
    error "Execute este script no diretório raiz do projeto"
    exit 1
fi

log "🚀 Iniciando configuração da integração 3W..."

# 1. Verificar se o diretório 3W já existe
if [ -d "3W" ]; then
    warn "Diretório 3W já existe. Atualizando..."
    cd 3W
    git pull origin main
    cd ..
else
    log "📥 Clonando repositório 3W..."
    git clone https://github.com/petrobras/3W.git
fi

# 2. Verificar se o git está disponível
if ! command -v git &> /dev/null; then
    error "Git não está instalado. Instale o git primeiro."
    exit 1
fi

# 3. Verificar se o Python está disponível
if ! command -v python &> /dev/null; then
    error "Python não está instalado. Instale o Python 3.11+ primeiro."
    exit 1
fi

# 4. Verificar se o uv está disponível
if ! command -v uv &> /dev/null; then
    warn "uv não está instalado. Instalando..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.cargo/env
fi

# 5. Criar diretório de logs se não existir
if [ ! -d "logs" ]; then
    log "📁 Criando diretório de logs..."
    mkdir -p logs
fi

# 6. Criar diretório de configurações se não existir
if [ ! -d "config" ]; then
    log "📁 Criando diretório de configurações..."
    mkdir -p config
fi

# 7. Verificar se o ambiente virtual existe
if [ ! -d ".venv" ]; then
    log "🐍 Criando ambiente virtual..."
    uv venv
fi

# 8. Ativar ambiente virtual
log "🔧 Ativando ambiente virtual..."
source .venv/bin/activate

# 9. Sincronizar dependências
log "📦 Sincronizando dependências..."
uv sync

# 10. Verificar se as dependências do 3W estão instaladas
log "🔍 Verificando dependências do 3W..."
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
log "🧪 Testando integração..."
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
if [ ! -f "config/3w_config.yaml" ]; then
    log "⚙️ Criando arquivo de configuração padrão..."
    cat > config/3w_config.yaml << 'EOF'
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
EOF
fi

# 13. Verificar se o notebook de exemplo existe
if [ ! -f "notebooks/3W_integration_example.py" ]; then
    warn "Notebook de exemplo não encontrado. Verifique se foi criado corretamente."
else
    log "📓 Notebook de exemplo encontrado"
fi

# 14. Testar carregamento de dados
log "📊 Testando carregamento de dados..."
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
log "📁 Verificando estrutura do projeto..."
required_dirs=("src/data" "src/config" "notebooks" "config" "logs")
for dir in "${required_dirs[@]}"; do
    if [ -d "$dir" ]; then
        log "✅ Diretório $dir existe"
    else
        warn "⚠️ Diretório $dir não encontrado"
    fi
done

# 16. Resumo final
log "🎉 Configuração da integração 3W concluída!"
echo ""
info "📋 Resumo da configuração:"
echo "   • Repositório 3W: $(if [ -d "3W" ]; then echo "✅ Clonado"; else echo "❌ Não encontrado"; fi)"
echo "   • Ambiente virtual: $(if [ -d ".venv" ]; then echo "✅ Criado"; else echo "❌ Não encontrado"; fi)"
echo "   • Dependências: $(if [ -d ".venv" ]; then echo "✅ Sincronizadas"; else echo "❌ Não sincronizadas"; fi)"
echo "   • Configurações: $(if [ -f "config/3w_config.yaml" ]; then echo "✅ Criadas"; else echo "❌ Não criadas"; fi)"
echo "   • Logs: $(if [ -d "logs" ]; then echo "✅ Diretório criado"; else echo "❌ Não criado"; fi)"
echo ""

# 17. Instruções de uso
info "🚀 Para usar a integração 3W:"
echo ""
echo "1. Execute o notebook de exemplo:"
echo "   marimo edit notebooks/3W_integration_example.py"
echo ""
echo "2. Ou use no seu código Python:"
echo "   from src.data.threew_dataset import is_threew_available"
echo "   from src.data.data_loader import create_data_loader"
echo ""
echo "3. Verifique a documentação completa em: docs/3W_INTEGRATION.md"
echo ""

# 18. Verificar se há problemas
if [ -d "3W" ] && [ -d ".venv" ] && [ -f "config/3w_config.yaml" ]; then
    log "🎯 Integração 3W configurada com sucesso!"
    log "📚 Consulte a documentação para começar a usar: docs/3W_INTEGRATION.md"
else
    warn "⚠️ Alguns componentes podem não ter sido configurados corretamente."
    warn "Verifique os logs acima e execute o script novamente se necessário."
fi

echo ""
log "✨ Configuração concluída! Boa sorte com sua pesquisa em detecção de anomalias!"
