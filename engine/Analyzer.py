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
        exp_time = 5
        print(f"Analizing: {asset}")
        #--------------------
        if(chart.is_acceptable_payout(payout)): 
            print(Message.success(f"Acceptable payout: {payout}%"))
            if( chart.is_high_volatility(asset, exp_time) or chart.is_asset_chart_lateralized(asset, exp_time)):
                return False
            else:
                return True
        else:
            return False
