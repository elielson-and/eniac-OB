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
    
    # 
    #
    #
    # Strategy area
    #
    #
    #
    
    #-----------------------------------------------------------------
    #| Support and Resistance - Strategy
    #-----------------------------------------------------------------
    def get_support_resistance(self, asset):
        qtd_candles = 50
        zone_range = 0.0020
        periods = [ 5, 15, 60]
        counts = {'support': 0, 'resistance': 0}
        # ----
        for index, period in enumerate(periods):
            candles = self.api.get_candles(asset, period, qtd_candles, time.time())
            
            #opens = [candle['open'] for candle in candles]
            closes = [candle['close'] for candle in candles]
            highs = [candle['max'] for candle in candles]
            lows = [candle['min'] for candle in candles]
        
            # Mapeamento de topos e fundos
            tops = []
            bottoms = []
        
            for i in range(1, len(candles) - 1):
                if highs[i] > highs[i-1] and highs[i] > highs[i+1]:
                    tops.append((i, highs[i]))
                elif lows[i] < lows[i-1] and lows[i] < lows[i+1]:
                    bottoms.append((i, lows[i]))
        
            current_price = closes[-1]
        
            if len(tops) > 0 or len(bottoms) > 0:
                top_zones = []
                bottom_zones = []
        
                for top in tops:
                    top_diff = abs(current_price - top[1])
                    if top_diff <= zone_range:
                        top_zones.append(top_diff)
        
                for bottom in bottoms:
                    bottom_diff = abs(current_price - bottom[1])
                    if bottom_diff <= zone_range:
                        bottom_zones.append(bottom_diff)
        
                if top_zones or bottom_zones:
                    if top_zones and bottom_zones:
                        top_sum = sum(top_zones)
                        bottom_sum = sum(bottom_zones)
                        if top_sum >= bottom_sum:
                            counts['resistance'] += 1
                            continue
                        else:
                            counts['support'] += 1
                            continue
                    elif top_zones:
                        counts['resistance'] += 1
                        continue
                    else:
                        counts['support'] += 1
                        continue
        
            # return "no zone found"

        final_decision = max(counts, key=counts.get)
        print(final_decision)
        return final_decision
    


    #-----------------------------------------------------------------
    #| MHI - Strategy
    #-----------------------------------------------------------------
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



