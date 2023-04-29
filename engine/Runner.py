import time
import sys
from iqoptionapi.stable_api import IQ_Option
from app.Controller.Chart import Chart 
from engine.Analyzer import Analyzer
from engine.Asset import Asset
import json

class Runner:
    def __init__(self) -> None:
        self.api = IQ_Option("elielsonand123@gmail.com","andre4002")
        header={"User-Agent":r"Mozilla/5.0 (X11; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0"}
        cookie={"Iq":"GOOD"}
        self.api.set_session(header,cookie)
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
        analyzer = Analyzer(self.api)


        # Runner
        while True:
            #Vai obter todos os ativos disponiveis no momento
            self.available_assets = chart.get_all_available_assets()            # Array

            # For para validar ativo por ativo
            assets = json.loads(self.available_assets)
            print(assets)
            sys.exit()
            for asset, payouts in assets.items():
                payout_turbo = payouts['turbo']
                # se o ativo atual for elegivel realiza a entrada
                print(f"Analisando ativo [{asset}]...")
                if(analyzer.is_asset_elegible_to_trade(asset, payout_turbo)):
                    print(f"Realizando entrada [{asset}]")
                    # self.chart_trending = chart.get_chart_trend(asset, 5) 
                     
                    
        
            time.sleep(60 * 5)

            


            # chart.print_assets_payouts(self.available_assets)
        


       