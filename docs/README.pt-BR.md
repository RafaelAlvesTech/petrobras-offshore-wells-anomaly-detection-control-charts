# 📚 Índice de Documentação - Detecção de Anomalias em Poços Offshore da Petrobras

> **🇺🇸 [View documentation index in English](README.md)**

## 🎯 Bem-vindo à Documentação!

Esta documentação cobre todos os aspectos do projeto **Detecção de Anomalias em Poços Offshore da Petrobras**, uma iniciativa PIBIC (Programa Institucional de Bolsas de Iniciação Científica) focada na detecção de anomalias em séries temporais multivariadas de poços offshore usando técnicas de machine learning de última geração.

## 📖 Estrutura da Documentação

### 🚀 Primeiros Passos

- **[README Principal](../README.md)** - Visão geral do projeto e guia de início rápido
- **[Guia de Configuração](setup-guide.md)** - Configuração completa do ambiente de desenvolvimento
- **[Diretrizes de Contribuição](../CONTRIBUTING.md)** - Como contribuir para o projeto

### 🔧 Documentação Principal

- **[Integração 3W](3W_INTEGRATION.md)** - Integração com dataset 3W da Petrobras
- **[Configuração AWS](AWS_SETUP.md)** - Implantação e configuração AWS
- **[Configuração GCP](GCP_SETUP.md)** - Configuração Google Cloud Platform
- **[Commits Convencionais](CONVENTIONAL_COMMITS.md)** - Padrões de commits Git

### 🌐 Versões em Idiomas

| Documento                | Inglês                                 | Português (pt-BR)                                  |
| ------------------------ | -------------------------------------- | -------------------------------------------------- |
| **README Principal**     | [README.md](../README.md)              | [README.pt-BR.md](../README.pt-BR.md)              |
| **Guia de Configuração** | [setup-guide.md](setup-guide.md)       | [setup-guide.pt-BR.md](setup-guide.pt-BR.md)       |
| **Contribuição**         | [CONTRIBUTING.md](../CONTRIBUTING.md)  | [CONTRIBUTING.pt-BR.md](../CONTRIBUTING.pt-BR.md)  |
| **Integração 3W**        | [3W_INTEGRATION.md](3W_INTEGRATION.md) | [3W_INTEGRATION.pt-BR.md](3W_INTEGRATION.pt-BR.md) |

## 🎯 Navegação Rápida

### 🚀 Para Novos Usuários

1. **Comece com** [README Principal](../README.md) para visão geral do projeto
2. **Siga** [Guia de Configuração](setup-guide.md) para preparar seu ambiente
3. **Explore** [Integração 3W](3W_INTEGRATION.md) para entender o dataset

### 🔧 Para Desenvolvedores

1. **Revise** [Diretrizes de Contribuição](../CONTRIBUTING.md) para padrões de desenvolvimento
2. **Verifique** [Commits Convencionais](CONVENTIONAL_COMMITS.md) para padrões de commits
3. **Use** [Configuração AWS](AWS_SETUP.md) ou [Configuração GCP](GCP_SETUP.md) para implantação

### 🌍 Para Falantes de Português

Toda a documentação está disponível em Português Brasileiro:

- **Documentação Principal**: [README.pt-BR.md](../README.pt-BR.md)
- **Guia de Configuração**: [setup-guide.pt-BR.md](setup-guide.pt-BR.md)
- **Diretrizes de Contribuição**: [CONTRIBUTING.pt-BR.md](../CONTRIBUTING.pt-BR.md)
- **Integração 3W**: [3W_INTEGRATION.pt-BR.md](3W_INTEGRATION.pt-BR.md)

## 📊 Visão Geral do Projeto

### 🎯 Foco da Pesquisa

- **Detecção de Anomalias**: Análise de séries temporais multivariadas
- **Poços Offshore**: Dados operacionais da Petrobras
- **Machine Learning**: Algoritmos de última geração (TranAD, LSTM-VAE, USAD, ECOD)
- **Processamento em Tempo Real**: Fluxos de dados de sensores de alta frequência

