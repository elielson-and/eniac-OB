import time
import sys
from iqoptionapi.stable_api import IQ_Option
from app.Controller.Chart import Chart 
from engine.Analyzer import Analyzer
from engine.Asset import Asset
from view.Messages import Message
from config.Environment.Environment import Environment
import json

class Runner:
    def __init__(self) -> None:
        self.api = IQ_Option(Environment.get_iqoption_user_credentials())
        header={"User-Agent":r"Mozilla/5.0 (X11; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0"}
        cookie={"Iq":"GOOD"}
        self.api.set_session(header,cookie)
        self.api.connect()

        #------- Operational variables --------
    

        #------- Trade execution variables --------
        # ...


    def start_application(self):
        #---Instances---
        chart = Chart(self.api)
        analyzer = Analyzer(self.api)
        # Runner
        while True:
            #Vai obter todos os ativos disponiveis no momento
            for asset in chart.get_all_available_assets():
                if(analyzer.is_asset_elegible_to_trade(asset, chart.get_payout(asset))):
                    print(Message.success("Good conditions") + "\n")
                else:
                    print(Message.danger("Bad conditions") + "\n")
            sys.exit()
            
                

            
           


       