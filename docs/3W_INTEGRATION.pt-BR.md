# 🛢️ Integração com Dataset 3W da Petrobras

> **🇺🇸 [View integration in English](3W_INTEGRATION.md)**

## 📋 Visão Geral

Este documento descreve a integração completa do projeto com o **Dataset 3W da Petrobras**, um dataset público para detecção de anomalias em poços offshore. A integração permite usar dados reais da indústria petrolífera para treinar e avaliar modelos de machine learning.

## 🎯 Sobre o Dataset 3W

### Contexto do Projeto

O **Projeto 3W** é o primeiro repositório público da Petrobras no GitHub, lançado em 30 de maio de 2022. Representa uma ação estratégica liderada pelo departamento de Flow Assurance da Petrobras e centro de pesquisa (CENPES), com governança agora incluindo o departamento de Integridade de Poços desde 1º de maio de 2024.

### Características Principais

- **Fonte**: Petrobras (primeiro repositório público da empresa)
- **Tipo**: Séries temporais multivariadas de poços offshore
- **Eventos**: Detecção de eventos indesejáveis em poços
- **Formato**: Arquivos Parquet com compressão Brotli
- **Licença**: Creative Commons Attribution 4.0 International
- **Repositório**: [https://github.com/petrobras/3W](https://github.com/petrobras/3W)

### Motivação & Impacto

- **Perdas de Produção**: Eventos indesejáveis podem causar até 5% de perdas de produção
- **Custos de Manutenção**: Operações de sonda marítima excedem US$500.000 por dia
- **Segurança**: Prevenção de acidentes ambientais e humanos
- **Inovação**: Primeiro piloto do programa "Conexões para Inovação - Módulo Open Lab" da Petrobras

### Estratégia & Governança

- **Projeto Aberto**: Recursos publicamente disponíveis para desenvolvimento colaborativo global
- **Dirigido pela Comunidade**: Comunidade global em expansão de pesquisadores, startups e empresas
- **Evolução Contínua**: Dataset e toolkit evoluem com contribuições da comunidade
- **Rotulagem Profissional**: Profissionais especializados para rotulagem de instâncias
- **Ferramentas Digitais**: Investimento em ferramentas de rotulagem e exportação

### Estrutura dos Dados

- **Instâncias**: Cada arquivo representa uma instância de evento
- **Variáveis**: Pressão, temperatura, vazão, vibração, etc.
- **Labels**: Classificação binária (normal vs. anômalo)
- **Timestamps**: Índice temporal para cada observação
- **Compressão**: Compressão Brotli para armazenamento eficiente

### Problemas Disponíveis

1. **Classificador Binário de Fechamento Espúrio de DHSV**
   - Tipo: Classificação binária
   - Objetivo: Identificar fechamentos não intencionais de válvulas
   - Aplicação: Segurança e integridade de poços
   - Fase: Monitoramento da fase de produção

### Estratégia de Versionamento

- **Versão do Toolkit 3W**: Especificada no arquivo `__init__.py`
- **Versão do Dataset 3W**: Especificada no arquivo `dataset.ini`
- **Versão do Projeto 3W**: Tags do repositório Git com versionamento semântico
- **Evolução Independente**: Versões do dataset e toolkit são completamente independentes

## 🌍 Comunidade 3W & Recursos

### Comunidade Global

A Comunidade 3W está se expandindo globalmente, composta por:

- **Profissionais independentes** e pesquisadores
- **Instituições de pesquisa** de diferentes países
- **Startups** e empresas de tecnologia
- **Operadores de petróleo** e parceiros da indústria

### Recursos Principais

- **Repositório Oficial**: [https://github.com/petrobras/3W](https://github.com/petrobras/3W)
- **Estrutura do Dataset**: [3W_DATASET_STRUCTURE.md](https://github.com/petrobras/3W/blob/main/3W_DATASET_STRUCTURE.md)
- **Estrutura do Toolkit**: [3W_TOOLKIT_STRUCTURE.md](https://github.com/petrobras/3W/blob/main/3W_TOOLKIT_STRUCTURE.md)
- **Guia de Contribuição**: [CONTRIBUTING.md](https://github.com/petrobras/3W/blob/main/CONTRIBUTING.md)
- **Código de Conduta**: [CODE_OF_CONDUCT.md](https://github.com/petrobras/3W/blob/main/CODE_OF_CONDUCT.md)

### Engajamento da Comunidade

- **Discussões no GitHub**: [https://github.com/petrobras/3W/discussions](https://github.com/petrobras/3W/discussions)
- **Workshop Anual**: 4ª edição em 2025 - [Formulário de Inscrição](https://forms.gle/cmLa2u4VaXd1T7qp8)
- **Código Aberto**: Licença Apache 2.0 para contribuições de código
- **Desenvolvimento Colaborativo**: Evolução dirigida pela comunidade de ferramentas e datasets

### Impacto na Pesquisa

- **Artigos Acadêmicos**: Dataset descrito em "A realistic and public dataset with rare undesirable real events in oil wells" (Journal of Petroleum Science and Engineering)
- **Dataset de Referência**: Primeiro dataset público realista com eventos indesejáveis reais raros em poços de petróleo
- **Machine Learning**: Desenvolvimento de técnicas de ML para dificuldades de dados reais
- **Padrões da Indústria**: Padronização de pontos-chave do pipeline de ML

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
