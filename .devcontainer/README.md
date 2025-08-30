# 🐚 Configuração do Zsh no DevContainer

Este diretório contém as configurações do Zsh otimizadas para o ambiente de desenvolvimento containerizado do projeto Petrobras Offshore Wells Anomaly Detection.

## 📁 Arquivos de Configuração

### `.zshrc`

Configuração principal do Zsh com:

- Prompt personalizado com branding Petrobras 🛢️
- Variáveis de ambiente do projeto
- Aliases para desenvolvimento
- Funções úteis para data science
- Integração com plugins

### `.zshrc.project`

Configurações específicas do projeto de detecção de anomalias:

- Variáveis de ML/DL
- Aliases para modelos de anomalia
- Funções para pipeline completo
- Configurações de experimentos

### `.zshrc.local.example`

Template para configurações pessoais:

- Configurações de usuário
- Preferências pessoais
- Diretórios pessoais
- Funções personalizadas

## 🚀 Instalação Automática

As configurações são instaladas automaticamente quando o container é criado através do script `setup_shell.sh`.

### Processo de Instalação

1. **Cópia dos arquivos de configuração**
   - `.zshrc` → `~/.zshrc`
   - `.zshrc.project` → `~/.zshrc.project`
   - `.zshrc.local.example` → `~/.zshrc.local.example`

2. **Instalação de plugins**
   - zsh-autosuggestions
   - zsh-syntax-highlighting

3. **Configuração do Jupyter**
   - Configuração personalizada para o projeto

4. **Configuração de permissões**
   - Propriedade correta dos arquivos

## 🎯 Funcionalidades Principais

### Prompt Personalizado

```
🛢️ usuario@hostname ~/projeto (branch) [venv]
❯
```

### Aliases Úteis

- **Navegação**: `pj`, `data`, `models`, `notebooks`, `src`, `logs`, `config`
- **Python**: `py`, `pip`, `uv-add`, `uv-sync`, `uv-run`
- **Jupyter**: `jlab`, `jnotebook`, `jstop`
- **MLflow**: `mlflow-ui`, `mlflow-server`
- **TensorBoard**: `tensorboard`
- **Testes**: `test`, `test-cov`, `test-fast`, `test-verbose`
- **Qualidade**: `lint`, `format`, `type-check`, `security`
- **Git**: `gs`, `ga`, `gc`, `gp`, `gl`, `gd`, `gb`, `gco`
- **Docker**: `dbuild`, `drun`, `dstop`, `dclean`
- **Limpeza**: `clean-pyc`, `clean-cache`, `clean-logs`, `clean-models`

### Funções Personalizadas

- **Gerenciamento**: `activate_venv()`, `create_venv()`
- **Desenvolvimento**: `run_notebook()`, `train_model()`, `evaluate_model()`
- **Projeto**: `project_status()`, `backup_data()`, `clean_all()`
- **Específicas**: `run_pipeline()`, `run_experiment()`, `monitor_training()`

## 🔧 Configurações de Ambiente

### Variáveis do Projeto

```bash
PROJECT_ROOT="/workspaces/petrobras-offshore-wells-anomaly-detection-control-charts"
DATA_DIR="${PROJECT_ROOT}/data"
MODELS_DIR="${PROJECT_ROOT}/models"
NOTEBOOKS_DIR="${PROJECT_ROOT}/notebooks"
SRC_DIR="${PROJECT_ROOT}/src"
LOGS_DIR="${PROJECT_ROOT}/logs"
CONFIG_DIR="${PROJECT_ROOT}/config"
```

### Variáveis Python

```bash
PYTHONPATH="${PYTHONPATH}:$(pwd)/src:$(pwd)/notebooks"
PYTHONUNBUFFERED=1
PYTHONDONTWRITEBYTECODE=1
```

### Variáveis de ML

```bash
MLFLOW_TRACKING_URI="http://localhost:5000"
MLFLOW_EXPERIMENT_NAME="petrobras-anomaly-detection"
TENSORBOARD_LOG_DIR="./logs/tensorboard"
```

## 🎨 Personalização

### Configurações Pessoais

Para personalizar suas configurações:

1. **Copie o template**

   ```bash
   cp ~/.zshrc.local.example ~/.zshrc.local
   ```

2. **Edite suas configurações**

   ```bash
   nano ~/.zshrc.local
   ```

3. **Recarregue o Zsh**
   ```bash
   source ~/.zshrc
   ```

### Configurações Disponíveis

- **Usuário**: Nome, email, departamento
- **Preferências**: Editor, browser, terminal
- **Performance**: Threads, memória, GPU
- **Dados**: Diretórios pessoais, formatos
- **Modelos**: Tipos, parâmetros, experimentos
- **Monitoramento**: Logging, métricas, alertas

## 🧪 Testando a Configuração

### Verificar Instalação

```bash
# Verificar se Zsh está funcionando
zsh --version

# Verificar plugins
ls ~/.oh-my-zsh/custom/plugins/

# Verificar configurações
echo $PROJECT_NAME
echo $DATA_DIR
```

### Testar Funções

```bash
# Testar status do projeto
project_status

# Testar aliases
pj
data
models

# Testar funções
create_venv
```

## 🔧 Solução de Problemas

### Problema: Zsh não está sendo usado

```bash
# Verificar shell atual
echo $SHELL

# Alterar para Zsh
chsh -s $(which zsh)

# Reiniciar terminal
```

### Problema: Plugins não carregam

```bash
# Verificar se os diretórios existem
ls ~/.oh-my-zsh/custom/plugins/

# Recarregar configurações
source ~/.zshrc
```

### Problema: Variáveis não definidas

```bash
# Verificar se os arquivos existem
ls ~/.zshrc
ls ~/.zshrc.project

# Recarregar configurações
source ~/.zshrc
```

### Problema: Comandos não encontrados

```bash
# Verificar PATH
echo $PATH

# Verificar se o ambiente virtual está ativo
which python
which pip
```

## 📚 Recursos Adicionais

### Documentação

- [ZSH Configuration Documentation](../docs/ZSH_CONFIGURATION.md)
- [Oh My Zsh](https://ohmyz.sh/)
- [Zsh Documentation](https://zsh.sourceforge.io/Doc/)

### Comandos Úteis

```bash
# Ver histórico de comandos
history

# Buscar no histórico
Ctrl+R

# Autocompletar
Tab

# Buscar arquivos
fzf
```

## 🤝 Contribuindo

Para contribuir com melhorias nas configurações do Zsh:

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Modifique os arquivos de configuração
4. Teste as mudanças
5. Faça um pull request

### Estrutura de Contribuição

- `.zshrc`: Configurações gerais
- `.zshrc.project`: Configurações específicas do projeto
- `.zshrc.local.example`: Template de configurações pessoais
- `setup_shell.sh`: Script de instalação

## 📄 Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](../LICENSE) para mais detalhes.

---

**🛢️ Projeto Petrobras Offshore Wells Anomaly Detection**
_Configurações otimizadas para desenvolvimento em Python e Machine Learning_
