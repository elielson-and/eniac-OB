import time
from view.Messages import Message
from app.Controller.Chart import Chart 
import numpy as np
from config.Environment.Environment import Environment as Env

class Analyzer:
    def __init__(self, api) -> None:
        self.api = api
        self.available_assets = {}
        self.chart_volatility = ""
        self.is_chart_laterialized = False
        self.chart_trending = ""


    # ========================================================================
    def is_asset_elegible_to_trade(self, asset, payout):
        chart = Chart(self.api)
        print(f"\nAnalizing: {Message.txt_yellow(asset)} | Payout: {payout}%")
        
        if(chart.is_acceptable_payout(payout)): 

            non_compliant = [chart.is_high_volatility(asset), chart.is_asset_chart_lateralized(asset), chart.is_candles_small(asset), chart.is_big_wick(asset)]

            if any(non_compliant):
                return False
            else:
                return True
        else:
            return False
    # ======================================================================== 
    
    # Strategy

    def get_support_resistance(self, asset):
        candle_period = Env.candle_period() * 60

        candles100 = self.api.get_candles(asset, candle_period, 100, time.time())
        candles50 = self.api.get_candles(asset, candle_period, 50, time.time())
        candles20 = self.api.get_candles(asset, candle_period, 20, time.time())

        close100 = np.array([float(candle["close"]) for candle in candles100])
        close50 = np.array([float(candle["close"]) for candle in candles50])
        close20 = np.array([float(candle["close"]) for candle in candles20])

        # Etapa 1 - Analisando 100 candles
        support100 = np.min(close100)
        resistance100 = np.max(close100)

        # Etapa 2 - Analisando 50 candles
        support50 = np.min(close50)
        resistance50 = np.max(close50)

        if (support100 <= support50 + 0.0001 and support100 >= support50 - 0.0001):
            return "support"
        elif (resistance100 <= resistance50 + 0.0001 and resistance100 >= resistance50 - 0.0001):
            return "resistance"

        # Etapa 3 - Analisando 20 candles
        support20 = np.min(close20)
        resistance20 = np.max(close20)

        if (support20 <= support50 + 0.0001 and support20 >= support50 - 0.0001):
            return "support"
        elif (resistance20 <= resistance50 + 0.0001 and resistance20 >= resistance50 - 0.0001):
            return "resistance"

        return "nothing"
    
   
    def analyze_mhi_strategy(self, asset):

        candles = self.api.get_candles(asset, Env.candle_period() * 60, 500, time.time())  # Obtém os últimos 500 candles
        close_prices = np.array([float(candle["close"]) for candle in candles])

        entry_suggestion = None

        # Etapa 1: Analisar quadrandes de 12 velas nos últimos 100 candles
        for i in range(0, len(candles)-12, 12):
            quad_candles = close_prices[i:i+12]
            min_price = np.min(quad_candles)
            max_price = np.max(quad_candles)
            current_price = close_prices[i+11]

            if current_price == max_price:
                entry_suggestion = "put"  # Preço atual é o topo, sugere entrada PUT
                break
            elif current_price == min_price:
                entry_suggestion = "call"  # Preço atual é o fundo, sugere entrada CALL
                break

        if entry_suggestion:
            return entry_suggestion
        else:
            return 'nothing'



