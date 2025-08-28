# 🔐 Troubleshooting: Autenticação Google Cloud no GitHub Actions

> **Guia para resolver problemas de autenticação GCP nos workflows do GitHub Actions**

## 🚨 Problema Atual

**Erro**: `google-github-actions/auth failed with: the GitHub Action workflow must specify exactly one of "workload_identity_provider" or "credentials_json"!`

**Causa**: O workflow está configurado para usar **Workload Identity Federation**, mas os secrets necessários não estão configurados no GitHub.

## 🚀 Soluções Disponíveis

### 1. 🎯 **Solução Imediata: Workflow Simples**

Execute o workflow alternativo que funciona com credenciais JSON:

```yaml
# .github/workflows/test-gcp-auth-simple.yml
name: Test GCP Authentication (Simple)
```

**Para usar esta solução:**

1. Vá para `Actions` no repositório
2. Execute o workflow `Test GCP Authentication (Simple)`
3. Configure o secret `GCP_CREDENTIALS_JSON` com sua chave de serviço

### 2. 🔒 **Solução Recomendada: Workload Identity Federation**

Configure a autenticação segura usando Workload Identity:

#### **Opção A: Script Automático (Recomendado)**

```bash
# Execute o script de configuração
./scripts/setup_gcp_workload_identity.sh
```

O script irá:

- ✅ Configurar Workload Identity Pool
- ✅ Criar Service Account
- ✅ Configurar permissões
- ✅ Habilitar APIs necessárias
- ✅ Gerar arquivo com todos os secrets necessários

#### **Opção B: Configuração Manual**

Siga o guia completo em: [docs/GCP_SETUP.md](GCP_SETUP.md)

## 📋 Secrets Necessários

### Para Workflow Simples (Credenciais JSON)

| Secret                 | Descrição                         |
| ---------------------- | --------------------------------- |
| `GCP_PROJECT_ID`       | ID do projeto Google Cloud        |
| `GCP_CREDENTIALS_JSON` | Conteúdo da chave de serviço JSON |

### Para Workload Identity Federation

| Secret                           | Descrição                     |
| -------------------------------- | ----------------------------- |
| `GCP_PROJECT_ID`                 | ID do projeto Google Cloud    |
| `GCP_WORKLOAD_IDENTITY_PROVIDER` | Provider do Workload Identity |
| `GCP_SERVICE_ACCOUNT`            | Email do Service Account      |
| `GCP_REGION`                     | Região do Google Cloud        |

## 🔧 Como Configurar os Secrets

### 1. Acessar Configurações do Repositório

- Vá para seu repositório no GitHub
- Clique em `Settings` (aba)
- Clique em `Secrets and variables` → `Actions`

### 2. Adicionar Secrets

- Clique em `New repository secret`
- Digite o nome do secret (ex: `GCP_PROJECT_ID`)
- Digite o valor do secret
- Clique em `Add secret`

### 3. Repetir para Todos os Secrets

Adicione cada secret listado acima.

## 🧪 Testando a Configuração

### 1. Execute o Workflow de Teste

- Vá para `Actions` no repositório
- Clique no workflow `Test GCP Authentication`
- Clique em `Run workflow`
- Selecione a branch `main`
- Clique em `Run workflow`

### 2. Verifique os Logs

- Aguarde a execução
- Clique no job para ver os logs
- Procure por mensagens de sucesso:
  - ✅ `Authentication successful!`
  - ✅ `Basic GCP commands working!`
  - ✅ `Project access verified!`

## 🚨 Troubleshooting Comum

### Erro: "Secret not found"

**Solução**: Verifique se o secret está configurado corretamente no GitHub

### Erro: "Permission denied"

**Solução**: Verifique se o Service Account tem as permissões necessárias

### Erro: "Service account not found"

**Solução**: Verifique se o email do Service Account está correto

### Erro: "Workload Identity not configured"

**Solução**: Execute o script de configuração automática

## 📚 Recursos Adicionais

### 📖 Documentação

- [GCP Setup Guide](GCP_SETUP.md) - Guia completo de configuração
- [Google Cloud IAM](https://cloud.google.com/iam/docs) - Documentação oficial
- [GitHub Actions GCP](https://github.com/google-github-actions/auth) - Action oficial

### 🛠️ Scripts Úteis

- `scripts/setup_gcp_workload_identity.sh` - Configuração automática
- `scripts/install_extensions.sh` - Instalação de extensões VS Code

### 🔍 Verificações

- `gcp-config.yaml` - Configurações do projeto
- `.github/workflows/` - Workflows disponíveis

## 🎯 Próximos Passos

1. **Configure a autenticação** usando uma das soluções acima
2. **Teste o workflow** para verificar se está funcionando
3. **Execute treinamentos** usando os workflows configurados
4. **Monitore os custos** no Google Cloud Console

## 💡 Dicas Importantes

- 🔒 **Workload Identity Federation** é mais seguro que chaves de serviço
- 💰 **Configure alertas de billing** para evitar surpresas
- 📊 **Use Cloud Monitoring** para acompanhar o uso dos recursos
- 🧪 **Teste sempre em ambiente de desenvolvimento** primeiro

---

**Precisa de ajuda?** Abra uma issue no repositório ou consulte a documentação completa!
