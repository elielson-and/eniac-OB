import time
import sys
import json
import datetime
import talib
import numpy as np
from iqoptionapi.expiration import get_expiration_time
from view.Messages import Message
from config.Environment.Environment import Environment

class Chart:
    def __init__(self, api) -> None:
        self.api = api


    #------------------------------ 
    # Get all available assets 
    #------------------------------ 
    def get_all_available_assets(self):
        print(Message.info("Obtaining chart info..."))
        allow_otc = Environment.can_trade_otc()
        all_assets = self.api.get_all_open_time()
        open_digital_assets = {}
        desired_assets = ["EURUSD", "EURGBP", "EURJPY", "GBPUSD", "AUDCAD", "AUDUSD", "GBPJPY", "USDJPY", "AUDJPY"]
        for asset, data in all_assets.get("binary", {}).items():
            if data.get("open", False):
                if allow_otc:
                    if asset.split("-")[0] in desired_assets:
                        open_digital_assets[asset] = data
                else:
                    if asset.split("-")[0] in desired_assets and "-OTC" not in asset:
                        open_digital_assets[asset] = data
        #json_formatado = json.dumps(open_digital_assets, indent=2)
        return open_digital_assets

    #--------------------------------
    # Get payout from currently asset
    #--------------------------------
    # def get_payout(self, par, tipo = "digital", timeframe = 5):
    #     self.api.subscribe_strike_list(par, timeframe)
    #     while True:
    #         d = self.api.get_digital_current_profit(par, timeframe)
    #         if(d != False):
    #             d = int(d)
    #             break
    #         time.sleep(1)
    #     self.api.unsubscribe_strike_list(par, timeframe)
    #     return d
        
    def get_payout(self, par, tipo='digital', timeframe=5):
        return self.api.get_all_profit()[par]['binary']

    #------------------------------ 
    # Check if volatility is high
    #------------------------------ 
    def is_high_volatility(self, asset, expiration_time):
        pair = asset
        candles = self.api.get_candles(pair, expiration_time * 60, 50, time.time())
        
        volatility = []
        for candle in candles:
            diff = candle['open'] - candle['close']
            volatility.append(abs(diff))

        average_volatility = sum(volatility) / len(volatility)
        if average_volatility > 0.0015:
            print(Message.alert("High volatility"))
            return True # High
        else:
            print(Message.success("Low volatility"))
            return False # Low
        
    # (In test)
    def is_high_volatility_v2(self, pair, period=5): 
        candles = self.api.get_candles(pair, period * 60, 50, time.time())
        amplitudes = [candle["max"] - candle["min"] for candle in candles]
        average_amplitude = sum(amplitudes) / len(amplitudes)
        if average_amplitude >= 0.0015:
            print(Message.alert(f"{pair} => Alta vol"))
            return True # High
        else:
            print(Message.success(f"{pair} => Baixa vol"))
            return False # Low
    

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
            return average_change < 0.001 
        else:
            # Caso não haja nenhum candle, retorna False
            return False

    #Corrigir aqui
    def is_asset_chart_lateralized_v2(self, asset, expiration_time) :
        # get candles for the selected asset and period
        candles = self.api.get_candles(asset, expiration_time * 60, 50, time.time())
        # calculate the mean of the close prices
        close_prices = [candle["close"] for candle in candles]
        close_prices_mean = sum(close_prices) / len(close_prices)
        # check if the close prices are within a certain range
        deviation = 0.01 # set the deviation to 1% for example
        for close_price in close_prices:
            if close_price < close_prices_mean * (1 - deviation) or close_price > close_prices_mean * (1 + deviation):
                print(f"{asset} +> Laterializado ")
        print(f"{asset} +> Grafico normal \n ----")



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
            print(f"[{asset}] => HIGH TREND")
        else:
            print(f"[{asset}] => LOW TREND")

    
    #---------------------------------------
    #  Verify if payout value is acceptable
    #---------------------------------------
    def is_acceptable_payout(self,payout):
        if(payout >= 0.80):
            return True
        else:
            return False

    
    #---------------------------------------------------------
    #  Verify if the candle wick is big or not and return this
    #---------------------------------------------------------
    def is_big_wick(self, asset, period):
        aceitable_wick_size = 1.7
        # Verifica se o período informado é válido
        if period not in [60, 120, 180, 300, 600, 900, 1800, 3600, 7200, 14400, 21600, 43200, 86400]:
            print("Período inválido!")
            return

        # Pega os últimos 10 candles
        candles = self.api.get_candles(asset, period, 10, time.time())

        # Verifica se há pelo menos 10 candles
        if len(candles) < 10:
            print("Não há candles suficientes!")
            return

        # Calcula o tamanho do corpo e do pavil de cada candle
        sizes = []
        for candle in candles:
            body_size = abs(candle["open"] - candle["close"])
            pavil_size = abs(candle["max"] - candle["min"]) - body_size
            sizes.append((body_size, pavil_size))

        # Calcula a média do pavil de todos os candles
        pavil_avg = sum([pavil for _, pavil in sizes]) / 10

        # Verifica se a média é maior do que 2x o tamanho do corpo
        body_avg = sum([body for body, _ in sizes]) / 10
        if pavil_avg > (aceitable_wick_size - 0.1) * body_avg:
            return True
        else:
            return False