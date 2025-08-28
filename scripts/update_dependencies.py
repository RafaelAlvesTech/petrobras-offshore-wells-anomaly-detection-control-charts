#!/usr/bin/env python3
"""
Script para atualizar dependências e resolver vulnerabilidades de segurança.
Este script atualiza as dependências Python para versões mais seguras.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Executa um comando e trata erros."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(
            command, shell=True, check=True, capture_output=True, text=True
        )
        print(f"✅ {description} concluído com sucesso")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao {description.lower()}: {e}")
        print(f"Stderr: {e.stderr}")
        return None


def main():
    """Função principal para atualizar dependências."""
    print("🚀 Iniciando atualização de dependências de segurança...")

    # Verificar se estamos no diretório correto
    if not Path("pyproject.toml").exists():
        print(
            "❌ Erro: pyproject.toml não encontrado. Execute este script do diretório raiz do projeto."
        )
        sys.exit(1)

    # Verificar se uv está instalado
    if run_command("uv --version", "Verificando versão do uv") is None:
        print("❌ Erro: uv não está instalado ou não está no PATH")
        sys.exit(1)

    # Atualizar dependências
    print("\n📦 Atualizando dependências...")

    # Remover arquivo de lock antigo
    if Path("uv.lock").exists():
        os.remove("uv.lock")
        print("🗑️  Arquivo uv.lock removido")

    # Sincronizar dependências
    if run_command("uv sync", "Sincronizando dependências com uv") is None:
        print("❌ Falha ao sincronizar dependências")
        sys.exit(1)

    # Verificar vulnerabilidades
    print("\n🔍 Verificando vulnerabilidades...")
    if run_command("uv pip audit", "Executando auditoria de segurança") is None:
        print("⚠️  Não foi possível executar auditoria de segurança")

    # Regenerar requirements.txt
    print("\n📝 Regenerando requirements.txt...")
    if (
        run_command(
            "uv export --frozen --output-file=requirements.txt",
            "Exportando requirements.txt",
        )
        is None
    ):
        print("❌ Falha ao exportar requirements.txt")
        sys.exit(1)

    print("\n🎉 Atualização de dependências concluída com sucesso!")
    print("\n📋 Próximos passos:")
    print("1. Teste o projeto: uv run pytest")
    print("2. Verifique se não há quebras: uv run python -m src")
    print(
        "3. Commit as mudanças: git add . && git commit -m 'chore(deps): update dependencies for security'"
    )
    print("4. Push para o repositório: git push")


if __name__ == "__main__":
    main()
