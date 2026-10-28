from datetime import datetime, timedelta
import requests
from api_client import fetch_history, fetch_forecast, trigger_collection
from analysis import (
    calcular_resumo_periodo,
    analisar_precipitacao,
    analisar_umidade_temperatura,
    analisar_extremos_previsao
)

BASE_URL = "http://127.0.0.1:8000"


def obter_limites_periodo():
    """Calcula a janela exata de 90 dias atrás até 7 dias à frente."""
    hoje = datetime.now().date()
    data_min = hoje - timedelta(days=90)
    data_max = hoje + timedelta(days=7)
    return str(data_min), str(data_max)


def pedir_data(mensagem: str):
    """
    Pede uma data no formato YYYY-MM-DD.
    Valida se está dentro do período disponível (últimos 90 dias até próximos 7 dias).
    Permite digitar '0' ou 'v' para cancelar.
    """
    data_min_str, data_max_str = obter_limites_periodo()
    data_min = datetime.strptime(data_min_str, "%Y-%m-%d").date()
    data_max = datetime.strptime(data_max_str, "%Y-%m-%d").date()

    while True:
        entrada = input(f"{mensagem} (ou '0' para voltar): ").strip()

        if entrada.lower() in ["0", "v", "voltar"]:
            return None

        try:
            data_digitada = datetime.strptime(entrada, "%Y-%m-%d").date()
        except ValueError:
            print("⚠️ Formato inválido! Digite no padrão YYYY-MM-DD (exemplo: 2026-09-15).")
            continue

        if data_digitada < data_min or data_digitada > data_max:
            print(f"⚠️ Data fora do intervalo permitido! Digite entre {data_min_str} e {data_max_str}.")
            continue

        return entrada


def exibir_cabecalho_analise(titulo: str):
    """Exibe o título da tela e destaca claramente o intervalo de datas aceito."""
    data_min, data_max = obter_limites_periodo()
    print("\n" + "=" * 55)
    print(f"   {titulo}")
    print(f"   📅 Digite entre: {data_min} e {data_max}")
    print("=" * 55)


def ver_condicao_atual():
    try:
        res = requests.get(f"{BASE_URL}/weather/current", timeout=5)
        if res.status_code == 200:
            d = res.json()
            print("\n📍 CONDIÇÃO MAIS RECENTE REGISTRADA:")
            print(f" - Data/Hora: {d.get('datetime')}")
            print(f" - Temperatura: {d.get('temperature')}°C (Sensação: {d.get('apparent_temperature')}°C)")
            print(f" - Umidade: {d.get('relative_humidity')}% | Vento: {d.get('wind_speed')} km/h")
            print(f" - Precipitação: {d.get('precipitation')} mm")
        else:
            print("❌ Nenhum dado recente encontrado.")
    except Exception as e:
        print(f"❌ Erro ao consultar condição atual: {e}")


