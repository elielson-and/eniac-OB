import time
import sys
from iqoptionapi.stable_api import IQ_Option


class Runner:
    def __init__(self) -> None:
        self.api = IQ_Option("elielsonand123@gmail.com","andre4002")
        self.api.connect()


    def start_application(self):
        print("Chegou aqui")
        sys.exit()
        

        asset = "AUDJPY"
        timeframe = 5

        # Obtendo os últimos 10 candles
        candles = self.api.get_candles(asset, timeframe * 60, 100, time.time())
        candles_list = candles

        print("\n Obtendo últimas 100 velas... \n")
        time.sleep(1)
        # Obtendo a cor de cada candle
        qtdVermelhas = 0
        qtdverdes = 0

        for candle in candles_list:
            candle_open = candle["open"]
            candle_close = candle["close"]
            if candle_open < candle_close:
                print( "verde" )
                qtdverdes +=1
            elif candle_open > candle_close:
                print("vermelho" )
                qtdVermelhas +=1 
            else:
                print("DOGE")
            time.sleep(0.1)

        operacao = ''
        if qtdVermelhas > qtdverdes:
            operacao = "CALL"
        else:
            operacao = "PUT"

        print("\n operação sugerida: " + operacao )