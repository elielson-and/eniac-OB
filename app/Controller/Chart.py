import time
import sys
import json
import datetime

class Chart:
    def __init__(self, api) -> None:
        self.api = api


    #------------------------------ 
    # Get all available assets 
    #------------------------------ 
    def get_all_available_assets(self):
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

    #------------------------------ 
    # Check if volatility is high
    #------------------------------ 
    def is_high_volatility(self):
        pair = 'EURUSD'
        candles = self.api.get_candles(pair, 5 * 60, 30, time.time())
        
        volatility = []
        for candle in candles:
            diff = candle['open'] - candle['close']
            volatility.append(abs(diff))

        average_volatility = sum(volatility) / len(volatility)
        if average_volatility > 0.001:
            print("O mercado está volátil.")
        else:
            print("O mercado não está volátil.")
    
    #-------------------------------------
    #  Check if the market is lateralized
    #-------------------------------------
    def is_asset_chart_lateralized(self):
        # Define o horário atual como o horário de término dos candles
        endtime = int(datetime.datetime.now().timestamp())

        # Obtém os últimos 20 candles do ativo EURUSD
        candles = self.api.get_candles("EURUSD", 60*5, endtime, 20)

        # Calcula a variação entre o preço de abertura e fechamento de cada candle
        price_changes = []
        for candle in candles:
            price_changes.append(abs(candle["close"] - candle["open"]))

        # Verifica se há pelo menos um candle na lista de preços
        if len(price_changes) > 0:
            # Calcula a média da variação de preços
            average_change = sum(price_changes) / len(price_changes)
            print( average_change < 0.001 )
        else:
            # Caso não haja nenhum candle, retorna False
            print( False)


    #------------------------------ 
    #  Get chart trend, up or down
    #------------------------------ 
    def get_chart_trend(self, asset = "EURUSD", expiration_time = 5):
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

    
        
    

    
    
            