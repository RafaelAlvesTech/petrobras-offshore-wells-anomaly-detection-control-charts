# 🌟 Diretrizes de Contribuição - Detecção de Anomalias em Poços Offshore da Petrobras

> **🇺🇸 [View contributing guidelines in English](CONTRIBUTING.md)**

## 🎯 Bem-vindo Contribuidores!

Obrigado pelo seu interesse em contribuir para o projeto **Detecção de Anomalias em Poços Offshore da Petrobras**! Este é um projeto PIBIC (Programa Institucional de Bolsas de Iniciação Científica) focado na detecção de anomalias em séries temporais multivariadas de poços offshore usando técnicas de machine learning de última geração.

## 🚀 Como Contribuir

### 📋 Antes de Começar

1. **Leia a documentação do projeto** - Entenda os objetivos e arquitetura
2. **Verifique issues existentes** - Veja se sua ideia já está sendo trabalhada
3. **Participe das discussões** - Junte-se às Discussões e Issues do GitHub
4. **Configure seu ambiente** - Siga o [Guia de Configuração](docs/setup-guide.md)

### 🔄 Fluxo de Contribuição

#### 1. **Fork & Clone**

```bash
# Faça fork do repositório no GitHub
# Então clone seu fork
git clone https://github.com/SEU_USUARIO/petrobras-offshore-wells-anomaly-detection.git
cd petrobras-offshore-wells-anomaly-detection

# Adicione o remote upstream
git remote add upstream https://github.com/REPO_ORIGINAL/petrobras-offshore-wells-anomaly-detection.git
```

#### 2. **Criar Branch de Feature**

```bash
# Crie e mude para uma nova branch
git checkout -b feature/nome-da-sua-feature

# Ou para correções de bugs
git checkout -b fix/descricao-do-seu-bug
```

#### 3. **Fazer Mudanças**

