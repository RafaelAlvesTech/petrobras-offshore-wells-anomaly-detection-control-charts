# 🛢️ Resumo da Integração com Dataset 3W da Petrobras

## 📋 Visão Geral

Este documento resume a integração completa implementada entre o projeto **Petrobras Offshore Wells Anomaly Detection Control Charts** e o **Dataset 3W da Petrobras**. A integração permite usar dados reais da indústria petrolífera para treinar e avaliar modelos de detecção de anomalias.

## 🎯 O que foi Implementado

### 1. **Módulos de Dados (`src/data/`)**
- ✅ **`threew_dataset.py`**: Interface principal com o dataset 3W
- ✅ **`data_loader.py`**: Carregador unificado de dados com cache inteligente
- ✅ **`preprocessing.py`**: Sistema avançado de pré-processamento
- ✅ **`__init__.py`**: Módulo organizado e documentado

### 2. **Sistema de Configuração (`src/config/`)**
- ✅ **`config_manager.py`**: Gerenciador de configurações YAML
- ✅ **`threew_config.py`**: Configurações específicas para o 3W
- ✅ **`__init__.py`**: Módulo de configuração organizado

### 3. **Arquivos de Configuração**
- ✅ **`config/3w_config.yaml`**: Configuração principal do 3W
- ✅ **Configurações padrão**: Valores otimizados para diferentes cenários

### 4. **Scripts de Automação**
- ✅ **`scripts/setup_3w_integration.sh`**: Setup automático para Linux/macOS
- ✅ **`scripts/setup_3w_integration.ps1`**: Setup automático para Windows
- ✅ **`test_3w_integration.py`**: Script de teste da integração

### 5. **Notebooks de Exemplo**
- ✅ **`notebooks/3W_integration_example.py`**: Demonstração completa da integração

### 6. **Documentação**
- ✅ **`docs/3W_INTEGRATION.md`**: Documentação completa da integração
- ✅ **README atualizado**: Instruções de uso integradas

## 🚀 Funcionalidades Implementadas

### **Carregamento de Dados**
- Interface unificada com o dataset 3W
- Suporte a múltiplos formatos (Parquet, CSV)
- Cache inteligente para performance
- Divisão automática treino/validação/teste
- Normalização automática dos dados

### **Pré-processamento Avançado**
- Imputação de valores faltantes (múltiplas estratégias)
- Normalização robusta (Standard, MinMax, Robust)
- Seleção de atributos (mutual_info, f_classif, variance)
- Redução de dimensionalidade (PCA)
- Janelas deslizantes para séries temporais

### **Sistema de Configuração**
- Arquivos YAML para configurações
- Valores padrão otimizados
- Validação de configurações
- Gerenciamento de diferentes ambientes
- Configurações específicas por problema

### **Integração com 3W**
- Carregamento automático de instâncias
- Configuração de folds para validação cruzada
- Metadados do dataset
- Gerenciamento de problemas implementados
- Tratamento de erros robusto

## 📊 Problemas Disponíveis

### **1. Classificador Binário de Fechamento Espúrio de DHSV**
- **Tipo**: Classificação binária
- **Objetivo**: Identificar fechamentos não intencionais de válvulas
- **Aplicação**: Segurança e integridade de poços
- **Métricas**: Accuracy, Precision, Recall, F1-Score, ROC-AUC
- **Validação**: Stratified K-Fold (5 folds)

## 🔧 Como Usar

### **Setup Automático (Recomendado)**
```bash
# Linux/macOS
chmod +x scripts/setup_3w_integration.sh
./scripts/setup_3w_integration.sh

# Windows (PowerShell)
.\scripts\setup_3w_integration.ps1
```

### **Setup Manual**
```bash
# 1. Clonar o dataset 3W
git clone https://github.com/petrobras/3W.git

# 2. Verificar integração
python test_3w_integration.py

# 3. Executar notebook de exemplo
marimo edit notebooks/3W_integration_example.py
```

### **Uso no Código**
```python
from src.data.threew_dataset import is_threew_available
from src.data.data_loader import create_data_loader
from src.data.preprocessing import create_preprocessor

# Verificar disponibilidade
if is_threew_available():
    # Criar carregador
    loader = create_data_loader(use_threew=True, cache_data=True)

    # Carregar dados
    data = loader.load_threew_problem(
        problem_name="01_binary_classifier_of_spurious_closure_of_dhsv",
        fold_config="folds_clf_01",
        normalize=True
    )

    # Pré-processar
    preprocessor = create_preprocessor(
        scaling_method="robust",
        feature_selection_method="mutual_info"
    )

    X_processed = preprocessor.fit_transform(data["X_train"], data["y_train"])
```

## ⚙️ Configurações Disponíveis

### **Carregamento**
- Cache habilitado/desabilitado
- Tamanho do cache (MB)
- Normalização automática
- Proporção de teste
- Estado aleatório

