import time
import sys
import json
import datetime
import talib
import numpy as np
from view.Messages import Message
from config.Environment.Environment import Environment as Env

class Chart:
    def __init__(self, api) -> None:
        self.api = api


    #------------------------------ 
    # Get all available assets 
    #------------------------------ 
    def get_all_available_assets(self):
        print(Message.info("Updating chart info..."))
        assets = self.api.get_all_open_time()
        open_assets = {}
        for asset in assets['digital']:
            if assets['digital'][asset]['open'] == True:
                if Env.allow_otc:
                    open_assets[asset] = assets[asset]
                elif "-OTC" not in asset:
                    open_assets[asset] = assets[asset]
        return open_assets
   
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
        
    def get_payout(self, asset):
        modality = Env.trade_modality()
        if modality == 'binary':
            return self.api.get_all_profit()[asset][modality]
        
        elif modality == 'turbo': # Unused for this time, but available
            binary_payout_assets = self.api.get_all_profit()
            return int(100 * binary_payout_assets[asset, Env.candle_period()])
        
        elif modality == 'digital':
            self.api.subscribe_strike_list(asset, Env.candle_period())
            while True:
                digital_payout_asset = self.api.get_digital_current_profit(asset, Env.candle_period())
                if digital_payout_asset != False:
                    digital_payout_asset = int(digital_payout_asset)
                    break
                time.sleep(0.4)
            self.api.unsubscribe_strike_list(asset, Env.candle_period())
            return digital_payout_asset
        

    #------------------------------ 
    # Check if volatility is high
    #------------------------------ 
    # def is_high_volatility(self, asset, expiration_time):
    #     pair = asset
    #     candles = self.api.get_candles(pair, expiration_time * 60, 50, time.time())
        
    #     volatility = []
    #     for candle in candles:
    #         diff = candle['open'] - candle['close']
    #         volatility.append(abs(diff))

    #     average_volatility = sum(volatility) / len(volatility)
    #     if average_volatility > 0.0015:
    #         print(Message.alert("High volatility"))
    #         return True # High
    #     else:
    #         print(Message.success("Low volatility"))
    #         return False # Low
        
    # (In test)
    def is_high_volatility_v2(self, asset):
        candle_period = Env.candle_period() * 60
        # Obtem os ultimos 288 candles de 5 min, gera uma media de oscilação
        # e compara os ultimos 20 candles com esta média para analisar possivel volatilidade
        candles = self.api.get_candles(asset, candle_period, 1000, time.time()) # < 288 = 24h
        print(f"Analized candles: {len(candles)} - M{Env.candle_period()}")
        # Calculate average volatility of last 10 candles
        volatility = []
        for candle in candles:
            diff = candle['open'] - candle['close']
            volatility.append(abs(diff))
        average_volatility = sum(volatility) / len(volatility)
        # Calculate average volatility of last 20 candles
        volatility = []
        for candle in candles[-20:]:
            diff = candle['open'] - candle['close']
            volatility.append(abs(diff))
        average_volatility_10 = sum(volatility) / len(volatility)
        # Compare average volatilities and return result
        if average_volatility_10 > average_volatility:
            print(Message.alert("High volatility"))
            return True # High
        else:
            print(Message.success("Low volatility"))
            return False # Low
        
        
    # Ultiliza as bandas de bolliger para realizar a a analise de volatilidade
    def is_high_volatility_v3(self, asset):
        # Obtem os ultimos 8640 candles de 5 min (equivalente a 30 dias), calcula a volatilidade
        candles = self.api.get_candles(asset, Env.candle_period() * 60, 1000, time.time())
        print(f"Analized candles: {len(candles)} - M{Env.candle_period()}")
        prices = np.array([candle['close'] for candle in candles])
        # Configurando periodo de 20 e desvio de 2
        upper, middle, lower = talib.BBANDS(prices, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
        volatility = upper - lower
        average_volatility = np.mean(volatility)

        # Calcula a largura atual das bandas de Bollinger
        current_price = candles[-1]['close']
        current_upper, current_middle, current_lower = talib.BBANDS(prices[-21:], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
        current_width = current_upper[-1] - current_lower[-1]

        # Compara a largura atual com a média de volatilidade
        if current_width > average_volatility:
            print(f"Volatility: {Message.txt_red('[ HIGH ]')}")
            return True # High
        else:
            print(f"Volatility: {Message.txt_green('[ LOW ]')}")
            return False # Low
            

    #-------------------------------------
    #  Check if the market is lateralized
    #-------------------------------------
    def is_asset_chart_lateralized(self, asset):
        num_candles_behind = 20
        # Define o horário atual como o horário de término dos candles
        endtime = int(datetime.datetime.now().timestamp())

        # Obtém os últimos 20 candles do ativo EURUSD
        candles = self.api.get_candles(asset, Env.candle_period() * 60, endtime, num_candles_behind)

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
    def is_asset_chart_lateralized_v2(self, asset) :
        # get candles for the selected asset and period
        candles = self.api.get_candles(asset, Env.candle_period() * 60, 10, time.time())
        # calculate the mean of the close prices
        close_prices = [candle["close"] for candle in candles]
        close_prices_mean = sum(close_prices) / len(close_prices)
        # check if the close prices are within a certain range
        deviation = 0.01 # set the deviation to 1% for example
        for close_price in close_prices:
            if close_price < close_prices_mean * (1 - deviation) or close_price > close_prices_mean * (1 + deviation):
                print(f"Laterialized: {Message.txt_red('[ YES ]')}")
                return True
        print(f"Laterialized: {Message.txt_green('[ NO ]')}")
        return False



    #------------------------------ 
    #  Get chart trend, up or down
    #------------------------------ 
    def get_chart_trend(self, asset  ):
 
        # Busca os dados do histórico do ativo no período definido
        candles = self.api.get_candles(asset, Env.candle_period() * 60, 100, time.time())
        
        # Calcula a média móvel simples de 20 períodos
        sma_20 = sum(candle["close"] for candle in candles[-20:]) / 20
        
        # Calcula a média móvel simples de 50 períodos
        sma_50 = sum(candle["close"] for candle in candles[-50:]) / 50
        
        # Verifica se a média móvel de 20 períodos está acima da média móvel de 50 períodos
        if sma_20 > sma_50:
            print(f"[{asset}] => HIGH TREND")
            return 'high'
        else:
            print(f"[{asset}] => LOW TREND")
            return 'low'

    
    #---------------------------------------
    #  Verify if payout value is acceptable
    #---------------------------------------
    def is_acceptable_payout(self,payout):
        acceptable_payout = ''
        if Env.trade_modality() == 'binary':
            acceptable_payout = '0.'+Env.payout()
        elif Env.trade_modality() == 'digital':
            acceptable_payout = Env.payout()

        if(payout >= float(acceptable_payout)):
            return True
        else:
            return False


    
    #---------------------------------------------------------
    #  Verify if the candle wick is big or not and return this
    #---------------------------------------------------------
    def is_big_wick(self, asset):
        aceitable_wick_size = 1.7
   
        # Pega os últimos 10 candles
        candles = self.api.get_candles(asset, Env.candle_period() * 60, 10, time.time())

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
    
    def verificar_pavios_grandes(self, asset ):
        candles = self.api.get_candles(asset, Env.candle_period() * 60, 1000, time.time())  # Obtém os últimos 1000 candles

        pavios = []
        for i in range(1000):
            candle = candles[i]
            tamanho_pavio_superior = abs(candle['max'] - max(candle['close'], candle['open']))
            tamanho_pavio_inferior = abs(candle['min'] - min(candle['close'], candle['open']))
            pavios.append(tamanho_pavio_superior)
            pavios.append(tamanho_pavio_inferior)

        media_pavios = sum(pavios) / (len(pavios) // 2)  # Correção: Dividir por 2 para considerar apenas um dos lados dos pavios

        ultimos_candles = candles[-20:]
        for candle in ultimos_candles:
            tamanho_pavio_superior = abs(candle['max'] - max(candle['close'], candle['open']))
            tamanho_pavio_inferior = abs(candle['min'] - min(candle['close'], candle['open']))
            if tamanho_pavio_superior > media_pavios or tamanho_pavio_inferior > media_pavios:
                print("Pavios grandes")
                return

        print("Pavios normais em relação à maioria")

    
    def is_candles_small(self, asset):
        candles = self.api.get_candles(asset, Env.candle_period() * 60, 400, time.time())  # Obtém os últimos 400 candles

        tamanho_corpo_candles = []
        for candle in candles:
            tamanho_corpo = abs(candle['close'] - candle['open'])
            tamanho_corpo_candles.append(tamanho_corpo)

        media_tamanho_corpo_400 = sum(tamanho_corpo_candles) / len(tamanho_corpo_candles)

        ultimos_candles = candles[-5:]
        tamanho_corpo_ultimos_candles = []
        for candle in ultimos_candles:
            tamanho_corpo = abs(candle['close'] - candle['open'])
            tamanho_corpo_ultimos_candles.append(tamanho_corpo)

        media_tamanho_corpo_10 = sum(tamanho_corpo_ultimos_candles) / len(tamanho_corpo_ultimos_candles)

        if media_tamanho_corpo_10 < media_tamanho_corpo_400:
            print("Candles muito pequenos")
            return True

        print("Candles normais")
        return False


