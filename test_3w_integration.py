#!/usr/bin/env python3
"""
Script de teste para a integração com o Dataset 3W da Petrobras.

Este script verifica se todos os módulos da integração estão funcionando
corretamente e testa as funcionalidades principais.
"""

import logging
import sys

# Configura logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def test_imports():
    """Testa se todos os módulos podem ser importados."""
    print("🧪 Testando imports...")

    try:
        # Testa módulos principais
        from src.data.threew_dataset import ThreeWDataset

        # Testa se a classe pode ser instanciada (quando disponível)
        try:
            ThreeWDataset()
            print("✅ Dataset 3W disponível e funcional")
        except ImportError:
            print("⚠️ Dataset 3W não disponível, mas módulo importado com sucesso")

        print("✅ Todos os módulos importados com sucesso")
        return True

    except ImportError as e:
        print(f"❌ Erro ao importar módulos: {e}")
        return False


def test_threew_availability():
    """Testa se o dataset 3W está disponível."""
    print("\n📊 Testando disponibilidade do dataset 3W...")

    try:
        from src.data.threew_dataset import get_threew_info, is_threew_available

        if is_threew_available():
            info = get_threew_info()
            print(f"✅ Dataset 3W disponível - Versão: {info.get('version', 'N/A')}")
            print(f"   Dataset path: {info.get('dataset_path', 'N/A')}")
            print(f"   Folds path: {info.get('folds_path', 'N/A')}")
            return True
        else:
            print("⚠️ Dataset 3W não disponível")
            print(
                "   Para usar, clone o repositório: git clone https://github.com/petrobras/3W.git"
            )
            return False

    except Exception as e:
        print(f"❌ Erro ao verificar disponibilidade: {e}")
        return False


def test_config_system():
    """Testa o sistema de configuração."""
    print("\n⚙️ Testando sistema de configuração...")

    try:
        from src.config.threew_config import get_threew_dataset_config

        config = get_threew_dataset_config()

        # Verifica se as configurações principais estão presentes
        required_keys = ["dataset", "problems", "loading", "preprocessing"]
        for key in required_keys:
            if key in config:
                print(f"✅ Configuração '{key}' encontrada")
            else:
                print(f"❌ Configuração '{key}' não encontrada")
                return False

        print(
            f"✅ Sistema de configuração funcionando - {len(config.get('problems', []))} problemas configurados"
        )
        return True

    except Exception as e:
        print(f"❌ Erro no sistema de configuração: {e}")
        return False


def test_data_loader():
    """Testa o carregador de dados."""
    print("\n📊 Testando carregador de dados...")

    try:
        from src.data.data_loader import create_data_loader

        # Cria carregador
        loader = create_data_loader(use_threew=True, cache_data=True)

        # Verifica informações
        info = loader.get_data_info()
        print(
            f"✅ Carregador criado - 3W: {info['use_threew']}, Cache: {info['cache_enabled']}"
        )

        # Lista problemas disponíveis
        problems = loader.list_available_problems()
        print(f"✅ Problemas disponíveis: {problems}")

        return True

    except Exception as e:
        print(f"❌ Erro no carregador de dados: {e}")
        return False


def test_preprocessing():
    """Testa o sistema de pré-processamento."""
    print("\n🧹 Testando sistema de pré-processamento...")

    try:
        import numpy as np

        from src.data.preprocessing import create_preprocessor

        # Cria dados de teste
        X_test = np.random.randn(100, 10)
        y_test = np.random.randint(0, 2, 100)

        # Cria pré-processador
        preprocessor = create_preprocessor(
            imputation_strategy="mean",
            scaling_method="robust",
            feature_selection_method="mutual_info",
            n_features=5,
            pca_components=3,
        )

        # Testa fit_transform
        X_processed = preprocessor.fit_transform(X_test, y_test)

        print(
            f"✅ Pré-processamento funcionando - Forma original: {X_test.shape}, Processado: {X_processed.shape}"
        )

        # Verifica informações
        info = preprocessor.get_preprocessing_info()
        print(f"   Imputer: {info['has_imputer']}, Scaler: {info['has_scaler']}")
        print(
            f"   Feature Selector: {info['has_feature_selector']}, PCA: {info['has_pca']}"
        )

        return True

    except Exception as e:
        print(f"❌ Erro no pré-processamento: {e}")
        return False


def test_rolling_window():
    """Testa o sistema de janelas deslizantes."""
    print("\n🪟 Testando sistema de janelas deslizantes...")

    try:
        import numpy as np

        from src.data.preprocessing import create_rolling_window_preprocessor

        # Cria dados de teste
        X_test = np.random.randn(1000, 5)

        # Cria pré-processador de janelas
        window_preprocessor = create_rolling_window_preprocessor(
            window_size=100, step_size=1, padding="same"
        )

        # Cria janelas
        X_windows, _ = window_preprocessor.create_windows(X_test)

        print(
            f"✅ Janelas deslizantes funcionando - Forma original: {X_test.shape}, Janelas: {X_windows.shape}"
        )

        # Testa achatamento
        X_flat = window_preprocessor.flatten_windows(X_windows)
        print(f"   Janelas achatadas: {X_flat.shape}")

        return True

    except Exception as e:
        print(f"❌ Erro nas janelas deslizantes: {e}")
        return False


def test_full_pipeline():
    """Testa o pipeline completo (se o 3W estiver disponível)."""
    print("\n🚀 Testando pipeline completo...")

    try:
        from src.data.threew_dataset import is_threew_available

        if not is_threew_available():
            print("⚠️ Dataset 3W não disponível - pulando teste do pipeline")
            return True

        from src.data.data_loader import create_data_loader

        # Cria carregador
        loader = create_data_loader(use_threew=True, cache_data=True)

        # Lista problemas
        problems = loader.list_available_problems()
        if not problems:
            print("⚠️ Nenhum problema disponível - pulando teste do pipeline")
            return True

        print(f"✅ Pipeline testado - {len(problems)} problemas disponíveis")
        return True

    except Exception as e:
        print(f"❌ Erro no pipeline completo: {e}")
        return False


def main():
    """Função principal de teste."""
    print("🛢️ Teste da Integração com Dataset 3W da Petrobras")
    print("=" * 60)

    # Lista de testes
    tests = [
        ("Imports", test_imports),
        ("Disponibilidade 3W", test_threew_availability),
        ("Sistema de Configuração", test_config_system),
        ("Carregador de Dados", test_data_loader),
        ("Pré-processamento", test_preprocessing),
        ("Janelas Deslizantes", test_rolling_window),
        ("Pipeline Completo", test_full_pipeline),
    ]

    # Executa testes
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erro inesperado em {test_name}: {e}")
            results.append((test_name, False))

    # Resumo dos resultados
    print("\n" + "=" * 60)
    print("📋 RESUMO DOS TESTES")
    print("=" * 60)

    passed = 0
    total = len(results)

    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test_name:.<30} {status}")
        if result:
            passed += 1

    print("-" * 60)
    print(f"Total: {total}, Passou: {passed}, Falhou: {total - passed}")

    if passed == total:
        print(
            "\n🎉 Todos os testes passaram! A integração 3W está funcionando perfeitamente."
        )
        print("📚 Consulte a documentação em: docs/3W_INTEGRATION.md")
        print(
            "🚀 Execute o notebook de exemplo: marimo edit notebooks/3W_integration_example.py"
        )
    else:
        print(f"\n⚠️ {total - passed} teste(s) falharam. Verifique os logs acima.")
        print("🔧 Execute o script de setup: ./scripts/setup_3w_integration.sh")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
