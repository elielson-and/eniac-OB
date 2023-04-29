import time
import sys
import json
import datetime
from view.Messages import Message
from config.Environment.Environment import Environment

class Chart:
    def __init__(self, api) -> None:
        self.api = api


    #------------------------------ 
    # Get all available assets 
    #------------------------------ 
    def get_all_available_assets(self):
        print(Message.info("Obtendo lista de ativos disponíveis..."))
        allow_otc = Environment.can_trade_otc()
        all_assets = self.api.get_all_open_time()
        open_digital_assets = {}
        desired_assets = ["EURUSD", "EURGBP", "EURJPY", "GBPUSD", "AUDCAD", "AUDUSD", "GBPJPY", "USDJPY", "AUDJPY"]
        for asset, data in all_assets.get("digital", {}).items():
            if data.get("open", False):
                if allow_otc:
                    if asset.split("-")[0] in desired_assets:
                        open_digital_assets[asset] = data
                else:
                    if asset.split("-")[0] in desired_assets and "-OTC" not in asset:
                        open_digital_assets[asset] = data
        json_formatado = json.dumps(open_digital_assets, indent=2)
        return json_formatado

      

    #------------------------------ 
    # Check if volatility is high
    #------------------------------ 
    def is_high_volatility(self, asset, expiration_time):
        pair = asset
        candles = self.api.get_candles(pair, expiration_time * 60, 30, time.time())
        
        volatility = []
        for candle in candles:
            diff = candle['open'] - candle['close']
            volatility.append(abs(diff))

        average_volatility = sum(volatility) / len(volatility)
        if average_volatility > 0.001:
            print("Alta volatilidade")
            return True
        else:
            print("Baixa volatilidade")
            return False



    #-------------------------------------
    #  Check if the market is lateralized
    #-------------------------------------
    def is_asset_chart_lateralized(self, asset, expiration_time):
        num_candles_behind = 20
        # Define o horário atual como o horário de término dos candles
        endtime = int(datetime.datetime.now().timestamp())

        # Obtém os últimos 20 candles do ativo EURUSD
        candles = self.api.get_candles(asset, 60 * expiration_time, endtime, num_candles_behind)

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
    def get_chart_trend(self, asset , expiration_time ):
        # Define o período de 5 minutos
        period = expiration_time * 60
        
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

    


    def is_acceptable_payout(self,payout):
        if(payout >= 0.80):
            return True
        else:
            return False

    
    
            