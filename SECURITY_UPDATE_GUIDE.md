# 🔒 Guia de Atualização de Segurança - Dependabot Alerts

Este documento explica como resolver as vulnerabilidades de segurança identificadas pelo Dependabot no projeto Petrobras Offshore Wells Anomaly Detection.

## 🚨 Vulnerabilidades Identificadas

### 1. **certifi** (CVE-2023-37920)

- **Versão atual**: 2022.12.7
- **Versão segura**: >= 2024.2.2
- **Descrição**: Vulnerabilidade de segurança relacionada a certificados SSL/TLS

### 2. **charset-normalizer** (CVE-2023-43626)

- **Versão atual**: 2.1.1
- **Versão segura**: >= 3.3.2
- **Descrição**: Vulnerabilidade de segurança relacionada a normalização de caracteres

### 3. **cffi** (CVE-2023-37920)

- **Versão atual**: 1.17.1
- **Versão segura**: >= 1.17.1 (já está na versão mínima segura)
- **Descrição**: Vulnerabilidade de segurança relacionada a certificados SSL/TLS

### 4. **requests** (CVE-2023-32681)

- **Versão atual**: 2.28.1
- **Versão segura**: >= 2.31.0
- **Descrição**: Vulnerabilidade de segurança relacionada a requisições HTTP

### 5. **urllib3** (CVE-2023-45803)

- **Versão atual**: 1.26.13
- **Versão segura**: >= 2.0.7
- **Descrição**: Vulnerabilidade de segurança relacionada a requisições HTTP

## 🛠️ Como Resolver

### Opção 1: Script Automático (Recomendado)

```bash
# Execute o script de atualização
./scripts/update_dependencies.sh

# Ou usando Python
python scripts/update_dependencies.py
```

### Opção 2: Atualização Manual

1. **Atualizar pyproject.toml**:

   ```bash
   # As dependências já foram atualizadas no arquivo
   # Verifique se as versões estão corretas
   cat pyproject.toml
   ```

2. **Sincronizar dependências**:

   ```bash
   # Remover arquivo de lock antigo
   rm uv.lock

   # Sincronizar com novas versões
   uv sync
   ```

3. **Regenerar requirements.txt**:

   ```bash
   uv export --frozen --output-file=requirements.txt
   ```

4. **Verificar vulnerabilidades**:
   ```bash
   uv pip audit
   ```

## 🧪 Testes Após Atualização

### 1. Testes Unitários

```bash
uv run pytest
```

### 2. Testes de Importação

```bash
uv run python -c "import src; print('✅ Imports funcionando')"
```

### 3. Testes de Funcionalidade

```bash
# Execute seus testes específicos
uv run python test_app.py
```

## 📝 Commit e Push

```bash
# Adicionar mudanças
git add .

# Commit com mensagem convencional
git commit -m "chore(deps): update dependencies for security

- Update certifi to 2024.2.2 (fixes CVE-2023-37920)
- Update charset-normalizer to 3.3.2 (fixes CVE-2023-43626)
- Update requests to 2.31.0 (fixes CVE-2023-32681)
- Update urllib3 to 2.0.7 (fixes CVE-2023-45803)
- Regenerate uv.lock and requirements.txt"

# Push para o repositório
git push
```

## 🔍 Verificação Contínua

### 1. Dependabot Configurado

- ✅ Arquivo `.github/dependabot.yml` criado
- ✅ Monitoramento semanal de dependências Python
- ✅ Monitoramento semanal de GitHub Actions
- ✅ Atualizações automáticas de segurança

### 2. Comandos de Verificação

```bash
# Verificar dependências desatualizadas
uv pip list --outdated

# Auditoria de segurança
uv pip audit

# Verificar versões específicas
uv pip show certifi charset-normalizer requests urllib3
```

## ⚠️ Possíveis Problemas

### 1. **Incompatibilidades de Versão**

- Algumas dependências podem ter breaking changes
- Teste sempre após atualizações
- Considere usar `>=` em vez de `==` para versões

### 2. **Conflitos de Dependências**

- Use `uv tree` para visualizar árvore de dependências
- Resolva conflitos manualmente se necessário

### 3. **Testes Falhando**

- Verifique logs de erro
- Consulte documentação das novas versões
- Considere rollback se necessário

## 📚 Recursos Adicionais

- [Dependabot Documentation](https://docs.github.com/en/code-security/dependabot)
- [Python Security Advisories](https://github.com/pypa/advisory-database)
- [CVE Database](https://cve.mitre.org/)
- [uv Documentation](https://docs.astral.sh/uv/)

## 🎯 Próximos Passos

1. ✅ Configurar Dependabot
2. ✅ Atualizar dependências vulneráveis
3. ✅ Testar funcionalidades
4. ✅ Commit e push das mudanças
5. 🔄 Monitorar futuras atualizações automáticas

---

**Nota**: Este guia deve ser atualizado sempre que novas vulnerabilidades forem identificadas.
