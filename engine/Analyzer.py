import time
from view.Messages import Message
from app.Controller.Chart import Chart 
class Analyzer:
    def __init__(self, api) -> None:
        self.api = api

        self.available_assets = {}
        self.chart_volatility = ""
        self.is_chart_laterialized = False
        self.chart_trending = ""



    def is_asset_elegible_to_trade(self, asset, payout):
        chart = Chart(self.api)
        periodo = 5
        print(f"Analizing: {asset} | Payout: {payout}")
        #--------------------
        if(chart.is_acceptable_payout(payout)): 
            if( chart.is_high_volatility_v3(asset, periodo) or chart.is_asset_chart_lateralized_v2(asset, periodo)):
                return False
            else:
                return True
        else:
            return False
