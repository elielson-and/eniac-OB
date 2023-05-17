import time
from view.Messages import Message
from app.Controller.Chart import Chart 
import numpy as np

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
        periodo = 5
        print(f"\nAnalizing: {Message.txt_yellow(asset)} | Payout: {payout}%")
        
        #--------------------
        if(chart.is_acceptable_payout(payout)): 
            if( chart.is_high_volatility_v3(asset, periodo) or chart.is_asset_chart_lateralized_v2(asset, periodo)):
                return False
            else:
                chart.get_chart_trend(asset,5)
                return True
        else:
            return False
    # ======================================================================== 
    
    # Strategy

    def get_support_resistance(self, asset, timeframe):
        candle_period = timeframe * 60

        candles200 = self.api.get_candles(asset, candle_period, 200, time.time())
        candles100 = self.api.get_candles(asset, candle_period, 100, time.time())
        candles20 = self.api.get_candles(asset, candle_period, 20, time.time())
        
        close200 = np.array([float(candle["close"]) for candle in candles200])
        close100 = np.array([float(candle["close"]) for candle in candles100])
        close20 = np.array([float(candle["close"]) for candle in candles20])
        
        
        # Etapa 1 - Analisando 200 candles
        support200 = np.min(close200)
        resistance200 = np.max(close200)
        
        # Etapa 2 - Analisando 100 candles
        support100 = np.min(close100)
        resistance100 = np.max(close100)
        if (support100 <= support200+0.0001 and support100 >= support200-0.0001):
            return "support"
        elif (resistance100 <= resistance200+0.0001 and resistance100 >= resistance200-0.0001):
            return "resistance"
        
        # Etapa 3 - Analisando 20 candles
        support20 = np.min(close20)
        resistance20 = np.max(close20)
        if (support20 <= support200+0.0001 and support20 >= support200-0.0001):
            return "support"
        elif (resistance20 <= resistance200+0.0001 and resistance20 >= resistance200-0.0001):
            return "resistance"
        
        return "nothing"
    

    def get_support_resistance_v2(self, asset, timeframe):
        candle_period = timeframe * 60

        candles200 = self.api.get_candles(asset, candle_period, 200, time.time())
        candles100 = self.api.get_candles(asset, candle_period, 100, time.time())
        candles20 = self.api.get_candles(asset, candle_period, 20, time.time())
        
        close200 = np.array([float(candle["close"]) for candle in candles200])
        close100 = np.array([float(candle["close"]) for candle in candles100])
        close20 = np.array([float(candle["close"]) for candle in candles20])
        
        
        # Etapa 1 - Analisando 200 candles
        supports200 = []
        resistances200 = []
        
        for i in range(2, len(close200)-2):
            if close200[i] > close200[i-1] and close200[i] > close200[i+1]:
                resistances200.append(close200[i])
            elif close200[i] < close200[i-1] and close200[i] < close200[i+1]:
                supports200.append(close200[i])
        
        # Etapa 2 - Analisando 100 candles
        supports100 = []
        resistances100 = []
        
        for i in range(2, len(close100)-2):
            if close100[i] > close100[i-1] and close100[i] > close100[i+1]:
                resistances100.append(close100[i])
            elif close100[i] < close100[i-1] and close100[i] < close100[i+1]:
                supports100.append(close100[i])
        
        # Etapa 3 - Analisando 20 candles
        supports20 = []
        resistances20 = []
        
        for i in range(2, len(close20)-2):
            if close20[i] > close20[i-1] and close20[i] > close20[i+1]:
                resistances20.append(close20[i])
            elif close20[i] < close20[i-1] and close20[i] < close20[i+1]:
                supports20.append(close20[i])
        
        # Verificar se o preço atual corresponde a um suporte ou resistência registrado
        
        current_price = close20[-1]
        
        margin = 0.0001  # Definir a margem
        
        for support in supports20:
            if support - margin <= current_price <= support + margin:
                return "support"
        
        for resistance in resistances20:
            if resistance - margin <= current_price <= resistance + margin:
                return "resistance"
        
        for support in supports100:
            if support - margin <= current_price <= support + margin:
                return "support"
        
        for resistance in resistances100:
            if resistance - margin <= current_price <= resistance + margin:
                return "resistance"
        
        for support in supports200:
            if support - margin <= current_price <= support + margin:
                return "support"
        
        for resistance in resistances200:
            if resistance - margin <= current_price <= resistance + margin:
                return "resistance"
        
        return "nothing"


    

    # Esta versao estava analisano 500 velas com quadrantes de 5 unidades
    # def analyze_mhi_strategy(self, asset, timeframe):
    #     candle_period = timeframe * 60

    #     candles = self.api.get_candles(asset, candle_period, 500, time.time())  # Obtém os últimos 500 candles
    #     close_prices = np.array([float(candle["close"]) for candle in candles])

    #     entry_suggestion = None

    #     # Etapa 1: Analisar quadrandes de 5 velas nos últimos 100 candles
    #     for i in range(0, len(candles)-5, 5):
    #         quad_candles = close_prices[i:i+5]
    #         min_price = np.min(quad_candles)
    #         max_price = np.max(quad_candles)
    #         current_price = close_prices[i+4]

    #         if current_price == max_price:
    #             entry_suggestion = "PUT"  # Preço atual é o topo, sugere entrada PUT
    #             break
    #         elif current_price == min_price:
    #             entry_suggestion = "CALL"  # Preço atual é o fundo, sugere entrada CALL
    #             break

    #     if entry_suggestion:
    #         return f"Entrada recomendada: {entry_suggestion}"
    #     else:
    #         return "Nenhuma sugestão de entrada encontrada"

    def analyze_mhi_strategy(self, asset, timeframe):
        candle_period = timeframe * 60

        candles = self.api.get_candles(asset, candle_period, 500, time.time())  # Obtém os últimos 500 candles
        close_prices = np.array([float(candle["close"]) for candle in candles])

        entry_suggestion = None

        # Etapa 1: Analisar quadrandes de 12 velas nos últimos 100 candles
        for i in range(0, len(candles)-12, 12):
            quad_candles = close_prices[i:i+12]
            min_price = np.min(quad_candles)
            max_price = np.max(quad_candles)
            current_price = close_prices[i+11]

            if current_price == max_price:
                entry_suggestion = "PUT"  # Preço atual é o topo, sugere entrada PUT
                break
            elif current_price == min_price:
                entry_suggestion = "CALL"  # Preço atual é o fundo, sugere entrada CALL
                break

        if entry_suggestion:
            return f"Entrada recomendada: {entry_suggestion}"
        else:
            return "Nenhuma sugestão de entrada encontrada"



