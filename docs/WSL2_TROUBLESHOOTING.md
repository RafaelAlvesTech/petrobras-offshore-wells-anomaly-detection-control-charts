# 🐧 WSL2 Troubleshooting Guide

## 🚨 Problemas Comuns e Soluções

### 1. **Erro de Conexão WSL (0x8007274c)**

**Sintoma**: Timeout de conexão ou falha na comunicação entre Windows e WSL2

**Soluções**:

```bash
# No PowerShell como Administrador
wsl --shutdown
wsl --update
wsl --distribution Ubuntu

# Verificar status do serviço WSL
Get-Service LxssManager
Restart-Service LxssManager
```

### 2. **Cursor Server Installation Failed**

**Sintoma**: Falha na instalação do servidor Cursor no WSL2

**Soluções**:

```bash
# Limpar cache do Cursor
rm -rf ~/.cursor-server
rm -rf ~/.vscode-server

# Verificar permissões
ls -la ~/
sudo chown -R $USER:$USER ~/

# Reinstalar Cursor no Windows
# Baixar a versão mais recente de https://cursor.sh
```

### 3. **Problemas de Performance WSL2**

**Sintoma**: Sistema lento, alto uso de memória

**Soluções**:

```bash
# Criar/editar .wslconfig no Windows (C:\Users\<user>\.wslconfig)
[wsl2]
memory=8GB
processors=4
swap=2GB
localhostForwarding=true
```

### 4. **Docker não funciona no WSL2**

**Sintoma**: Erro de permissão ou serviço não encontrado

**Soluções**:

```bash
# Verificar status do Docker
sudo systemctl status docker

# Iniciar Docker
sudo systemctl start docker
sudo systemctl enable docker

# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER

# Verificar se o Docker Desktop está rodando no Windows
# O Docker Desktop deve estar configurado para WSL2
```

### 5. **Problemas de Rede WSL2**

**Sintoma**: Não consegue acessar internet ou serviços externos

**Soluções**:

```bash
# Verificar configuração de rede
ip addr show
cat /etc/resolv.conf

# Resetar rede WSL2 (no PowerShell como Admin)
wsl --shutdown
netsh winsock reset
netsh int ip reset
ipconfig /flushdns
wsl --distribution Ubuntu
```

### 6. **Problemas de Permissão de Arquivos**

**Sintoma**: Erro de permissão ao acessar arquivos do Windows

**Soluções**:

```bash
# Verificar montagem do Windows
ls -la /mnt/c/

# Ajustar permissões
sudo chown -R $USER:$USER /mnt/c/Users/$USER

# Usar WSL2 nativo em vez de montagem Windows
# Mover projeto para /home/$USER/ em vez de /mnt/c/
```

## 🔧 Configuração Recomendada para WSL2

### 1. **Arquivo .wslconfig**

Crie `C:\Users\<seu_usuario>\.wslconfig`:

```ini
[wsl2]
memory=8GB
processors=4
swap=2GB
localhostForwarding=true
nestedVirtualization=true
```

### 2. **Configuração do Ubuntu**

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar ferramentas essenciais
sudo apt install -y build-essential curl wget git zsh

# Configurar zsh como shell padrão
chsh -s $(which zsh)
```

### 3. **Configuração do Python**

```bash
# Instalar Python 3.11
sudo apt install -y python3.11 python3.11-venv python3.11-dev

# Instalar uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Configurar PATH
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

## 🚀 Setup Alternativo sem Devcontainer

### 1. **Executar Script de Setup**

```bash
# Dar permissão de execução
chmod +x scripts/setup_wsl2.sh

# Executar setup
./scripts/setup_wsl2.sh
```

### 2. **Configuração Manual do VS Code/Cursor**

```json
// .vscode/settings.json
{
  "python.defaultInterpreterPath": "/home/rafael/.venv/bin/python",
  "python.terminal.activateEnvironment": true,
  "terminal.integrated.defaultProfile.linux": "zsh"
}
```

### 3. **Ativar Ambiente Virtual**

```bash
# Ativar virtual environment
source .venv/bin/activate

# Verificar instalação
python --version
pip list
```

## 📊 Monitoramento e Diagnóstico

### 1. **Verificar Status do Sistema**

```bash
# Status WSL2
wsl --list --verbose

# Uso de recursos
htop
free -h
df -h

# Status dos serviços
sudo systemctl status docker
sudo systemctl status ssh
```

### 2. **Logs do Sistema**

```bash
# Logs do WSL2
dmesg | tail -20

# Logs do Docker
sudo journalctl -u docker -f

# Logs do sistema
sudo journalctl -f
```

### 3. **Testes de Conectividade**

```bash
# Testar DNS
nslookup google.com

# Testar conectividade
ping -c 4 8.8.8.8

# Testar portas
netstat -tulpn | grep :8888
```

## 🆘 Recursos de Ajuda

### 1. **Comandos Úteis**

```bash
# Reiniciar WSL2
wsl --shutdown && wsl

# Verificar versão WSL
wsl --version

# Atualizar WSL2
wsl --update

# Verificar distribuições instaladas
wsl --list --online
```

### 2. **Links Úteis**

- [Documentação oficial do WSL2](https://docs.microsoft.com/en-us/windows/wsl/)
- [Troubleshooting WSL2](https://docs.microsoft.com/en-us/windows/wsl/troubleshooting)
- [Docker Desktop WSL2](https://docs.docker.com/desktop/windows/wsl/)
- [Cursor WSL2 Guide](https://cursor.sh/docs/remote-development/wsl)

### 3. **Comunidade**

- [WSL GitHub Issues](https://github.com/microsoft/WSL/issues)
- [Stack Overflow - WSL2](https://stackoverflow.com/questions/tagged/wsl2)
- [Reddit - WSL](https://www.reddit.com/r/bashonubuntuonwindows/)

## 🔄 Procedimento de Recuperação

Se nada funcionar, siga este procedimento:

1. **Backup dos dados importantes**
2. **Desinstalar WSL2 completamente**
3. **Reinstalar WSL2 do zero**
4. **Restaurar dados do backup**
5. **Reconfigurar ambiente**

```bash
# Desinstalar WSL2 (PowerShell como Admin)
wsl --unregister Ubuntu
wsl --shutdown

# Reinstalar (PowerShell como Admin)
wsl --install -d Ubuntu
```

## 📝 Notas Importantes

- **Sempre faça backup** antes de fazer mudanças drásticas
- **Use WSL2 nativo** em vez de montagem Windows quando possível
- **Mantenha o sistema atualizado** regularmente
- **Monitore o uso de recursos** para evitar problemas de performance
- **Use o script de setup** fornecido para configuração automática