### 🛠️ Stack Tecnológico

- **Python 3.11+**: Python moderno com type hints
- **Polars**: Manipulação de dados de alta performance
- **Marimo**: Notebooks interativos para desenvolvimento colaborativo
- **PyTorch**: Framework de deep learning
- **uv**: Gerenciamento rápido de pacotes Python

### 🏗️ Arquitetura

```
petrobras-offshore-wells-anomaly-detection/
├── src/                    # Código fonte principal
│   ├── models/            # Implementações de modelos ML/DL
│   ├── data/              # Pipelines de processamento de dados
│   ├── features/          # Engenharia de features
│   └── utils/             # Funções utilitárias
├── notebooks/             # Notebooks interativos Marimo
├── data/                  # Datasets e dados processados
├── tests/                 # Suite de testes automatizados
├── docs/                  # Documentação (este diretório)
├── config/                # Arquivos de configuração
├── docker/                # Containerização
└── scripts/               # Scripts de automação
```

## 🔍 Buscar na Documentação

### 📝 Por Tópico

- **Configuração & Instalação**: [setup-guide.md](setup-guide.md)
- **Dados & Datasets**: [3W_INTEGRATION.md](3W_INTEGRATION.md)
- **Desenvolvimento**: [CONTRIBUTING.md](../CONTRIBUTING.md)
- **Implantação**: [AWS_SETUP.md](AWS_SETUP.md), [GCP_SETUP.md](GCP_SETUP.md)

### 🐍 Por Tecnologia

- **Python**: [setup-guide.md](setup-guide.md), [CONTRIBUTING.md](../CONTRIBUTING.md)
- **Machine Learning**: [3W_INTEGRATION.md](3W_INTEGRATION.md)
- **Cloud**: [AWS_SETUP.md](AWS_SETUP.md), [GCP_SETUP.md](GCP_SETUP.md)
- **Git**: [CONVENTIONAL_COMMITS.md](CONVENTIONAL_COMMITS.md)

## 🚀 Obtendo Ajuda

### 📚 Auto-atendimento

1. **Verifique este índice** para documentação relevante
2. **Use a busca** no seu navegador (Ctrl+F / Cmd+F)
3. **Siga referências cruzadas** entre documentos

### 🆘 Precisa de Mais Ajuda?

- **GitHub Issues**: [Issues do Projeto](https://github.com/seu-repo/issues)
- **GitHub Discussions**: [Discussões do Projeto](https://github.com/seu-repo/discussions)
- **Email**: [seu.email@universidade.edu]
- **Problemas na Documentação**: Reporte problemas com a documentação

## 🔄 Mantendo a Documentação Atualizada

### 📝 Contribuindo para a Documentação

1. **Siga** [Diretrizes de Contribuição](../CONTRIBUTING.md)
2. **Atualize** versões em inglês e português
3. **Mantenha** consistência entre versões de idioma
4. **Teste** todos os links e exemplos

### 🌐 Diretrizes de Tradução

- **Idioma principal**: Inglês (documentação principal)
- **Idioma secundário**: Português Brasileiro (pt-BR)
- **Links cruzados**: Sempre inclua links entre versões de idioma
- **Consistência**: Mantenha ambas as versões sincronizadas

## 📈 Métricas da Documentação

### 📊 Status Atual

- **Total de Documentos**: 8 (4 Inglês + 4 Português)
- **Cobertura**: 100% bilíngue
- **Última Atualização**: [Data Atual]
- **Mantido Por**: Equipe do Projeto

### 🎯 Objetivos de Qualidade

- **Precisão**: Toda informação técnica verificada
- **Completude**: Cobrir todos os aspectos principais do projeto
- **Acessibilidade**: Navegação clara e referências cruzadas
- **Bilíngue**: Qualidade igual em ambos os idiomas

---

> **🇺🇸 [Ver índice em Inglês](README.md)**

<div align="center">
  <sub>Documentação organizada com ❤️ para facilitar o desenvolvimento</sub>
</div>