- Siga os [padrões de código](#-padrões-de-código)
- Escreva testes para nova funcionalidade
- Atualize documentação conforme necessário
- Certifique-se de que todos os testes passem

#### 4. **Commit das Mudanças**

```bash
# Use commits convencionais
git commit -m "feat: adicionar novo modelo de detecção de anomalias"

# Ou para correções de bugs
git commit -m "fix: resolver problema de pré-processamento de dados"
```

#### 5. **Push & Criar Pull Request**

```bash
git push origin feature/nome-da-sua-feature
# Crie PR no GitHub com descrição detalhada
```

## 📝 Padrões de Código

### 🐍 Estilo de Código Python

#### **Type Hints & Documentação**

```python
from typing import List, Optional, Union
import numpy as np
import polars as pl

def detect_anomalies(
    data: pl.DataFrame,
    threshold: float = 0.95,
    window_size: Optional[int] = None
) -> tuple[List[int], np.ndarray]:
    """
    Detecta anomalias em dados de séries temporais multivariadas.

    Args:
        data: DataFrame de entrada com dados de séries temporais
        threshold: Limiar de detecção de anomalias (0.0 a 1.0)
        window_size: Tamanho da janela deslizante para análise

    Returns:
        Tupla de (indices_anomalias, scores_anomalias)

    Raises:
        ValueError: Se o threshold estiver fora do intervalo válido
    """
    if not 0.0 <= threshold <= 1.0:
        raise ValueError("Threshold deve estar entre 0.0 e 1.0")

    # Implementação aqui...
    return indices_anomalias, scores_anomalias
```

#### **Formatação de Código**

- Use **Ruff** para formatação e linting
- Comprimento máximo de linha: **88 caracteres**
- Use **f-strings** para formatação de strings
- Prefira **list comprehensions** sobre loops explícitos quando apropriado

#### **Organização de Imports**

```python
# Imports da biblioteca padrão
import os
import sys
from typing import List, Optional

# Imports de terceiros
import numpy as np
import polars as pl
import torch

# Imports locais
from src.models.base import BaseModel
from src.utils.helpers import validate_data
```

### 🧪 Padrões de Teste

#### **Estrutura de Teste**

```python
# tests/test_models.py
import pytest
import polars as pl
from src.models.anomaly_detector import AnomalyDetector

class TestAnomalyDetector:
    """Suite de testes para a classe AnomalyDetector."""

    @pytest.fixture
    def sample_data(self) -> pl.DataFrame:
        """Cria dados de exemplo para teste."""
        return pl.DataFrame({
            "timestamp": range(100),
            "pressure": [100 + i * 0.1 for i in range(100)],
            "temperature": [25 + i * 0.05 for i in range(100)]
        })

    def test_detector_initialization(self):
        """Testa se o detector inicializa corretamente."""
        detector = AnomalyDetector(threshold=0.95)
        assert detector.threshold == 0.95
        assert detector.is_fitted is False

    def test_detector_fitting(self, sample_data):
        """Testa o processo de treinamento do detector."""
        detector = AnomalyDetector(threshold=0.95)
        detector.fit(sample_data)
        assert detector.is_fitted is True
        assert detector.n_features == 2
```

#### **Requisitos de Cobertura de Testes**

- **Cobertura mínima**: 80%
- **Funções críticas**: 95% de cobertura
- **Novas funcionalidades**: Devem incluir testes
- **Correções de bugs**: Devem incluir testes de regressão

### 📚 Padrões de Documentação

#### **Formato de Docstring (Estilo Google)**

```python
def train_model(
    data: pl.DataFrame,
    model_type: str = "tranad",
    hyperparameters: Optional[dict] = None
) -> BaseModel:
    """Treina um modelo de detecção de anomalias.

    Esta função treina vários tipos de modelos de detecção de anomalias
    incluindo TranAD, LSTM-VAE e USAD.

    Args:
        data: Dados de treinamento como DataFrame Polars
        model_type: Tipo de modelo para treinar ('tranad', 'lstm-vae', 'usad')
        hyperparameters: Dicionário opcional de hiperparâmetros

    Returns:
        Instância do modelo treinado

    Raises:
        ValueError: Se model_type não for suportado
        DataError: Se o formato dos dados for inválido

    Example:
        >>> data = load_well_data("well_001.csv")
        >>> model = train_model(data, "tranad")
        >>> predictions = model.predict(data)
    """
```

#### **Atualizações do README**

- Atualize README.md para novas funcionalidades
- Inclua exemplos de uso
- Atualize instruções de instalação se necessário
- Adicione novas dependências aos requirements

## 🔧 Configuração de Desenvolvimento

### **Configuração do Ambiente**

```bash
# Clone e configuração
git clone <seu-fork>
cd petrobras-offshore-wells-anomaly-detection

# Criar ambiente virtual
uv venv
source .venv/bin/activate  # Linux/macOS
# ou .venv\Scripts\activate  # Windows

# Instalar dependências
uv sync --group dev

# Instalar hooks pre-commit
uv run pre-commit install
```

### **Hooks Pre-commit**

O projeto usa hooks pre-commit para garantir qualidade do código:

- **Ruff**: Formatação e linting de código
- **Black**: Formatação de código
- **MyPy**: Verificação de tipos
- **Pytest**: Execução de testes

### **Executar Verificações de Qualidade**

```bash
# Formatar código
uv run ruff format .

# Lint código
uv run ruff check .

# Verificação de tipos
uv run mypy src/

# Executar testes
uv run pytest

# Executar todas as verificações
uv run pre-commit run --all-files
```

## 📊 Diretrizes de Pull Request

### **Template de PR**

```markdown
## 🎯 Descrição

Breve descrição das mudanças e motivação

## 🔧 Mudanças Feitas

- [ ] Funcionalidade A adicionada
- [ ] Bug B corrigido
- [ ] Documentação C atualizada

## 🧪 Testes

- [ ] Testes unitários passam
- [ ] Testes de integração passam
- [ ] Teste manual completado

## 📚 Documentação

- [ ] Código documentado
- [ ] README atualizado
- [ ] Documentação da API atualizada

## 🔍 Checklist

- [ ] Código segue diretrizes de estilo
- [ ] Testes adicionados para nova funcionalidade
- [ ] Todos os testes existentes passam
- [ ] Documentação atualizada
- [ ] Nenhuma mudança quebra funcionalidade introduzida
```

### **Processo de Revisão**

1. **Verificações automatizadas** devem passar
2. **Revisão de código** por mantenedores
3. **Requisitos de cobertura de testes** atendidos
4. **Documentação** atualizada
5. **Squash commits** antes do merge

## 🐛 Relatórios de Bugs

### **Template de Relatório de Bug**

```markdown
## 🐛 Descrição do Bug

Descrição clara do bug

## 🔍 Passos para Reproduzir

1. Passo 1
2. Passo 2
3. Passo 3

## 📱 Comportamento Esperado vs Atual

- **Esperado**: O que deveria acontecer
- **Atual**: O que realmente acontece

## 💻 Ambiente

- OS: [ex: Ubuntu 20.04]
- Python: [ex: 3.11.5]
- Versões dos pacotes: [ex: polars==1.32.3]

## 📋 Contexto Adicional

Qualquer outra informação relevante
```

## 💡 Solicitações de Funcionalidades

### **Template de Solicitação de Funcionalidade**

```markdown
## 🚀 Descrição da Funcionalidade

Descrição clara da funcionalidade solicitada

## 🎯 Caso de Uso

Por que esta funcionalidade é necessária e como será usada

## 🔧 Ideias de Implementação

Qualquer pensamento sobre como implementar esta funcionalidade

## 📚 Issues Relacionadas

Links para issues ou discussões relacionadas
```

## 🤝 Diretrizes da Comunidade

### **Código de Conduta**

- **Seja respeitoso** e inclusivo
- **Ajude novatos** a começar
- **Forneça feedback construtivo**
- **Foque no código**, não na pessoa
- **Celebre contribuições** e melhorias

### **Canais de Comunicação**

- **GitHub Issues**: Relatórios de bugs e solicitações de funcionalidades
- **GitHub Discussions**: Perguntas gerais e ideias
- **Pull Requests**: Contribuições de código
- **Email**: [seu.email@universidade.edu]

## 🏆 Reconhecimento

### **Níveis de Contribuidor**

- **🌱 Novo Contribuidor**: Primeira contribuição
- **🌿 Contribuidor Regular**: Múltiplas contribuições
- **🌳 Contribuidor Principal**: Contribuições significativas
- **🏆 Mantenedor**: Liderança do projeto

### **Hall da Fama**

Contribuidores serão reconhecidos em:

- README do projeto
- Notas de release
- Documentação de contribuidores
- Agradecimentos anuais

## 📞 Obtendo Ajuda

### **Recursos**

- [Documentação do Projeto](docs/)
- [Guia de Configuração](docs/setup-guide.md)
- [Integração 3W](docs/3W_INTEGRATION.md)
- [GitHub Issues](https://github.com/seu-repo/issues)

### **Contato**

- **Líder do Projeto**: [Seu Nome]
- **Email**: [seu.email@universidade.edu]
- **Instituição**: [Sua Universidade]

---

> **🇺🇸 [Ver diretrizes em Inglês](CONTRIBUTING.md)**

<div align="center">
  <sub>Construído com ❤️ pela comunidade open source</sub>
</div>
