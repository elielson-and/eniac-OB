import time
import sys
from iqoptionapi.stable_api import IQ_Option
from app.Requerements.Volatility import Volatility
from app.Requerements.Candle import Candle 
from engine.Asset import Asset

class Runner:
    def __init__(self) -> None:
        self.api = IQ_Option("elielsonand123@gmail.com","andre4002")
        self.api.connect()

    def start_application(self):
        # Verificar os ativos disponíveis no momento

        # Verificar volatilidade
        volatility = Volatility(self.api)
        volatility.is_volatility_high()
        
        avr = Candle(self.api)
        avr.check_trend()


       