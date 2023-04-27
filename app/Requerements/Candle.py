import time
import sys
import json

class Candle:
    def __init__(self, api) -> None:
        self.api = api


    def check_trend(self, asset = "EURUSD", expiration_time = 5):
        # Define o período de 5 minutos
        period = 5 * 60
        
        # Define o intervalo de tempo a ser verificado
        end_time = time.time()
        start_time = end_time - period
        
        # Busca os dados do histórico do ativo no período definido
        candles = self.api.get_candles(asset, period, 100, start_time)
        
        
        # Calcula a média móvel simples de 20 períodos
        sma_20 = sum(candle["close"] for candle in candles[-20:]) / 20
        
        # Calcula a média móvel simples de 50 períodos
        sma_50 = sum(candle["close"] for candle in candles[-50:]) / 50
        
        # Verifica se a média móvel de 20 períodos está acima da média móvel de 50 períodos
        if sma_20 > sma_50:
            print("tendência de alta")
        else:
            print("tendência de baixa")


    def get_all_available_assets(self):
        #----------------------------------------------------------------
        # Busca os ativos disponíveis que não estão em OTC
        # Filtra os ativos disponíveis no momento e retorna apenas 
        # os que de fato estão na lista de permitidos para operar no bot
        #----------------------------------------------------------------
        assets = self.api.get_all_profit()
        filtered_assets = {}
        for asset in assets:
            if asset in ["EURUSD", "EURGBP", "EURJPY", "GBPUSD", "AUDCAD", "AUDUSD", "GBPJPY", "USDJPY", "AUDJPY"]:
                filtered_assets[asset] = assets[asset]

        # Ordena os ativos por payout em ordem decrescente
        sorted_assets = sorted(filtered_assets.items(), key=lambda x: x[1]["turbo"], reverse=True)

        # Cria um novo dicionário com os ativos ordenados
        ordered_assets = {}
        for asset in sorted_assets:
            ordered_assets[asset[0]] = asset[1]

        json_formatado = json.dumps(ordered_assets, indent=2)

        # Imprime o resultado
        print(json_formatado)

   