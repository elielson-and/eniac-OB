import time
import sys
import os
from iqoptionapi.stable_api import IQ_Option
from app.Controller.Chart import Chart 
from engine.Analyzer import Analyzer
from engine.Asset import Asset
from view.Messages import Message
from engine.Trade import Trade
from config.Environment.Environment import Environment as Env
import json

class Runner:
    def __init__(self) -> None:
        self.api = IQ_Option(Env.get_iqoption_user_credentials())
        header={"User-Agent":r"Mozilla/5.0 (X11; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0"}
        cookie={"Iq":"GOOD"}
        self.api.set_session(header,cookie)
        self.api.connect()
        self.api.change_balance("PRACTICE")
        #------- Operational variables --------
       
        #------- Trade execution variables --------
        self.is_sup_res = ""
        self.mhi_sugestion = ""
        self.chart_trend = ""
        self.is_candles_small = False
        # ...


    def start_application(self):
        #---Instances---

    
        chart = Chart(self.api)
        analyzer = Analyzer(self.api)
        trade = Trade(self.api)

        # Runner
        while True:
            #Vai obter todos os ativos disponiveis no momento
            for asset in chart.get_all_available_assets():
                if(analyzer.is_asset_elegible_to_trade(asset, chart.get_payout(asset, Env.trade_modality()))):
                    # Payload das variaveis de analise
                    # self.is_sup_res = analyzer.get_support_resistance_v2(asset,5)
                    # self.mhi_sugestion = analyzer.analyze_mhi_strategy(asset,5)
                    # self.chart_trend = chart.get_chart_trend(asset, 5)
                    # self.is_candles_small = chart.is_candles_small(asset, 5)
                    # --------- Entrada
                    #trade.buy(asset,'call',5,1)
                    #print(chart.is_big_wick(asset))
                    #trade.buy(asset,"call")
                    print(asset)
                else:
                    print("Chart conditions: " + Message.txt_red("[ BAD ]") + "\n--------------")
                    # print(f"[ {asset} ] - Compra cancelada, condições não favoráveis.")
                    # os.system('cls||clear')
            sys.exit()
            
            
                

            
           


       