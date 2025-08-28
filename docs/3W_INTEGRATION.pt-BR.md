# 🛢️ Integração com Dataset 3W da Petrobras

> **🇺🇸 [View integration in English](3W_INTEGRATION.md)**

## 📋 Visão Geral

Este documento descreve a integração completa do projeto com o **Dataset 3W da Petrobras**, um dataset público para detecção de anomalias em poços offshore. A integração permite usar dados reais da indústria petrolífera para treinar e avaliar modelos de machine learning.

## 🎯 Sobre o Dataset 3W

### Características Principais
- **Fonte**: Petrobras (primeiro repositório público da empresa)
- **Tipo**: Séries temporais multivariadas de poços offshore
- **Eventos**: Detecção de eventos indesejáveis em poços
- **Formato**: Arquivos Parquet com compressão Brotli
- **Licença**: Creative Commons Attribution 4.0 International

### Estrutura dos Dados
- **Instâncias**: Cada arquivo representa uma instância de evento
- **Variáveis**: Pressão, temperatura, vazão, vibração, etc.
- **Labels**: Classificação binária (normal vs. anômalo)
- **Timestamps**: Índice temporal para cada observação

### Problemas Disponíveis
1. **Classificador Binário de Fechamento Espúrio de DHSV**
   - Tipo: Classificação binária
   - Objetivo: Identificar fechamentos não intencionais de válvulas
   - Aplicação: Segurança e integridade de poços

## 🏗️ Arquitetura da Integração

### Módulos Principais

#### 1. `src/data/threew_dataset.py`
Interface principal com o dataset 3W:
- Carregamento de instâncias
- Configuração de folds
- Metadados do dataset
- Gerenciamento de problemas

#### 2. `src/data/data_loader.py`
Carregador de dados unificado:
- Suporte a múltiplos formatos (Parquet, CSV)
- Cache inteligente de dados
- Normalização automática
- Divisão treino/validação/teste

#### 3. `src/data/preprocessing.py`
Pré-processamento avançado:
- Imputação de valores faltantes
- Normalização robusta
- Seleção de atributos
- Redução de dimensionalidade (PCA)
- Janelas deslizantes para séries temporais

#### 4. `src/config/`
Sistema de configuração:
- Configurações YAML
- Valores padrão otimizados
- Validação de configurações
- Gerenciamento de ambientes

## 🚀 Como Usar

### 1. Pré-requisitos

#### Clonar o Repositório 3W
```bash
# Na raiz do projeto
git clone https://github.com/petrobras/3W.git
```

#### Instalar Dependências
```bash
# Atualizar dependências do projeto principal
uv sync

# Ou instalar manualmente as dependências do 3W
cd 3W
conda env create -f environment.yml
conda activate 3W
```

### 2. Uso Básico

#### Verificar Disponibilidade
```python
from src.data.threew_dataset import is_threew_available, get_threew_info

# Verifica se o 3W está disponível
if is_threew_available():
    info = get_threew_info()
    print(f"Dataset 3W disponível - Versão: {info['version']}")
```

#### Carregar Dados
```python
from src.data.data_loader import create_data_loader

# Cria carregador de dados
loader = create_data_loader(use_threew=True, cache_data=True)
```

---

> **🇺🇸 [Ver integração em Inglês](3W_INTEGRATION.md)**

<div align="center">
  <sub>Integrado com ❤️ para detecção de anomalias em poços offshore</sub>
</div>