def main_menu():
    while True:
        print("\n" + "=" * 50)
        print("   🌤️ WEATHER ANALYZER — MENU PRINCIPAL")
        print("=" * 50)
        print("1. Disparar Coleta de Dados (Open-Meteo)")
        print("2. Ver Condição Atual (Mais recente)")
        print("3. Análise 1: Resumo Meteorológico (Média, Mín, Máx)")
        print("4. Análise 2: Análise de Precipitação (Chuva)")
        print("5. Análise 3: Comparativo Temperatura x Umidade")
        print("6. Análise 4: Extremos da Previsão (7 dias)")
        print("7. Sair")
        print("=" * 50)

        opcao = input("Escolha uma opção (1-7): ").strip()

        # --- OPÇÃO 1: COLETA ---
        if opcao == "1":
            print("\nColetando dados da Open-Meteo...")
            res = trigger_collection()
            if res:
                print(f"✅ Sucesso: {res.get('message')} ({res.get('total_records', 0)} registros salvos)")
            else:
                print("❌ Falha na coleta.")

        # --- OPÇÃO 2: ATUAL ---
        elif opcao == "2":
            ver_condicao_atual()

        # --- OPÇÃO 3: RESUMO ---
        elif opcao == "3":
            exibir_cabecalho_analise("📊 ANÁLISE 1: RESUMO METEOROLÓGICO")
            ini = pedir_data("Data inicial (YYYY-MM-DD)")
            if not ini:
                print("↩️ Operação cancelada.")
                continue

            fim = pedir_data("Data final (YYYY-MM-DD)")
            if not fim:
                print("↩️ Operação cancelada.")
                continue

            dados = fetch_history(ini, fim)
            res = calcular_resumo_periodo(dados)
            if res:
                print(f"\n📊 Resultados para o período de {ini} até {fim} ({res['total']} leituras):")
                print(f" - Temp Média: {res['media']}°C")
                print(f" - Temp Mínima: {res['min']}°C")
                print(f" - Temp Máxima: {res['max']}°C")
            else:
                print("⚠️ Nenhum dado retornado pela API para esse período.")

        # --- OPÇÃO 4: PRECIPITAÇÃO ---
        elif opcao == "4":
            exibir_cabecalho_analise("🌧️ ANÁLISE 2: PRECIPITAÇÃO (CHUVA)")
            ini = pedir_data("Data inicial (YYYY-MM-DD)")
            if not ini:
                print("↩️ Operação cancelada.")
                continue

            fim = pedir_data("Data final (YYYY-MM-DD)")
            if not fim:
                print("↩️ Operação cancelada.")
                continue

            dados = fetch_history(ini, fim)
            res = analisar_precipitacao(dados)
            if res:
                print(f"\n🌧️ Resultados de Precipitação ({ini} até {fim}):")
                print(f" - Volume Acumulado Total: {res['total_acumulado_mm']} mm")
                print(f" - Dia com maior volume de chuva: {res['dia_mais_chuvoso']} ({res['chuva_no_dia_mm']} mm)")
            else:
                print("⚠️ Nenhum dado retornado pela API para esse período.")

        # --- OPÇÃO 5: TEMP X UMIDADE ---
        elif opcao == "5":
            exibir_cabecalho_analise("💧 ANÁLISE 3: COMPARATIVO TEMP X UMIDADE")
            ini = pedir_data("Data inicial (YYYY-MM-DD)")
            if not ini:
                print("↩️ Operação cancelada.")
                continue

            fim = pedir_data("Data final (YYYY-MM-DD)")
            if not fim:
                print("↩️ Operação cancelada.")
                continue

            dados = fetch_history(ini, fim)
            res = analisar_umidade_temperatura(dados)
            if res:
                print(f"\n💧 Médias comparativas ({ini} até {fim}):")
                print(f" - Temperatura Média: {res['temp_media']}°C")
                print(f" - Umidade Relativa Média: {res['umid_media']}%")
            else:
                print("⚠️ Nenhum dado retornado pela API para esse período.")

        # --- OPÇÃO 6: PREVISÃO ---
        elif opcao == "6":
            hoje = datetime.now().strftime("%Y-%m-%d")
            semana = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
            print("\n" + "=" * 55)
            print(f"   🔮 ANÁLISE 4: EXTREMOS DA PREVISÃO")
            print(f"   Período previsto: {hoje} até {semana}")
            print("=" * 55)

            dados = fetch_forecast(hoje, semana)
            res = analisar_extremos_previsao(dados)
            if res:
                print(f"\n🔥 Dia mais quente previsto: {res['dia_mais_quente']} (Média: {res['media_quente']}°C)")
                print(f"❄️ Dia mais frio previsto:   {res['dia_mais_frio']} (Média: {res['media_frio']}°C)")
            else:
                print("⚠️ Nenhuma previsão encontrada no banco.")

        # --- OPÇÃO 7: SAIR ---
        elif opcao == "7":
            print("\nEncerrando o analisador. Até logo!")
            break

        else:
            print("\n⚠️ Opção inválida. Digite um número de 1 a 7.")


if __name__ == "__main__":
    main_menu()