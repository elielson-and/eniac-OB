
from app.Controller.Chart import Chart 

class Analyzer:
    def __init__(self, api) -> None:
        self.api = api

        self.available_assets = {}
        self.chart_volatility = ""
        self.is_chart_laterialized = False
        self.chart_trending = ""



    def is_asset_elegible_to_trade(self, asset, payout_turbo):
        chart = Chart(self.api)
        exp_time = 5
        print(f"\nAvaliando: {asset}")
        #--------------------
        if(chart.is_acceptable_payout(payout_turbo)): # Retorna true caso os 3 fatores estiverem 
            if( chart.is_high_volatility(asset, exp_time) or chart.is_asset_chart_lateralized(asset, exp_time)):
                print("Condições de operação ruins")
                return False
            else:
                print("Boas condições de operação")
                return True
        else:
            print("Condições de operação ruins")
            return False
