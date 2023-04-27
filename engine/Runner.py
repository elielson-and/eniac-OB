import time
import sys
from iqoptionapi.stable_api import IQ_Option
from app.Requerements.Volatility import Volatility
from app.Controller.Chart import Chart 
from engine.Asset import Asset

class Runner:
    def __init__(self) -> None:
        self.api = IQ_Option("elielsonand123@gmail.com","andre4002")
        self.api.connect()

        #------- Operational variables --------
        self.available_assets = {}
        self.chart_volatility = ""
        self.is_chart_laterialized = False
        self.chart_trending = ""
        #------- Trade execution variables --------


    def start_application(self):
        #---Instances---
        chart = Chart(self.api)

        self.available_assets = chart.get_all_available_assets()            # Array
        self.chart_volatility = chart.is_high_volatility()                  # String
        self.is_chart_laterialized = chart.is_asset_chart_lateralized()     # Bool
        self.chart_trending = chart.get_chart_trend()                       # String

        
     
        


       