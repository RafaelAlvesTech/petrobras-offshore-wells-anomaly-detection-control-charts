# 🔐 Configuração GPG para Assinatura de Commits

Este documento descreve como configurar a assinatura GPG para todos os commits do projeto Petrobras Offshore Wells Anomaly Detection.

## 🎯 Objetivo

Configurar assinatura GPG para garantir a autenticidade e integridade de todos os commits e tags do projeto.

## ✅ Status Atual

- ✅ Chave GPG configurada: `3E2E96B458A47E2B`
- ✅ Assinatura automática de commits habilitada
- ✅ Assinatura automática de tags habilitada
- ✅ Configuração aplicada globalmente e localmente

## 🚀 Configuração Rápida

### 1. Executar Script Automático

```bash
./scripts/setup_gpg.sh
```

### 2. Configuração Manual

```bash
# Configurar chave GPG
git config --global user.signingkey 3E2E96B458A47E2B

# Habilitar assinatura automática de commits
git config --global commit.gpgsign true

# Habilitar assinatura automática de tags
git config --global tag.gpgsign true

# Configurar programa GPG
git config --global gpg.program gpg
```

## 🔑 Chave GPG Atual

**ID da Chave:** `3E2E96B458A47E2B`
**Email:** rafaelpereiraalves@ufba.br
**Tipo:** RSA 4096 bits
**Data de Criação:** 2025-03-20

## 📋 Configurações Aplicadas

### Configuração Global

```bash
user.signingkey=3E2E96B458A47E2B
commit.gpgsign=true
tag.gpgsign=true
gpg.program=gpg
```

### Configuração Local (Repositório)

```bash
user.signingkey=3E2E96B458A47E2B
commit.gpgsign=true
tag.gpgsign=true
```

## 🌐 Configuração no GitHub

### 1. Adicionar Chave Pública

1. Acesse [GitHub Settings > SSH and GPG keys](https://github.com/settings/keys)
2. Clique em "New GPG key"
3. Cole a chave pública exportada:

```bash
gpg --armor --export 3E2E96B458A47E2B
```

### 2. Verificar Assinatura

Após adicionar a chave, todos os commits assinados mostrarão um badge "Verified" no GitHub.

## 🧪 Testando a Configuração

### 1. Fazer um Commit de Teste

```bash
# Adicionar um arquivo de teste
echo "test" > test_gpg.txt

# Fazer commit (será assinado automaticamente)
git add test_gpg.txt
git commit -m "test: verificando assinatura GPG"

# Verificar se foi assinado
git log --show-signature -1
```

### 2. Verificar Assinatura

```bash
# Verificar último commit
git verify-commit HEAD

# Verificar todos os commits
git log --show-signature
```

## 🔧 Solução de Problemas

### Erro: "gpg failed to sign the data"

```bash
# Verificar se o agente GPG está rodando
gpg-agent --daemon

# Ou reiniciar o agente
gpgconf --kill gpg-agent
gpg-agent --daemon
```

### Erro: "No secret key"

```bash
# Verificar chaves disponíveis
gpg --list-secret-keys

# Verificar configuração Git
git config --list | grep signingkey
```

### Erro: "Bad passphrase"

```bash
# Limpar cache de senha
gpgconf --reload gpg-agent
```

## 📚 Comandos Úteis

### Gerenciamento de Chaves GPG

```bash
# Listar chaves
gpg --list-keys

# Listar chaves secretas
gpg --list-secret-keys

# Exportar chave pública
gpg --armor --export 3E2E96B458A47E2B

# Exportar chave privada (backup)
gpg --armor --export-secret-key 3E2E96B458A47E2B > private_key.asc
```

### Verificação de Assinaturas

```bash
# Verificar commit específico
git verify-commit <commit-hash>

# Verificar tag
git verify-tag <tag-name>

# Verificar todos os commits
git log --show-signature
```

## 🚨 Segurança

### Boas Práticas

1. **Nunca compartilhe sua chave privada**
2. **Use senha forte para a chave GPG**
3. **Faça backup da chave privada**
4. **Revogue chaves comprometidas imediatamente**

### Backup da Chave

```bash
# Exportar chave privada (para backup seguro)
gpg --armor --export-secret-key 3E2E96B458A47E2B > backup_private_key.asc

# Importar chave de backup
gpg --import backup_private_key.asc
```

## 📖 Referências

- [GitHub Docs - Signing Commits](https://docs.github.com/en/authentication/managing-commit-signature-verification)
- [Git Documentation - GPG](https://git-scm.com/book/en/v2/Git-Tools-Signing-Your-Work)
- [GnuPG Documentation](https://gnupg.org/documentation/)

## 🤝 Suporte

Se encontrar problemas com a configuração GPG:

1. Verifique este documento
2. Execute o script de configuração
3. Consulte as referências acima
4. Abra uma issue no repositório

---

**Última atualização:** $(date)
**Responsável:** RafaelAlvesTech <rafaelpereiraalves@ufba.br>
