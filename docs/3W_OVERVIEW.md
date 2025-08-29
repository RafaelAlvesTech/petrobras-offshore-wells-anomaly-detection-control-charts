# 🛢️ Visão Geral do Projeto 3W da Petrobras

> **🇺🇸 [View in English](3W_OVERVIEW_EN.md)**

## 📋 Introdução

O **Projeto 3W (Three Worlds)** é o primeiro repositório público da Petrobras no GitHub, lançado em 30 de maio de 2022. Representa uma iniciativa estratégica para promover a experimentação e desenvolvimento de abordagens baseadas em Machine Learning para problemas específicos relacionados à detecção e classificação de eventos indesejáveis que ocorrem em poços de petróleo offshore.

## 🎯 Por que "3W"?

O nome **3W** foi escolhido porque este dataset é composto por instâncias de **3** fontes diferentes e que contêm eventos indesejáveis que ocorrem em poços de petróleo (**W**ells).

## 🚀 Motivação e Impacto

### Problemas da Indústria

- **Perdas de Produção**: Eventos indesejáveis podem causar até **5% de perdas de produção** em certos cenários
- **Custos de Manutenção**: O custo de uma sonda marítima, necessária para realizar vários tipos de operações, pode exceder **US$ 500.000 por dia**
- **Segurança**: Prevenção de acidentes ambientais e humanos
- **Integridade**: Monitoramento da integridade de poços e sistemas submarinos

### Benefícios Esperados

- **Melhorar o processo** de identificação de eventos indesejáveis nas fases de perfuração, completação e produção
- **Aumentar a eficiência** do monitoramento da integridade de poços e sistemas submarinos
- **Prevenir perdas** para pessoas, meio ambiente e imagem da empresa

## 🏗️ Estratégia e Governança

### Programa Conexões para Inovação

O 3W é o primeiro piloto do programa **"Conexões para Inovação - Módulo Open Lab"** da Petrobras, composto por:

1. **3W Dataset**: Evolui e é complementado com mais instâncias ao longo do tempo
2. **3W Toolkit**: Evolui de várias formas para cobrir um número crescente de eventos indesejáveis

### Governança

- **Liderança**: Departamento de Flow Assurance e centro de pesquisa (CENPES)
- **Expansão**: Desde 1º de maio de 2024, inclui o departamento de Integridade de Poços
- **Evolução**: Projeto cada vez mais consolidado na Petrobras
- **Profissionais**: Mais especialistas em rotulagem de instâncias
- **Ferramentas**: Mais investimento em ferramentas digitais para rotulagem e exportação

## 📊 Recursos do Projeto

### 3W Dataset

- **Primeiro dataset realista e público** com eventos indesejáveis reais raros em poços de petróleo
- **Formato**: Arquivos Parquet com compressão Brotli
- **Licença**: Creative Commons Attribution 4.0 International
- **Estrutura**: Múltiplos arquivos Parquet salvos em subdiretórios
- **Teoria**: Baseado no paper "A realistic and public dataset with rare undesirable real events in oil wells" (Journal of Petroleum Science and Engineering)

### 3W Toolkit

- **Pacote de software** escrito em Python 3
- **Facilita**: Geração de visões gerais do dataset, experimentação e análise comparativa
- **Padronização**: Pontos-chave do pipeline de desenvolvimento de algoritmos baseados em ML
- **Escolhas arbitrárias**: Cuidadosamente feitas para permitir análise comparativa adequada

### Problemas Incorporados

Atualmente disponível:

- **Classificador Binário de Fechamento Espúrio de DHSV**
  - Tipo: Classificação binária
  - Objetivo: Identificar fechamentos não intencionais de válvulas
  - Aplicação: Segurança e integridade de poços
  - Fase: Produção

## 🌍 Comunidade e Contribuições

### Tipos de Contribuições Esperadas

- **Indivíduos**: Pesquisadores independentes
- **Instituições de Pesquisa**: Universidades e centros de pesquisa
- **Startups**: Empresas de tecnologia
- **Empresas**: Parceiros da indústria
- **Operadores de Petróleo**: Outras empresas do setor

