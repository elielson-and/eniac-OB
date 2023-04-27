import time
import sys
from iqoptionapi.stable_api import IQ_Option
from app.Requerements.Volatility import Volatility
from app.Requerements.Chart import Chart 
from engine.Asset import Asset

class Runner:
    def __init__(self) -> None:
        self.api = IQ_Option("elielsonand123@gmail.com","andre4002")
        self.api.connect()

        #------- Operational variables --------
        self.available_assets = {}
        self.current_chart_trending = ""








    def start_application(self):
        # Verificar os ativos disponíveis no momento

        # Verificar volatilidade
        # volatility = Volatility(self.api)
        # volatility.is_volatility_high()

        
        avr = Chart(self.api)
        # avr.check_trend()
        # avr.get_all_available_assets()
        # avr.is_eurusd_market_lateralized()
        avr.check_volatility()


       