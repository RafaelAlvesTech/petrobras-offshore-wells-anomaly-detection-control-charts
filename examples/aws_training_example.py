#!/usr/bin/env python3
"""
Exemplo de Uso AWS para Petrobras Offshore Wells Anomaly Detection

Este script demonstra como usar a integração AWS para treinar modelos
de detecção de anomalias na cloud.
"""

import logging
import sys
from pathlib import Path

# Adiciona o diretório src ao path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from aws.aws_config_manager import AWSConfigManager
from aws.aws_training import AWSTrainingManager

# Configuração de logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """Função principal do exemplo."""
    print("🚀 Exemplo de Uso AWS para Petrobras Anomaly Detection")
    print("=" * 60)

    try:
        # 1. Inicializar gerenciador de configuração
        print("\n1️⃣ Inicializando gerenciador de configuração AWS...")
        config_manager = AWSConfigManager()

        # Verificar status da configuração
        config_manager.print_status()

        # 2. Criar bucket S3 se não existir
        print("\n2️⃣ Configurando bucket S3...")
        if config_manager.create_s3_bucket():
            print("✅ Bucket S3 configurado com sucesso")
        else:
            print("❌ Falha na configuração do bucket S3")
            return

        # Configurar estrutura de pastas
        if config_manager.setup_s3_structure():
            print("✅ Estrutura S3 configurada com sucesso")
        else:
            print("❌ Falha na configuração da estrutura S3")
            return

        # 3. Inicializar gerenciador de treinamento
        print("\n3️⃣ Inicializando gerenciador de treinamento...")
        training_manager = AWSTrainingManager()

        # 4. Exemplo de configuração para LSTM-VAE
        print("\n4️⃣ Configurando treinamento para LSTM-VAE...")
        lstm_config = training_manager.get_training_config("lstm_vae")

        if lstm_config:
            print("✅ Configuração LSTM-VAE obtida:")
            print(f"   • Instance Type: {lstm_config.instance_type}")
            print(f"   • Batch Size: {lstm_config.hyperparameters.get('batch_size')}")
            print(
                f"   • Learning Rate: {lstm_config.hyperparameters.get('learning_rate')}"
            )
            print(f"   • Epochs: {lstm_config.hyperparameters.get('epochs')}")

            # 5. Estimativa de custo
            print("\n5️⃣ Estimativa de custo:")
            cost_estimate = training_manager.get_cost_estimate(lstm_config)
            if cost_estimate:
                print(
                    f"   • Custo por hora: ${cost_estimate.get('hourly_rate', 0):.2f}"
                )
                print(
                    f"   • Horas estimadas: {cost_estimate.get('estimated_hours', 0):.1f}"
                )
                print(
                    f"   • Custo total estimado: ${cost_estimate.get('total_cost', 0):.2f}"
                )
            else:
                print("   ⚠️ Não foi possível estimar o custo")

            # 6. Listar jobs existentes
            print("\n6️⃣ Jobs de treinamento existentes:")
            try:
                jobs = training_manager.list_training_jobs()
                if jobs:
                    for job in jobs[:5]:  # Mostra apenas os 5 mais recentes
                        print(f"   • {job['job_name']} - {job['status']}")
                else:
                    print("   📝 Nenhum job de treinamento encontrado")
            except Exception as e:
                print(f"   ⚠️ Erro ao listar jobs: {e}")

            # 7. Exemplo de criação de job (comentado para segurança)
            print("\n7️⃣ Exemplo de criação de job de treinamento:")
            print("   # Para criar um job de treinamento, descomente as linhas abaixo:")
            print("   # job_name = training_manager.create_training_job(lstm_config)")
            print("   # print(f'Job criado: {job_name}')")

            # 8. Exemplo de tuning de hiperparâmetros
            print("\n8️⃣ Exemplo de tuning de hiperparâmetros:")
            print("   # Para criar um job de tuning, descomente as linhas abaixo:")
            print(
                "   # tuning_job_name = training_manager.create_hyperparameter_tuning_job(lstm_config)"
            )
            print("   # print(f'Job de tuning criado: {tuning_job_name}')")

        else:
            print("❌ Falha ao obter configuração de treinamento")
            return

        # 9. Próximos passos
        print("\n9️⃣ Próximos passos:")
        print("   📚 Leia a documentação: docs/AWS_SETUP.md")
        print("   🔧 Configure suas credenciais AWS no arquivo .env.aws")
        print("   🚀 Execute: python src/aws/aws_training.py")
        print("   💰 Configure alertas de custo no CloudWatch")
        print("   🔒 Revise as configurações de segurança IAM")

        print("\n🎉 Exemplo concluído com sucesso!")

    except Exception as e:
        logger.error(f"Erro durante a execução: {e}")
        print(f"\n❌ Erro: {e}")
        print("\n🔧 Verifique:")
        print("   • Se as credenciais AWS estão configuradas")
        print("   • Se o arquivo aws-config.yaml existe")
        print("   • Se as dependências estão instaladas")
        print("   • Se você tem permissões adequadas na AWS")


