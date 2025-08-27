"""
Módulo de configuração para o projeto.

Este módulo contém funcionalidades para:
- Carregamento de configurações de arquivos YAML
- Configurações específicas para diferentes módulos
- Validação de configurações
- Configurações padrão
"""

from . import config_manager, threew_config

__all__ = ["config_manager", "threew_config"]