### Como Contribuir

Antes de contribuir, é necessário ler e concordar com:

- [Código de Conduta](https://github.com/petrobras/3W/blob/main/CODE_OF_CONDUCT.md)
- [Acordo de Licença de Contribuidor](https://github.com/petrobras/3W/blob/main/CLA.md)
- [Guia de Contribuição](https://github.com/petrobras/3W/blob/main/CONTRIBUTING.md)

### Engajamento da Comunidade

- **Discussões**: [GitHub Discussions](https://github.com/petrobras/3W/discussions)
- **Workshop Anual**: 4ª edição em 2025 - [Formulário de Inscrição](https://forms.gle/cmLa2u4VaXd1T7qp8)
- **Participação**: Leia, participe e siga as discussões

## 📚 Licenças e Versionamento

### Licenças

- **Código**: Licenciado sob Apache 2.0 License
- **Dados**: Arquivos de dados do dataset licenciados sob Creative Commons Attribution 4.0 International License

### Estratégia de Versionamento

- **3W Toolkit**: Versão especificada no arquivo `__init__.py`
- **3W Dataset**: Versão especificada no arquivo `dataset.ini`
- **3W Project**: Versão especificada com tags no repositório git
- **Padrão**: Exclusivamente versionamento semântico definido em [semver.org](https://semver.org)
- **Atualizações**: Sempre atualizadas manualmente
- **Independência**: Versionamento do Toolkit e Dataset são completamente independentes
- **Tags**: Apenas tags anotadas com releases automáticos no GitHub

## 🔬 Impacto na Pesquisa

### Características Únicas

- **Primeiro dataset realista** com eventos raros reais em poços de petróleo
- **Benchmark dataset** para desenvolvimento de técnicas de ML
- **Dificuldades inerentes** de dados reais
- **Padrões da indústria** para pipeline de ML

### Aplicações

- **Flow Assurance**: Monitoramento de fluxo em poços
- **Métodos de Elevação Artificial**: Sistemas de bombeamento
- **Integridade de Poços**: Segurança estrutural
- **Sistemas Submarinos**: Infraestrutura offshore

## 🚀 Próximos Passos

### Desenvolvimento

- **Evolução do Dataset**: Mais instâncias e tipos de eventos
- **Expansão do Toolkit**: Novas funcionalidades e problemas
- **Aproximações e Algoritmos**: Incorporação de sistemas dedicados
- **Ferramentas Úteis**: Desenvolvimento de utilitários

### Comunidade

- **Expansão Global**: Mais países e instituições
- **Workshops Anuais**: Eventos presenciais e online
- **Colaborações**: Parcerias com universidades e empresas
- **Publicações**: Artigos científicos e técnicos

## 📞 Suporte e Contato

### Recursos de Ajuda

1. **Documentação Oficial**: [GitHub 3W](https://github.com/petrobras/3W)
2. **Discussões**: [GitHub Discussions](https://github.com/petrobras/3W/discussions)
3. **Workshop**: [Formulário de Inscrição](https://forms.gle/cmLa2u4VaXd1T7qp8)
4. **Contribuições**: [Guia de Contribuição](https://github.com/petrobras/3W/blob/main/CONTRIBUTING.md)

### Perguntas

- Consulte a seção de discussões
- Abra discussões para perguntas específicas
- Participe da comunidade ativamente

---

**🔗 Links Importantes:**

- [Repositório Principal 3W](https://github.com/petrobras/3W)
- [Estrutura do Dataset](https://github.com/petrobras/3W/blob/main/3W_DATASET_STRUCTURE.md)
- [Estrutura do Toolkit](https://github.com/petrobras/3W/blob/main/3W_TOOLKIT_STRUCTURE.md)
- [Guia de Contribuição](https://github.com/petrobras/3W/blob/main/CONTRIBUTING.md)
- [Workshop 3W 2025](https://forms.gle/cmLa2u4VaXd1T7qp8)