def demo_hyperparameter_tuning():
    """Demonstração de tuning de hiperparâmetros."""
    print("\n🔧 Demonstração de Tuning de Hiperparâmetros")
    print("=" * 50)

    try:
        training_manager = AWSTrainingManager()

        # Configuração para TranAD
        tranad_config = training_manager.get_training_config("tranad")

        if tranad_config:
            print("✅ Configuração TranAD obtida:")
            print(f"   • Instance Type: {tranad_config.instance_type}")
            print(f"   • Batch Size: {tranad_config.hyperparameters.get('batch_size')}")
            print(
                f"   • Learning Rate: {tranad_config.hyperparameters.get('learning_rate')}"
            )

            # Espaço de busca
            search_space = training_manager.get_hyperparameter_search_space("tranad")
            if search_space:
                print("\n🔍 Espaço de busca de hiperparâmetros:")
                for param, config in search_space.items():
                    if config.get("type") == "Continuous":
                        print(
                            f"   • {param}: {config['min_value']} - {config['max_value']}"
                        )
                    elif config.get("type") == "Categorical":
                        print(f"   • {param}: {config['values']}")

            # Estimativa de custo
            cost_estimate = training_manager.get_cost_estimate(tranad_config)
            if cost_estimate:
                print(
                    f"\n💰 Custo estimado para tuning: ${cost_estimate.get('total_cost', 0):.2f}"
                )

    except Exception as e:
        logger.error(f"Erro na demonstração de tuning: {e}")


def demo_cost_optimization():
    """Demonstração de otimização de custos."""
    print("\n💰 Demonstração de Otimização de Custos")
    print("=" * 50)

    try:
        config_manager = AWSConfigManager()

        # Criar alarme de custo
        print("🔔 Configurando alarme de custo...")
        if config_manager.create_cost_alarm(100, "MONTHLY"):
            print("✅ Alarme de custo mensal criado ($100)")
        else:
            print("⚠️ Falha ao criar alarme de custo")

        # Configurações de otimização
        cost_config = config_manager.config.get("cost_optimization", {})
        print("\n⚙️ Configurações de otimização:")
        print(
            f"   • Spot Instances: {'✅ Habilitado' if cost_config.get('spot_instances', {}).get('enabled') else '❌ Desabilitado'}"
        )
        print(
            f"   • Reserved Instances: {'✅ Habilitado' if cost_config.get('reserved_instances', {}).get('enabled') else '❌ Desabilitado'}"
        )
        print(
            f"   • Savings Plans: {'✅ Habilitado' if cost_config.get('savings_plans', {}).get('enabled') else '❌ Desabilitado'}"
        )

        # Alertas de custo
        alerts_config = cost_config.get("cost_alerts", {})
        if alerts_config.get("enabled"):
            print(f"   • Orçamento mensal: ${alerts_config.get('monthly_budget', 0)}")
            print(f"   • Orçamento diário: ${alerts_config.get('daily_budget', 0)}")

    except Exception as e:
        logger.error(f"Erro na demonstração de otimização de custos: {e}")


if __name__ == "__main__":
    # Executar exemplo principal
    main()

    # Executar demonstrações adicionais
    demo_hyperparameter_tuning()
    demo_cost_optimization()

    print("\n" + "=" * 60)
    print("🎯 Para mais informações, consulte:")
    print("   📚 docs/AWS_SETUP.md")
    print("   🚀 scripts/setup_aws.sh")
    print("   🔧 src/aws/aws_config_manager.py")
    print("   🚀 src/aws/aws_training.py")
    print("=" * 60)