### **Pré-processamento**
- Estratégia de imputação (mean, median, most_frequent)
- Método de normalização (standard, minmax, robust)
- Seleção de atributos (mutual_info, f_classif, variance)
- Número de atributos a selecionar
- Componentes PCA

### **Janelas Deslizantes**
- Tamanho da janela
- Tamanho do passo
- Tipo de padding (same, valid, full)

### **Experimentos**
- Número de folds
- Validação cruzada
- Otimização de hiperparâmetros
- Número de tentativas

## 📈 Métricas e Avaliação

### **Métricas Padrão**
- **Classificação Binária**: Accuracy, Precision, Recall, F1-Score, ROC-AUC
- **Detecção de Anomalias**: AUC-PR, F1-Score (para dados desbalanceados)
- **Validação Cruzada**: Stratified K-Fold para dados desbalanceados

### **Estratégias de Validação**
- Validação cruzada estratificada
- Divisão treino/validação/teste
- Folds configurados automaticamente
- Reproduzibilidade garantida

## 🔍 Testes e Validação

### **Script de Teste**
```bash
python test_3w_integration.py
```

### **Testes Implementados**
- ✅ Imports de módulos
- ✅ Disponibilidade do dataset 3W
- ✅ Sistema de configuração
- ✅ Carregador de dados
- ✅ Pré-processamento
- ✅ Janelas deslizantes
- ✅ Pipeline completo

## 📚 Documentação

### **Arquivos Principais**
- **`docs/3W_INTEGRATION.md`**: Documentação completa
- **`README.md`**: Instruções integradas
- **Docstrings**: Documentação inline dos módulos

### **Exemplos**
- **`notebooks/3W_integration_example.py`**: Notebook demonstrativo
- **`test_3w_integration.py`**: Script de teste
- **Scripts de setup**: Automação da configuração

## 🚨 Troubleshooting

### **Problemas Comuns**
1. **Dataset 3W não encontrado**: Execute `git clone https://github.com/petrobras/3W.git`
2. **Erro de importação**: Verifique se todas as dependências estão instaladas
3. **Erro de memória**: Reduza o tamanho do cache ou use processamento em lotes
4. **Problemas de performance**: Habilite multiprocessamento

### **Soluções**
- Execute o script de setup automático
- Verifique as configurações em `config/3w_config.yaml`
- Consulte a documentação completa
- Execute o script de teste para diagnóstico

## 🔄 Manutenção e Atualizações

### **Atualizar Dataset 3W**
```bash
cd 3W
git pull origin main
cd ..
```

### **Verificar Versões**
```python
from src.data.threew_dataset import get_threew_info
info = get_threew_info()
print(f"Versão: {info['version']}")
```

### **Backup de Configurações**
```python
from src.config.config_manager import get_config_manager
config_manager = get_config_manager()
config_manager.save_config("3w_backup", current_config)
```

## 🎯 Próximos Passos

### **Desenvolvimento Futuro**
1. **Novos Problemas**: Incorporação de mais tipos de eventos
2. **Modelos SOTA**: Implementação de TranAD, LSTM-VAE, USAD
3. **Otimização**: Hiperparâmetros com Optuna
4. **Deployment**: API para inferência em tempo real
5. **Monitoramento**: Dashboards para acompanhamento de performance

### **Contribuições**
- Implementar novos algoritmos
- Adicionar métricas de avaliação
- Melhorar documentação
- Otimizar performance
- Adicionar testes automatizados

## 📞 Suporte

### **Recursos de Ajuda**
1. **Documentação**: `docs/3W_INTEGRATION.md`
2. **Script de teste**: `python test_3w_integration.py`
3. **Notebook de exemplo**: `marimo edit notebooks/3W_integration_example.py`
4. **Documentação oficial 3W**: [GitHub 3W](https://github.com/petrobras/3W)

### **Comunidade**
- [Workshop 3W](https://forms.gle/cmLa2u4VaXd1T7qp8) - 4ª edição em 2025
- [Discussions no GitHub](https://github.com/petrobras/3W/discussions)
- [Issues do projeto](https://github.com/RafaelAlvesTech/petrobras-offshore-wells-anomaly-detection-control-charts/issues)

---

## ✨ Resumo Final

A integração com o Dataset 3W da Petrobras foi **completamente implementada** e oferece:

- 🎯 **Interface unificada** para dados reais da indústria petrolífera
- 🚀 **Performance otimizada** com cache inteligente e multiprocessamento
- 🧹 **Pré-processamento avançado** para séries temporais multivariadas
- ⚙️ **Sistema de configuração** flexível e robusto
- 📊 **Validação cruzada** estratificada para dados desbalanceados
- 🔧 **Scripts de automação** para setup e teste
- 📚 **Documentação completa** com exemplos práticos

**Status**: ✅ **INTEGRAÇÃO COMPLETA E FUNCIONAL**

A integração está pronta para uso em produção e pode ser facilmente estendida para novos problemas e funcionalidades conforme necessário.
